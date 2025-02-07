from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.forms import AuthUserChangeForm, AuthUserCreationForm
from accounts.models import AuthUser


@admin.register(AuthUser)
class AuthUserAdmin(UserAdmin):
    add_form = AuthUserCreationForm
    form = AuthUserChangeForm
    model = AuthUser
    list_display = ["email", "username"]
