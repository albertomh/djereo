import textwrap
from pathlib import Path

import pytest
from sh import just, nox

from tests._utils import remove_ansi_escape_codes

TEST_MODELS_PY_CONTENT = textwrap.dedent("""

from django.db import models

class SomeModel(models.Model):
    name = models.CharField(max_length=100)
""")


@pytest.mark.integration
@pytest.mark.slow
def test_migrations_check_fails_if_pending_migrations(
    test_project_name: str,
    test_project_dir: Path,
    generate_test_project_with_db,
):
    models_py_path = test_project_dir / test_project_name / "models.py"
    with open(models_py_path, "a") as models_file:
        models_file.write(TEST_MODELS_PY_CONTENT)
    migrations_dir = test_project_dir / test_project_name / "migrations"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    (migrations_dir / "__init__.py").touch()
    res = nox(
        "--",
        "-k",
        "test_no_pending_migrations",
        # 1 is okay since we are expecting `test_no_pending_migrations` to fail
        _ok_code=[0, 1],
        _cwd=test_project_dir,
        _return_cmd=True,
    )

    combined_output = (
        f"{remove_ansi_escape_codes(res.stdout)}\n{remove_ansi_escape_codes(res.stderr)}"
    )

    assert (
        "test_no_pending_migrations (tests.test_migrations.PendingMigrationsTests."
        in combined_output
    )
    assert "test_no_pending_migrations) ... FAIL" in combined_output


@pytest.mark.integration
@pytest.mark.slow
def test_makemigrations_creates_a_max_migration_file(
    test_project_name: str,
    test_project_dir: Path,
    generate_test_project_with_db,
):
    models_py_path = test_project_dir / test_project_name / "models.py"
    with open(models_py_path, "a") as models_file:
        models_file.write(TEST_MODELS_PY_CONTENT)

    just("manage", "makemigrations", test_project_name, _cwd=test_project_dir)

    migrations_dir = test_project_dir / test_project_name / "migrations"
    migrations_fnames = [f.name for f in migrations_dir.iterdir()]
    assert "max_migration.txt" in migrations_fnames
