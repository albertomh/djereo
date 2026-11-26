from uuid import uuid4

import requests
from playwright.sync_api import Page, expect

from tests_e2e import MailPitMessage
from tests_e2e.conftest import BASE_URL, MAILPIT_API_BASE_URL, log_in


def _account_in_main_navigation(page, email):
    return page.locator("header nav > ul").get_by_text(email, exact=False)


USER_EMAIL = "user@example.com"
USER_PASSWORD = "password"
LOGIN_URL = f"{BASE_URL}/accounts/login/"
SIGNUP_URL = f"{BASE_URL}/accounts/signup/"


class TestSignUp:
    def test_sign_up_navigation(self, page: Page):
        page.goto(BASE_URL)
        page.get_by_text("Sign up").click()
        expect(page).to_have_url(SIGNUP_URL)

    def test_sign_up(self, page: Page):
        page.goto(SIGNUP_URL)

        email = f"{uuid4().hex}@example.com"
        page.fill("#id_email", email)
        password = uuid4().hex
        page.fill("#id_password1", password)
        page.click("button[type=submit]")

        expect(page).to_have_url(f"{BASE_URL}/")
        expect(
            _account_in_main_navigation(page, email), "should be logged in"
        ).to_be_visible()
        mp_res = requests.get(f"{MAILPIT_API_BASE_URL}/api/v1/messages").json()
        msg: MailPitMessage = mp_res["messages"][0]
        assert msg["To"][0]["Address"] == email
        snippet = (
            f"Hello from example.com! You're receiving this email because user "
            f"{email.split('@', maxsplit=1)[0]} has given your email address to register"
        )
        assert snippet in msg["Snippet"]

    def test_attempt_sign_up_with_existing_email(self, page: Page):
        page.goto(SIGNUP_URL)

        page.fill("#id_email", USER_EMAIL)
        page.fill("#id_password1", USER_PASSWORD)
        page.click("button[type=submit]")

        expect(
            page.get_by_text("Check your email to confirm your account."),
            "should show ambiguous message",
        ).to_be_visible()
        mp_res = requests.get(f"{MAILPIT_API_BASE_URL}/api/v1/messages").json()
        msg: MailPitMessage = mp_res["messages"][0]
        snippet = (
            f"You are receiving this email because you or someone else tried to "
            f"signup for an account using email address: {USER_EMAIL}"
        )
        assert snippet in msg["Snippet"]


class TestLogInPage:
    def test_log_in_as_a_regular_user(self, page: Page):
        log_in(page, USER_EMAIL, USER_PASSWORD)
        expect(page).to_have_url(f"{BASE_URL}/")
        expect(_account_in_main_navigation(page, USER_EMAIL)).to_be_visible()

    def test_log_in_requires_email_address(self, page: Page):
        page.goto(LOGIN_URL)
        page.fill("#id_login", "not_an_email")
        page.fill("#id_password", USER_PASSWORD)

        page.click("button[type=submit]")

        validation_msg = page.eval_on_selector("#id_login", "el => el.validationMessage")
        assert "@" in validation_msg

    def test_forgot_password_link_on_log_in_page(self, page: Page):
        page.goto(LOGIN_URL)

        page.get_by_text("Forgot your password?").click()

        expect(page).to_have_url(f"{BASE_URL}/accounts/password/reset/")


class TestLogOut:
    def test_log_out(self, page: Page):
        log_in(page, USER_EMAIL, USER_PASSWORD)
        _account_in_main_navigation(page, USER_EMAIL).click()
        page.click("text=Sign out")

        expect(page).to_have_url(f"{BASE_URL}/accounts/logout/")
        page.click("button[type=submit]")

        expect(page).to_have_url(f"{BASE_URL}/")
