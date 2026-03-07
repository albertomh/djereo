import textwrap
from pathlib import Path

import pytest
from sh import just

TEST_MODELS_PY_CONTENT = textwrap.dedent("""
class SomeModel(models.Model):
    name = models.CharField(max_length=100)
""")


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.skip_migrate
def test_migrations_check_fails_if_pending_migrations(
    set_up_generated_project: Path,
):
    test_project_dir = set_up_generated_project
    models_py_path = test_project_dir / "core" / "models.py"
    with open(models_py_path, "a") as models_file:
        models_file.write(TEST_MODELS_PY_CONTENT)
    migrations_dir = test_project_dir / "core" / "migrations"
    migrations_dir.mkdir(parents=True, exist_ok=True)
    (migrations_dir / "__init__.py").touch()

    # Run 'makemigrations --check' directly via 'uv run' to detect pending changes.
    # This is much faster than running 'nox' and its associated environment setup.
    import subprocess

    result = subprocess.run(
        ["uv", "run", "manage.py", "makemigrations", "--check", "--dry-run"],
        cwd=test_project_dir,
        capture_output=True,
        text=True,
        check=False,
    )

    # Return code 1 indicates that changes were detected (pending migrations).
    assert result.returncode == 1
    assert "No changes detected" not in result.stdout
    assert "Changes detected" in result.stdout or "Migrations for" in result.stdout


@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.skip_migrate
def test_makemigrations_creates_a_max_migration_file(
    set_up_generated_project: Path,
):
    test_project_dir = set_up_generated_project
    models_py_path = test_project_dir / "core" / "models.py"
    with open(models_py_path, "a") as models_file:
        models_file.write(TEST_MODELS_PY_CONTENT)

    just("manage", "makemigrations", "core", _cwd=test_project_dir)

    migrations_dir = test_project_dir / "core" / "migrations"
    migrations_fnames = [f.name for f in migrations_dir.iterdir()]
    assert "max_migration.txt" in migrations_fnames
