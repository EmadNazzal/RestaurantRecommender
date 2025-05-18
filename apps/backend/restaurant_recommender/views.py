# type: ignore
"""
Views for restaurant recommender including: RestaurantFreeTextEntrySearchView, MapRestaurantSearchView, and PredictBusyness.

This module defines views for the restaurant recommender application, including: RestaurantFreeTextEntrySearchView, MapRestaurantSearchView, and PredictBusyness.
These views handle requests for searching restaurants by location or free text entry, and predicting restaurant busyness.

Typical usage example:

    # Example of fetching all restaurants
    response = self.client.get('/api/all-restaurants/')
    data = response.json()

    # Example of free text search for restaurants
    response = self.client.get('/api/free-text-restaurant-search/')
    data = response.json()

    # Example of fetching restaurant busyness prediction
    response = self.client.get('/api/2024-07-07T12:00:00/zone/')
    data = response.json()
"""

import logging
from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView


from restaurant_recommender.models import Restaurant
from restaurant_recommender.predictions import make_predictions
from restaurant_recommender.serializers import (
    LocationFreeEntrySearchViewSerializer,
    MapRestaurantSearchSerializer,
)


logger = logging.getLogger(__name__)


class MapRestaurantSearchView(APIView):
    """
    View for retrieving restaurants to be displayed on the map{GET}.

    This view allows users to see all restaurants in Manhattan on the map.

    Query Parameters:
        restaurant_name: query to filter restaurants by name.
    """

    def get(self, request):
        restaurant_name = request.query_params.get('restaurant_name')

        # Define cache key
        cache_key = f'restaurants_search_{restaurant_name}' if restaurant_name else 'restaurants_all'

        # Check cache
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Retrieved cached data for key: {cache_key}")
            return Response(cached_data)

        # Retrieve data from database with query optimization
        restaurants = self.get_restaurants(restaurant_name)

        # Serialize data
        serializer = MapRestaurantSearchSerializer(
            restaurants, many=True, context={'request': request}
        )
        serialized_data = serializer.data

        # Cache serialized data
        cache.set(cache_key, serialized_data,
                  timeout=60 * 60 * 2)  # Cache for 2 hours
        logger.info(f"Cached data for key: {cache_key}")

        return Response(serialized_data)

    def get_restaurants(self, restaurant_name):
        if restaurant_name:
            # Use prefetch_related for the Aspect model as it has a ForeignKey relationship
            return Restaurant.objects.filter(
                restaurant_name__icontains=restaurant_name
            ).prefetch_related('aspects')  # Use prefetch_related if Aspect is related by ForeignKey
        else:
            return Restaurant.objects.all().prefetch_related('aspects')


class RestaurantFreeTextEntrySearchView(generics.ListAPIView):
    """
    View for retrieving restaurants with free entry search{GET}.

    This view allows users to search a restaurant by its name, and provides
    an ouput of the specific restaurant with all of its associated aspects.

    Query Parameters:
        restaurant: The restaurant search with all of its aspects.
    """
    serializer_class = LocationFreeEntrySearchViewSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            queryset = Restaurant.objects.filter(
                restaurant_name__icontains=query
            ).distinct()
        else:
            queryset = Restaurant.objects.none()

        return queryset.prefetch_related('aspects')


class PredictBusyness(APIView):
    # TODO(RiinKal): probably this feature will be available for all users
    # permission_classes = [IsAuthenticated]

    """
    View for retrieving machine learning predictions, predicting busyness of zones in Manhattan{GET}.
    Input is a dynamic time.

    This view allows users to choose a date and time to detect busyness in Manhattan 
    according to the Manhattan zones from the restaurant table.

    Query Parameters:
        time: The specific date and time in '%Y-%m-%dT%H:%M:%S' format for which the prediction is made.

    Returns:
        A Response object containing serialized prediction data for each zone,
        or an error message if the prediction fails.
    """

    def get(self, request, time):
        try:
            # Directly call make_predictions to see what is happening without storing predictions
            result = make_predictions(time)

            print(result)

            if 'error' in result:
                return Response(result, status=500)
            # Return the raw result for inspection
            return Response(result)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


"""
TODO(RiinKal): not in use currently
class LocationDropdownMenuView(generics.ListAPIView):
    
    View for retrieving restaurants based on neighborhood for a dropdown menu[GET].

    This view allows users to filter restaurants by neighborhood using neighborhood as a query.

    Query Parameters:
        neighborhood: The neighborhood to filter restaurants by.
    
    serializer_class = NeighborhoodCuisineSerializer

    def get_queryset(self):
        neighborhood = self.request.query_params.get('neighborhood', None)
        if neighborhood:
            return Restaurant.objects.filter(neighborhood=neighborhood)
        return Restaurant.objects.none()


TODO(RiinKal): Not in use currently
class LocationFreeEntrySearchView(generics.ListAPIView):
    
    View for retrieving restaurants based on location free entry search{GET}.

    This view allows users to search locations/neighborhoods and provides 
    an ouput of all the restaurants in the neighborhood, with their specific aspects.

    Query Parameters:
        location/neighborhood: The neighborhood to filter restaurants by.
    
    serializer_class = LocationFreeEntrySearchViewSerializer

    def get_queryset(self):
        neighborhood = self.request.query_params.get('neighborhood', None)
        if neighborhood:
            queryset = Restaurant.objects.filter(neighborhood=neighborhood)
        else:
            queryset = Restaurant.objects.none()

        return queryset.prefetch_related('aspects')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
"""
