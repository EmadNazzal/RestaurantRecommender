"""This script loads the XGBoost model from the pickle file and saves it to the database."""

import os
import sys
from pathlib import Path

import django
from django.core.management.base import BaseCommand

from restaurant_recommender.models import PredictionModel, Restaurant  # type: ignore

# Add the path to your Django project directory.
# Change this to the path of the backend directory in your project.
sys.path.append("/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialise Django.
django.setup()


class Command(BaseCommand):
    """A Django management command to load the XGBoost model from the pickle file and save it to the database."""

    help = "Save the XGBoost model to the database"

    def handle(self, *args, **options):  # noqa: ARG002
        """Handle the command execution."""
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        data_dir = base_dir / "data"
        pickle_file = data_dir / "XGBoost.pkl"

        if not pickle_file.exists():
            self.stdout.write(self.style.ERROR(f"File {pickle_file} does not exist."))
            return

        with pickle_file.open("rb") as file:
            pickle_data = file.read()

        try:
            restaurant = Restaurant.objects.first()
        except Restaurant.DoesNotExist:
            self.stdout.write(self.style.ERROR("No restaurants found in the database."))
            return

        PredictionModel.objects.create(
            model_name="XGBoost",
            pickle_file=pickle_data,
            restaurant=restaurant,
        )

        self.stdout.write(self.style.SUCCESS("XGBoost model saved to the database successfully."))
