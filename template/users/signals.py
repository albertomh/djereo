from contextlib import contextmanager

from django.db.models.signals import post_save

from users.models import AuthUser, create_or_update_user_profile


@contextmanager
def disable_authuser_postsave_signal():
    """Temporarily disable the `post_save` signal for `AuthUser`.

    Intended to be used alongside Factory Boy model factories."""

    post_save.disconnect(create_or_update_user_profile, sender=AuthUser)
    try:
        yield
    finally:
        post_save.connect(create_or_update_user_profile, sender=AuthUser)
