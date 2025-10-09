import warnings

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

from tests_e2e.conftest import BASE_URL


class TestAccessibility:
    @pytest.mark.parametrize(
        "url",
        [
            BASE_URL,
            f"{BASE_URL}/accounts/login/",
            f"{BASE_URL}/accounts/signup/",
        ],
    )
    def test_page_accessibility(self, page: Page, axe: Axe, url: str):
        page.goto(url)
        results = axe.run(page)

        count = results.violations_count
        if count > 0:
            report = results.generate_report()
            warnings.warn(  # noqa: B028 no-explicit-stacklevel
                f"\n{count} accessibility violations at {url}:\n{report}",
                UserWarning,
            )
