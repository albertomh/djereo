from django.core.exceptions import PermissionDenied


def permission_denied_view(request):
    raise PermissionDenied
