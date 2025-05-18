"""Test the API endpoint for recommending restaurants based on user preferences.

This script creates a test user, assigns preferences to the user, and creates a test request to call
the API endpoint for recommending restaurants based on the user's preferences. The response is then
written to a JSON file for inspection.
"""

import json
import uuid
from pathlib import Path

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.test import RequestFactory
from rest_framework.response import Response  # type: ignore
from rest_framework.test import force_authenticate  # type: ignore

from user_management.models import Preference, UserPreference  # type: ignore
from user_management.views import recommend_restaurants


class Command(BaseCommand):
    """A Django management command to test the recommend_restaurants function."""

    help = "Test the recommend_restaurants function"

    def handle(self, *args, **kwargs):  # noqa: ARG002
        """Handle the command execution."""
        # Create a test user with a unique email
        User = get_user_model()  # noqa: N806
        # Unique email to avoid conflicts
        email = f"testuser-{uuid.uuid4()}@example.com"
        test_user = User.objects.create_user(  # type: ignore
            email=email,
            password="password",  # noqa: S106
            first_name="Test",
            surname="User",
        )  # type: ignore

        # Create preferences for the test user
        # Select the first 3 preferences
        preferences = Preference.objects.all()[:3]
        for preference in preferences:
            UserPreference.objects.create(
                user=test_user, preference=preference)

        # Create a test request
        factory = RequestFactory()
        request = factory.get("/api/api/restaurants/recommend/")
        force_authenticate(request, user=test_user)

        # Call the recommend_restaurants function
        response = recommend_restaurants(request)

        # Add print statements to debug the response rendering issue
        print("Response type:", type(response))
        response_content = ""
        if isinstance(response, TemplateResponse):
            print("Rendering response...")
            response = response.render()
            print("Response rendered.")
            response_content = response.content.decode()
        elif isinstance(response, Response):
            print("Response is a rest_framework.response.Response")
            if hasattr(response, "render"):
                print("Rendering response...")
                response = response.render()
                print("Response rendered.")
            response_content = response.content.decode()
        elif isinstance(response, JsonResponse):
            print("Response is a django.http.response.JsonResponse")
            response_content = response.content.decode()
        else:
            print(
                "Response is not a TemplateResponse, rest_framework.response.Response, or JsonResponse.")
            response_content = "Unsupported response type"

        # Write the output to a JSON file
        output_path = Path("recommendation_output.json")
        with output_path.open("w", encoding="utf-8") as file:
            try:
                json.dump(json.loads(response_content), file, indent=4)
            except json.JSONDecodeError:
                file.write(response_content)
