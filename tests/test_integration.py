import time
import urllib
from contextlib import suppress
from http import HTTPStatus
from io import StringIO

import pytest
from sh import ErrorReturnCode

from tests._utils import get_free_port_from_os, remove_ansi_escape_codes

TIMEOUT_SECONDS = 60.0


def wait_for_server_start(
    out: StringIO,
    *,
    timeout=TIMEOUT_SECONDS,
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
                with urllib.request.urlopen(url) as response:
                    time.sleep(interval)
                    assert response.status == expected_status
            return True
        time.sleep(interval)

    return False


@pytest.mark.integration
@pytest.mark.slow
def test_sys_check_warn_no_dev_mode_when_debug(
    generated_project_sqlite,
    project_cmd,
):
    """Ensure system check warns if Python Dev Mode disabled while DEBUG=True."""
    out, err = StringIO(), StringIO()

    project_cmd(
        generated_project_sqlite,
        "manage.py",
        "check",
        _out=out,
        _err=err,
        _env={"PYTHONUNBUFFERED": "1"},
    )

    stderr = remove_ansi_escape_codes(err.getvalue())

    assert "Python Development Mode is not enabled yet DEBUG is true" in stderr


@pytest.mark.integration
@pytest.mark.slow
def test_missing_env_file_warning_and_traceback_suppression(
    generated_project,
    project_cmd,
):
    out, err = StringIO(), StringIO()
    expected_warning = "No .env file found. Run `cp .env.in .env` to get started."
    expected_error = (
        'environs.exceptions.EnvError: Environment variable "SECRET_KEY" not set'
    )

    env_file = generated_project / ".env"
    if env_file.exists():
        env_file.unlink()
    try:
        project_cmd(
            generated_project,
            "manage.py",
            "check",
            _out=out,
            _err=err,
        )
    except ErrorReturnCode:
        pass

    clean_stderr = remove_ansi_escape_codes(err.getvalue())

    assert expected_warning in clean_stderr
    assert expected_error in clean_stderr
    # since `tracebacklimit =0`, "Traceback (most ...):" should NOT be in stderr
    assert "Traceback (most recent call last):" not in clean_stderr


@pytest.mark.integration
@pytest.mark.smoke
def test_runserver(
    generated_project_sqlite,
    project_cmd,
):
    out = StringIO()
    addrport = f"127.0.0.1:{get_free_port_from_os()}"

    with suppress(Exception):
        project_cmd(
            generated_project_sqlite,
            "manage.py",
            "runserver",
            addrport,
            _timeout=TIMEOUT_SECONDS,
            _bg=True,
            _bg_exc=False,
            _out=out,
        )

        started = wait_for_server_start(out, addrport)

        if not started:
            pytest.fail("Django runserver did not start")


@pytest.mark.integration
@pytest.mark.slow
def test_django_debug_toolbar_is_enabled(
    generated_project_sqlite,
    project_cmd,
):
    """Ensure debug toolbar middleware is active."""
    out = StringIO()
    addrport = f"127.0.0.1:{get_free_port_from_os()}"

    with suppress(Exception):
        project_cmd(
            generated_project_sqlite,
            "manage.py",
            "runserver",
            addrport,
            _timeout=TIMEOUT_SECONDS,
            _bg=True,
            _bg_exc=False,
            _out=out,
        )

        if not wait_for_server_start(out, addrport):
            pytest.fail("Django runserver did not start")

        resp = urllib.request.urlopen(f"http://{addrport}/")
        html = resp.read().decode()

        assert "djDebug" in html or "debug_toolbar" in html


@pytest.mark.integration
@pytest.mark.slow
def test_runserver_dev_logs_use_rich(
    generated_project_sqlite,
    project_cmd,
):
    """Ensure dev server logs use Rich formatting."""
    out = StringIO()
    addrport = f"127.0.0.1:{get_free_port_from_os()}"

    with suppress(Exception):
        project_cmd(
            generated_project_sqlite,
            "manage.py",
            "runserver",
            addrport,
            _timeout=TIMEOUT_SECONDS,
            _bg=True,
            _bg_exc=False,
            _out=out,
        )

        if not wait_for_server_start(out, addrport):
            pytest.fail("Django runserver did not start")

        urllib.request.urlopen(f"http://{addrport}/")

        logs = out.getvalue()

        assert "GET /" in logs


@pytest.mark.integration
@pytest.mark.smoke
@pytest.mark.slow
def test_django_allauth_pages_exist(
    generated_project_sqlite,
    project_cmd,
):
    """Ensure key Django Allauth pages return HTTP 200."""
    out = StringIO()
    addrport = f"127.0.0.1:{get_free_port_from_os()}"

    with suppress(Exception):
        project_cmd(
            generated_project_sqlite,
            "manage.py",
            "runserver",
            addrport,
            _timeout=TIMEOUT_SECONDS,
            _bg=True,
            _bg_exc=False,
            _out=out,
        )

        if not wait_for_server_start(out, addrport):
            pytest.fail("Django runserver did not start")

        urls = [
            "/accounts/login/",
            "/accounts/signup/",
            "/accounts/password/reset/",
        ]

        for path in urls:
            resp = urllib.request.urlopen(f"http://{addrport}{path}")
            assert resp.status == HTTPStatus.OK
