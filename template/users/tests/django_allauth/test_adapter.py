from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from users.django_allauth.adapter import (
    AMBIGUOUS_EMAIL_CLASH_MESSAGE,
    CustomAccountAdapter,
)

User = get_user_model()


@override_settings(
    ACCOUNT_SITES_ENABLED=True,
    DEFAULT_FROM_EMAIL="noreply@example.com",
    SITE_URL="https://example.com",
)
class CustomAccountAdapterTests(TestCase):
    def setUp(self):
        self.adapter = CustomAccountAdapter()

    def test_clean_email_allows_new_email(self):
        email = "new@example.com"
        result = self.adapter.clean_email(email)
        self.assertEqual(result, email)
        self.assertEqual(len(mail.outbox), 0)

    def test_clean_email_existing_verified_email_sends_builtin_reminder(self):
        user = User.objects.create(username="alice", email="alice@example.com")
        EmailAddress.objects.create(user=user, email="alice@example.com", verified=True)

        with self.assertRaises(ValidationError) as ctx:
            self.adapter.clean_email("alice@example.com")

        self.assertEqual(ctx.exception.message, AMBIGUOUS_EMAIL_CLASH_MESSAGE)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("alice@example.com", mail.outbox[0].to)

    def test_error_message_replaced(self):
        self.assertEqual(
            self.adapter.error_messages["email_taken"],
            AMBIGUOUS_EMAIL_CLASH_MESSAGE,
        )
