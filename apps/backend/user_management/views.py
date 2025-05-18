"""This module provides API views for user management, including registration, login, profile management and preferences, password reset, logout, and contact us functionality.

It uses Django REST framework and SimpleJWT for authentication and authorization.

The module includes views for handling user registration, token-based authentication,
profile retrieval and updates, password reset requests and confirmations, logging out,
and submitting contact inquiries.

See https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html for more
information on SimpleJWT.

See https://stackoverflow.com/questions/35830779/django-rest-framework-apiview-pagination for more
information on pagination in Django REST framework.
"""

import logging
import operator
from datetime import UTC, datetime, timedelta


import numpy as np
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes, force_str
from django.utils.http import http_date, urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import generics, status, viewsets  # type: ignore
from rest_framework.decorators import api_view, permission_classes  # type: ignore
from rest_framework.permissions import AllowAny, IsAuthenticated  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.views import APIView  # type: ignore
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from restaurant_recommender.models import Restaurant  # type: ignore
from user_management.models import ContactUs, Preference, Profile, UserLikedRestaurant, UserPreference  # type: ignore
from user_management.serializers import (
    ContactUsSerializer,
    MyTokenObtainPairSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PreferenceSerializer,
    ProfileSerializer,
    RegistrationSerializer,
    UserLikedRestaurantSerializer,
    UserPreferenceSerializer,
)

from user_management.utils import (
    calculate_cosine_similarity,
    get_all_preferences,
    get_liked_restaurants_matrix,
    user_preferences_to_vector,
)

User = get_user_model()  # type: ignore

logger = logging.getLogger(__name__)


class RegistrationAPIView(APIView):
    """
    Handle user registration.

    Register a new user with first and a surname, and with email as a username and a password.

    Args:
        request: The HTTP request containing user registration data.

    Returns:
        Response: An object containing the user data and HTTP status code 201 if request is successful,
                  or an object containing the errors and HTTP status code 400 if user registration fails.
    """

    def post(self, request):
        """
        Register a new user.

        Args:
            request: The HTTP request containing user registration data.

        Returns:
            Response: An object containing the user data and HTTP status code 201 if request is successful,
                      or an object containing the errors and HTTP status code 400 if user registration fails.
        """
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Profile.objects.create(
                user=user, first_name=user.first_name, surname=user.surname)
            user_data = RegistrationSerializer(user).data
            return Response(user_data, status=status.HTTP_201_CREATED)
        # Log and return detailed errors
        logger.error(f"Registration failed with errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer  # type: ignore

    """Token/login user view."""

    def post(self, request):
        """
        Obtain JWT token pair for a user.

        Args:
            request: The HTTP request containing login credentials.

        Returns:
            Response: An object containing the access and refresh tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Retrieve the user data from the validated_data dictionary
        user_data = serializer.validated_data["user"]

        # Retrieve the actual user instance
        user = User.objects.get(id=user_data["id"])

        remember_me = request.data.get("remember_me", False)

        # Adjust token lifetimes based on remember_me checkbox
        access_token_lifetime = timedelta(
            days=30) if remember_me else timedelta(minutes=60)
        refresh_token_lifetime = timedelta(
            days=30) if remember_me else timedelta(minutes=60)

        refresh = RefreshToken.for_user(user)

        # Set the lifetimes
        refresh.set_exp(lifetime=refresh_token_lifetime)
        access = refresh.access_token
        access.set_exp(lifetime=access_token_lifetime)

        # Create response object
        response = Response({
            "access": str(access),
            "refresh": str(refresh),
        })

        access_expiry = datetime.now(UTC) + access_token_lifetime
        refresh_expiry = datetime.now(UTC) + refresh_token_lifetime

        # Ensure max_age is an integer
        access_max_age = int(access_token_lifetime.total_seconds())
        refresh_max_age = int(refresh_token_lifetime.total_seconds())

        response.set_cookie(
            key="access_token",
            value=str(access),
            expires=http_date(access_expiry.timestamp()),
            max_age=access_max_age,
            httponly=False,
            secure=False,
            samesite="None",
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            expires=http_date(refresh_expiry.timestamp()),
            max_age=refresh_max_age,
            httponly=False,
            secure=False,
            samesite="None",
        )

        return response


class ProfileViewSet(viewsets.ModelViewSet):
    """View for handling user profiles."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the profile for the current user.

        Returns:
            QuerySet: The profile for the current user.
        """
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            cache_key = f"profile_{user_id}"
            cached_profile = cache.get(cache_key)
            if cached_profile:
                logger.info(f"Profile for user {user_id} retrieved from cache")
                # Deserialize cached data back into queryset
                return Profile.objects.filter(user=self.request.user)

            queryset = self.queryset.filter(user=self.request.user)
            serialized_data = ProfileSerializer(queryset, many=True).data
            cache.set(cache_key, serialized_data, timeout=3600)
            logger.info(f"Profile for user {user_id} saved to cache")
            return queryset
        return self.queryset.none()

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the user profile.

        Args:
            request: The HTTP request containing the profile data.

        Returns:
            Response: A Response object containing the profile data.
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        user_id = self.request.user.id
        cache_key = f"profile_{user_id}"
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        Create the user profile.

        Args:
            serializer: The ProfileSerializer containing the profile data.
        """
        serializer.save(user=self.request.user)
        user_id = self.request.user.id
        cache_key = f"profile_{user_id}"
        cache.delete(cache_key)
        logger.info(f"Profile cache for user {user_id} invalidated")

    def perform_update(self, serializer):
        """
        Update the user profile.

        Args:
            serializer: The ProfileSerializer containing the updated profile data.
        """
        avatar = self.request.data.get(
            "avatar", "media/profile_images/default.jpg")
        serializer.save(user=self.request.user, avatar=avatar)
        user_id = self.request.user.id
        cache_key = f"profile_{user_id}"
        cache.delete(cache_key)
        logger.info(f"Profile cache for user {user_id} invalidated")

    def destroy(self, request, *args, **kwargs):
        """
        Delete the user profile.

        Args:
            request: The HTTP request to delete the profile.

        Returns:
            Response: A Response object with HTTP 204 status.
        """
        profile = self.get_object()
        user_id = profile.user.id
        profile.delete()
        cache_key = f"profile_{user_id}"
        cache.delete(cache_key)
        logger.info(f"Profile cache for user {user_id} invalidated")
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordResetRequestView(generics.GenericAPIView):
    """View for handling password reset requests."""

    serializer_class = PasswordResetRequestSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        """
        Request password reset.

        Args:
            request: The HTTP request containing the email for password reset.

        Returns:
            Response: A Response object with a message and HTTP status code 200 if successful,
                      or a Response object with HTTP status code 404 if the user is not found.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        # Find user with unique email
        user = get_object_or_404(User, email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{request.build_absolute_uri('/api/reset-password/confirm/')}{uid}/{token}/"

        send_mail(
            "Password Reset Requested",
            f"Click the link to reset your password: {reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({"message": "Password reset email has been sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, uidb64, token):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_object_or_404(User, pk=uid)

            if not default_token_generator.check_token(user, token):
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"success": "Password reset successfully."}, status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    """View for handling user logout."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logout user by blacklisting the refresh token.

        Args:
            request: The HTTP request containing the refresh token.

        Returns:
            Response: An object with HTTP status code 205 if successful,
                      or an object with HTTP status code 400 if the refresh token is invalid.
        """
        error_messages = {"missing_token": "Refresh token not provided",
                          "invalid_token": "Invalid refresh token"}

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"error": error_messages["missing_token"]}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": error_messages["invalid_token"]}, status=status.HTTP_400_BAD_REQUEST)


class ContactUsCreateView(generics.CreateAPIView):
    """View for handling contact us form submissions."""

    queryset = ContactUs.objects.all()
    serializer_class = ContactUsSerializer

    def get_serializer_context(self):
        """
        Add request context to serializer context.

        Returns:
            dict: The serializer context with the request added.
        """
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

    def perform_create(self, serializer):
        """
        Save contact inquiry with associated user if authenticated.

        Args:
            serializer: The serializer containing the contact inquiry data.
        """
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class PreferenceViewSet(viewsets.ModelViewSet):
    """View for handling user preferences."""

    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer

    # permission_classes = [IsAuthenticated]


class UserPreferenceViewSet(viewsets.ModelViewSet):
    """View for handling user preferences."""

    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the preferences for the current user.

        Returns:
            QuerySet: The preferences for the current user.
        """
        user_id = self.request.user.id
        cache_key = f"user_preferences_{user_id}"
        cached_preferences = cache.get(cache_key)
        if cached_preferences:
            logger.info(f"Preferences for user {user_id} retrieved from cache")
            return UserPreference.objects.filter(user=self.request.user)

        queryset = self.queryset.filter(user=self.request.user)
        serialized_data = UserPreferenceSerializer(queryset, many=True).data
        cache.set(cache_key, serialized_data, timeout=3600)
        logger.info(f"Preferences for user {user_id} saved to cache")
        return queryset

    def perform_create(self, serializer):
        """
        Save the user preference with the associated user.

        Args:
            serializer: The UserPreferenceSerializer containing the user preference data.
        """
        serializer.save(user=self.request.user)
        user_id = self.request.user.id
        cache_key = f"user_preferences_{user_id}"
        cache.delete(cache_key)
        logger.info(f"Preferences cache for user {user_id} invalidated")


class UserLikedRestaurantViewSet(viewsets.ModelViewSet):
    """View for handling user liked restaurants."""

    queryset = UserLikedRestaurant.objects.all()
    serializer_class = UserLikedRestaurantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Get the liked restaurants for the current user.

        Returns:
            QuerySet: The liked restaurants for the current user.
        """
        user_id = self.request.user.id
        cache_key = f"user_liked_restaurants_{user_id}"
        cached_liked_restaurants = cache.get(cache_key)
        if cached_liked_restaurants:
            logger.info(
                f"Liked restaurants for user {user_id} retrieved from cache")
            return UserLikedRestaurant.objects.filter(user=self.request.user)

        queryset = self.queryset.filter(user=self.request.user)
        serialized_data = UserLikedRestaurantSerializer(
            queryset, many=True).data
        cache.set(cache_key, serialized_data, timeout=3600)
        logger.info(f"Liked restaurants for user {user_id} saved to cache")
        return queryset

    def perform_create(self, serializer):
        """
        Save the liked restaurant with the associated user.

        Args:
            serializer: The UserLikedRestaurantSerializer containing the liked restaurant data.
        """
        serializer.save(user=self.request.user)
        user_id = self.request.user.id
        cache_key = f"user_liked_restaurants_{user_id}"
        cache.delete(cache_key)
        logger.info(f"Liked restaurants cache for user {user_id} invalidated")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def find_similar_users(request):
    """
    Find similar users based on preferences.

    Args:
        request: The HTTP request containing the user data.

    Returns:
        JsonResponse: A JSON response containing the similar users and their similarity scores.
    """
    # Get the current user.
    current_user = request.user

    # Set the user model.
    User = get_user_model()  # noqa: N806
    # Get all users.
    all_users = User.objects.exclude(id=current_user.id)

    # Get all preferences.
    all_preferences = get_all_preferences()

    # Get the current user vector.
    current_user_vector = user_preferences_to_vector(
        current_user, all_preferences)

    # Set an empty list for similar users.
    similar_users = []
    # Exclude the current user.
    all_users = User.objects.exclude(id=current_user.id)

    # For each user:
    for user in all_users:
        # Get the user vector.
        user_vector = user_preferences_to_vector(user, all_preferences)
        # Calculate the cosine similarity.
        similarity = calculate_cosine_similarity(
            current_user_vector, user_vector)

        # If the similarity is greater than 0:
        if similarity > 0:
            # Append the user email and similarity score to the similar users list.
            similar_users.append(
                {"email": user.email, "similarity": similarity})  # type: ignore

    # Sort the similar users by similarity score in descending order.
    similar_users = sorted(
        similar_users, key=operator.itemgetter("similarity"), reverse=True)

    # Return the similar users as a JSON response.
    return JsonResponse(similar_users, safe=False)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommend_restaurants(request):  # noqa: PLR0914
    """
    Recommend restaurants based on user preferences.

    Args:
        request: The HTTP request containing the user data.

    Returns:
        JsonResponse: A JSON response containing the recommended restaurants.
    """
    # Get the current user.
    current_user = request.user
    user_id = current_user.id
    cache_key = f"recommend_restaurants_{user_id}"
    cached_recommendations = cache.get(cache_key)
    if cached_recommendations:
        logger.info(f"Recommendations for user {user_id} retrieved from cache")
        return JsonResponse(cached_recommendations, safe=False)

    # Get all preferences.
    all_preferences = get_all_preferences()
    # Get the current user vector.
    current_user_vector = user_preferences_to_vector(
        current_user, all_preferences)

    # Ensure the request object is of the correct type.
    if not isinstance(request, HttpRequest):
        request = request._request  # noqa: SLF001

    # Set the user model.
    User = get_user_model()  # noqa: N806
    # Get all users.
    all_users = User.objects.exclude(id=current_user.id)

    # Set an empty list for similar users.
    similar_users = []

    # For each user:
    for user in all_users:
        # Get the user vector.
        user_vector = user_preferences_to_vector(user, all_preferences)
        # Calculate the cosine similarity.
        similarity = calculate_cosine_similarity(
            current_user_vector, user_vector)
        # If the similarity is greater than 0:
        if similarity > 0:
            similar_users.append(
                {"email": user.email, "similarity": similarity})  # type: ignore

    # Sort the similar users by similarity score in descending order.
    similar_users = sorted(
        similar_users, key=operator.itemgetter("similarity"), reverse=True)

    # Get all restaurants.
    all_restaurants = list(Restaurant.objects.values_list("id", flat=True))

    # Get the liked restaurants matrix.
    liked_matrix = get_liked_restaurants_matrix(similar_users, all_restaurants)

    # Calculate the restaurant scores.
    restaurant_scores = np.sum(liked_matrix, axis=0)

    # Get the top restaurant indices.
    # This is set to all restaurants for now.
    top_restaurant_indices = np.argsort(restaurant_scores)[::-1]

    # Set an empty list for recommendations.
    recommendations = []

    # For each sorted number and index in the top restaurant indices:
    for sort_order, idx in enumerate(top_restaurant_indices, start=1):
        # If the restaurant score is greater than 0:
        if restaurant_scores[idx] > 0:
            # Get the restaurant ID.
            restaurant_id = all_restaurants[idx]
            # Get the restaurant object.
            restaurant = Restaurant.objects.get(id=restaurant_id)

            # Append the restaurant data to the recommendations list.
            recommendations.append({
                "id": restaurant.id,  # type: ignore
                "name": restaurant.restaurant_name,
                "primary_cuisine": restaurant.primary_cuisine,
                "overall_rating": restaurant.overall_rating,
                "latitude": restaurant.latitude,
                "longitude": restaurant.longitude,
                "zone": restaurant.zone,
                "telephone": restaurant.telephone,
                "website": restaurant.website,
                "price": restaurant.price,
                "food_rating": restaurant.food_rating,
                "service_rating": restaurant.service_rating,
                "value_rating": restaurant.value_rating,
                "ambience_rating": restaurant.ambience_rating,
                "noise_level": restaurant.noise_level,
                "photo_url": restaurant.photo_url,
                "address": restaurant.address,
                "location_id": restaurant.location_id,
                "dress_code": restaurant.dress_code,
                "score": restaurant_scores[idx],
                "sort": sort_order,
            })

    cache.set(cache_key, recommendations, timeout=3600)
    logger.info(f"Recommendations for user {user_id} saved to cache")
    # Return the recommendations as a JSON response.
    return JsonResponse(recommendations, safe=False)


"""
TODO(RiinKal): not in use
class BookmarkViewSet(viewsets.ModelViewSet):
    View for handling user bookmarks.

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):  # noqa: ARG002, D417
        
        List all bookmarks for the current user.

        Args:
            request: The HTTP request containing the user data.

        Returns:
            Response: A Response object containing the bookmarks data.
        
        user = self.request.user
        user_id = user.id
        cache_key = f"bookmarks_{user_id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(
                f"Retrieved cached bookmarks for user {user_id} from cache")
            return Response(cached_data)

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        response_data = serializer.data
        cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour
        logger.info(f"Cached bookmarks for user {user_id}")
        return Response(response_data)

    def retrieve(self, request, *args, **kwargs):  # noqa: ARG002, D417
        
        Retrieve a bookmark.

        Args:
            request: The HTTP request containing the bookmark data.

        Returns:
            Response: A Response object containing the bookmark data.
        
        instance = self.get_object()
        cache_key = f"bookmark_{instance.id}"
        cached_data = cache.get(cache_key)
        if cached_data:
            logger.info(f"Retrieved cached bookmark {instance.id}")
            return Response(cached_data)

        serializer = self.get_serializer(instance)
        response_data = serializer.data
        cache.set(cache_key, response_data, timeout=3600)  # Cache for 1 hour
        logger.info(f"Cached bookmark {instance.id}")
        return Response(response_data)

    def get_queryset(self):
        
        Get the bookmarks for the current user.

        Returns:
            QuerySet: The bookmarks for the current user.
        
        user_id = self.get_user_id()
        if user_id:
            cached_bookmarks = cache.get(f"bookmarks_{user_id}")
            if cached_bookmarks:
                return Bookmark.objects.filter(user=self.request.user)

            queryset = self.queryset.filter(user=self.request.user).prefetch_related(
                "restaurants__positive_aspects")
            cache.set(f"bookmarks_{user_id}", list(queryset), timeout=3600)
            return queryset
        return self.queryset.none()

    def perform_create(self, serializer):
        
        Save the bookmark with the associated user.

        Args:
            serializer: The BookmarkSerializer containing the bookmark data.
        
        serializer.save(user=self.request.user)
        cache.delete(f"bookmarks_{self.request.user.id}")

    def perform_update(self, serializer):
        
        Update the bookmark.

        Args:
            serializer: The BookmarkSerializer containing the updated bookmark data.
        
        serializer.save(user=self.request.user)
        cache.delete(f"bookmarks_{self.request.user.id}")
        cache.delete(f"bookmark_{serializer.instance.id}")

    def perform_destroy(self, instance):
        
        Delete the bookmark.

        Args:
            instance: The Bookmark instance to delete.
        
        instance.delete()
        cache.delete(f"bookmarks_{instance.user.id}")
        cache.delete(f"bookmark_{instance.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_user_id(self) -> Optional[int]:
        Get the user ID if the user is authenticated.
        if self.request.user.is_authenticated:
            return self.request.user.id
        return None

"""
