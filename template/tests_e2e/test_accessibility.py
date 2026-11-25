import warnings

import pytest
from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

from tests_e2e.conftest import BASE_URL


def _format_target(target):
    if isinstance(target, list):
        return " >> ".join(_format_target(part) for part in target)
    return str(target)


def _format_report(violations):
    lines = [f"Found {len(violations)} accessibility violations:"]
    for violation in violations:
        lines.append(
            f"{violation['id']} ({violation['impact']}) : "
            f"{len(violation['nodes'])} element(s)"
        )
        for number, node in enumerate(violation["nodes"], start=1):
            targets = ", ".join(_format_target(target) for target in node["target"])
            snippet = (node.get("html") or "").replace("\n", "")
            lines.extend(
                [
                    f"  {number}) Target: {targets}",
                    f"     Snippet: {snippet}",
                    "     Messages:",
                ]
            )
            checks = node.get("all", []) + node.get("any", []) + node.get("none", [])
            for check in checks:
                lines.append(f"       * {check['message']}")
    return "\n".join(lines)


@pytest.mark.axe
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
            report = _format_report(results.response["violations"])
            warnings.warn(  # noqa: B028 no-explicit-stacklevel
                f"\n{count} accessibility violations at {url}:\n{report}",
                UserWarning,
            )
