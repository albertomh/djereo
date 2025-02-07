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


@pytest.mark.integration
@pytest.mark.smoke
def test_uv_lockfile_exists(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    uv_lock_file = test_project_dir / "uv.lock"
    assert uv_lock_file.exists(), f"Expected lock file {uv_lock_file} not found."


@pytest.mark.integration
@pytest.mark.smoke
def test_dotenv_exists(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    dotenv_file = test_project_dir / ".env"
    assert dotenv_file.exists(), f"Expected dotenv {dotenv_file} not found."


@pytest.mark.integration
@pytest.mark.smoke
def test_initial_accounts_migration_exists(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    initial_migration = test_project_dir / "accounts" / "migrations" / "0001_initial.py"
    assert initial_migration.exists(), (
        f"Expected migration {initial_migration} not found."
    )
