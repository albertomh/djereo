import os
import re
import signal
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Callable, Generator
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag


def start_process_and_capture_streams(
    command_args: list, test_project_dir: Path, env: dict | None = None
) -> Generator[None, None, tuple[list[str], list[str]]]:
    """
    Starts a subprocess with the given command and environment variables,
    capturing stdout and stderr. Yields control to the caller after starting.
    """
    full_env = os.environ.copy()
    full_env.update({"PYTHONUNBUFFERED": "1"})
    if env:
        full_env.update(env)
    stdout_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    stderr_file = tempfile.NamedTemporaryFile(mode="w+", delete=False)

    try:
        stdout_file.close()
        stderr_file.close()

        process = subprocess.Popen(
            command_args,
            cwd=test_project_dir,
            stdout=open(stdout_file.name, "w"),
            stderr=open(stderr_file.name, "w"),
            text=True,
            env=full_env,
        )
        yield stdout_file.name, stderr_file.name
        process.wait(timeout=10)
    except subprocess.TimeoutExpired:
        if process.poll() is None:
            process.send_signal(signal.SIGINT)
    finally:
        stdout_lines, stderr_lines = [], []
        if os.path.exists(stdout_file.name):
            with open(stdout_file.name, "r") as f:
                stdout_lines = f.readlines()
            os.unlink(stdout_file.name)
        if os.path.exists(stderr_file.name):
            with open(stderr_file.name, "r") as f:
                stderr_lines = f.readlines()
            os.unlink(stderr_file.name)

    return stdout_lines, stderr_lines


def run_process_and_wait(
    command_args: list, test_project_dir: Path, env: dict | None = None
) -> tuple[list[str], list[str]]:
    """
    Runs a subprocess and waits for it to complete, capturing stdout and stderr.
    """
    generator = start_process_and_capture_streams(command_args, test_project_dir, env)
    try:
        next(generator)
        return next(generator)
    except StopIteration as e:
        return e.value


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

    _, stderr = run_process_and_wait(
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

    stdout, _ = run_process_and_wait(
        ["just", "runserver"],
        test_project_dir,
    )

    assert "Starting development server at http://127.0.0.1:8000/" in "".join(stdout)


@pytest.mark.integration
@pytest.mark.slow
def test_django_debug_toolbar_is_enabled(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)
    run_process_and_wait(
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
def test_runserver_dev_logs_use_rich(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    # arrange
    copier_copy(copier_input_data)
    process_generator = start_process_and_capture_streams(
        ["just", "runserver"],
        test_project_dir,
    )
    stdout_path, _ = next(process_generator)

    # act
    sentinel = "Quit the server with CONTROL-C."
    timeout, interval = 10, 0.1  # seconds
    start_time = time.time()

    while True:
        with open(stdout_path, "r") as stdout_file:
            stdout_lines = stdout_file.readlines()

        for line in stdout_lines:
            if sentinel in line:
                break
        else:
            if time.time() - start_time > timeout:
                pytest.fail(f"'{sentinel}' not found within timeout")
            time.sleep(interval)
            continue
        break

    with urlopen("http://127.0.0.1:8000/") as response:
        assert response.status == 200

    try:
        stdout, _ = next(process_generator)
    except StopIteration as e:
        stdout, _ = e.value

    # assert
    pattern = r'\[\d{2}:\d{2}:\d{2}\] INFO\s+"GET \/ HTTP\/1\.1" 200 \d+\s+basehttp\.py'
    match = re.search(pattern, "".join(stdout))
    assert match is not None


@pytest.mark.integration
@pytest.mark.slow
def test_shell_uses_ipython(
    skip_if_github_actions,
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    stdout, _ = run_process_and_wait(["just", "shell"], test_project_dir)

    assert "An enhanced Interactive Python" in "".join(stdout)
