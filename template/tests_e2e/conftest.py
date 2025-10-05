# >>> uv run pytest tests_e2e/
# Locally, set the CI environment variable to run in headless browser:
# >>> CI=true uv run pytest tests_e2e/

import sys
import time

import pytest
import requests  # type: ignore
from environs import Env
from playwright.sync_api import Browser, Playwright, sync_playwright
from playwright.sync_api import Error as PlaywrightError

env = Env()
env.read_env()

BASE_URL = "http://127.0.0.1:8000"


def _launch_browser(headless: bool = True) -> tuple[Playwright, Browser]:
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    return playwright, browser


def pytest_sessionstart(session):
    """Check webapp is available before attempting to collect and run the test suite."""
    timeout = 10
    interval = 0.5
    start = time.time()
    while True:
        try:
            resp = requests.get(BASE_URL, timeout=1)
            if resp.status_code < 500:
                break
        except Exception:
            pass
        if time.time() - start > timeout:
            pytest.exit(f"Server at {BASE_URL} is unavailable", returncode=1)
        time.sleep(interval)

    try:
        playwright, browser = _launch_browser(True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL, timeout=3000)

    except PlaywrightError as e:
        print(e, file=sys.stderr)  # noqa: T201 print
        pytest.exit("Startup check failed", returncode=1)

    finally:
        context.close()
        browser.close()
        playwright.stop()


@pytest.fixture(scope="session")
def browser():
    """Start Playwright Chromium once per test session."""
    is_ci = env.bool("CI", default=False)
    is_gha = env.bool("GITHUB_ACTIONS", default=False)
    headless = is_ci or is_gha
    playwright, browser = _launch_browser(headless)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def page(browser):
    """Provide a fresh page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
