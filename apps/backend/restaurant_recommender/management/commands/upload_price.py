import json
import os
import sys

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
    help = "Replace existing prices with new prices from JSON file"

    def handle(self, *args, **options):
        # Define the base and data directories
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(base_dir, "..", "..", "..")
        base_dir = os.path.abspath(base_dir)
        data_dir = os.path.join(base_dir, "data")
        restaurants_file = os.path.join(data_dir, "Restaurants_JUL17.json")

        # Check if the file exists
        if not os.path.exists(restaurants_file):
            self.stdout.write(self.style.ERROR(
                f"File {restaurants_file} does not exist"))
            return

        # Load restaurant data from the JSON file
        with open(restaurants_file) as jsonfile:
            data = json.load(jsonfile)

            # Create a dictionary mapping restaurant names to prices
            prices_dict = {}
            for item in data:
                restaurant_name = item.get("Restaurant Name")
                price = item.get("Price")
                if restaurant_name and price:
                    prices_dict[restaurant_name] = price

            # Update each restaurant with the new prices
            for restaurant in Restaurant.objects.all():
                restaurant_name = restaurant.restaurant_name
                if restaurant_name in prices_dict:
                    new_price = prices_dict[restaurant_name]

                    # Update the price
                    restaurant.price = new_price
                    restaurant.save()
                    self.stdout.write(self.style.SUCCESS(
                        f"Updated price for restaurant {restaurant.restaurant_name}"))

        self.stdout.write(self.style.SUCCESS(
            "Successfully updated restaurant prices"))
