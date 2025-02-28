import re
import time
from contextlib import suppress
from io import StringIO
from pathlib import Path
from typing import Callable
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag
from sh import TimeoutException, just

from tests._utils import remove_ansi_escape_codes


@pytest.mark.integration
@pytest.mark.slow
def test_sys_check_warn_no_dev_mode_when_debug(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_name: str,
    test_project_dir: Path,
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    """
    Verify that a system check warning is shown when Python Development Mode is disabled
    and DEBUG is true.
    """
    copier_copy(copier_input_data)
    set_up_test_database()
    out, err = StringIO(), StringIO()
    timeout, interval = 10, 0.1  # seconds
    expected_warning = (
        f"({test_project_name}.W001) Python Development Mode is not enabled yet DEBUG is"
        " true."
    )

    sentinel = "Quit the server with CONTROL-C."
    start = time.time()
    with suppress(TimeoutException):
        just(
            # PYTHONDEVMODE can only be disabled by setting it to an empty string
            "runserver",
            "",
            _timeout=timeout,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _err=err,
            _cwd=test_project_dir,
        )
        while (time.time() - start) < timeout:
            if sentinel in out.getvalue():
                clean_stderr = remove_ansi_escape_codes(err.getvalue())
                assert expected_warning in clean_stderr
                return
            time.sleep(interval)

    raise AssertionError("Django runserver did not start in time")


@pytest.mark.integration
@pytest.mark.smoke
def test_runserver(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    copier_copy(copier_input_data)
    set_up_test_database()
    out = StringIO()
    timeout, interval = 10, 0.1  # seconds

    sentinel = "Quit the server with CONTROL-C."
    start = time.time()
    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=timeout,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        while (time.time() - start) < timeout:
            if sentinel in out.getvalue():
                start_message = "Starting development server at http://127.0.0.1:8000/"
                assert start_message in out.getvalue()
                return
            time.sleep(interval)

    raise AssertionError("Django runserver did not start in time")


@pytest.mark.integration
@pytest.mark.slow
def test_django_debug_toolbar_is_enabled(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    copier_copy(copier_input_data)
    set_up_test_database()
    out = StringIO()
    timeout, interval = 10, 0.1  # seconds

    sentinel = "Quit the server with CONTROL-C."
    start = time.time()
    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=timeout,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        while (time.time() - start) < timeout:
            if sentinel in out.getvalue():
                with urlopen("http://127.0.0.1:8000/") as response:
                    res_bytes = response.read()
            time.sleep(interval)

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
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    copier_copy(copier_input_data)
    set_up_test_database()
    out = StringIO()
    timeout, interval = 10, 0.1  # seconds

    sentinel = "Quit the server with CONTROL-C."
    start = time.time()
    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=timeout,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        while (time.time() - start) < timeout:
            if sentinel in out.getvalue():
                with urlopen("http://127.0.0.1:8000/") as response:
                    assert response.status == 200
            time.sleep(interval)

    pattern = r"\[\d{2}:\d{2}:\d{2}\] INFO\s+ 200 GET \/ HTTP\/1\.1\s+"
    clean_stdout = remove_ansi_escape_codes(out.getvalue())
    match = re.search(pattern, clean_stdout)
    assert match is not None


@pytest.mark.integration
@pytest.mark.smoke
@pytest.mark.slow
def test_django_allauth_pages_exist(
    copier_copy: Callable[[dict], None],
    copier_input_data: dict,
    test_project_dir: Path,
    set_up_test_database: Callable[[], None],
    tear_down_test_database,
):
    allauth_urls = [
        "/accounts/login/",
        "/accounts/signup/",
    ]
    copier_copy(copier_input_data)
    set_up_test_database()
    just("manage", "migrate", _cwd=test_project_dir)
    out = StringIO()
    timeout, interval = 15, 0.1  # seconds

    sentinel = "Quit the server with CONTROL-C."
    start = time.time()
    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=timeout,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        while (time.time() - start) < timeout:
            if sentinel in out.getvalue():
                for url in allauth_urls:
                    with urlopen(f"http://127.0.0.1:8000{url}") as response:
                        assert response.status == 200
                return
            time.sleep(interval)

    raise AssertionError("Django runserver did not start in time")
