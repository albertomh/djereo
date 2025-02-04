import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Callable

import pytest
from copier.cli import CopierApp

from tests._utils import set_up_postgres, tear_down_postgres

DJEREO_TEST_TEMP_DIR = Path("/", "tmp", "djereo_test")


@pytest.fixture
def skip_if_github_actions():
    if os.getenv("GITHUB_ACTIONS") == "true":
        pytest.skip("Test fails in a GitHub Actions context")


@pytest.fixture
def djereo_root_dir() -> Path:
    """Provides the path to the djereo project root."""
    project_root = Path(__file__).resolve().parent.parent
    if not project_root.exists():
        pytest.fail(f"djereo project root does not exist at {project_root}")
    return project_root


@pytest.fixture
def djereo_test_temp_dir() -> Path:
    return DJEREO_TEST_TEMP_DIR


@pytest.fixture
def test_project_name() -> str:
    return "djereo_test_project"


@pytest.fixture
def test_project_dir(djereo_test_temp_dir: Path, test_project_name: str) -> Path:
    return djereo_test_temp_dir / test_project_name


@pytest.fixture
def copier_input_data(test_project_name: str) -> dict:
    """Answers to core djereo template questions."""
    return {
        "project_name": test_project_name,
        "author_name": "Miguel de Cervantes",
        "author_email": "mike@alcala.net",
    }


@pytest.fixture
def copier_copy(djereo_root_dir: Path, test_project_dir: Path) -> Callable[[dict], None]:
    """
    Fixture to run `copier copy`, cleaning up destination directory beforehand.
    Uses the `djereo_root_dir` & `test_project_dir` fixtures as source and
    destination directories respectively, so tests should use these fixtures
    """

    def _quote_if_has_space(string: str) -> str:
        if isinstance(string, str) and " " in string:
            return f"'{string}'"
        return string

    def _run(copier_input_data: dict, *, generate_dotenv=True):
        if test_project_dir.exists():
            shutil.rmtree(test_project_dir, ignore_errors=True)

        copier_args = ["--vcs-ref=HEAD", "--defaults", "--trust"]
        copier_args.extend(
            [f"--data={k}={_quote_if_has_space(v)}" for k, v in copier_input_data.items()]
        )

        # Use `CopierApp.run` because `run_copy` does not accept `--trust` as a flag,
        # which is needed in order for post-creation tasks to run.
        CopierApp.run(
            [
                "copier",
                "copy",
                *copier_args,
                str(djereo_root_dir),
                str(test_project_dir),
            ],
            exit=False,
        )

        if generate_dotenv:
            env_path = test_project_dir / ".env"
            shutil.copyfile(test_project_dir / ".env.in", env_path)
            with env_path.open("r+") as file:
                env_content = file.read()
                env_content = env_content.replace("{password}", "password")
                file.seek(0)
                file.write(env_content)
                file.truncate()

    return _run


@pytest.fixture(autouse=True, scope="session")
def session_setup_and_teardown():
    def _set_up():
        if not DJEREO_TEST_TEMP_DIR.exists():
            DJEREO_TEST_TEMP_DIR.mkdir()

    def _tear_down():
        pass

    _set_up()
    yield
    _tear_down()


@pytest.fixture
def install_test_project(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
    test_project_name: str,
):
    """Generate a test project, install and remove it before/after a test."""
    copier_copy(copier_input_data)
    subprocess.run(
        [sys.executable, "-m", "pip", "install", str(test_project_dir)],
        check=True,
    )

    yield

    subprocess.run(
        [sys.executable, "-m", "pip", "uninstall", "-y", test_project_name],
        check=True,
    )


@pytest.fixture
def set_up_test_database(test_project_dir: Path) -> Callable[[], None]:
    def _run() -> None:
        set_up_postgres(test_project_dir)

    return _run


@pytest.fixture
def tear_down_test_database(test_project_dir: Path):
    yield
    tear_down_postgres(test_project_dir)
