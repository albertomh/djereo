from typing import ClassVar

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
    list_display = ("email", "date_joined", "last_login")
    readonly_fields = ("id",)
    search_fields = ("email",)

    add_fieldsets = ((None, {"fields": ("email", "password1", "password2")}),)
    fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("id", "email", "password"),
            },
        ),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    inlines: ClassVar[list] = [UserProfileInline]

    def get_inline_instances(self, request, obj=None):
        """Avoid a blank UserProfileInline in the Django admin AuthUser creation form."""
        return (
            obj and super(UserAdmin, self).get_inline_instances(request, obj)
        ) or []  # pragma: no cover


admin.site.register(UserProfile)
