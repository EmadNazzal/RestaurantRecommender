import random
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from faker import Faker

from user_management.models import Preference, Profile, User, UserPreference  # type: ignore


class Command(BaseCommand):
    """A Django management command to generate 200 users with random preferences."""

    help = "Generate 200 users with random preferences"

    def handle(self, *args, **kwargs):  # noqa: ARG002
        """Handle the command execution."""
        fake = Faker()

        # Clear existing users and related data
        User.objects.all().delete()
        # Clear out existing UserPreference entries
        UserPreference.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            "Cleared existing users and user preferences"))

        # Fetch preferences
        preferences = Preference.objects.all()
        total_preferences = preferences.count()
        self.stdout.write(self.style.SUCCESS(
            f"Found {total_preferences} preferences"))

        # Generate 200 users
        user_count = 200
        created_users = 0

        while created_users < user_count:
            first_name = fake.first_name()
            surname = fake.last_name()
            email = fake.email()
            password = fake.password()

            # Create user
            user = User.objects.create_user(
                email=email, first_name=first_name, surname=surname, password=password)  # type: ignore

            # Create profile with unique slug
            while True:
                slug = fake.slug()
                try:
                    Profile.objects.create(
                        user=user, first_name=first_name, surname=surname, slug=slug)
                    break
                except IntegrityError:
                    # If slug is not unique, generate a new one and retry
                    continue

            # Assign random preferences
            if total_preferences > 0:  # Check if preferences are available
                # Limit to 10 or available preferences
                num_preferences = random.randint(1, min(10, total_preferences))
                random_preferences = random.sample(
                    list(preferences), num_preferences)

                user_preferences = [
                    UserPreference(user=user, preference=preference)
                    for preference in random_preferences
                ]

                UserPreference.objects.bulk_create(user_preferences)

            self.stdout.write(self.style.SUCCESS(
                f"Created user: {user.email} with {num_preferences} preferences"))

            created_users += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully created {created_users} users with random preferences"))
