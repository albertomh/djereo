# Test the effects of the tasks that run after generating or updating a project.

from pathlib import Path
from typing import Callable

import pytest

from tests._utils import is_git_repo


@pytest.mark.integration
@pytest.mark.smoke
def test_is_git_repo(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    assert is_git_repo(test_project_dir), "The test project is not a Git repository."


@pytest.mark.parametrize(
    "file_path, expected_message",
    [
        ("uv.lock", "lock file"),
        (".env", "dotenv"),
        ("accounts/migrations/0001_initial.py", "migration"),
    ],
)
@pytest.mark.integration
@pytest.mark.smoke
def test_file_exists(
    file_path: str,
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
    expected_message: str,
):
    copier_copy(copier_input_data)

    file_to_check = test_project_dir / file_path
    assert file_to_check.exists(), (
        f"Expected {expected_message} {file_to_check} not found."
    )
