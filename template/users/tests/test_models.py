import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import AuthUser, UserProfile


class AuthUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="spanza",
            email="escudero@quijano.es",
            password="equusasinus",
        )

    def test_timestamps_exist(self):
        profile = AuthUser.objects.get(username=self.user.username)
        assert profile.updated_at is not None

    def test_create_user_without_email_raises_error(self):
        with pytest.raises(ValueError, match="The 'email' field must be set"):
            get_user_model().objects.create_user(email=None, password="testpassword")

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            email="super@quijano.es", password="testpassword"
        )
        assert superuser.is_staff
        assert superuser.is_superuser


class UserProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="aquijano",
            email="alonso@quijano.es",
            password="rocinante",
        )

    def test_user_profile_created_when_auth_user_created(self):
        profile = UserProfile.objects.get(user=self.user)
        assert profile.user == self.user
        assert str(profile) == f"Profile for {self.user}"
