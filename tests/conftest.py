# ruff: noqa: PLR0913

import hashlib
import json
import os
import re
import shutil
import uuid
from collections.abc import Callable
from io import TextIOWrapper
from pathlib import Path

import copier
import pytest
from sh import python as sh_python

from tests._utils import set_up_postgres, tear_down_postgres

TESTS_DIR = Path(__file__).resolve().parent
DJEREO_TESTS_SANDBOX_DIR = Path("/", "tmp", "djereo_test")
IS_CI = os.getenv("CI") == "true"


@pytest.fixture
def djereo_root_dir() -> Path:
    """Provides the path to the djereo project root."""
    project_root = Path(__file__).resolve().parent.parent
    if not project_root.exists():
        pytest.fail(f"djereo project root does not exist at {project_root}")
    return project_root


@pytest.fixture
def test_project_name() -> str:
    return f"djereo_test_{uuid.uuid4().hex[:8]}"


STABLE_PROJECT_NAME = "djereo_stable_cache_project"


def _rename_project(project_dir: Path, old_name: str, new_name: str):
    """Recursively renames project name in filenames and file contents."""
    old_title = old_name.title()
    new_title = new_name.title()

    # Replace project name in file contents
    for root, _dirs, files in os.walk(project_dir):
        for file in files:
            file_path = Path(root) / file
            try:
                content = file_path.read_text()
                new_content = content.replace(old_name, new_name).replace(
                    old_title, new_title
                )
                if new_content != content:
                    file_path.write_text(new_content)
            except (UnicodeDecodeError, PermissionError):
                continue

    # Rename directories and files (bottom-up to avoid path changes during iteration)
    for root, dirs, files in os.walk(project_dir, topdown=False):
        for name in files + dirs:
            if old_name in name:
                new_item_name = name.replace(old_name, new_name)
                os.rename(os.path.join(root, name), os.path.join(root, new_item_name))


def test_session_temp_dir(session: pytest.Session) -> Path:
    config = getattr(session, "config", None)
    # Provided by pytest-xdist
    worker_id = getattr(config, "workerinput", {}).get("workerid", "master")
    return DJEREO_TESTS_SANDBOX_DIR / f"session_{worker_id}"


@pytest.fixture
def test_project_dir(
    request: pytest.FixtureRequest,
) -> Path:
    """Path of a temporary directory for test isolation. Namespaced per pytest session.

    Used to avoid conflict when many tests (run in parallel) are attempting to create
    'djereo' projects using 'copier'.
    """
    # Per-session namespacing to ensure xdist workers delete the right subdir
    # during clean-up in the sessionfinish hook
    session_tmp_dir = test_session_temp_dir(request.session)
    session_tmp_dir.mkdir(parents=True, exist_ok=True)
    test_run_id = uuid.uuid4().hex[:8]
    return session_tmp_dir / f"test_{test_run_id}"


@pytest.fixture
def copier_input_data(test_project_name: str) -> dict:
    """Answers to core djereo template questions."""
    input_data = {
        "project_name": test_project_name,
        "author_name": "Miguel de Cervantes",
        "author_email": "mike@alcala.net",
    }

    nox_session = os.getenv("NOX_SESSION", "")
    match = re.search(r"(\d+\.\d+)", nox_session)
    if match:
        input_data["min_python_version"] = match.group(1)

    return input_data


def _compute_copier_hash(
    djereo_root_dir: Path,
    copier_input_data: dict,
    generate_dotenv: bool,
    is_ci: bool,
) -> str:
    """Computes a hash of the copier inputs and template state."""
    stable_data = copier_input_data.copy()
    stable_data["project_name"] = STABLE_PROJECT_NAME

    hasher = hashlib.md5()
    hasher.update(json.dumps(stable_data, sort_keys=True).encode())
    hasher.update(str(generate_dotenv).encode())
    hasher.update(str(is_ci).encode())

    template_dir = djereo_root_dir / "template"
    copier_yaml = djereo_root_dir / "copier.yaml"

    # Files to hash - filenames and mtimes are enough for cache invalidation
    files_to_hash = sorted([copier_yaml, *template_dir.rglob("*")])
    for path in files_to_hash:
        if path.is_file() and ".git" not in path.parts:
            hasher.update(str(path.relative_to(djereo_root_dir)).encode())
            hasher.update(str(path.stat().st_mtime).encode())

    return hasher.hexdigest()


@pytest.fixture
def copier_copy(djereo_root_dir: Path, test_project_dir: Path) -> Callable:
    """Fixture to run `copier copy`, cleaning up destination directory beforehand.

    Uses caching to speed up successive runs with identical inputs.
    Reuses a stable generated project and renames it for speed.
    """

    def _run(copier_input_data: dict, *, generate_dotenv=True, use_cache=True):
        if test_project_dir.exists():
            shutil.rmtree(test_project_dir, ignore_errors=True)

        actual_project_name = copier_input_data["project_name"]
        cache_dir = DJEREO_TESTS_SANDBOX_DIR / "copier_cache"
        cache_dir.mkdir(exist_ok=True)

        cache_key = _compute_copier_hash(
            djereo_root_dir, copier_input_data, generate_dotenv, IS_CI
        )
        cached_result = cache_dir / cache_key

        if use_cache and cached_result.exists():
            shutil.copytree(cached_result, test_project_dir)
            _rename_project(test_project_dir, STABLE_PROJECT_NAME, actual_project_name)
            return

        # Cache miss: run copier with real data
        copier.run_copy(
            str(djereo_root_dir),
            str(test_project_dir),
            data=copier_input_data,
            vcs_ref="HEAD",
            defaults=True,
            unsafe=True,
        )

        if generate_dotenv:

            def _rewrite_password_in_dotenv(file: TextIOWrapper):
                env_content = file.read()
                env_content = env_content.replace("{password}", "password")
                file.seek(0)
                file.write(env_content)
                file.truncate()

            dotenv_path = test_project_dir / ".env"
            shutil.copyfile(test_project_dir / ".env.in", dotenv_path)
            with dotenv_path.open("r+") as file:
                _rewrite_password_in_dotenv(file)

        if IS_CI:
            test_dotenv_path = test_project_dir / ".env.test"
            with test_dotenv_path.open("r+") as file:
                test_env_content = file.read()
                new_env_content = re.sub(
                    r"DATABASE_URL=.*",
                    f'DATABASE_URL="postgres://{actual_project_name}:password@localhost:5432/{actual_project_name}"',
                    test_env_content,
                )
                file.seek(0)
                file.write(new_env_content)
                file.truncate()

        if use_cache:
            # Since copier ran with the actual project name to ensure questionnaire
            # validation works, we need to rename it to the stable name for caching.
            _rename_project(test_project_dir, actual_project_name, STABLE_PROJECT_NAME)

            # Save the stable version to cache
            temp_cache = cached_result.with_suffix(f".{uuid.uuid4().hex[:8]}.tmp")
            shutil.copytree(test_project_dir, temp_cache)
            try:
                temp_cache.rename(cached_result)
            except OSError:
                shutil.rmtree(temp_cache, ignore_errors=True)

            # Rename back stable -> actual for the current test so it sees the name it
            # expects from pyproject.toml, .env.test, etc.
            _rename_project(test_project_dir, STABLE_PROJECT_NAME, actual_project_name)

    return _run


def pytest_sessionstart(session):
    if not DJEREO_TESTS_SANDBOX_DIR.exists():
        DJEREO_TESTS_SANDBOX_DIR.mkdir(exist_ok=True)


def pytest_sessionfinish(session):
    # cleanup implemented in `noxfile.py` to ensure all xdist workers have finished
    pass


@pytest.fixture
def install_test_project(
    copier_copy: Callable,
    copier_input_data: dict,
    test_project_dir: Path,
    test_project_name: str,
):
    """Generate a test project, install and remove it before/after a test."""
    copier_copy(copier_input_data)
    sh_python("-m", "pip", "install", str(test_project_dir))

    yield

    sh_python("-m", "pip", "uninstall", "-y", test_project_name)


@pytest.fixture
def set_up_test_database(
    test_project_dir: Path, test_project_name: str
) -> Callable[[], None]:
    def _run() -> None:
        set_up_postgres(test_project_dir, test_project_name)

    return _run


@pytest.fixture
def tear_down_test_database(test_project_dir: Path, test_project_name: str):
    return


@pytest.fixture
def generate_test_project_with_db(
    copier_copy: Callable,
    copier_input_data: dict,
    set_up_test_database,
    test_project_dir: Path,
    test_project_name: str,
    tear_down_test_database,
):
    copier_copy(copier_input_data)
    set_up_test_database()

    yield

    tear_down_postgres(test_project_dir, test_project_name)
