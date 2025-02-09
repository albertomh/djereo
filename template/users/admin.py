from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.forms import AuthUserChangeForm, AuthUserCreationForm
from users.models import AuthUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    show_change_link = True
    verbose_name_plural = "User Profile"


@admin.register(AuthUser)
class AuthUserAdmin(UserAdmin):
    add_form = AuthUserCreationForm
    form = AuthUserChangeForm
    model = AuthUser
    list_display = ["email", "username"]
    inlines = [UserProfileInline]


admin.site.register(UserProfile)
