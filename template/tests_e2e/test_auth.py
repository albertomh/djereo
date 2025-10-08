import random
import string

import requests
from playwright.sync_api import expect

from tests_e2e import MailPitMessage
from tests_e2e.conftest import BASE_URL, MAILPIT_API_BASE_URL


class AuthTest:
    @classmethod
    def setup_class(cls):
        cls.user_email = "user@example.com"
        cls.user_password = "password"
        cls.login_url = f"{BASE_URL}/accounts/login/"
        cls.signup_url = f"{BASE_URL}/accounts/signup/"


class TestSignUp(AuthTest):
    def test_sign_up_navigation(self, page):
        page.goto(BASE_URL)
        page.get_by_text("Sign up").click()
        expect(page).to_have_url(self.signup_url)

    def test_sign_up(self, page):
        page.goto(self.signup_url)

        email = f"{''.join(random.choices(string.ascii_lowercase, k=6))}@example.com"
        page.fill("#id_email", email)
        password = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
        page.fill("#id_password1", password)
        page.click("button[type=submit]")

        expect(page).to_have_url(f"{BASE_URL}/")
        expect(page.get_by_text(email), "should be logged in").to_be_visible()
        mp_res = requests.get(f"{MAILPIT_API_BASE_URL}/api/v1/messages").json()
        msg: MailPitMessage = mp_res["messages"][0]
        assert msg["To"][0]["Address"] == email
        snippet = (
            f"Hello from example.com! You're receiving this email because user "
            f"{email.split('@')[0]} has given your email address to register"
        )
        assert snippet in msg["Snippet"]

    def test_attempt_sign_up_with_existing_email(self, page):
        page.goto(self.signup_url)

        page.fill("#id_email", self.user_email)
        page.fill("#id_password1", self.user_password)
        page.click("button[type=submit]")

        expect(
            page.get_by_text("Check your email to confirm your account."),
            "should show ambiguous message",
        ).to_be_visible()
        mp_res = requests.get(f"{MAILPIT_API_BASE_URL}/api/v1/messages").json()
        msg: MailPitMessage = mp_res["messages"][0]
        snippet = (
            f"You are receiving this email because you or someone else tried to "
            f"signup for an account using email address: {self.user_email}"
        )
        assert snippet in msg["Snippet"]


class TestLogInPage(AuthTest):
    def test_log_in_as_a_regular_user(self, page):
        page.goto(self.login_url)
        page.fill("#id_login", self.user_email)
        page.fill("#id_password", self.user_password)
        page.click("button[type=submit]")

        expect(page).to_have_url(f"{BASE_URL}/")

        nav_text = page.locator("//header/nav/ul").inner_text()
        assert nav_text.startswith(self.user_email)

    def test_log_in_requires_email_address(self, page):
        page.goto(self.login_url)
        page.fill("#id_login", "not_an_email")
        page.fill("#id_password", self.user_password)

        page.click("button[type=submit]")

        validation_msg = page.eval_on_selector("#id_login", "el => el.validationMessage")
        assert "@" in validation_msg

    def test_forgot_password_link_on_log_in_page(self, page):
        page.goto(self.login_url)

        page.get_by_text("Forgot your password?").click()

        expect(page).to_have_url(f"{BASE_URL}/accounts/password/reset/")


class TestLogOut(AuthTest):
    def test_log_out(self, page):
        page.goto(self.login_url)
        page.fill("#id_login", self.user_email)
        page.fill("#id_password", self.user_password)
        page.click("button[type=submit]")
        page.click(f"text={self.user_email}")
        page.click("text=Sign out")

        expect(page).to_have_url(f"{BASE_URL}/accounts/logout/")
        page.click("button[type=submit]")

        expect(page).to_have_url(f"{BASE_URL}/")
