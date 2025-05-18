"""This module contains the URL configuration for the restaurant_recommender app."""
from django.urls import path

from restaurant_recommender.views import (  # type: ignore
    MapRestaurantSearchView,
    PredictBusyness,
    RestaurantFreeTextEntrySearchView,
)

urlpatterns = [
    # search things
    # url providing all restaurants
    path('all-restaurants/', MapRestaurantSearchView.as_view(),
         name='all-restaurants'),
    # Restaurant search, providing one restaurant and aspects of the specific restaurant
    path('free-text-restaurant-search/', RestaurantFreeTextEntrySearchView.as_view(),
         name='free-text-restaurant-search'),
    # url that uses pickle prediction to predict busyness in zones, defined in restaurant table
    # Input is a dynamic time
    path('<str:time>/zone/', PredictBusyness.as_view(), name='predict-busyness'),
]
