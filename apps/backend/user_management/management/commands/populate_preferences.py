"""Populate preferences table with cuisine types and price ranges."""

from django.core.management.base import BaseCommand

from user_management.models import Preference  # type: ignore


class Command(BaseCommand):
    """A Django management command to populate the preferences table with cuisine types and price ranges."""

    help = "Populate preferences table"

    def handle(self, *args, **kwargs):  # noqa: ARG002
        """Handle the command execution."""
        cuisine_types = [
            "Afghan",
            "African",
            "Afternoon Tea",
            "American",
            "Argentinean",
            "Asian",
            "Australian",
            "Austrian",
            "Bar / Lounge / Bottle Service",
            "Barbecue",
            "Basque",
            "Belgian",
            "Bistro",
            "Brazilian",
            "Breakfast",
            "British",
            "Burgers",
            "Burmese",
            "Café",
            "Californian",
            "Caribbean",
            "Chinese",
            "Chinese (Beijing)",
            "Chinese (Canton)",
            "Chinese (Sichuan)",
            "Cocktail Bar",
            "Colombian",
            "Comfort Food",
            "Contemporary American",
            "Contemporary Asian",
            "Contemporary European",
            "Contemporary French",
            "Contemporary French / American",
            "Contemporary Indian",
            "Contemporary Italian",
            "Contemporary Latin",
            "Contemporary Mexican",
            "Continental",
            "Creole / Cajun / Southern",
            "Cuban",
            "Dim Sum",
            "Eastern European",
            "European",
            "Farm-to-table",
            "Filipino",
            "French",
            "French American",
            "Fusion / Eclectic",
            "Gastro Pub",
            "Georgian",
            "Global, International",
            "Greek",
            "Indian",
            "International",
            "Irish",
            "Israeli",
            "Italian",
            "Izakaya",
            "Jamaican",
            "Japanese",
            "Japanese Speciality",
            "Kaiseki",
            "Korean",
            "Kosher",
            "Latin / Spanish",
            "Latin American",
            "Lebanese",
            "Lounge",
            "Mediterranean",
            "Mexican",
            "Middle Eastern",
            "Nordic",
            "Not Provided",
            "Pan-Asian",
            "Persian",
            "Peruvian",
            "Pizza Bar",
            "Pizzeria",
            "Provencal",
            "Pub",
            "Puerto Rican",
            "Ramen",
            "Regional Italian (Sardinia)",
            "Regional Mexican",
            "Russian",
            "Scandinavian",
            "Seafood",
            "Spanish",
            "Speakeasy",
            "Sports Bar",
            "Steak",
            "Steakhouse",
            "Sushi",
            "Tapas / Small Plates",
            "Tex-Mex",
            "Thai",
            "Traditional French",
            "Turkish",
            "Vegan",
            "Vegetarian",
            "Vegetarian / Vegan",
            "Vietnamese",
            "West African",
            "West Indian",
            "Wine Bar",
        ]

        prices = ["$30 and under", "$31 to $50", "$50 and over"]

        for cuisine in cuisine_types:
            Preference.objects.get_or_create(
                description=cuisine, type="Cuisine")

        for price in prices:
            Preference.objects.get_or_create(description=price, type="Price")

        # Handling "Not Provided" as non-selectable
        Preference.objects.get_or_create(
            description="Not Provided", type="Cuisine", defaults={"is_selectable": False})

        self.stdout.write(self.style.SUCCESS(
            "Successfully populated preferences"))
