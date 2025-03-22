import re
import time
from contextlib import suppress
from io import StringIO
from pathlib import Path
from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from bs4.element import Tag
from sh import TimeoutException, just

from tests._utils import remove_ansi_escape_codes


def wait_for_server_start(
    out: StringIO,
    *,
    timeout=10.0,
    interval=0.1,
    urls_to_get: list[tuple[str, int]] = None,
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


@pytest.mark.integration
@pytest.mark.slow
def test_sys_check_warn_no_dev_mode_when_debug(
    test_project_name: str,
    test_project_dir: Path,
    generate_test_project_with_db,
):
    """
    Verify that a system check warning is shown when Python Development Mode is disabled
    and DEBUG is true.
    """
    out, err = StringIO(), StringIO()
    expected_warning = (
        f"({test_project_name}.W001) Python Development Mode is not enabled yet DEBUG is"
        " true."
    )

    with suppress(TimeoutException):
        just(
            "runserver",
            # PYTHONDEVMODE can only be disabled by setting it to an empty string
            "",
            _timeout=10,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _err=err,
            _cwd=test_project_dir,
        )
        assert wait_for_server_start(out), "Django runserver did not start in time"

    clean_stderr = remove_ansi_escape_codes(err.getvalue())
    assert expected_warning in clean_stderr


@pytest.mark.integration
@pytest.mark.smoke
def test_runserver(
    test_project_dir: Path,
    generate_test_project_with_db,
):
    out = StringIO()

    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=10,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        assert wait_for_server_start(out), "Django runserver did not start in time"

    start_message = "Starting development server at http://127.0.0.1:8000/"
    assert start_message in out.getvalue()


@pytest.mark.integration
@pytest.mark.slow
def test_django_debug_toolbar_is_enabled(
    test_project_dir: Path,
    generate_test_project_with_db,
):
    out = StringIO()

    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=10,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        assert wait_for_server_start(out), "Django runserver did not start in time"
    with urlopen("http://127.0.0.1:8000/") as response:
        res_bytes = response.read()
    res_html = res_bytes.decode("utf8")
    html = BeautifulSoup(res_html, features="html.parser")
    dj_debug_toolbar = html.find("div", {"id": "djDebug"})

    assert type(dj_debug_toolbar) is Tag


@pytest.mark.integration
@pytest.mark.slow
def test_runserver_dev_logs_use_rich(
    test_project_dir: Path,
    generate_test_project_with_db,
):
    out = StringIO()

    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=10,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        urls_to_get = [("http://127.0.0.1:8000/", 200)]
        assert wait_for_server_start(out, urls_to_get=urls_to_get), (
            "Django runserver did not start in time"
        )

    pattern = r"\[\d{2}:\d{2}:\d{2}\] INFO\s+ 200 GET \/ HTTP\/1\.1\s+"
    clean_stdout = remove_ansi_escape_codes(out.getvalue())
    match = re.search(pattern, clean_stdout)
    assert match is not None


@pytest.mark.integration
@pytest.mark.smoke
@pytest.mark.slow
def test_django_allauth_pages_exist(
    test_project_dir: Path,
    generate_test_project_with_db,
):
    allauth_urls = [
        "accounts/login/",
        "accounts/signup/",
    ]
    just("manage", "migrate", _cwd=test_project_dir)
    out = StringIO()

    with suppress(TimeoutException):
        just(
            "runserver",
            _timeout=10,
            _bg=True,
            _bg_exc=False,
            _out=out,
            _cwd=test_project_dir,
        )
        urls_to_get = [(f"http://127.0.0.1:8000/{url}", 200) for url in allauth_urls]
        assert wait_for_server_start(out, urls_to_get=urls_to_get), (
            "Django runserver did not start in time"
        )
