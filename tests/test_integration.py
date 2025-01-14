import os
import signal
import subprocess
import time
from pathlib import Path
from typing import Callable, Literal

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


def collect_stream_output(
    stream: Literal["stdout", "stderr"],
    process,
    timeout: int,
    break_condition: Callable[[str], bool],
):
    """Collect stdout or stderr output until a break condition or timeout is met."""
    output = []
    start_time = time.time()

    while time.time() - start_time < timeout:
        if stream == "stdout":
            line = process.stdout.readline()
        elif stream == "stderr":
            line = process.stderr.readline()
        if line:
            output.append(line)
            if break_condition(line):
                break

    return "".join(output)


def terminate_process(process):
    """Terminate the process safely."""
    if process.poll() is None:
        process.send_signal(signal.SIGINT)


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
        stderr_output = collect_stream_output(
            "stderr",
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


@pytest.mark.integration
@pytest.mark.slow
def test_shell_uses_ipython(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
):
    copier_copy(copier_input_data)

    shell_process = subprocess.Popen(
        ["just", "shell"],
        cwd=test_project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    ipython_sentinel = "An enhanced Interactive Python"
    try:
        stdout_output = collect_stream_output(
            "stdout",
            shell_process,
            TIMEOUT,
            lambda line: ipython_sentinel in line,
        )

        assert ipython_sentinel in stdout_output

    finally:
        terminate_process(shell_process)
