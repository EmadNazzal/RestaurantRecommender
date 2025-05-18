import json
import os
import sys
from pathlib import Path

import django
from django.core.management.base import BaseCommand

from restaurant_recommender.models import Restaurant  # type: ignore

TEN = 10

# Add the path to your Django project directory.
# Change this to the path of the backend directory in your project.
sys.path.append(
    "/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
# Change this to the settings file of your Django project.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialise Django.
django.setup()


class Command(BaseCommand):
    """A Django management command to load restaurant data from a JSON file."""

    help = "Load restaurants from JSON file"

    def handle(self, *args, **options):  # noqa: ARG002
        """Handle the command execution."""
        base_dir = Path(__file__).resolve().parent.parent.parent.parent

        data_dir = base_dir / "data"
        restaurants_file = data_dir / "restaurants_new.json"

        if not restaurants_file.exists():
            self.stdout.write(self.style.ERROR(
                f"File {restaurants_file} does not exist"))
            return

        # Clear existing data.
        Restaurant.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            "Cleared existing restaurant data"))

        # Load restaurants data.
        try:
            with restaurants_file.open(encoding='utf-8') as jsonfile:
                data = json.load(jsonfile)
        except json.JSONDecodeError as e:
            self.stdout.write(self.style.ERROR(
                f"Error decoding JSON: {e}"))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f"Error reading file {restaurants_file}: {e}"))
            return

        missing_location_id_restaurants = []

        for index, item in enumerate(data):
            # Debug: print the raw JSON entry.
            if index < TEN:  # Only print the first 10 entries for debugging.
                self.stdout.write(self.style.WARNING(
                    f"Entry {index + 1}: {json.dumps(item, indent=4)}"))

            # Ensure location_id is not null or missing and convert to integer.
            location_id_str = item.get("location_id")
            try:
                location_id = int(location_id_str)
            except (TypeError, ValueError):
                missing_location_id_restaurants.append(item)
                continue

            # Map JSON keys to model field names
            mapped_item = {
                "restaurant_name": item.get("Restaurant Name", "Unknown"),
                "primary_cuisine": item.get("Primary Cuisine", ""),
                "overall_rating": float(item["Overall Rating"]) if item.get("Overall Rating") else None,
                "latitude": float(item["Latitude"]) if item.get("Latitude") else None,
                "longitude": float(item["Longitude"]) if item.get("Longitude") else None,
                "location_id": location_id,
                "telephone": item.get("Telephone", ""),
                "price": item.get("Price", ""),
                "food_rating": float(item["Food Rating"]) if item.get("Food Rating") else None,
                "service_rating": float(item["Service Rating"]) if item.get("Service Rating") else None,
                "value_rating": float(item["Value Rating"]) if item.get("Value Rating") else None,
                "noise_level": item.get("Noise Level", ""),
                "zone": item.get("zone", ""),
                "photo_url": item.get("Photos", ""),
                "address": item.get("Address", ""),
                "website": item.get("Website", ""),
                "ambience_rating": item.get("Ambience Rating", ""),
                "dress_code": item.get("Dress Code", ""),
            }

            # Debug: Print the mapped item.
            if index < TEN:  # Only print the first 10 entries for debugging.
                self.stdout.write(self.style.WARNING(
                    f"Mapped Item {index + 1}: {mapped_item}"))

            # Create new restaurant entry.
            try:
                Restaurant.objects.create(**mapped_item)
            except ValueError as e:
                self.stdout.write(self.style.ERROR(
                    f"Error creating restaurant entry: {e}."))
                continue

        self.stdout.write(self.style.SUCCESS(
            "Successfully loaded restaurants data."))

        # Print restaurants missing location_id.
        if missing_location_id_restaurants:
            self.stdout.write(self.style.ERROR(
                "Restaurants missing location_id:"))
            for restaurant in missing_location_id_restaurants:
                self.stdout.write(
                    self.style.ERROR(
                        f"{restaurant.get('Restaurant Name', 'Unknown')} (Lat: {restaurant.get('Latitude', 'N/A')}, Long: {restaurant.get('Longitude', 'N/A')})"
                    )
                )
