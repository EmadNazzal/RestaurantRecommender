
# type: ignore
#  type ignore, for false positive need type annotation for each variable
"""Models for restaurant recommender including: Restaurant, Aspect, Profile, and PredictionModel.

This module defines models for a restaurant recommender, including: Restaurant, Aspect, Profile, and PredictionModel.
It also includes functionality for creating and managing restaurant data, aspects (restaurant-specific),
machine learning model-related data, user preferences, and user liked restaurants.
"""

from django.db import models


class Restaurant(models.Model):
    """Creates and saves a Restaurant table in Postgresql database.

    Args:
        restaurant_name: Restaurant name.
        primary_cuisine: Primary cuisine of the restaurant.
        overall_rating: Overall rating of the restaurant.
        latitude & longitude: Latitude and longitude of the restaurant.
        zone: Manhattan zone defined in database, where the restaurant is.
        telephone: Contact number of the restaurant.

    Returns:
        str: String representation of the restaurant name
    """

    restaurant_name = models.CharField(max_length=255)
    primary_cuisine = models.CharField(max_length=255, blank=True)
    overall_rating = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    zone = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(max_length=255, blank=True, null=True)
    food_rating = models.FloatField(blank=True, null=True)
    service_rating = models.FloatField(blank=True, null=True)
    value_rating = models.FloatField(blank=True, null=True)
    ambience_rating = models.FloatField(blank=True, null=True)
    noise_level = models.CharField(max_length=20, blank=True, null=True)
    photo_url = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    location_id = models.IntegerField()
    dress_code = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        """String representation of the restaurant name."""
        return self.restaurant_name

    class Meta:
        """Meta class for the Restaurant model."""

        verbose_name = "Restaurant"
        verbose_name_plural = "Restaurants"
        indexes = [
            models.Index(fields=["restaurant_name"]),
            models.Index(fields=["primary_cuisine"]),
            models.Index(fields=["overall_rating"]),
            models.Index(fields=["zone"]),
        ]


class Aspect(models.Model):
    """Creates and saves an Aspect table, with aspects of each restaurant in restaurant table.

    Args:
        restaurant: Restaurant name, that is a foreign key of restaurant table variable restaurant_name.
        aspect: Aspect of the restaurant; service, food, server, view etc.
        rating_type: Categorized as either 'negative' or 'positive' based on the count value
        aspects with negative counts are labeled as 'negative', and those with positive counts are labeled as 'positive'.
        count: Total number of all the specific aspects. Example service count of 129,
        means aspect having 139 positive service reviews. Negative counts are attained the same way.

    Returns:
        str: String represantation of the restaurant name
    """

    restaurant = models.ForeignKey(
        Restaurant, related_name="aspects", on_delete=models.CASCADE)
    aspect = models.CharField(max_length=255)
    rating_type = models.CharField(max_length=10)
    count = models.IntegerField()

    def __str__(self):
        """String representation of the restaurant name."""
        return f"{self.restaurant.restaurant_name} - Aspect: {self.aspect}, Rating Type: {self.rating_type}, Count: {self.count}"

    class Meta:
        """Meta class for the Aspect model."""

        verbose_name = "Aspect"
        verbose_name_plural = "Aspects"
        indexes = [
            models.Index(fields=["restaurant"]),
            models.Index(fields=["aspect"]),
            models.Index(fields=["rating_type"]),
        ]


class PredictionModel(models.Model):
    """
    Model representing a machine learning prediction model stored in the database.

    Fields:
        model_name: Name of the machine learning model.
        description: Description of the machine learning model.
        pickle_file: Serialized machine learning model file.
        restaurant: Foreign key to the Restaurant table, used for associating a prediction
        model with a specific zone in restaurant table.
        is_active: Indicates if the model is active for administrative purposes.
        updated_at: Timestamp of the last update for administrative purposes.
        created_at: Timestamp of when the model was created.

    Returns:
    str: String represantation of the restaurant name
    """

    model_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    pickle_file = models.BinaryField()
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """String representation of the restaurant name."""
        return f"{self.model_name} - {self.restaurant.restaurant_name}"

    class Meta:
        """Meta class for the PredictionModel model."""

        indexes = [
            models.Index(fields=["model_name"]),
            models.Index(fields=["restaurant"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["updated_at"]),
        ]


class WeatherData(models.Model):
    """Model representing weather data stored in the database.

    Fields:
        timestamp: Timestamp of the weather data.
        temperature: Temperature data.
        dewpoint: Dewpoint data.
        precipitation: Precipitation data.

    Returns:
        str: String representation of the timestamp
    """

    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    dewpoint = models.FloatField()
    precipitation = models.FloatField()

    class Meta:
        """Meta class for the WeatherData model."""

        indexes = [
            models.Index(fields=["timestamp"]),
        ]
