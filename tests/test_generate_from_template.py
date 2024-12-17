import os
import subprocess
from pathlib import Path
from typing import Callable

import pytest
import yaml

from tests._utils import count_dirs_and_files


@pytest.mark.integration
@pytest.mark.smoke
def test_pycliche_jinja_templates_converted(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    pycliche_root_dir: Path,
    test_project_dir: Path,
):
    """Validate that generating a project converts Jinja templates to files."""
    copier_copy(copier_input_data)

    template_files: list[Path] = [
        f.relative_to(pycliche_root_dir / "template")
        for f in pycliche_root_dir.rglob("*.jinja")
        if not f.name.startswith("{")
    ]

    def _transform_file_name(fname: str):
        fname = fname.replace("{{project_name}}", copier_input_data["project_name"])
        fname = fname.removesuffix(".jinja")
        return fname

    template_file_names: list[str] = [str(f) for f in template_files]
    template_file_names: list[str] = list(map(_transform_file_name, template_file_names))

    for file_name in template_file_names:
        expected_file_path = test_project_dir / file_name

        assert (
            expected_file_path.exists()
        ), f"Expected file {expected_file_path} not found."


@pytest.mark.integration
@pytest.mark.parametrize(
    "is_github_project, expected_directory_count, expected_file_count",
    [(True, 4, 15), (False, 3, 13)],
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
        }
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

    assert version(test_project_name) == "0.1.0"


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
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    install_res = subprocess.run(
        ["uv", "pip", "install", "-e", "."],
        cwd=test_project_dir,
        capture_output=True,
        text=True,
    )
    assert (
        install_res.returncode == 0
    ), f"Dependency installation failed:\n{install_res.stdout}\n{install_res.stderr}"

    result = subprocess.run(
        ["pytest"], cwd=test_project_dir, capture_output=True, text=True
    )

    assert result.returncode == 0, f"Pytest failed:\n{result.stdout}\n{result.stderr}"


@pytest.mark.integration
@pytest.mark.smoke
def test_generated_project_pre_commit_hooks_run_successfully(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    # pre-commit will only run against files tracked by git
    subprocess.run(["git", "init"], cwd=test_project_dir, check=True)
    subprocess.run(["git", "add", "."], cwd=test_project_dir, check=True)

    env = os.environ.copy()
    env["SKIP"] = "no-commit-to-branch"
    pre_commit_result = subprocess.run(
        ["uv", "run", "pre-commit", "run", "--all-files"],
        cwd=test_project_dir,
        env=env,
        capture_output=True,
        text=True,
    )
    assert (
        pre_commit_result.returncode == 0
    ), f"Pre-commit hooks failed:\n{pre_commit_result.stdout}\n{pre_commit_result.stderr}"
