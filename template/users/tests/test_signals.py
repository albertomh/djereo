from django.db.models.signals import post_save
from django.test import SimpleTestCase

from users.models import AuthUser
from users.signals import disable_authuser_postsave_signal


class UserProfileTestCase(SimpleTestCase):
    def test_disable_authuser_postsave_signal(self):
        has_listeners_before = post_save.has_listeners(AuthUser)

        with disable_authuser_postsave_signal():
            has_listeners_in_context = post_save.has_listeners(AuthUser)
        has_listeners_after = post_save.has_listeners(AuthUser)

        self.assertTrue(has_listeners_before)
        self.assertFalse(has_listeners_in_context)
        self.assertTrue(has_listeners_after)
