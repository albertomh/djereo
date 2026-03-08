import os
import re
import shutil
import uuid
from collections.abc import Callable
from io import TextIOWrapper
from pathlib import Path

import copier
import pytest
from sh import uv

from tests._utils import set_up_postgres, tear_down_postgres

TESTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = TESTS_DIR.parent

SANDBOX = Path("/tmp/djereo_test")
IS_CI = os.getenv("CI") == "true"


# -------------------------------------------------------------------
# sandbox management
# -------------------------------------------------------------------

# reuse cache across xdist workers
os.environ.setdefault("UV_CACHE_DIR", "/tmp/uv_cache")


def _worker_id(session: pytest.Session) -> str:
    return getattr(session.config, "workerinput", {}).get("workerid", "master")


def _session_tmp_dir(session: pytest.Session) -> Path:
    return SANDBOX / f"session_{_worker_id(session)}"


def pytest_sessionstart(session: pytest.Session):
    SANDBOX.mkdir(exist_ok=True)


# -------------------------------------------------------------------
# basic fixtures
# -------------------------------------------------------------------


@pytest.fixture
def djereo_root_dir() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def test_project_name() -> str:
    return f"djereo_test_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_project_dir(request: pytest.FixtureRequest, test_project_name: str) -> Path:
    tmp = _session_tmp_dir(request.session)
    tmp.mkdir(parents=True, exist_ok=True)
    return tmp / test_project_name


@pytest.fixture
def copier_input_data(test_project_name: str) -> dict:
    data = {
        "_is_test": True,
        "project_name": test_project_name,
        "author_name": "Miguel de Cervantes",
        "author_email": "mike@alcala.net",
        "is_github_project": False,
    }

    nox_session = os.getenv("NOX_SESSION", "")
    match = re.search(r"(\d+\.\d+)", nox_session)
    if match:
        data["min_python_version"] = match.group(1)

    django_version = os.getenv("DJANGO_VERSION")
    if django_version:
        data["django_version"] = django_version

    return data


# -------------------------------------------------------------------
# project generation
# -------------------------------------------------------------------


@pytest.fixture
def copier_copy(test_project_dir: Path, copier_quiet=True) -> Callable[[dict], None]:

    def _run(
        copier_input_data: dict,
        *,
        copier_quiet=copier_quiet,
        generate_dotenv=True,
        dotenv_overrides: dict[str, str] | None = None,
    ):
        if test_project_dir.exists():
            shutil.rmtree(test_project_dir, ignore_errors=True)

        copier.run_copy(
            str(PROJECT_ROOT),
            str(test_project_dir),
            data=copier_input_data,
            vcs_ref="HEAD",
            defaults=True,
            quiet=copier_quiet,
            unsafe=True,
        )

        if generate_dotenv:

            def _rewrite_dotenv(file: TextIOWrapper):
                env_content = file.read()
                env_content = env_content.replace("{password}", "password")
                if dotenv_overrides:
                    for key, value in dotenv_overrides.items():
                        env_content = re.sub(
                            f"^{key}=.*",
                            f"{key}={value}",
                            env_content,
                            flags=re.MULTILINE,
                        )
                file.seek(0)
                file.write(env_content)
                file.truncate()

            dotenv_path = test_project_dir / ".env"
            shutil.copyfile(test_project_dir / ".env.in", dotenv_path)
            with dotenv_path.open("r+") as file:
                _rewrite_dotenv(file)

    return _run


# -------------------------------------------------------------------
# generated project fixtures
# -------------------------------------------------------------------


@pytest.fixture
def generated_project(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
) -> Path:
    copier_copy(copier_input_data)

    uv("sync", "--frozen", "--quiet", _cwd=test_project_dir)

    return test_project_dir


@pytest.fixture
def generated_project_sqlite(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
) -> Path:
    copier_copy(
        copier_input_data,
        dotenv_overrides={"DATABASE_URL": "sqlite:///:memory:"},
    )

    uv("sync", "--frozen", "--quiet", _cwd=test_project_dir)

    return test_project_dir


@pytest.fixture
def generated_project_postgres(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    uv("sync", "--frozen", "--quiet", _cwd=test_project_dir)

    set_up_postgres(test_project_dir)

    yield test_project_dir

    tear_down_postgres(test_project_dir)


@pytest.fixture
def install_test_project(
    generated_project: Path,
    test_project_name: str,
):
    uv("pip", "install", "--quiet", str(generated_project))

    yield

    uv("pip", "uninstall", "--quiet", test_project_name)


# -------------------------------------------------------------------
# project command runner
# -------------------------------------------------------------------


@pytest.fixture
def project_cmd():
    def run(project_dir: Path, *args, **kwargs):
        return uv("run", *args, _cwd=project_dir, **kwargs)

    return run
