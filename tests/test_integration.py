import os
import re
import time
from http import HTTPStatus
from io import StringIO
from pathlib import Path
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag
from sh import ErrorReturnCode, uv

from tests._utils import get_free_port_from_os, remove_ansi_escape_codes, wait_for_server

TIMEOUT_SECONDS = 30.0


def _wait_for_output(
    stream: StringIO,
    pattern: str | re.Pattern,
    *,
    timeout=TIMEOUT_SECONDS,
    interval=0.1,
) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        content = remove_ansi_escape_codes(stream.getvalue())
        if isinstance(pattern, str):
            if pattern in content:
                return True
        elif pattern.search(content):
            return True
        time.sleep(interval)
    return False


def _wait_for_server_start(
    out: StringIO,
    *,
    timeout=30.0,
    interval=0.1,
    urls_to_get: list[tuple[str, int]] | None = None,
) -> bool:
    if urls_to_get is None:
        urls_to_get = []
    sentinel = "Quit the server with CONTROL-C."
    start = time.time()

    while time.time() - start < timeout:
        if sentinel in out.getvalue():
            for url, expected_status in urls_to_get:
                with urlopen(url) as response:
                    time.sleep(interval)
                    assert response.status == expected_status
            return True
        time.sleep(interval)

    return False


@pytest.mark.xdist_group(name="integration")
@pytest.mark.integration
@pytest.mark.smoke
def test_runserver(
    set_up_generated_project: Path,
):
    out = StringIO()
    host = "127.0.0.1"
    port = get_free_port_from_os()

    server = uv.run(
        "manage.py",
        "runserver",
        f"{host}:{port}",
        "--noreload",
        _bg=True,
        _cwd=set_up_generated_project,
        _env={"PYTHONUNBUFFERED": "1"},
        _ok_code=[0, 143],
        _out=out,
    )

    try:
        wait_for_server(host, port)
        start_message = f"Starting development server at http://{host}:{port}/"
        assert start_message in out.getvalue()
    finally:
        if server is not None:
            server.terminate()
            server.wait()


@pytest.mark.xdist_group(name="integration")
@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize("django_debug", [True])
def test_django_debug_toolbar_is_enabled(
    set_up_generated_project: Path,
    django_debug: bool,
):
    out = StringIO()
    host = "127.0.0.1"
    port = get_free_port_from_os()

    server = uv.run(
        "manage.py",
        "runserver",
        f"{host}:{port}",
        "--noreload",
        _bg=True,
        _cwd=set_up_generated_project,
        _ok_code=[0, 143],
        _out=out,
    )

    try:
        wait_for_server(host, port)
        with urlopen(f"http://{host}:{port}/") as response:
            res_bytes = response.read()
        res_html = res_bytes.decode("utf8")
        html = BeautifulSoup(res_html, features="html.parser")
        dj_debug_toolbar = html.find("div", {"id": "djDebug"})
        assert type(dj_debug_toolbar) is Tag
    finally:
        if server is not None:
            server.terminate()
            server.wait()


@pytest.mark.xdist_group(name="integration")
@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize("django_debug", [True])
def test_sys_check_warn_no_dev_mode_when_debug(
    set_up_generated_project: Path,
    django_debug: bool,
):
    """Ensure a system check warning is raised if Dev Mode is disabled & DEBUG is True."""
    out, err = StringIO(), StringIO()

    expected_warning = (
        "(core.W001) Python Development Mode is not enabled yet DEBUG is true."
    )

    env = {**os.environ}
    env.pop("PYTHONDEVMODE", None)  # ensure dev mode disabled
    env["PYTHONUNBUFFERED"] = "1"

    uv.run(
        "manage.py",
        "check",
        _out=out,
        _err=err,
        _cwd=set_up_generated_project,
        _env=env,
    )

    stderr = err.getvalue()
    assert expected_warning in stderr


@pytest.mark.xdist_group(name="integration")
@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.parametrize("django_debug", [True])
def test_runserver_dev_logs_use_rich(
    set_up_generated_project: Path,
    django_debug: bool,
):
    out = StringIO()
    host = "127.0.0.1"
    port = get_free_port_from_os()

    server = uv.run(
        "manage.py",
        "runserver",
        f"{host}:{port}",
        "--noreload",
        _bg=True,
        _bg_exc=False,
        _cwd=set_up_generated_project,
        _env={"PYTHONUNBUFFERED": "1"},
        _err=out,
        _ok_code=[0, 143],
        _out=out,
    )

    try:
        wait_for_server(host, port)
        with urlopen(f"http://{host}:{port}/") as response:
            response.read()
        max_wait = 5
        start = time.time()
        pattern = r"\[\d{2}:\d{2}:\d{2}\] INFO\s+ 200 GET \/ HTTP\/1\.1\s+"

        while True:
            clean_stdout = remove_ansi_escape_codes(out.getvalue())
            if re.search(pattern, clean_stdout):
                break
            if time.time() - start > max_wait:
                raise TimeoutError("Expected log line not found")  # noqa: TRY003
            time.sleep(0.1)
        pattern = r"\[\d{2}:\d{2}:\d{2}\] INFO\s+ 200 GET \/ HTTP\/1\.1\s+"
    finally:
        if server is not None:
            server.terminate()
            server.wait()


@pytest.mark.xdist_group(name="integration")
@pytest.mark.integration
@pytest.mark.slow
def test_missing_env_file_warning_and_traceback_suppression(
    set_up_generated_project: Path,
):
    """Ensure a warning is raised and traceback suppressed if .env is missing."""
    env_file = set_up_generated_project / ".env"
    temp_env_file = set_up_generated_project / ".env.temp"
    if env_file.exists():
        env_file.rename(temp_env_file)

    out, err = StringIO(), StringIO()
    expected_warning = "No .env file found. Run `cp .env.in .env` to get started."
    expected_error = (
        'environs.exceptions.EnvError: Environment variable "SECRET_KEY" not set'
    )

    try:
        uv(
            "run",
            "manage.py",
            "check",
            _out=out,
            _err=err,
            _cwd=set_up_generated_project,
            _env={"PYTHONUNBUFFERED": "1"},
        )
    except ErrorReturnCode:
        # command is expected to fail
        pass

    stderr = remove_ansi_escape_codes(err.getvalue())

    assert expected_warning in stderr
    assert expected_error in stderr

    if temp_env_file.exists():
        temp_env_file.rename(env_file)


@pytest.mark.smoke
def test_django_allauth_pages_exist(django_test_client):
    allauth_urls = [
        "/accounts/login/",
        "/accounts/signup/",
    ]
    for url in allauth_urls:
        response = django_test_client.get(url)
        assert response.status_code == HTTPStatus.OK
