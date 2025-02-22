import textwrap
from pathlib import Path
from typing import Callable

import pytest

from tests._utils import run_process_and_wait

TEST_MODELS_PY_CONTENT = textwrap.dedent("""

from django.db import models

class SomeModel(models.Model):
    name = models.CharField(max_length=100)
""")


@pytest.mark.integration
@pytest.mark.slow
def test_migrations_check_fails_if_pending_migrations(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    copier_copy(copier_input_data)
    set_up_test_database()
    models_py_path = test_project_dir / test_project_name / "models.py"
    with open(models_py_path, "a") as models_file:
        models_file.write(TEST_MODELS_PY_CONTENT)
    migrations_dir = test_project_dir / test_project_name / "migrations"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    (migrations_dir / "__init__.py").touch()

    _, stderr = run_process_and_wait(
        ["just", "test", "-k", "test_no_pending_migrations"],
        test_project_dir,
    )

    expected_error = (
        "test_no_pending_migrations (tests.test_migrations.PendingMigrationsTests."
        "test_no_pending_migrations) ... FAIL\n"
    )
    assert expected_error in stderr


@pytest.mark.integration
@pytest.mark.slow
def test_makemigrations_creates_a_max_migration_file(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    copier_copy(copier_input_data)
    set_up_test_database()
    models_py_path = test_project_dir / test_project_name / "models.py"
    with open(models_py_path, "a") as models_file:
        models_file.write(TEST_MODELS_PY_CONTENT)

    run_process_and_wait(
        ["just", "manage", "makemigrations", test_project_name], test_project_dir
    )

    migrations_dir = test_project_dir / test_project_name / "migrations"
    migrations_fnames = [f.name for f in migrations_dir.iterdir()]
    assert "max_migration.txt" in migrations_fnames
