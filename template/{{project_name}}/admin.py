from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group


class CustomAdminAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"


class CustomAdminSite(AdminSite):
    login_form = CustomAdminAuthenticationForm


admin.site = CustomAdminSite()

# re-register default models
admin.site.register(get_user_model(), UserAdmin)
admin.site.register(Group, GroupAdmin)
