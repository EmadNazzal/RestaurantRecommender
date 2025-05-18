"""Serializers for user management models.

Serializers for user management models, including: RegistrationSerializer, LoginSerializer,
MyTokenObtainPairSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
PorfileSerializer, BookmarkSerializer, ContactUsSerializer,
PreferenceSerializer, UserPreferenceSerializer, and UserLikedRestaurantSerializer.

This module defines serializers for the user management application.
These serializers handle the conversion of model objects to JSON and vice versa, facilitating data transfer between the back-end and front-end.
"""

import re

# Django imports
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers  # type: ignore

# Django Rest Framework imports
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user_management.models import (  # type: ignore
    ContactUs,
    Preference,
    Profile,
    User,
    UserLikedRestaurant,
    UserPreference,
)
User = get_user_model()

EIGHT = 8
MAX_PREFERENCES = 9


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializes the registration user profile."""

    password_confirm = serializers.CharField(write_only=True)
    preferences = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Preference.objects.all(), write_only=True)

    class Meta:
        """
        Meta class for the RegistrationSerializer.

        Attributes:
            model (User): The User model.
            fields (list): The fields to include in the serialized output.
            extra_kwargs (dict): Additional keyword arguments for the fields.
        """

        model = User
        fields = ["id", "email", "first_name", "surname",
                  "password", "password_confirm", "preferences"]
        extra_kwargs = {
            "email": {"required": True},
            "password": {"write_only": True},
        }

    def validate(self, data):
        """Check that the passwords match and meet the password complexity requirements."""
        password = data.get("password")
        password_confirm = data.pop("password_confirm", None)
        preferences = data.get("preferences", [])

        if password != password_confirm:
            msg = "Passwords do not match."
            raise serializers.ValidationError(msg)

        if len(password) < EIGHT or not re.search(r"\d", password):
            msg = "Password must be at least 8 characters long and contain at least one digit."
            raise serializers.ValidationError(msg)

        if len(preferences) > MAX_PREFERENCES:
            msg = f"You can select a maximum of {MAX_PREFERENCES} preferences."
            raise serializers.ValidationError(msg)

        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages)) from e

        return data

    def create(self, validated_data):
        """Create a new user and assign preferences."""
        preferences = validated_data.pop("preferences", [])
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()

        # Create UserPreference instances
        for preference in preferences:
            UserPreference.objects.create(user=user, preference=preference)

        return user


class LoginSerializer(serializers.Serializer):
    """Serializes the user login object."""

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Check that the email and password are provided and are valid."""
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            msg = "Both email and password are required."
            raise serializers.ValidationError(msg)

        user = authenticate(email=email, password=password)
        if not user:
            msg = "Invalid email or password."
            raise serializers.ValidationError(msg)

        data["user"] = user
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializes the user login object."""

    username_field = "email"
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """Check that the email and password are provided and are valid."""
        credentials = {
            self.username_field: attrs.get(self.username_field),
            "password": attrs.get("password"),
        }

        if all(credentials.values()):
            user = authenticate(**credentials)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        _("User account is disabled"))
            else:
                raise serializers.ValidationError(
                    _("Invalid email or password"))
        else:
            raise serializers.ValidationError(
                _("Please enter email and a password"))

        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "surname": user.surname
            }
        }

        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializes the password reset request object."""

    email = serializers.EmailField()

    def validate_email(self, value):
        """Check if the email exists in the User model."""
        # Check if the email exists in the User model
        user = User.objects.filter(email=value).first()
        if not user:
            msg = "No user found with this email."
            raise serializers.ValidationError(msg)
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializes the password reset confirm object."""

    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        """Validate the new password using Django's built-in validators."""
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""

    class Meta:
        """
        Meta class for the ProfileSerializer.

        Attributes:
            model (Profile): The Profile model.
            fields (list): The fields to include in the serialized output.
            read_only_fields (list): The fields that are read-only.
        """

        model = Profile
        fields = ["id", "user", "first_name", "surname", "avatar", "slug"]
        read_only_fields = ["slug", "user"]

    def validate(self, data):
        """Ensure that the user is assigned correctly.

        This method should only handle validation, not assignment,
        as assignment is handled in the view.
        """
        return data


class ContactUsSerializer(serializers.ModelSerializer):
    """Serializer for the ContactUs model.

    This serializer is used to serialize the ContactUs model.
    It includes the user, name, email, subject, message, and created_at fields.
    """

    user = serializers.ReadOnlyField(source="user.email", required=False)

    class Meta:
        """Meta class for the ContactUsSerializer."""

        model = ContactUs
        fields = ["id", "user", "name", "email",
                  "subject", "message", "created_at"]

    def validate(self, data):
        """Ensure that the user is assigned correctly.

        This method should only handle validation, not assignment,
        as assignment is handled in the view.
        """
        if self.context["request"].user.is_authenticated:
            data["email"] = self.context["request"].user.email
            data["name"] = self.context["request"].user.get_full_name()
        elif "email" not in data or "name" not in data:
            msg = "Please enter name and an email address."
            raise serializers.ValidationError(msg)
        return data


class PreferenceSerializer(serializers.ModelSerializer):
    """Serializer for the Preference model."""

    class Meta:
        """Meta class for the PreferenceSerializer."""

        model = Preference
        fields = "__all__"


class UserPreferenceSerializer(serializers.ModelSerializer):
    """Serializer for the UserPreference model."""

    class Meta:
        """Meta class for the UserPreferenceSerializer."""
        model = UserPreference
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}

    def validate(self, data):
        """Ensure the user does not duplicate preferences."""
        user = self.context['request'].user
        preference = data.get("preference")
        if UserPreference.objects.filter(user=user, preference=preference).exists():
            raise serializers.ValidationError(
                "This preference already exists for the user.")
        return data


class UserLikedRestaurantSerializer(serializers.ModelSerializer):
    """Serializer for the UserLikedRestaurant model."""

    class Meta:
        """Meta class for the UserLikedRestaurantSerializer."""
        model = UserLikedRestaurant
        fields = "__all__"
        extra_kwargs = {'user': {'read_only': True}}

    def validate(self, data):
        """Ensure the user does not like the same restaurant multiple times."""
        user = self.context['request'].user
        restaurant = data.get("restaurant")
        if UserLikedRestaurant.objects.filter(user=user, restaurant=restaurant).exists():
            raise serializers.ValidationError(
                "This restaurant is already liked by the user.")
        return data


"""
class PositiveAspectSerializer(serializers.ModelSerializer):
    Serializes the positive aspects of a restaurant.

    class Meta:
        
        Meta class for the PositiveAspectSerializer.

        Attributes:
            model (Aspect): The Aspect model.
            fields (list): The fields to include in the serialized output.
        

        model = Aspect
        fields = ["aspect", "count"]
TODO(RiinKal): not in use
class BookmarkSerializer(serializers.ModelSerializer):
    Serializer for the Bookmark model.

    This serializer is used to serialize the Bookmark model.
    It includes the user and the restaurants associated with the bookmark.


    restaurants = RestaurantSerializerforBookmarks(many=True, read_only=True)
    restaurant_ids = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), many=True, write_only=True, source="restaurants"
    )

    class Meta:
        
        Meta class for the BookmarkSerializer.

        Attributes:
            model (Bookmark): The Bookmark model.
            fields (list): The fields to include in the serialized output.
            read_only_fields (list): The fields that are read-only.
        

        model = Bookmark
        fields = ["id", "user", "restaurants", "restaurant_ids"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        Create a new bookmark and assign restaurants.
        restaurant_ids = validated_data.pop("restaurants")
        bookmark = Bookmark.objects.create(**validated_data)
        bookmark.restaurants.set(restaurant_ids)
        return bookmark

    def update(self, instance, validated_data):
        Update an existing bookmark and assign restaurants.
        restaurant_ids = validated_data.pop("restaurants")
        instance.restaurants.set(restaurant_ids)
        return super().update(instance, validated_data)"""
