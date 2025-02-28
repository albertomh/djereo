import os
import signal
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Generator

from sh import ErrorReturnCode, git, psql, whoami


def is_git_repo(path: Path) -> bool:
    """Check if the given path is a Git repository."""
    try:
        git("-C", str(path), "status")
        return True
    except ErrorReturnCode:
        return False


def count_dirs_and_files(path: Path) -> tuple[int, int]:
    """Count the number of directories and files in a given path.

    Args:
        path (Path): The directory path to inspect.

    Returns:
        tuple[int, int]: A tuple of the number of directories and the number of files.
    """
    num_dirs, num_files = 0, 0
    for entry in path.iterdir():
        if entry.is_file():
            num_files += 1
        elif entry.is_dir():
            num_dirs += 1
    return num_dirs, num_files


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
        if Path(stdout_file.name).exists():
            with open(stdout_file.name, "r") as f:
                stdout_lines = f.readlines()
            os.unlink(stdout_file.name)
        if Path(stderr_file.name).exists():
            with open(stderr_file.name, "r") as f:
                stderr_lines = f.readlines()
            os.unlink(stderr_file.name)

    return stdout_lines, stderr_lines


def run_process_and_wait(
    command_args: list, test_project_dir: Path, *, env: dict | None = None
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


def in_ci() -> bool:
    return os.getenv("CI") == "true"


def get_current_os_user() -> str:
    current_user = whoami()
    return current_user.strip()


def get_postgres_user() -> str:
    if in_ci():
        return "postgres"
    return get_current_os_user()


def set_up_postgres(test_project_dir: Path) -> Callable[[], None]:
    if in_ci():
        os.environ["PGPASSWORD"] = "password"

    psql(
        "--user",
        get_postgres_user(),
        "--host",
        "localhost",
        "--dbname",
        "postgres",
        "--set=APP_USER_PASSWORD=password",
        "--file",
        "_db/set_up.sql",
        _cwd=test_project_dir.absolute().as_posix(),
    )


def tear_down_postgres(test_project_dir: Path):
    if in_ci():
        os.environ["PGPASSWORD"] = "password"

    psql(
        "--user",
        get_postgres_user(),
        "--host",
        "localhost",
        "--dbname",
        "postgres",
        "--file",
        "_db/tear_down.sql",
        _cwd=test_project_dir.absolute().as_posix(),
    )
