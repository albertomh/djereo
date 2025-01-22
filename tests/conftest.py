import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable, Generator

import pytest
from copier.cli import CopierApp

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
    return "test_project"


@pytest.fixture
def test_project_dir(djereo_test_temp_dir: Path, test_project_name: str) -> Path:
    return djereo_test_temp_dir / test_project_name


@pytest.fixture
def copier_input_data() -> dict:
    """Answers to core djereo template questions."""
    return {
        "project_name": "test_project",
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
            shutil.copyfile(test_project_dir / ".env.in", test_project_dir / ".env")

    return _run


def pytest_sessionstart(session):
    """Hook to perform initial setup before all tests."""
    if not DJEREO_TEST_TEMP_DIR.exists():
        DJEREO_TEST_TEMP_DIR.mkdir()


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


def start_process_and_capture_streams(
    command_args: list, test_project_dir: Path, env: dict | None = None
) -> Generator[None, None, tuple[list[str], list[str]]]:
    """
    Starts a subprocess with the given command and environment variables,
    capturing stdout and stderr. Yields control to the caller after starting.
    """
    full_env = os.environ.copy()
    full_env.update({"PYTHONUNBUFFERED": "1"})
    if env:
        full_env.update(env)
    stdout_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    stderr_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)

    try:
        stdout_file.close()
        stderr_file.close()

        process = subprocess.Popen(
            command_args,
            cwd=test_project_dir,
            stdout=open(stdout_file.name, "w"),
            stderr=open(stderr_file.name, "w"),
            text=True,
            env=full_env,
        )
        yield stdout_file.name, stderr_file.name
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
    finally:
        stdout_lines, stderr_lines = [], []
        if os.path.exists(stdout_file.name):
            with open(stdout_file.name, "r") as f:
                stdout_lines = f.readlines()
            os.unlink(stdout_file.name)
        if os.path.exists(stderr_file.name):
            with open(stderr_file.name, "r") as f:
                stderr_lines = f.readlines()
            os.unlink(stderr_file.name)

    return stdout_lines, stderr_lines


def run_process_and_wait(
    command_args: list, test_project_dir: Path, env: dict | None = None
) -> tuple[list[str], list[str]]:
    """
    Runs a subprocess and waits for it to complete, capturing stdout and stderr.
    """
    generator = start_process_and_capture_streams(command_args, test_project_dir, env)
    try:
        next(generator)
        return next(generator)
    except StopIteration as e:
        return e.value


def is_git_repo(path: Path) -> bool:
    """Check if the given path is a Git repository."""
    try:
        subprocess.run(
            ["git", "-C", str(path), "status"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except subprocess.CalledProcessError:
        return False
