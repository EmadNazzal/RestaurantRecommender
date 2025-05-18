import json
import os
import sys
from pathlib import Path
from typing import NoReturn

import django
from django.core.management.base import BaseCommand

from restaurant_recommender.models import Aspect, Restaurant  # type: ignore

# Add the path to your Django project directory.
sys.path.append(
    "/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialise Django.
django.setup()


class Command(BaseCommand):
    """A Django management command to load aspects data from a JSON file."""

    help = "Load aspects from JSON file"

    def handle(self, *args, **options):  # noqa: ARG002, PLR0912, PLR0915, C901
        """Handle the command execution."""
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        data_dir = base_dir / "data"
        aspects_file = data_dir / "restaurants_new.json"

        if not aspects_file.exists():
            self.stdout.write(self.style.ERROR(
                f"File {aspects_file} does not exist"))
            return

        Aspect.objects.all().delete()

        missing_restaurants = []
        successful_creations = 0
        failed_creations = 0

        def raise_key_error(msg: str) -> NoReturn:
            raise KeyError(msg)

        def raise_value_error(msg: str) -> NoReturn:
            raise ValueError(msg)

        try:  # noqa: PLR1702
            with aspects_file.open(encoding="utf-8") as file:
                aspects_data = json.load(file)
                for item in aspects_data:
                    try:
                        restaurant_name = item.get("Restaurant Name")
                        if not restaurant_name:
                            raise_key_error("Restaurant Name")

                        restaurant = Restaurant.objects.filter(
                            restaurant_name=restaurant_name).first()

                        if not restaurant:
                            self.stdout.write(
                                self.style.ERROR(
                                    f"Restaurant {restaurant_name} does not exist in the database.")
                            )
                            missing_restaurants.append(restaurant_name)
                            continue

                        positive_aspects = item.get(
                            "5 Most Common Positive Aspects") or []
                        if not isinstance(positive_aspects, list):
                            raise_value_error(
                                f"Invalid format for positive aspects in {restaurant_name}.")

                        for aspect, count in positive_aspects:
                            try:
                                Aspect.objects.create(
                                    restaurant=restaurant, aspect=aspect, rating_type="positive", count=count
                                )
                                successful_creations += 1
                            except ValueError as e:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f"Failed to create positive aspect for {restaurant.restaurant_name}: {e}."
                                    )
                                )
                                failed_creations += 1

                        negative_aspects = item.get(
                            "5 Most Common Negative Aspects") or []
                        if not isinstance(negative_aspects, list):
                            raise_value_error(
                                f"Invalid format for negative aspects in {restaurant_name}.")

                        for aspect, count in negative_aspects:
                            try:
                                Aspect.objects.create(
                                    restaurant=restaurant, aspect=aspect, rating_type="negative", count=count
                                )
                                successful_creations += 1
                            except ValueError as e:
                                self.stdout.write(
                                    self.style.ERROR(
                                        f"Failed to create negative aspect for {restaurant.restaurant_name}: {e}"
                                    )
                                )
                                failed_creations += 1

                    except KeyError as e:
                        self.stdout.write(self.style.ERROR(
                            f"Missing key in JSON data: {e}"))
                    except ValueError as e:
                        self.stdout.write(self.style.ERROR(
                            f"Invalid value in JSON data: {e}"))
                    except (TypeError, AttributeError) as e:
                        self.stdout.write(
                            self.style.ERROR(
                                f"Unexpected error processing item {item.get('Restaurant Name', 'Unknown')}: {e}."
                            )
                        )
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(
                f"Error decoding JSON file: {e}."))
        except ValueError as e:
            self.stdout.write(self.style.ERROR(
                f"Unexpected error reading JSON file: {e}."))

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully loaded {successful_creations} aspects with {failed_creations} failures.")
        )
        self.stdout.write(self.style.WARNING(
            f"Missing restaurants: {missing_restaurants}."))
