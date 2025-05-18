"""Have users like some of the restaurants that match their preferences."""

import random

from django.core.management.base import BaseCommand

from restaurant_recommender.models import Restaurant  # type: ignore
from user_management.models import User, UserLikedRestaurant, UserPreference  # type: ignore


class Command(BaseCommand):
    """A Django management command to have users like some of the restaurants that match their preferences."""

    help = "Have users like some of the restaurants that match their preferences"

    def handle(self, *args, **kwargs):  # noqa: ARG002
        """Handle the command execution."""
        users = User.objects.all()

        for user in users:
            user_preferences = UserPreference.objects.filter(user=user)
            liked_restaurants = set()

            for user_preference in user_preferences:
                matching_restaurants = Restaurant.objects.filter(
                    primary_cuisine=user_preference.preference.description)

                if matching_restaurants.exists():
                    num_to_like = random.randint(1, matching_restaurants.count())  # noqa: S311
                    restaurants_to_like = random.sample(
                        list(matching_restaurants), num_to_like)

                    for restaurant in restaurants_to_like:
                        if restaurant not in liked_restaurants:
                            UserLikedRestaurant.objects.create(
                                user=user, restaurant=restaurant)
                            liked_restaurants.add(restaurant)

            self.stdout.write(self.style.SUCCESS(
                f"User {user.email} liked {len(liked_restaurants)} restaurants"))

        self.stdout.write(self.style.SUCCESS(
            "Successfully liked restaurants based on user preferences"))
