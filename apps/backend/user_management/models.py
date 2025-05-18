# type: ignore
# to ignore assign type annotation error from linter
"""Models for user management including; CustomUserManager, User, Profile, Preferences, Preference, Userpreference, Userlikedpreference and ContactUs.

This module defines models for user management, including custom user models, profiles, preferences, userpreference, userlikedrestaurant and contact us.
It also includes functionality for creating and managing user accounts, profiles, and user-related data.

Typical usage example:

  user = User.objects.create_user(email='test@example.com', first_name='John', surname='Doe', password='password123')
  profile = Profile.objects.create(user=user, first_name='John', surname='Doe')
  contact = ContactUs.objects.create(name='John Doe', email='john@example.com', subject='Feedback', message='Great service!')
"""

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from user_management.tasks import resize_image


class CustomUserManager(BaseUserManager):
    """Custom user manager for creating and managing user accounts.

    Inherits from Django BaseUserManager to provide custom user account creation and management
    functionality.

    Attributes:
        use_in_migrations: Boolean indicating if the manager should be used in migrations.
    """

    def create_user(self, email, first_name, surname, password=None, **extra_fields):
        """Creates and saves a User with the given email, first name, surname, and password.

        Args:
            email: The email address of the user that user can login with.
            first_name: The first name of the user, that user has to provide when creating an account.
            surname: The surname of the user, that user has to provide when creating an account.
            password: The password for the user, that user will sign and and register with.
            **extra_fields: Additional fields for the user, that can be defined in front-end.

        Returns:
            The created user object.

        Raises:
            ValueError: If any of the required fields are not provided.
        """
        required_fields = {
            "email": "The Email field must be set",
            "first_name": "First name must be provided",
            "surname": "Surname must be provided",
            "password": "Password must be provided",
        }

        for field, error_message in required_fields.items():
            if not locals().get(field):
                raise ValueError(error_message)

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, surname, password=None, **extra_fields):
        """Creates and saves a Superuser with the email, first name, surname, and password.

        Args:
            email: The email address of the superuser, that is used to login and sign up with.
            first_name: The first name of the superuser, that is used to sign up with.
            surname: The surname of the superuser, that is used to sign up with.
            password: The password for the superuser, that is used to sign up and login with.
            **extra_fields: Additional fields for the superuser.

        Returns:
            The created superuser instance.

        Raises:
            ValueError: If is_staff or is_superuser are not set to True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        staff_error_message = "Superuser must have is_staff=True."
        superuser_error_message = "Superuser must have is_superuser=True."

        if extra_fields.get("is_staff") is not True:
            raise ValueError(staff_error_message)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(superuser_error_message)

        return self.create_user(email, first_name, surname, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model for custom user authentication and management.

    Inherits from Django AbstractBaseUser and PermissionsMixin to provide authentication and permissions functionality.

    Attributes:
        email: The email address of the user, that user will sign up and sign in with.
        first_name: The first name of the user, that is required to register with.
        surname: The surname of the user, that is required to register with.
        is_active: Boolean indicating if the user account is active, for administrative purposes.
        is_staff: Boolean indicating if the user is a staff member, to distinct between admin and a regular user.
        date_joined: The date and time when the user joined, for administrative purposes.
        last_login: The date and time when the user last logged in, for administrative purposes.
    """

    email = models.EmailField(verbose_name="Email", unique=True)
    first_name = models.CharField(verbose_name="First name", max_length=32)
    surname = models.CharField(verbose_name="Surname", max_length=32)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        verbose_name="Date joined", default=timezone.now)
    last_login = models.DateTimeField(
        verbose_name="Last login", blank=True, null=True)
    groups = models.ManyToManyField(
        Group, related_name="user_management_users")
    user_permissions = models.ManyToManyField(
        Permission, related_name="user_management_users")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "surname"]

    class Meta:
        """Meta class for the User model."""

        db_table = "user_management"
        verbose_name = "User"
        verbose_name_plural = "Users"
        indexes = [
            models.Index(fields=["email"]),
        ]

    def get_full_name(self) -> str:
        """Returns the user's full name."""
        return f"{self.first_name} {self.surname}".strip()

    def get_short_name(self) -> str:
        """Returns the user's first name."""
        return self.first_name


class Profile(models.Model):
    """
    Profile model to store additional user information.

    Attributes:
        user: One-to-One relationship with the User model defined earlier.
        first_name: The first name of the user, that is defined when user registers.
        surname: The surname of the user, that is stored and defined when user registers.
        avatar: The profile image of the user, that user can upload an image for.
        slug: A unique slug for the user's profile, to use in URLs to create human-readable and SEO-friendly links.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(
        verbose_name="First name", max_length=32, blank=True)
    surname = models.CharField(
        verbose_name="Surname", max_length=32, blank=True)
    avatar = models.ImageField(
        upload_to="profile_images", blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        """Meta class for the Profile model."""

        db_table = "user_profile"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        """String representation of the Profile model."""
        return f"Profile for {self.user.get_full_name()}"

    def save(self, *args, **kwargs):
        """Save method for the Profile model."""
        if not self.avatar:
            self.avatar = "profile_images/default.jpg"
        self.slug = slugify(self.user.get_full_name())
        super().save(*args, **kwargs)
        if self.avatar:
            # Check the type of resize_image
            print(f"resize_image type: {type(resize_image)}")
            # Ensure resize_image is a callable
            if callable(resize_image):
                resize_image.delay(self.avatar.path)
            else:
                print("resize_image is not callable")


class ContactUs(models.Model):
    """Contact Us model to store user and non-user feedback in the database.

    Attributes:
        user: ForeignKey relationship with the User model.
        name: The name of the person contacting.
        email: The email address of the person contacting.
        subject: The subject of the contact message.
        message: The contact message.
        created_at: The date and time when the message was created.
    """

    user = models.ForeignKey(User, null=True, blank=True,
                             on_delete=models.SET_NULL, verbose_name="User")
    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=500, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Created At")

    class Meta:
        """Meta class for the ContactUs model."""

        verbose_name = "Contact Us Inquiry"
        verbose_name_plural = "Contact Us Inquiries"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self):
        """String representation of the ContactUs model."""
        return self.subject


class Preference(models.Model):
    """Preference model for storing user preferences.

    Attributes:
        description: Description of the preference.
        type: Type of the preference, e.g. Cuisine, Price.
        is_selectable: Boolean indicating if the preference is selectable.
    """

    TYPE_CHOICES = (
        ("Cuisine", "Cuisine"),
        ("Price", "Price"),
    )
    description = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    is_selectable = models.BooleanField(default=True)

    class Meta:
        """Meta class for the Preference model."""
        indexes = [
            models.Index(fields=["type"]),
        ]

    def __str__(self):
        """String representation of the Preference model."""
        return f"{self.type}: {self.description}"


class UserPreference(models.Model):
    """UserPreference model for storing user preferences.

    Attributes:
        user: ForeignKey relationship with the User model.
        preference: ForeignKey relationship with the Preference model.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preferences")
    preference = models.ForeignKey(Preference, on_delete=models.CASCADE)

    class Meta:
        """Meta class for the UserPreference model."""

        unique_together = ("user", "preference")
        verbose_name_plural = "User Preferences"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["preference"]),
        ]

    def __str__(self):
        """String representation of the UserPreference model."""
        return f"{self.user.email} - {self.preference.description}"


class UserLikedRestaurant(models.Model):
    """UserLikedRestaurant model for storing liked restaurants by users.

    Attributes:
        user: ForeignKey relationship with the User model.
        restaurant: ForeignKey relationship with the Restaurant model.
        liked_date: The date and time when the restaurant was liked.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        "restaurant_recommender.Restaurant", on_delete=models.CASCADE)
    liked_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta class for the UserLikedRestaurant model."""

        unique_together = ("user", "restaurant")
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["restaurant"]),
        ]

    def __str__(self):
        """String representation of the UserLikedRestaurant model."""
        return f"{self.user.email} likes {self.restaurant.restaurant_name}"


class TimeStamp(models.Model):
    """TimeStamp model for user account audit and trial, growth tracking, and behavioral analysis.

    - TODO(RiinKal): Implement search algorithm

    """


"""

class Bookmark(models.Model):
    Preference/Bookmark for user to save preferences such as favorite primary cuisine, price range, etc.

    Attributes:
        user: One-To-One relationship with the User model.
        primary_cuisine: Preferred primary cuisine of the user.
        price: Preferred price range of the user.
        dress_code: Preferred dress code.
        positive_aspects: Preferred positive aspects of a restaurant.
        restaurants: Many-to-Many relationship with Restaurant model.
    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="preference_bookmark")
    primary_cuisine = models.CharField(max_length=255, null=True, blank=True)
    price = models.CharField(max_length=255, null=True, blank=True)
    dress_code = models.CharField(max_length=255, null=True, blank=True)
    positive_aspects = models.ManyToManyField(
        Aspect, related_name="bookmarks", blank=True)
    restaurants = models.ManyToManyField(
        Restaurant, related_name="bookmarks", blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        Meta class for the Bookmark model.

        db_table = "preference_bookmark"
        indexes = [
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        String representation of the Bookmark model.
        if self.id is None:
            return "PreferenceBookmark (unsaved instance)"
        return f"PreferenceBookmark {self.id} for {self.user.get_full_name()}"
"""
