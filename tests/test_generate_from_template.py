import os
import tomllib
from pathlib import Path
from typing import Callable

import pytest
import yaml
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from sh import RunningCommand, git, nox, uv

from tests._utils import count_dirs_and_files


@pytest.mark.integration
@pytest.mark.smoke
def test_djereo_jinja_templates_converted(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    djereo_root_dir: Path,
    test_project_dir: Path,
):
    """Validate that generating a project converts Jinja templates to files."""
    copier_copy(copier_input_data)

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
    "is_github_project, expected_directory_count, expected_file_count",
    [(True, 8, 21), (False, 7, 19)],
)
def test_is_github_project(
    is_github_project: bool,
    expected_directory_count: int,
    expected_file_count: int,
    test_project_dir: Path,
    copier_copy: Callable[[dict], None],
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
    install_test_project,
    test_project_name: str,
):
    from importlib.metadata import version

    assert version(test_project_name) == "0.0.0"


@pytest.mark.integration
@pytest.mark.smoke
def test_generated_project_django_version_range(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    django_version = "5.1"
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
def test_generated_yaml_is_valid(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    yaml_files = [
        test_project_dir / ".markdownlint-cli2.yaml",
        test_project_dir / ".pre-commit-config.yaml",
    ]

    copier_copy(copier_input_data)

    for file_path in yaml_files:
        with open(file_path, "r") as f:
            try:
                yaml.safe_load(f)
            except yaml.YAMLError as e:
                pytest.fail(f"Invalid YAML file: {file_path}\nError: {e}")


@pytest.mark.integration
@pytest.mark.smoke
def test_generated_project_tests_run_successfully(
    test_project_dir: Path,
    generate_test_project_with_db,
):
    result: RunningCommand = nox(_cwd=test_project_dir, _return_cmd=True)

    assert result.exit_code == 0, f"Pytest failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.integration
@pytest.mark.smoke
def test_generated_project_pre_commit_hooks_run_successfully(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    # pre-commit will only run against files tracked by git
    git("init", _cwd=test_project_dir)
    git("add", ".", _cwd=test_project_dir)

    env = os.environ.copy()
    env["SKIP"] = "no-commit-to-branch"
    pre_commit_res = uv(
        "run",
        "pre-commit",
        "run",
        "--all-files",
        _cwd=test_project_dir,
        _env=env,
        _return_cmd=True,
    )
    assert pre_commit_res.exit_code == 0, (
        f"Pre-commit hooks failed:\n{pre_commit_res.stdout}\n{pre_commit_res.stderr}"
    )
