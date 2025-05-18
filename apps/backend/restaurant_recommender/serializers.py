# type: ignore
"""
Serializers for restaurant recommender models, including: RestaurantSerializer, AspectSerializer, and PredictionModelSerializer.

This module defines serializers for the restaurant recommender application, including: RestaurantSerializer, AspectSerializer, and PredictionModelSerializer.
These serializers handle the conversion of model objects to JSON and vice versa, facilitating data transfer between the back-end and front-end.

Typical usage example:

    # Serialize a Restaurant instance
    restaurant = Restaurant.objects.get(id=1)
    serializer = class MapRestaurantSearchSerializer(restaurant)
    data = serializer.data

    # Deserialize JSON data to a Restaurant instance
    data = {'restaurant_name': 'Sample Restaurant', 'primary_cuisine': 'Italian',
        'overall_rating': 4.5, 'latitude': 40.7128, 'longitude': -74.0060, 'zone': 'Zone 1'}
    serializer = class MapRestaurantSearchSerializer(serializers.ModelSerializer):(data=data)
    if serializer.is_valid():
        restaurant = serializer.save()
"""
import json
import ast
from rest_framework import serializers
from restaurant_recommender.models import Aspect, Restaurant


class PositiveAspectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aspect
        fields = ['aspect', 'count']


class RestaurantSerializerforBookmarks(serializers.ModelSerializer):
    positive_aspects = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ['primary_cuisine', 'price', 'dress_code',
                  'id', 'restaurant_name', 'positive_aspects']

    def get_positive_aspects(self, obj):
        positive_aspects = obj.aspects.filter(rating_type='positive')
        return PositiveAspectSerializer(positive_aspects, many=True).data


class AspectSerializer(serializers.ModelSerializer):
    """
    Serializer for Aspect model.

    Converts Aspect model object to JSON and vice versa.

    Fields:
        id: Unique identifier for the aspect.
        restaurant: Foreign key to the Restaurant model.
        aspect: Specific aspect of the restaurant (e.g., service, food).
        rating_type: Indicates whether the aspect is positive or negative.
        count: Number of positive or negative reviews mentioning the aspect.
    """
    class Meta:
        model = Aspect
        fields = '__all__'


class LocationFreeEntrySearchViewSerializer(serializers.ModelSerializer):
    """
    Serializer for Restaurant model focused on search view with location-free entry.

    Fields:
        id: Unique identifier for the restaurant.
        restaurant_name: Name of the restaurant.
        primary_cuisine: Primary cuisine of the restaurant.
        overall_rating: Overall rating of the restaurant.
        aspects: List of associated aspects of the restaurant.
        latitude: Latitude of the restaurant.
        longitude: Longitude of the restaurant.
        zone: Zone in Manhattan where the restaurant is located.
    """
    aspects = AspectSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'restaurant_name', 'primary_cuisine', 'overall_rating',
                  'aspects', 'latitude', 'longitude', 'zone', 'photo_url']


class MapRestaurantSearchSerializer(serializers.ModelSerializer):
    aspects = AspectSerializer(many=True, read_only=True)
    photo_url = serializers.SerializerMethodField()

    """
    Serializer for Restaurant model focused on map search view.
    Fields:
        id: Unique identifier for the restaurant.
        primary_cuisine: Primary cuisine of the restaurant.
        overall_rating: Overall rating of the restaurant.
        restaurant_name: Name of the restaurant.
        latitude: Latitude of the restaurant.
        longitude: Longitude of the restaurant.
        zone: Zone in Manhattan where the restaurant is located.
        location_id: Location identifier for the restaurant.
        photo_url: URL of the restaurant's photo.
    """
    class Meta:
        model = Restaurant
        fields = [
            'id', 'restaurant_name', 'website', 'telephone', 'primary_cuisine',
            'price', 'overall_rating', 'ambience_rating', 'food_rating',
            'service_rating', 'value_rating', 'noise_level',
            'address', 'latitude', 'longitude', 'zone', 'location_id', 'aspects', 'photo_url'
        ]

    def get_photo_url(self, obj):
        # Convert JSON string to list
        if obj.photo_url:
            try:
                return json.loads(obj.photo_url)
            except json.JSONDecodeError:
                return []
        return []

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        # Convert list to JSON string
        if 'photo_url' in data and isinstance(data['photo_url'], list):
            internal_value['photo_url'] = json.dumps(data['photo_url'])
        return internal_value


class PredictionResultSerializer(serializers.Serializer):
    """
    Serializer for prediction results.

    Converts prediction result data to JSON.

    Fields:
        zone: Zone for which the prediction is made.
        predicted_value: The predicted value.
    """
    zone = serializers.CharField()
    predicted_value = serializers.FloatField()


"""
TODO(RiinKal): not in use currently
class NeighborhoodCuisineSerializer(serializers.ModelSerializer):
    
    Serializer for Restaurant model focused on neighborhood and cuisine details.

    Fields:
        id: Unique identifier for the restaurant.
        primary_cuisine: Primary cuisine of the restaurant.
        restaurant_name: Name of the restaurant.
        latitude: Latitude of the restaurant.
        longitude: Longitude of the restaurant.
        zone: Zone in Manhattan where the restaurant is located.
    
    class Meta:
        model = Restaurant
        fields = ['id', 'neighborhood', 'primary_cuisine',
                  'restaurant_name', 'latitude', 'longitude', 'zone']

class RestaurantSerializer(serializers.ModelSerializer):
    
    Serializer for Restaurant model.

    Converts Restaurant model instances to JSON and vice versa.

    Fields:
        id: Unique identifier for the restaurant.
        restaurant_name: Name of the restaurant.
        primary_cuisine: Primary cuisine of the restaurant.
        overall_rating: Overall rating of the restaurant.
        neighborhood: Neighborhood where the restaurant is located.
        latitude: Latitude of the restaurant.
        longitude: Longitude of the restaurant.
        zone: Zone in Manhattan where the restaurant is located.
        aspects: List of associated aspects of the specific restaurant.
    
    aspects = AspectSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'restaurant_name', 'primary_cuisine', 'overall_rating',
            'latitude', 'longitude', 'zone', 'telephone',
            'price', 'food_rating', 'service_rating', 'value_rating',
            'noise_level', 'photo_url', 'positive_aspects', 'negative_aspects',
            'aspects'
        ]

"""
