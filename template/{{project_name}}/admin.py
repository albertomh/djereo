from django.contrib.admin import AdminSite
from django.contrib.auth.forms import AuthenticationForm


class CustomAdminAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Email"


class CustomAdminSite(AdminSite):
    login_form = CustomAdminAuthenticationForm


admin_site = CustomAdminSite()
