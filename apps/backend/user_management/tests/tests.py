
"""

from user_management.models import Profile  # type: ignore
from django.urls import reverse
import time
import unittest
from restaurant_recommender.models import Restaurant   # type: ignore
from user_management.models import ContactUs, Preference  # type: ignore
from django.core.cache import cache

from django.contrib.auth import get_user_model
from datetime import datetime, timedelta, timezone
import jwt
from rest_framework import status  # type: ignore
from rest_framework.test import APITestCase  # type: ignore
from rest_framework_simplejwt.tokens import AccessToken
from datetime import timedelta
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

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

sample_users = [
    {"email": "nipitiri@example.com", "password1": "password123"},
    {"email": "nipitiri1@example.com", "password1": "password234",
     "password2": "password234", "first_name": "Nipi", "surname": "Tiri1"},
    {"email": "nipitiri2@example.com", "password1": "password", "first_name": "Nipi1"},
    {"email": "nipitiri3@example.com", "password1": "abc",
     "password2": "abc", "first_name": "Nipi", "surname": "Tiri2"},
    {"email": "nipitiri4@duplicate.com", "password1": "password344",
     "password2": "password344", "first_name": "Nipi", "surname": "Tiri3"},
    {"email": "NipiTiri5@example.com", "password1": "password432",
     "password2": "password432", "first_name": "Nipi", "surname": "Tiri4"},
    {"email": "nipitiri6@duplicatetest.com", "password1": "password432", "password2": "password432",
     "name": "Nipi", "surname": "Tiri4", "subject": "I am not happy at all", "message": "Should be happier"},
    {"email": "nipitiri7@example.com", "password1": "initialpassword",
     "password_reset": "newpassword123"},
]

# cache hit and cache miss;
# Bookmark fetch time with cache miss: 0.0339 seconds
# Bookmark fetch time with cache hit: 0.0000 seconds
# Profile fetch time with cache miss: 0.0156 seconds
# Profile fetch time with cache hit: 0.0000 seconds


class LoginTest(APITestCase):

    def setUp(self):
        Set up the test environment by creating multiple User instances in the database.

        This method creates User instances in the database using email-password pairs
        from the sample_users dictionary. Each user is saved with a hashed password.

        The created users are used to test login functionality in different scenarios.
        
        for testuser in sample_users:
            user = User.objects.create(email=testuser['email'])
            user.set_password(testuser['password1'])
            user.save()

    def test_incorrect_login(self):
        Test user login functionality.

        Verifies that a user cannot log in with an email and a password, that have not been registered.

        This test ensures that a user who has not registered cannot log in.
        
        response = self.client.post('/api/login/', {
            'email': 'notindatabase@example.com',
            'password': 'doesnotmakeadifference123'
        })
        self.assertIn(response.status_code, [
                      status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])

    def test_correct_login(self):
        Test correct user login functionality.

        Verifies that a user can log in with the correct email and password,
        and ensures correct user authentication.
        
        sample_user = sample_users[0]
        response = self.client.post('/api/login/', {
            'email': sample_user['email'],
            'password': sample_user['password1']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertIn('access', result)

    def test_login_with_remember_me(self):
        sample_user = sample_users[0]
        response = self.client.post('/api/login/', {
            'email': sample_user['email'],
            'password': sample_user['password1'],
            'remember_me': True
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertIn('access', result)

        access_token = result['access']
        decoded_access_token = jwt.decode(
            access_token, options={"verify_signature": False})

        exp_timestamp = decoded_access_token['exp']
        exp_datetime = datetime.fromtimestamp(exp_timestamp, timezone.utc)
        expected_exp_datetime = datetime.now(timezone.utc) + timedelta(days=30)

        # Allow a margin of error in the comparison due to processing time to use remember me global settings
        self.assertAlmostEqual(
            exp_datetime, expected_exp_datetime, delta=timedelta(seconds=5))


class TestRegister(APITestCase):
    def setUp(self):
        Set up the test environment by creating a user with a duplicate email address.

        This method creates a user in the database with an email address already present
        in the sample_users dictionary to test the email uniqueness constraint.

        sample_user = sample_users[4]
        user = User.objects.create(
            email=sample_user['email']
        )
        user.set_password(sample_user['password1'])
        user.save()

    def test_correct_register(self):
        Test user registration of a CustomUserManager.

        Verifies that a new user instance:
        - Has email 'nipitiri@example.com'.
        - Has a password that matches 'password123' after hashing.

        This test ensures correct user registration with CustomUserManager.

        sample_user = sample_users[1]
        response = self.client.post('/api/register/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
            'password_confirm': sample_user["password2"],
            'first_name': sample_user.get("first_name", ""),
            'surname': sample_user.get('surname', ""),
        }, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        result = response.json()
        self.assertEqual(result['email'], sample_user["email"])

    def test_missing_fields_register(self):
        Test creating user with missing required fields, example with missing surname and password_confirm.

        Confirms that registration fails with a 400 status code when surname is not provided.

        This test ensures correct error handling for missing fields during registration.

        sample_user = sample_users[2]
        response = self.client.post('/api/register/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
            'first_name': sample_user.get("first_name", ""),
        }, follow=True)
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])

    def test_short_password(self):
        Test creating user with too short password.

        Verifies that a user registers with a password having a numeric value.

        This test ensures correct user registration with CustomUserManager.

        sample_user = sample_users[3]
        response = self.client.post('/api/register/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
            'password_confirm': sample_user['password2'],
            'first_name': sample_user.get("first_name", ""),
            'surname': sample_user.get('surname', ""),
        }, follow=True)
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])
        result = response.json()
        self.assertIn('non_field_errors', result)
        self.assertTrue(result['non_field_errors'])

    def test_email_exists(self):
        Test creating user with already registered email.

        Verifies that an email address that has already been used to register cannot be used to register again.

        This test ensures correct user registration with CustomUserManager.

        sample_user = sample_users[4]
        response = self.client.post('/api/register/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
            'password_confirm': sample_user['password2'],
            'first_name': sample_user.get("first_name", ""),
            'surname': sample_user.get('surname', ""),
        }, follow=True)
        self.assertIn(response.status_code, [
            status.HTTP_400_BAD_REQUEST, status.HTTP_401_UNAUTHORIZED])
        result = response.json()
        self.assertIn('email', result)
        self.assertIn('User with this Email already exists.', result['email'])

    def test_normalize_email(self):
        Test email normalization when registering a user.

        Verifies that email addresses are normalized to lowercase even if provided with uppercase format.

        This test verifies email normalization in user registering.

        sample_user = sample_users[5]
        response = self.client.post('/api/register/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
            'password_confirm': sample_user["password2"],
            'first_name': sample_user.get("first_name", ""),
            'surname': sample_user.get('surname', ""),
        }, follow=True)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED,
                         msg=f"Response content: {response.content}")
        result = response.json()
        self.assertIn('email', result,
                      msg=f"Response content: {response.content}")
        stored_email = result['email'].strip().lower()
        expected_email = sample_user["email"].strip().lower()
        self.assertEqual(stored_email, expected_email)


class TestJWTToken(APITestCase):
    def setUp(self):
        Set up the test environment by creating multiple User instances in database.

        This method creates User instances in the database using email-password pairs
        from the sample_users dictionary. Each user is saved with a hashed password.

        The created users are used to test login functionality in different scenarios.

        for testuser in sample_users:
            user = User.objects.create(
                email=testuser['email']
            )
            user.set_password(testuser['password1'])
            user.save()

    def test_jwt_token(self):
        Test JWT access and refresh token.

        - Verifies that user is logged in for the token to be returned.
        - Ensures that access and refresh token are returned.
        - Asserts that both tokens; access and refresh are different with assertEqual.

        This test ensures correct user authentication with JWT tokens.

        sample_user = sample_users[0]
        response = self.client.post('/api/login/', {
            'email': sample_user['email'],
            'password': sample_user['password1']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.json()
        self.assertIn('access', result)
        token_1 = result['access']
        refresh_token = result['refresh']

        response_refresh = self.client.post('/api/token/refresh/', {
            'refresh': refresh_token
        })
        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        result_refresh = response_refresh.json()
        self.assertIn('access', result_refresh)
        token_2 = result_refresh['access']
        self.assertNotEqual(token_1, token_2)




class TestPasswordReset(APITestCase):
    def setUp(self):
        Set up the test environment by creating multiple User instances in the database.

        This method creates User instances in the database using email-password pairs
        from the sample_users dictionary. Each user is saved with a hashed password.

        The created users are used to test password reset functionality in different scenarios.
        
        for testuser in sample_users:
            user = User.objects.create(email=testuser['email'])
            user.set_password(testuser['password1'])
            user.save()

    def test_password_reset_request(self):
        Test the password reset request process.

        Verifies that a password reset token is sent when a valid email is provided.
        
        sample_user = sample_users[7]
        response = self.client.post('/api/reset-password/', {
            'email': sample_user['email']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'],
                         'Password reset email has been sent.')

    def test_password_reset_confirm(self):
        Test the password reset confirmation process.

        Verifies that a user's password can be reset with a valid token and UID.
        
        sample_user = sample_users[7]
        user = User.objects.get(email=sample_user['email'])
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        new_password = 'newpassword123'
        url = f'/api/reset-password/confirm/{uid}/{token}/'
        print(f"Constructed URL: {url}")  # Add this line to debug
        response = self.client.post(url, {
            'new_password': new_password
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)
        self.assertEqual(response.data['success'],
                         'Password reset successfully.')

        # Verify that the password has been changed
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))


TODO(RiinKal): Continue from here
class ProfileViewSetTests(APITestCase):
    def setUp(self):
        sample_user = {
            'email': 'test@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Nipi',
            'surname': 'User'
        }

        self.client.post('/api/register/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
            'password_confirm': sample_user["password2"],
            'first_name': sample_user.get("first_name", ""),
            'surname': sample_user.get('surname', ""),
        }, follow=True)

        self.user = User.objects.get(email=sample_user["email"])
        self.profile = Profile.objects.get(user=self.user)

        login_response = self.client.post('/api/login/', {
            'email': sample_user['email'],
            'password': sample_user['password1']
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Clear cache at the start of each test
        cache.clear()

    # Include all the tests as they were before
    def test_get_profile_with_cache(self):
        Test retrieving the user's profile and ensure it's cached.
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

        # First request to populate cache
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Nipi')

        # Ensure cache is populated
        cached_profile = cache.get(f'profile_{self.user.id}')
        self.assertIsNotNone(
            cached_profile, "Cache is not populated as expected")

        self.profile.first_name = 'Modified'
        self.profile.save()

        # Second request should return cached data
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Cached response
        self.assertEqual(response.data['first_name'], 'Nipi')

    def test_update_profile(self):
        Test updating the user's profile and cache invalidation.
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})
        data = {
            'first_name': 'UpdatedName',
            'surname': 'UpdatedSurname'
        }
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'UpdatedName')
        self.assertEqual(self.profile.surname, 'UpdatedSurname')

        # Check that the cache is invalidated
        self.assertIsNone(cache.get(f'profile_{self.user.id}'))

    def test_delete_profile(self):
        Test deleting the user's profile and cache invalidation.
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(user=self.user).exists())

        # Check that the cache is invalidated
        self.assertIsNone(cache.get(f'profile_{self.user.id}'))

    def test_get_profile(self):
        Test retrieving the user's profile.
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Nipi')


class MiscellaneousTests(APITestCase):
    def setUp(self):
         Set up the test environment by creating multiple User instances in database.

         This method creates User instances in the database using email-password pairs
         from the sample_users dictionary. Each user is saved with a hashed password.

         The created users are used to test login functionality in different scenarios.
 
        for testuser in sample_users:
            user = User.objects.create(
                email=testuser['email']
            )
            user.set_password(testuser['password1'])
            user.save()

    def test_logout(self):
        Logout test to check if the user is able to logout.

        - First user logs in .
        - JWT tokens are extracted from the response data.
        - Ensures that the access token is present.
        - Sends a post request to the logout endpoint with a JWT token in the Authorization header to ensure successful logout.

        The test ensures logout functionality and correct token handling.

        sample_user = sample_users[0]
        login_response = self.client.post('/api/login/', {
            'email': sample_user["email"],
            'password': sample_user["password1"],
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data.get('access')
        refresh_token = login_response.data.get('refresh')
        self.assertIsNotNone(token)
        self.assertIsNotNone(refresh_token)

        logout_response = self.client.post(
            '/api/logout/',
            {'refresh': refresh_token},
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )
        self.assertIn(logout_response.status_code, [
            status.HTTP_200_OK, status.HTTP_205_RESET_CONTENT])

    def test_contact_us(self):
        Test contact us functionality.

        Verifies that a user can submit a contact us form and the data is stored correctly.

        sample_user = sample_users[6]
        url = reverse('contact-us')
        data = {
            'name': sample_user['name'],
            'email': sample_user['email'],
            'subject': sample_user['subject'],
            'message': sample_user['message'],
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ContactUs.objects.filter(
            email=data['email'], message=data['message']).exists())



class CachePerformanceTest(APITestCase):
    def setUp(self):
        Set up the test environment by creating restaurant objects with location_id using
        sample_restaurants dictionary and user for profile and bookmark tests.
        # Create user
        self.user = User.objects.create_user(
            email=sample_users[1]["email"],
            password=sample_users[1]["password1"],
            first_name=sample_users[1]["first_name"],
            surname=sample_users[1]["surname"]
        )

        # Create restaurants
        for restaurant in sample_restaurants:
            Restaurant.objects.create(
                restaurant_name=restaurant["restaurant_name"],
                primary_cuisine=restaurant["primary_cuisine"],
                overall_rating=restaurant["overall_rating"],
                latitude=restaurant["latitude"],
                longitude=restaurant["longitude"],
                zone=restaurant["zone"],
                telephone=restaurant["telephone"],
                website=restaurant["website"],
                price=restaurant["price"],
                food_rating=restaurant["food_rating"],
                service_rating=restaurant["service_rating"],
                value_rating=restaurant["value_rating"],
                ambience_rating=restaurant["ambience_rating"],
                noise_level=restaurant["noise_level"],
                photo_url=restaurant["photo_url"],
                address=restaurant["address"],
                location_id=restaurant["location_id"],
                dress_code=restaurant["dress_code"]
            )

        # Create profile
        self.profile = Profile.objects.create(
            user=self.user,
            first_name=self.user.first_name,
            surname=self.user.surname,
            slug=self.user.email.replace('@', '-at-')
        )

        # Create bookmark
        self.bookmark = Preference.objects.create(user=self.user)
        self.bookmark.restaurants.set(Restaurant.objects.all())

        # Authenticate the client with token
        login_response = self.client.post('/api/login/', {
            'email': self.user.email,
            'password': sample_users[1]["password1"]
        })
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_profile_cache_performance(self):
        url = reverse('profile-detail', kwargs={'pk': self.profile.pk})

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
            f"Profile fetch time with cache miss: {cache_miss_time:.4f} seconds")
        print(
            f"Profile fetch time with cache hit: {cache_hit_time:.4f} seconds")

    def test_bookmark_cache_performance(self):
        url = reverse('bookmark-list')

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
            f"Bookmark fetch time with cache miss: {cache_miss_time:.4f} seconds")
        print(
            f"Bookmark fetch time with cache hit: {cache_hit_time:.4f} seconds")


if __name__ == "__main__":
    unittest.main()



TODO(RiinKal): not used
class BookmarkViewSetTests(APITestCase):
    def setUp(self):
        sample_user = {
            'email': 'test@example.com',
            'password': 'testpassword123',
            'first_name': 'Nipi',
            'surname': 'User'
        }
        self.user = User.objects.create_user(
            email=sample_user["email"],
            password=sample_user["password"],
            first_name=sample_user.get("first_name", ""),
            surname=sample_user.get("surname", "")
        )

        # Create restaurants from the sample_restaurants dictionary
        self.restaurants = [Restaurant.objects.create(
            **restaurant) for restaurant in sample_restaurants]

        response = self.client.post('/api/login/', {
            'email': sample_user["email"],
            'password': sample_user["password"]
        })
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')

        # Clear cache at the start of each test
        cache.clear()

    def test_list_caching(self):
        Test caching of the bookmarks list.
        url = reverse('bookmark-list')
        cache_key = 'all_bookmarks'
        cache.delete(cache_key)  # Ensure cache is empty

        # First request to populate cache
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get(cache_key))

        # Second request should hit cache (expecting no database queries)
        with self.assertNumQueries(0):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_caching(self):
        Test caching of a single bookmark retrieval.
        bookmark = Bookmark.objects.create(user=self.user)
        bookmark.restaurants.set(self.restaurants)
        url = reverse('bookmark-detail', kwargs={'pk': bookmark.pk})
        cache_key = f'bookmark_{bookmark.pk}'
        cache.delete(cache_key)  # Ensure cache is empty

        # First request to populate cache
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(cache.get(cache_key))

        # Second request should hit cache (expecting no database queries)
        with self.assertNumQueries(0):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cache_invalidation(self):
        Test invalidation of the cache upon bookmark update or delete.
        bookmark = Bookmark.objects.create(user=self.user)
        bookmark.restaurants.set(self.restaurants)
        url = reverse('bookmark-detail', kwargs={'pk': bookmark.pk})
        # Populate cache
        self.client.get(url)
        cache_key = f'bookmark_{bookmark.pk}'
        self.assertIsNotNone(cache.get(cache_key))

        # Update bookmark and check cache invalidation
        update_url = reverse('bookmark-detail', kwargs={'pk': bookmark.pk})
        data = {'restaurant_ids': [self.restaurants[0].id]}
        self.client.put(update_url, data, format='json')
        self.assertIsNone(cache.get(cache_key))

        # Delete bookmark and check cache invalidation
        delete_url = reverse('bookmark-detail', kwargs={'pk': bookmark.pk})
        self.client.delete(delete_url)
        self.assertIsNone(cache.get(f'bookmark_{bookmark.pk}'))
"""
