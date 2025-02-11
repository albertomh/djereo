from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from users.models import AuthUser


class Command(BaseCommand):
    help = "Seed database with three users: admin, staff and regular (non-privileged)."

    @transaction.atomic
    def handle(self, *args, **options):
        if AuthUser.objects.exists():
            raise CommandError(
                "This command cannot be run when any users exist to guard "
                + "against accidental use on production."
            )

        self.stdout.write("Seeding database...")

        users_data = [
            {
                "username": "admin",
                "email": "admin@example.com",
                "password": "password",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "staff",
                "email": "staff@example.com",
                "password": "password",
                "is_staff": True,
            },
            {"username": "user", "email": "user@example.com", "password": "password"},
        ]

        for data in users_data:
            create_user(data)

        self.stdout.write(self.style.SUCCESS("Done."))


def create_user(data):
    AuthUser.objects.create_user(**data)
