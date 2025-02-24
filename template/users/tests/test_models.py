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
        self.assertIsNotNone(profile.updated_at)


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
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile), f"Profile for {self.user}")
