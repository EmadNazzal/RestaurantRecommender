"""This script loads restaurants and aspects data from JSON files into the database."""

import json
import os
import sys
from pathlib import Path

import django
from django.core.management.base import BaseCommand

from restaurant_recommender.models import Aspect, Restaurant  # type: ignore

sys.path.append("/Users/hanzheng/Documents/GitHub/SummerTest/apps/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.setting")
django.setup()


class Command(BaseCommand):
    """A Django management command to load restaurants and aspects data from JSON files."""

    help = "Load restaurants and aspects from JSON files"

    def handle(self, *args, **options):  # noqa: ARG002
        """Handle the command execution."""
        base_dir = Path(__file__).resolve().parent.parent.parent.parent.parent

        data_dir = base_dir / "data"
        restaurants_file = data_dir / "restaurants.json"
        aspects_file = data_dir / "restaurant_aspects.json"

        if not restaurants_file.exists():
            self.stdout.write(self.style.ERROR(f"File {restaurants_file} does not exist."))
            return

        if not aspects_file.exists():
            self.stdout.write(self.style.ERROR(f"File {aspects_file} does not exist."))
            return

        # Load restaurants data
        with restaurants_file.open() as file:
            restaurants_data = json.load(file)
            for item in restaurants_data:
                Restaurant.objects.get_or_create(
                    restaurant_name=item["Restaurant Name"],
                    defaults={
                        "primary_cuisine": item.get("Primary Cuisine", ""),
                        "overall_rating": item.get("Overall Rating", None),
                        "neighborhood": item.get("Neighborhood", ""),
                        "latitude": item.get("Latitude", None),
                        "longitude": item.get("Longitude", None),
                    },
                )

        # Load aspects data
        with aspects_file.open() as file:
            aspects_data = json.load(file)
            for item in aspects_data:
                try:
                    restaurant = Restaurant.objects.get(restaurant_name=item["Restaurant Name"])

                    for aspect in item.get("5 Most Common Positive Aspects", []):
                        Aspect.objects.create(restaurant=restaurant, aspect=aspect, rating_type="positive")

                    for aspect in item.get("5 Most Common Negative Aspects", []):
                        Aspect.objects.create(restaurant=restaurant, aspect=aspect, rating_type="negative")
                except Restaurant.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f"Restaurant {item['Restaurant Name']} does not exist in the database.")
                    )

        self.stdout.write(self.style.SUCCESS("Successfully loaded restaurants and aspects."))
