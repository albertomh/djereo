from django.contrib.auth import get_user_model
from django.test import TestCase

from users.models import UserProfile


class UserProfileTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="aquijano",
            email="alonso@quijano.es",
            password="rocinante",
        )

    def test_user_profile_creation(self):
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.user, self.user)
        self.assertEqual(str(profile), f"Profile for {self.user}")
