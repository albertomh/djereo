import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Callable

import pytest

TIMEOUT = 15  # in seconds, timeout for server process checks
PYTHON_UNBUFFERED_ENV = {"PYTHONUNBUFFERED": "1"}


def run_server(test_project_dir: Path, command_args: list, env: dict):
    """Run the server process with the given arguments and environment."""
    full_env = os.environ.copy()
    full_env.update(env)

    return subprocess.Popen(
        ["just", "runserver", *command_args],
        cwd=test_project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=full_env,
    )


def collect_stderr_output(process, timeout: int, break_condition: Callable[[str], bool]):
    """Collect stderr output until a break condition or timeout is met."""
    stderr_output = []
    start_time = time.time()

    while time.time() - start_time < timeout:
        line = process.stderr.readline()
        if line:
            stderr_output.append(line)
            if break_condition(line):
                break

    return "".join(stderr_output)


def terminate_process(process):
    """Terminate the process safely."""
    if process.poll() is None:
        process.send_signal(signal.SIGINT)


@pytest.mark.integration
@pytest.mark.slow
def test_runserver_uses_python_dev_mode(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
):
    """
    Trigger an ImportWarning in a generated project and check it is visible when the
    `runserver` recipe is invoked.
    """
    copier_copy(copier_input_data)
    (test_project_dir / test_project_name / "__init__.py").write_text(
        "import warnings\n"
        "warnings.warn('This is a forced ImportWarning', ImportWarning)"
    )

    server_process = run_server(test_project_dir, [], PYTHON_UNBUFFERED_ENV)

    try:
        stderr_output = collect_stderr_output(
            server_process,
            TIMEOUT,
            lambda line: "Watching for file changes with StatReloader" in line,
        )

        assert "This is a forced ImportWarning" in stderr_output

    finally:
        terminate_process(server_process)


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

    server_process = run_server(test_project_dir, [""], PYTHON_UNBUFFERED_ENV)

    try:
        stderr_output = collect_stderr_output(
            server_process,
            TIMEOUT,
            lambda line: "System check identified 1 issue" in line,
        )

        expected_warning = (
            f"?: ({test_project_name}.W001) Python Development Mode is not enabled yet "
            "DEBUG is true."
        )
        assert expected_warning in stderr_output

    finally:
        terminate_process(server_process)
