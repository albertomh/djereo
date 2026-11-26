# >>> uv run pytest tests_e2e/
# Locally, set the HEADED environment variable to see the browser:
# >>> HEADED=true uv run pytest tests_e2e/

import time

import pytest
import requests  # type: ignore
from axe_playwright_python.sync_playwright import Axe
from environs import Env
from playwright.sync_api import Browser, Page, expect, sync_playwright

env = Env()
env.read_env()

BASE_URL = env.str("BASE_URL", "http://127.0.0.1:8000")
MAILPIT_API_BASE_URL = "http://127.0.0.1:8025"
HTTP_SERVER_ERROR = 500


def pytest_sessionstart(session):
    """Check webapp is available before attempting to collect and run the test suite."""
    timeout = 10
    interval = 0.5
    start = time.monotonic()
    while True:
        try:
            resp = requests.get(BASE_URL, timeout=1)
            if resp.status_code < HTTP_SERVER_ERROR:
                if "djDebugRoot" in resp.text:
                    pytest.exit(
                        "Django Debug Toolbar must be disabled during E2E", returncode=1
                    )
                break
        except requests.RequestException:
            pass
        if time.monotonic() - start > timeout:
            pytest.exit(f"Server at {BASE_URL} is unavailable", returncode=1)
        time.sleep(interval)


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Start Playwright Chromium once per test session."""
    headless = not env.bool("HEADED", False)
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=headless)
    yield browser
    browser.close()
    playwright.stop()


@pytest.fixture
def page(browser: Browser) -> Page:
    """Provide a fresh page for each test."""
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


def log_in(
    page: Page, email: str = "user@example.com", password: str = "password"
) -> None:
    page.goto(f"{BASE_URL}/accounts/login/")
    page.locator("#id_login").fill(email)
    page.locator("#id_password").fill(password)
    page.locator('button[type="submit"]').click()
    expect(page).to_have_url(f"{BASE_URL}/")


@pytest.fixture
def axe() -> Axe:
    """Provide an Axe instance for accessibility testing."""
    return Axe()
