from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from users.models import AuthUser, UserProfile
from users.signals import disable_authuser_postsave_signal


class AuthUserFactory(DjangoModelFactory):
    class Meta:
        model = AuthUser

    username = Faker("user_name")
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    password = Faker("password")

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override FactoryBoy's default create() to disable signals.

        Signals disabled because creating an AuthUser would create a UserProfile, which we
        wish to avoid and instead do explicitly via a subfactory in UserProfileFactory.
        """
        with disable_authuser_postsave_signal():
            return super()._create(model_class, *args, **kwargs)


class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile

    user = SubFactory(AuthUserFactory)
