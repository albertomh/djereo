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

    def test_create_user_without_email_raises_error(self):
        with self.assertRaisesRegex(ValueError, "The 'email' field must be set"):
            get_user_model().objects.create_user(email=None, password="testpassword")

    def test_create_superuser(self):
        superuser = get_user_model().objects.create_superuser(
            email="super@quijano.es", password="testpassword"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

    def test_create_user_creates_profile(self):
        user = get_user_model().objects.create_user(
            email="newuser@example.com", password="testpassword"
        )
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_profile_property_creates_profile_if_missing(self):
        """Tests the safety net behavior of the profile property."""
        UserProfile.objects.filter(user=self.user).delete()
        self.user.refresh_from_db()
        self.assertFalse(UserProfile.objects.filter(user=self.user).exists())

        profile = self.user.profile
        self.assertIsInstance(profile, UserProfile)
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())
        self.assertEqual(profile.user, self.user)


class UserProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="aquijano",
            email="alonso@quijano.es",
            password="rocinante",
        )

    def test_user_profile_created_by_default(self):
        self.assertTrue(UserProfile.objects.filter(user=self.user).exists())

        profile = self.user.profile
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile), f"Profile for {self.user}")
