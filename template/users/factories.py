from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from users.models import AuthUser, UserProfile


class AuthUserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser

    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = Faker("password")


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(AuthUserFactory)
