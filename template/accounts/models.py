from django.contrib.auth.models import AbstractUser


class AuthUser(AbstractUser):
    pass

    def __str__(self):
        return self.email
