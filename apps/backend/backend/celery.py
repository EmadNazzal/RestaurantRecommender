"""Celery configuration file."""

import os

from celery import Celery  # type: ignore
from celery.schedules import crontab  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
app = Celery("backend")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(["restaurant_recommender", "user_management"])


@app.task(bind=True)
def debug_task(self):
    """Debug task to print request information."""
    print(f"Request: {self.request!r}")


app.conf.beat_schedule = {
    "fetch-weather-data-every-6-hours": {
        "task": "restaurant_recommender.tasks.fetch_weather_data",
        # Fetch weather data every 6 hours
        "schedule": crontab(minute=0, hour="*/6"),  # type: ignore
    },
    "load-prediction-model-every-hour": {
        "task": "restaurant_recommender.tasks.load_prediction_model",
        # Load prediction model every hour
        "schedule": crontab(minute=0, hour="*/1"),  # type: ignore
    },
    "resize-images-every-1-hour": {
        "task": "user_management.tasks.resize_image",
        # Resize images every hour
        "schedule": crontab(minute=0, hour="*/1"),  # type: ignore
        "args": ("media/profile_images/default.jpg",),

    },
    "delete-old-avatars-every-6-hours": {
        "task": "user_management.tasks.delete_old_avatar",
        # Delete old avatars every 6 hours
        "schedule": crontab(minute=0, hour="*/6"),  # type: ignore
        # Include the image path here
        "args": ("media/profile_images/default.jpg",),

    },
    "cleanup-old-preferences-every-day": {
        "task": "user_management.tasks.cleanup_old_preferences",
        # Cleanup old preferences every day at midnight
        "schedule": crontab(minute=0, hour=0),  # type: ignore
    },
    "cleanup-old-contact-us-every-day": {
        "task": "user_management.tasks.cleanup_old_contact_us",
        # Cleanup old contact-us entries every day at midnight
        "schedule": crontab(minute=0, hour=0),  # type: ignore
    },
    "cleanup-old-liked-restaurants-every-day": {
        "task": "user_management.tasks.cleanup_old_liked_restaurants",
        # Cleanup old liked restaurants every day at midnight
        "schedule": crontab(minute=0, hour=0),  # type: ignore
    },
    "deactivate-inactive-users-every-day": {
        "task": "user_management.tasks.deactivate_inactive_users",
        # Deactivate inactive users every day at midnight
        "schedule": crontab(minute=0, hour=0),  # type: ignore
    },
    "cleanup-old-logs-every-day": {
        "task": "restaurant_recommender.tasks.cleanup_old_logs",
        # Cleanup old logs every day at midnight
        "schedule": crontab(minute=0, hour=0),  # type: ignore
    },
    "clear-cache-every-hour": {
        "task": "restaurant_recommender.tasks.clear_cache",
        # Clear cache every hour
        "schedule": crontab(minute=0, hour="*/1"),  # type: ignore
    },
}
