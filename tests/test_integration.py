import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Callable

import pytest


@pytest.mark.integration
@pytest.mark.slow
def test_runserver_uses_python_dev_mode(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
):
    """
    Trigger an ImportWarning in a generated project and check this is visible when the
    `runserver` recipe is invoked.
    """
    copier_copy(copier_input_data)
    with open(test_project_dir / test_project_name / "__init__.py", "w") as f:
        f.write("import warnings\n")
        f.write("warnings.warn('This is a forced ImportWarning', ImportWarning)\n")

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"  # allows Django sys checks to be visible in real time
    server_process = subprocess.Popen(
        ["just", "runserver"],
        cwd=test_project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    stderr_output = []
    try:
        start_time = time.time()
        while time.time() - start_time < 15:
            line = server_process.stderr.readline()
            if line:
                stderr_output.append(line)
                if "Watching for file changes with StatReloader" in line:
                    break

        server_process.send_signal(signal.SIGINT)

        full_stderr_output = "".join(stderr_output)
        assert "This is a forced ImportWarning" in full_stderr_output

    finally:
        if server_process.poll() is None:
            server_process.send_signal(signal.SIGINT)


@pytest.mark.integration
@pytest.mark.slow
def test_sys_check_warn_no_dev_mode_when_debug(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
):
    """"""
    copier_copy(copier_input_data)

    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"  # allows Django sys checks to be visible in real time
    server_process = subprocess.Popen(
        ["just", "runserver", ""],  # only an empty string disables PYTHONDEVMODE
        cwd=test_project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=env,
    )

    stderr_output = []
    try:
        start_time = time.time()
        while time.time() - start_time < 15:
            line = server_process.stderr.readline()
            if line:
                stderr_output.append(line)
                if "System check identified 1 issue" in line:
                    break

        server_process.send_signal(signal.SIGINT)

        expected_warning = (
            f"?: ({test_project_name}.W001) Python Development Mode is not enabled yet "
            "DEBUG is true."
        )
        full_stderr_output = "".join(stderr_output)
        assert expected_warning in full_stderr_output

    finally:
        if server_process.poll() is None:
            server_process.send_signal(signal.SIGINT)
