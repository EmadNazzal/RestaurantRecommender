"""Create a superuser if it does not exist."""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
User = get_user_model()


class Command(BaseCommand):
    """Create a superuser if it does not exist."""

    help = "Create a superuser if it does not exist"

    def handle(self, *args, **options):  # noqa: ARG002
        """Create a superuser if it does not exist."""

        def raise_missing_env_var_error():
            """Raise an error if one or more required environment variables are missing."""
            msg = "One or more required environment variables are missing"
            raise ValueError(msg)

        if not User.objects.filter(is_superuser=True).exists():
            try:
                email = os.getenv("DJANGO_SUPERUSER_EMAIL")
                password = os.getenv("DJANGO_SUPERUSER_PASSWORD")
                first_name = os.getenv("DJANGO_SUPERUSER_FIRST_NAME")
                surname = os.getenv("DJANGO_SUPERUSER_SURNAME")

                # Debug: Print environment variable values
                self.stdout.write(f"Email: {email}")
                self.stdout.write(f"First Name: {first_name}")
                self.stdout.write(f"Surname: {surname}")

                if not all([email, password, first_name, surname]):
                    raise_missing_env_var_error()

                User.objects.create_superuser(
                    email=email, password=password, first_name=first_name, surname=surname)  # type: ignore

                self.stdout.write(self.style.SUCCESS(
                    "Successfully created new superuser"))
            except ValueError as e:
                self.stdout.write(self.style.ERROR(
                    f"Error creating superuser: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))
