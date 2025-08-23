# >>> uv run pytest tests_e2e/
# Locally, set the CI environment variable to run in headless browser:
# >>> CI=true uv run pytest tests_e2e/

import sys

import pytest
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
    try:
        playwright, browser = _launch_browser(True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL, timeout=3000)

    except PlaywrightError as e:
        print(e, file=sys.stderr)  # noqa: T201
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
