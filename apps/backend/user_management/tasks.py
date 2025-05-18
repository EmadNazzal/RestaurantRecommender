"""Celery tasks for user management."""

from datetime import timedelta
from pathlib import Path

from celery import shared_task  # type: ignore
from django.utils import timezone
from PIL import Image

IMAGE_MAX_SIZE = 300


@shared_task(bind=True, max_retries=3)
def resize_image(self, image_path):
    """Resize the image to the specified max size."""
    try:
        img = Image.open(image_path)
        if img.height > IMAGE_MAX_SIZE or img.width > IMAGE_MAX_SIZE:
            output_size = (IMAGE_MAX_SIZE, IMAGE_MAX_SIZE)
            img.thumbnail(output_size)
            img.save(image_path)
            print(f"Image resized: {image_path}")
    except FileNotFoundError:
        print(f"File not found: {image_path}")
    except ValueError as e:
        print(f"Error processing image: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds


@shared_task(bind=True, max_retries=3)
def delete_old_avatar(self, image_path):
    """Delete old avatar image."""
    try:
        image_path = Path(image_path)
        if image_path.is_file() and image_path != Path("profile_images/default.jpg"):
            image_path.unlink()
            print(f"Deleted old image: {image_path}")
    except FileNotFoundError as e:
        print(f"Error deleting image: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds


@shared_task(bind=True, max_retries=3)
def cleanup_old_preferences(self):
    """Remove old bookmarks from database after 6 months."""
    try:
        from user_management.models import UserPreference   # noqa: PLC0415

        threshold_date = timezone.now() - timedelta(days=180)
        old_bookmarks = UserPreference.objects.filter(
            last_accessed__lt=threshold_date)
        old_bookmarks_count = old_bookmarks.count()
        old_bookmarks.delete()
        return f"Deleted {old_bookmarks_count} old preferences."  # noqa: TRY300
    except ValueError as e:
        print(f"Error cleaning up old preferences: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds


@shared_task(bind=True, max_retries=3)
def cleanup_old_liked_restaurants(self):
    """Remove old liked restaurants from database after a certain period."""
    try:
        from user_management.models import UserLikedRestaurant  # noqa: PLC0415

        threshold_date = timezone.now() - timedelta(days=180)  # Adjust the period as needed
        old_liked_restaurants = UserLikedRestaurant.objects.filter(
            last_accessed__lt=threshold_date)
        old_liked_restaurants_count = old_liked_restaurants.count()
        old_liked_restaurants.delete()
        return f"Deleted {old_liked_restaurants_count} old liked restaurants."
    except ValueError as e:
        print(f"Error cleaning up old liked restaurants: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds


@shared_task(bind=True, max_retries=3)
def cleanup_old_contact_us(self):
    """Remove old contact us inquiries from database after 1 year."""
    try:
        from user_management.models import ContactUs  # noqa: PLC0415

        threshold_date = timezone.now() - timedelta(days=365)
        old_inquiries = ContactUs.objects.filter(created_at__lt=threshold_date)
        old_inquiries_count = old_inquiries.count()
        old_inquiries.delete()
        return f"Deleted {old_inquiries_count} old contact inquiries."  # noqa: TRY300
    except ValueError as e:
        print(f"Error cleaning up old contact inquiries: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds


@shared_task(bind=True, max_retries=3)
def deactivate_inactive_users(self):
    """Deactivate user accounts that have been inactive for a certain period."""
    try:
        from user_management.models import User  # noqa: PLC0415

        threshold_date = timezone.now() - timedelta(days=365)
        inactive_users = User.objects.filter(
            last_login__lt=threshold_date, is_active=True)
        inactive_users_count = inactive_users.count()
        inactive_users.update(is_active=False)
        return f"Deactivated {inactive_users_count} inactive users."
    except Exception as e:
        print(f"Error deactivating inactive users: {e}")
        self.retry(exc=e, countdown=60)  # Retry after 60 seconds
