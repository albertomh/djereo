from django.test import TestCase

from users.factories import AuthUserFactory, UserProfileFactory
from users.models import AuthUser, UserProfile


class AuthUserFactoryTest(TestCase):
    def test_authuser_factory_creates_user(self):
        user = AuthUserFactory()

        assert isinstance(user, AuthUser)
        assert AuthUser.objects.filter(id=user.id).exists()

    def test_authuser_factory_does_not_trigger_post_save_signal(self):
        user = AuthUserFactory()

        assert not UserProfile.objects.filter(user=user).exists()


class UserProfileFactoryTest(TestCase):
    def test_userprofile_factory_creates_profile(self):
        profile = UserProfileFactory()

        assert isinstance(profile, UserProfile)
        assert UserProfile.objects.filter(id=profile.id).exists()

    def test_userprofile_factory_does_not_duplicate_profiles(self):
        profile = UserProfileFactory()

        assert UserProfile.objects.filter(user=profile.user).count() == 1
