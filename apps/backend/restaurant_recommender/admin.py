"""This file contains the admin configuration for the restaurant_recommender app."""

from django.contrib import admin

from restaurant_recommender.models import Aspect, PredictionModel, Restaurant  # type: ignore

admin.site.register(Restaurant)
admin.site.register(Aspect)
admin.site.register(PredictionModel)
