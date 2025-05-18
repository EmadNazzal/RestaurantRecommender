import json
import os
import sys
from typing import Dict, List


import django
from django.core.management.base import BaseCommand

from restaurant_recommender.models import Restaurant  # type: ignore

# Add the path to your Django project directory
sys.path.append(
    "/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialize Django
django.setup()


class Command(BaseCommand):
    help = "Replace existing photos with new photos from JSON file"

    def handle(self, *args, **options):
        # Define the base and data directories
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(base_dir, "..", "..", "..")
        base_dir = os.path.abspath(base_dir)
        data_dir = os.path.join(base_dir, "data")
        restaurants_file = os.path.join(data_dir, "restaurants_new.json")

        # Check if the file exists
        if not os.path.exists(restaurants_file):
            self.stdout.write(self.style.ERROR(
                f"File {restaurants_file} does not exist"))
            return

        # Load restaurant data from the JSON file
        with open(restaurants_file) as jsonfile:
            data = json.load(jsonfile)

            # Create a dictionary mapping restaurant names to photo URLs
            photos_dict: Dict[str, List[str]] = {}
            for item in data:
                restaurant_name = item.get("Restaurant Name")
                photo_urls_str = item.get("Photos")
                if restaurant_name and photo_urls_str:
                    try:
                        photo_urls = json.loads(
                            photo_urls_str.replace("'", '"'))
                        if restaurant_name in photos_dict:
                            photos_dict[restaurant_name].extend(photo_urls)
                        else:
                            photos_dict[restaurant_name] = photo_urls
                    except json.JSONDecodeError:
                        self.stdout.write(self.style.WARNING(
                            f"Invalid JSON for photos: {photo_urls_str}"))

            # Update each restaurant with the new photo URLs
            for restaurant in Restaurant.objects.all():
                restaurant_name = restaurant.restaurant_name
                if restaurant_name in photos_dict:
                    new_photo_urls = photos_dict[restaurant_name]

                    # Clear existing photo URLs
                    restaurant.photo_url = json.dumps([])

                    # Add new URLs, ensuring no duplicates
                    updated_photos = list(set(new_photo_urls))
                    restaurant.photo_url = json.dumps(updated_photos)
                    restaurant.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"Updated photos for restaurant {restaurant.restaurant_name}"))

        self.stdout.write(self.style.SUCCESS(
            "Successfully updated restaurant photos"))
