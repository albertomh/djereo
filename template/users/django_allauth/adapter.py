from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

AMBIGUOUS_EMAIL_CLASH_MESSAGE = _("Check your email to confirm your account.")


class CustomAccountAdapter(DefaultAccountAdapter):
    @staticmethod
    def _custom_error_messages() -> dict[str, str]:
        messages = DefaultAccountAdapter.error_messages
        messages["email_taken"] = AMBIGUOUS_EMAIL_CLASH_MESSAGE
        return messages

    error_messages = _custom_error_messages()

    def clean_email(self, email):
        """Intercept attempts to sign up with an existing email and send a reminder."""
        email = super().clean_email(email)
        existing = EmailAddress.objects.filter(email__iexact=email, verified=True).first()
        if existing:
            self.send_account_already_exists_mail(email)
            # Raise a ValidationError to stop normal signup, but use generic message
            # (default is "A user is already registered with this email address.")
            # <https://github.com/pennersr/django-allauth/blob/main/allauth/account/adapter.py#L67>

            raise ValidationError(AMBIGUOUS_EMAIL_CLASH_MESSAGE, code="email_taken")
        return email
