from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import AuthUser


class AuthUserCreationForm(UserCreationForm):
    class Meta:
        model = AuthUser
        fields = ("username", "email")


class AuthUserChangeForm(UserChangeForm):
    class Meta:
        model = AuthUser
        fields = ("username", "email")
