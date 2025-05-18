"""Create a CSV file with user IDs and their details."""

import csv
import os
import sys
from pathlib import Path

import django
from django.core.management.base import BaseCommand

from user_management.models import User  # type: ignore

# Add the path to your Django project directory.
# Change this to the path of the backend directory in your project.
sys.path.append("/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialise Django.
django.setup()


class Command(BaseCommand):
    """A Django management command to create a CSV file with user IDs and their details (email, first name, surname)."""

    help = "Generate a CSV file with user IDs and their details"

    def handle(self, *args, **kwargs):  # noqa: ARG002
        """Handle the command execution."""
        # Query all users
        users = User.objects.all()

        # Define the path to the CSV file
        csv_file_path = Path.cwd() / "users.csv"

        # Open the CSV file for writing
        with csv_file_path.open("w", newline="", encoding="utf-8") as csvfile:
            # Create a CSV writer object
            csv_writer = csv.writer(csvfile)

            # Write the header row
            csv_writer.writerow(["user_id", "email", "first_name", "surname"])

            # Write user details to the CSV file
            for user in users:
                # TODO: cannot access member 'id' for type 'User'
                csv_writer.writerow([user.id, user.email, user.first_name, user.surname])

        self.stdout.write(self.style.SUCCESS(f"Successfully created CSV file at {csv_file_path}"))
