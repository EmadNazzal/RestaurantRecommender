# get_user_model is used to get current active User model from project, defined in models.py
"""import pickle
import time
import unittest

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from rest_framework import status  # type: ignore
from rest_framework.reverse import reverse  # type: ignore
from rest_framework.test import APITestCase  # type: ignore

from restaurant_recommender.models import PredictionModel, Restaurant  # type: ignore
from restaurant_recommender.tasks import load_prediction_model

User = get_user_model()

sample_restaurants = [
    {
        "restaurant_name": "Westville - Chelsea",
        "primary_cuisine": "American",
        "overall_rating": 4.6,
        "latitude": 40.7396075,
        "longitude": -73.9991851,
        "zone": "Flatiron",
        "telephone": "123-456-7890",
        "website": "http://westvillechelsea.com",
        "price": "$$",
        "food_rating": 4.5,
        "service_rating": 4.4,
        "value_rating": 4.3,
        "ambience_rating": 4.2,
        "noise_level": "Moderate",
        "photo_url": "http://westvillechelsea.com/photo.jpg",
        "address": "246 W 18th St, New York, NY 10011",
        "location_id": 1,
        "dress_code": "Casual"
    },
    {
        "restaurant_name": "Cecconi's at The Ned NoMad",
        "primary_cuisine": "Contemporary Italian",
        "overall_rating": 4.6,
        "latitude": 40.7449561,
        "longitude": -73.9884704,
        "zone": "Union Sq",
        "telephone": "987-654-3210",
        "website": "http://cecconisnomad.com",
        "price": "$$$",
        "food_rating": 4.7,
        "service_rating": 4.6,
        "value_rating": 4.5,
        "ambience_rating": 4.8,
        "noise_level": "Low",
        "photo_url": "http://cecconisnomad.com/photo.jpg",
        "address": "1170 Broadway, New York, NY 10001",
        "location_id": 2,
        "dress_code": "Smart Casual"
    }
]

# To run these tests use: python manage.py test restaurant_recommender.tests

# TODO: (RiinKal): All tests passed, will comment this out temporarily
cache hit and miss results:
All restaurants fetch time with cache miss: 0.0815 seconds
All restaurants fetch time with cache hit: 0.0071 seconds
Prediction model load time with cache miss: 0.0134 seconds
Prediction model load time with cache hit: 0.0000 seconds


class RestaurantAPITest(APITestCase):

    def setUp(self):
        # Clear the cache before running tests
        cache.clear()

        # Create sample restaurants in the database
        for restaurant_data in sample_restaurants:
            Restaurant.objects.create(
                restaurant_name=restaurant_data['restaurant_name'],
                primary_cuisine=restaurant_data['primary_cuisine'],
                overall_rating=restaurant_data['overall_rating'],
                latitude=restaurant_data['latitude'],
                longitude=restaurant_data['longitude'],
                zone=restaurant_data['zone'],
                telephone=restaurant_data['telephone'],
                website=restaurant_data['website'],
                price=restaurant_data['price'],
                food_rating=restaurant_data['food_rating'],
                service_rating=restaurant_data['service_rating'],
                value_rating=restaurant_data['value_rating'],
                ambience_rating=restaurant_data['ambience_rating'],
                noise_level=restaurant_data['noise_level'],
                photo_url=restaurant_data['photo_url'],
                address=restaurant_data['address'],
                location_id=restaurant_data['location_id'],
                dress_code=restaurant_data['dress_code']
            )

    def test_all_restaurants_view(self):
        Test all-restaurants API endpoint.

        Verifies that all restaurants API endpoint returns all restaurants.
        
        url = reverse('all-restaurants')

        # First request to populate the cache
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(sample_restaurants))

        # Ensure that cache is populated
        cached_data = cache.get("restaurants_all")
        self.assertIsNotNone(cached_data, "Cache is not populated as expected")

        # Second request to use the cached data
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(sample_restaurants))

        # Verify that the response data from the cache matches the expected data
        self.assertEqual(response.data, cached_data)


class PredictionModelTest(TestCase):
    # TODO: (RiinKal): authentication is turned off for development, and test will fail due to that for now

    def setUp(self):
        # Clear cache before each test
        cache.clear()

        # Create restaurant objects from the sample data
        for restaurant_data in sample_restaurants:
            Restaurant.objects.create(
                restaurant_name=restaurant_data['restaurant_name'],
                primary_cuisine=restaurant_data['primary_cuisine'],
                overall_rating=restaurant_data['overall_rating'],
                latitude=restaurant_data['latitude'],
                longitude=restaurant_data['longitude'],
                zone=restaurant_data['zone'],
                telephone=restaurant_data['telephone'],
                website=restaurant_data['website'],
                price=restaurant_data['price'],
                food_rating=restaurant_data['food_rating'],
                service_rating=restaurant_data['service_rating'],
                value_rating=restaurant_data['value_rating'],
                ambience_rating=restaurant_data['ambience_rating'],
                noise_level=restaurant_data['noise_level'],
                photo_url=restaurant_data['photo_url'],
                address=restaurant_data['address'],
                location_id=restaurant_data['location_id'],
                dress_code=restaurant_data['dress_code']
            )

        # Create a test prediction model and save it to the database
        self.prediction_model = PredictionModel.objects.create(
            model_name="TestModel",
            pickle_file=pickle.dumps("test_model_data"),
            is_active=True,
            restaurant_id=Restaurant.objects.first().id  # Use the first restaurant's ID
        )

    def test_api_endpoint(self):
        pass

    def test_load_prediction_model_cache(self):
        load_prediction_model()

        # Check if the model is saved in the cache
        cached_model = cache.get('prediction_model')
        self.assertIsNotNone(cached_model, "Model should be in cache")

        # Run the task again to check if it retrieves from the cache
        with self.assertLogs('restaurant_recommender.tasks', level='INFO') as cm:
            load_prediction_model()
            self.assertTrue(any("Prediction model retrieved from cache" in message for message in cm.output),
                            "Expected log message not found in output")


class CachePerformanceTest(TestCase):
    def setUp(self):
        # Create restaurant objects from the sample data
        for restaurant_data in sample_restaurants:
            Restaurant.objects.create(
                restaurant_name=restaurant_data['restaurant_name'],
                primary_cuisine=restaurant_data['primary_cuisine'],
                overall_rating=restaurant_data['overall_rating'],
                latitude=restaurant_data['latitude'],
                longitude=restaurant_data['longitude'],
                zone=restaurant_data['zone'],
                telephone=restaurant_data['telephone'],
                website=restaurant_data['website'],
                price=restaurant_data['price'],
                food_rating=restaurant_data['food_rating'],
                service_rating=restaurant_data['service_rating'],
                value_rating=restaurant_data['value_rating'],
                ambience_rating=restaurant_data['ambience_rating'],
                noise_level=restaurant_data['noise_level'],
                photo_url=restaurant_data['photo_url'],
                address=restaurant_data['address'],
                location_id=restaurant_data['location_id'],
                dress_code=restaurant_data['dress_code']
            )

    def test_prediction_cache_performance(self):
        # Clear the cache before the test
        cache.clear()

        # Measure time with cache miss
        start_time = time.time()
        load_prediction_model()
        end_time = time.time()
        cache_miss_time = end_time - start_time

        # Measure time with cache hit
        start_time = time.time()
        load_prediction_model()
        end_time = time.time()
        cache_hit_time = end_time - start_time

        print(
            f"Prediction model load time with cache miss: {cache_miss_time:.4f} seconds")
        print(
            f"Prediction model load time with cache hit: {cache_hit_time:.4f} seconds")

    def test_all_restaurants_cache_performance(self):
        url = reverse('all-restaurants')

        # Clear the cache before the test
        cache.clear()

        # Measure time with cache miss
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        cache_miss_time = end_time - start_time
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Measure time with cache hit
        start_time = time.time()
        response = self.client.get(url)
        end_time = time.time()
        cache_hit_time = end_time - start_time
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(
            f"All restaurants fetch time with cache miss: {cache_miss_time:.4f} seconds")
        print(
            f"All restaurants fetch time with cache hit: {cache_hit_time:.4f} seconds")


if __name__ == "__main__":
    unittest.main()


TODO: (RiinKal): This API endpoint might not be used at all

    def test_restaurant_free_text_entry_search_view(self):
        Test restaurant free text entry search API endpoint.

        Verifies that it returns a restaurant, the data that the table contains
        and associated aspects.

        url = reverse('free-text-restaurant-search')
        search_params = {'query': 'Kings of Kobe - Wagyu Kitchen & Bar'}
        print(f"Searching with params: {search_params}")
        response = self.client.get(url, search_params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Debugging: Print the response data
        print("Response data:", response.data)

        # Validate response data
        self.assertEqual(len(response.data), 1)  # Ensure we have one result
        restaurant = response.data[0]  # Access the first result

        self.assertEqual(
            restaurant['restaurant_name'], 'Kings of Kobe - Wagyu Kitchen & Bar')
        self.assertEqual(restaurant['primary_cuisine'], 'Burgers')
        self.assertEqual(restaurant['overall_rating'], 4.4)
        self.assertEqual(restaurant['neighborhood'], 'Theater District')
        self.assertEqual(restaurant['latitude'], 40.7612218)
        self.assertEqual(restaurant['longitude'], -74.0003395)
        self.assertEqual(restaurant['zone'], 'West Chelsea/Hudson Yards')

        # Validate aspects
        self.assertEqual(len(restaurant['aspects']), 10)
        self.assertEqual(restaurant['aspects'][0]['aspect'], 'burger')
        self.assertEqual(restaurant['aspects'][0]['rating_type'], 'positive')
        self.assertEqual(restaurant['aspects'][0]['count'], 31)
        self.assertEqual(restaurant['aspects'][0]['restaurant'], 2925)
        """
