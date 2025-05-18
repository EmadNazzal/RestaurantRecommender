"""A Django management command to create fake preferences for users."""

import csv
import os
import random
import sys
from pathlib import Path

import django
from django.core.management.base import BaseCommand
from faker import Faker

from restaurant_recommender.models import Aspect, Restaurant  # type: ignore
from user_management.models import User, Preference  # type: ignore

# Add the path to your Django project directory.
sys.path.append(
    "/Users/riink/OneDrive/Summer_project/SummerProject/GitHub/apps/backend/")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialize Django
django.setup()


class Command(BaseCommand):
    """A Django management command to create fake preferences for users and save to CSV."""

    help = "Create multiple preferences for each user and save to CSV"

    def handle(self, *args, **options):  # noqa: ARG002
        """Handle the command execution."""

        # Fetch users and restaurants
        users = User.objects.filter(
            email__contains="@example.com").order_by("id")
        restaurants = Restaurant.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR(
                "No users found with @example.com email domain."))
            return

        if not restaurants.exists():
            self.stdout.write(self.style.ERROR("No restaurants found."))
            return

        # Define how many preferences each user should have
        number_of_preferences_per_user = 5
        preferences_list = []

        num_users = users.count()
        self.stdout.write(self.style.SUCCESS(f"Found {num_users} users."))

        total_preferences_created = 0

        # Process each user
        for user in users:
            self.stdout.write(self.style.SUCCESS(
                f"Processing user {user.email} with ID {user.id}"))

            # Sample unique restaurants for the user
            if restaurants.count() < number_of_preferences_per_user:
                self.stdout.write(
                    self.style.ERROR(
                        f"Not enough restaurants to give {number_of_preferences_per_user} preferences to user {user.id}."
                    )
                )
                continue

            unique_restaurants = random.sample(
                list(restaurants), number_of_preferences_per_user)

            if not unique_restaurants:
                self.stdout.write(self.style.WARNING(
                    f"No restaurants available for user {user.id}."))
                continue

            for restaurant in unique_restaurants:
                positive_aspects = Aspect.objects.filter(
                    restaurant=restaurant, rating_type="positive")

                # Create bookmark for the user
                bookmark = Preference.objects.create(
                    user=user,
                    primary_cuisine=restaurant.primary_cuisine,
                    price=restaurant.price,
                    dress_code=restaurant.dress_code,
                )
                bookmark.restaurant_name.add(restaurant)

                # Collect aspects data
                aspects_data = [
                    f"{aspect.aspect} (Count: {aspect.count}, Rating Type: {aspect.rating_type})"
                    for aspect in positive_aspects
                ]
                # Use set for updating related fields
                bookmark.positive_aspects.set(positive_aspects)

                # Append preference to the list
                preferences_list.append([
                    user.id,
                    restaurant.restaurant_name,
                    restaurant.primary_cuisine,
                    restaurant.price,
                    restaurant.dress_code,
                    "|".join(aspects_data),
                ])
                total_preferences_created += 1

            # Debug output for verification
            self.stdout.write(self.style.SUCCESS(
                f"User {user.id} assigned {len(unique_restaurants)} unique restaurants."))

        # Write preferences to CSV
        preferences_csv = Path.cwd() / "preferences_05.csv"
        with preferences_csv.open("w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "user_id",
                "restaurant_name",
                "primary_cuisine",
                "price",
                "dress_code",
                "positive_aspects",
            ])
            writer.writerows(preferences_list)

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {total_preferences_created} preferences and saved to {preferences_csv}"
            )
        )
