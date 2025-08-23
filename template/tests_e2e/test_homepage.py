from tests_e2e.conftest import BASE_URL


def test_home_title(page):
    page.goto(BASE_URL)
    assert "Home" in page.title()
