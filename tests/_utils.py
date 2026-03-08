import os
import re
import socket
from collections.abc import Callable
from pathlib import Path

from sh import ErrorReturnCode, git, uv, whoami


def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r"\x1b[^m]*m")
    return ansi_escape.sub("", text)


def is_git_repo(path: Path) -> bool:
    """Check if the given path is a Git repository."""
    try:
        git("-C", str(path), "status")
    except ErrorReturnCode:
        return False
    else:
        return True


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


def in_ci() -> bool:
    return os.getenv("CI") == "true"


def get_current_os_user() -> str:
    current_user = whoami()
    return current_user.strip()


def get_free_port_from_os() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


def set_up_postgres(test_project_dir: Path) -> Callable[[], None]:
    uv(
        "run",
        "--active",
        "_db/manage_db.py",
        "set_up",
        _cwd=test_project_dir,
    )


def tear_down_postgres(test_project_dir: Path):
    uv(
        "run",
        "--active",
        "_db/manage_db.py",
        "tear_down",
        _cwd=test_project_dir,
    )
