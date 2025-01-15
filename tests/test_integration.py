import os
import signal
import subprocess
import tempfile
from pathlib import Path
from typing import Callable
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag


def run_process_capture_streams(
    command_args: list, test_project_dir: Path, env: dict | None = None
) -> tuple[list[str], list[str]]:
    """
    Run a given shell command with the given environment variables, while capturing
    stdout and stderr. Wait for 10 seconds and terminate.
    """
    full_env = os.environ.copy()
    full_env.update({"PYTHONUNBUFFERED": "1"})
    if env:
        full_env.update(env)
    stdout_capture = tempfile.TemporaryFile(mode="w+")
    stderr_capture = tempfile.TemporaryFile(mode="w+")

    process = subprocess.Popen(
        command_args,
        cwd=test_project_dir,
        stdout=stdout_capture,
        stderr=stderr_capture,
        text=True,
        env=full_env,
    )
    try:
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)

    stdout_capture.seek(0)
    stdout_lines = stdout_capture.readlines()
    stderr_capture.seek(0)
    stderr_lines = stderr_capture.readlines()
    return stdout_lines, stderr_lines


@pytest.mark.integration
@pytest.mark.slow
def test_sys_check_warn_no_dev_mode_when_debug(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
):
    """
    Verify that a system check warning is shown when Python Development Mode is disabled
    and DEBUG is true.
    """
    copier_copy(copier_input_data)

    _, stderr = run_process_capture_streams(
        # PYTHONDEVMODE can only be disabled by setting it to an empty string
        ["just", "runserver", ""],
        test_project_dir,
    )

    expected_warning = (
        f"WARNINGS:\n?: ({test_project_name}.W001) Python Development Mode is not enabled"
        " yet DEBUG is true."
    )
    assert expected_warning in "".join(stderr)


@pytest.mark.integration
@pytest.mark.smoke
def test_runserver(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    stdout, _ = run_process_capture_streams(
        ["just", "runserver"],
        test_project_dir,
    )

    assert "Starting development server at http://127.0.0.1:8000/" in "".join(stdout)


@pytest.mark.integration
@pytest.mark.smoke
def test_django_debug_toolbar_is_enabled(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)
    run_process_capture_streams(
        ["just", "runserver"],
        test_project_dir,
    )

    with urlopen("http://127.0.0.1:8000/") as response:
        res_bytes = response.read()
    res_html = res_bytes.decode("utf8")
    html = BeautifulSoup(res_html)
    dj_debug_toolbar = html.find("div", {"id": "djDebug"})

    assert type(dj_debug_toolbar) is Tag


@pytest.mark.integration
@pytest.mark.slow
def test_shell_uses_ipython(
    skip_if_github_actions,
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    stdout, _ = run_process_capture_streams(["just", "shell"], test_project_dir)

    assert "An enhanced Interactive Python" in "".join(stdout)
