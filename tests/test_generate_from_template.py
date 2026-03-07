import os
import shutil
import subprocess
import tomllib
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml
from packaging.specifiers import SpecifierSet
from packaging.version import Version

from tests._utils import count_dirs_and_files


@pytest.mark.integration
@pytest.mark.smoke
def test_djereo_jinja_templates_converted(
    copier_copy: Callable,
    copier_input_data: dict,
    djereo_root_dir: Path,
    test_project_dir: Path,
):
    """Validate that generating a project converts Jinja templates to files."""
    copier_copy(
        {
            **copier_input_data,
            "is_github_project": True,
        }
    )

    template_files: list[Path] = [
        f.relative_to(djereo_root_dir / "template")
        for f in djereo_root_dir.rglob("*.jinja")
        if not f.name.startswith("{")
    ]

    def _transform_file_name(fname: str):
        fname = fname.replace("{{project_name}}", copier_input_data["project_name"])
        fname = fname.replace("{%if is_github_project%}.github{%endif%}", ".github")
        fname = fname.removesuffix(".jinja")
        return fname

    template_file_names: list[str] = [str(f) for f in template_files]
    template_file_names: list[str] = list(map(_transform_file_name, template_file_names))

    for file_name in template_file_names:
        expected_file_path = test_project_dir / file_name

        assert expected_file_path.exists(), (
            f"Expected file {expected_file_path} not found."
        )


@pytest.mark.integration
@pytest.mark.parametrize(
    ("is_github_project", "expected_directory_count", "expected_file_count"),
    [(True, 9, 23), (False, 8, 21)],
)
def test_is_github_project(
    is_github_project: bool,
    expected_directory_count: int,
    expected_file_count: int,
    test_project_dir: Path,
    copier_copy: Callable,
    copier_input_data: dict,
):
    copier_copy(
        {
            **copier_input_data,
            "is_github_project": is_github_project,
        },
        generate_dotenv=False,
    )

    num_dirs, num_files = count_dirs_and_files(test_project_dir)

    assert num_dirs == expected_directory_count
    assert num_files == expected_file_count


@pytest.mark.integration
def test_version_is_importable(
    set_up_generated_project: Path,
    copier_input_data: dict,
):
    from importlib.metadata import version

    assert version(copier_input_data["project_name"]) == "0.0.0"


@pytest.mark.integration
@pytest.mark.smoke
def test_generated_project_django_version_range(
    copier_copy: Callable,
    copier_input_data: dict,
    test_project_dir: Path,
):
    django_version = "5.2"
    copier_copy(
        {
            **copier_input_data,
            "django_version": django_version,
        }
    )
    with open(test_project_dir / "pyproject.toml", "rb") as f:
        toml_data = tomllib.load(f)

    dependencies = toml_data["project"]["dependencies"]
    django_dependency = next(dep for dep in dependencies if dep.startswith("django>="))
    constraint = django_dependency.split("django", 1)[1]

    specifier_set = SpecifierSet(constraint)

    assert Version(django_version) in specifier_set, (
        f"Django version {django_version} does not satisfy the constraint {constraint}"
    )


@pytest.mark.integration
def test_generated_toml_is_valid(
    copier_copy: Callable,
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    toml_files = list(test_project_dir.rglob("*.toml"))
    assert toml_files, "No TOML files found in the generated project."

    for file_path in toml_files:
        try:
            with open(file_path, "rb") as f:  # must be binary for tomllib
                tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            pytest.fail(f"Invalid TOML file: {file_path}\nError: {e}")


@pytest.mark.integration
def test_generated_yaml_is_valid(
    copier_copy: Callable,
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    yaml_files = list(test_project_dir.rglob("*.yaml")) + list(
        test_project_dir.rglob("*.yml")
    )
    assert yaml_files, "No YAML files found in the generated project."

    for file_path in yaml_files:
        with open(file_path) as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML file: {file_path}\nError: {e}")


@pytest.mark.integration
@pytest.mark.integration
@pytest.mark.smoke
@pytest.mark.skip_migrate
def test_generated_project_tests_run_successfully(
    set_up_generated_project: Path,
):
    """Verify that the generated project's tests pass using nox (end-user way)."""
    shutil.rmtree(set_up_generated_project / "tests_e2e", ignore_errors=True)

    # clear env vars to prevent meta-test variables from leaking into the nox sub-session
    env = os.environ.copy()
    env.pop("DEBUG", None)
    env.pop("USE_ENV_TEST", None)
    env.pop("DJANGO_SETTINGS_MODULE", None)

    result = subprocess.run(
        ["nox", "--", "--parallel=1"],
        cwd=set_up_generated_project,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, f"Nox failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.integration
@pytest.mark.smoke
def test_generated_project_pre_commit_hooks_run_successfully(
    set_up_generated_project: Path,
):
    test_project_dir = set_up_generated_project

    # prek will only run against files tracked by git
    subprocess.run(["git", "init"], cwd=test_project_dir, check=True, capture_output=True)
    subprocess.run(
        ["git", "add", "."], cwd=test_project_dir, check=True, capture_output=True
    )

    env = os.environ.copy()
    # ignore 'typos' as too noisy / picking up false positives in test context
    env["SKIP"] = "no-commit-to-branch,typos"

    result = subprocess.run(
        ["uv", "run", "prek", "run", "--all-files"],
        cwd=test_project_dir,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"Pre-commit hooks failed:\n{result.stdout}\n{result.stderr}"
    )
