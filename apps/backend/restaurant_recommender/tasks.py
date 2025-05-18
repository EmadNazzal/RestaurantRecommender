"""Celery tasks for loading the prediction model and fetching weather data."""

import pickle  # noqa: S403
from datetime import timedelta, datetime

import requests  # type: ignore
from celery import shared_task  # type: ignore
from celery.utils.log import get_task_logger  # type: ignore
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
import subprocess
import os

from restaurant_recommender.models import PredictionModel, WeatherData  # type: ignore

logger = get_task_logger(__name__)

# Ensure LOG_DIR is set correctly based on your settings
LOG_DIR = getattr(settings, 'LOG_DIR', str(settings.BASE_DIR / 'logs'))
RETENTION_DAYS = 30


@shared_task(bind=True, max_retries=3)
def cleanup_old_logs(self):
    """Remove log files older than the retention period."""
    try:
        now = datetime.now()
        if not os.path.exists(LOG_DIR):
            logger.warning(f"Log directory {LOG_DIR} does not exist.")
            return

        for filename in os.listdir(LOG_DIR):
            file_path = os.path.join(LOG_DIR, filename)
            if os.path.isfile(file_path):
                file_mtime = datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if now - file_mtime > timedelta(days=RETENTION_DAYS):
                    os.remove(file_path)
                    logger.info(f"Deleted old log file: {file_path}")
    except Exception as e:
        logger.exception(f"Error during cleanup_old_logs: {e}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def backup_database(self):
    """Backup the database."""
    try:
        backup_dir = "/path/to/backup/directory"
        os.makedirs(backup_dir, exist_ok=True)
        db_name = settings.DATABASES['default']['NAME']
        backup_file = os.path.join(
            backup_dir, f"db_backup_{db_name}_{timezone.now().strftime('%Y%m%d%H%M%S')}.sql")
        command = f"pg_dump -U {settings.DATABASES['default']['USER']} -F c {db_name} > {backup_file}"
        subprocess.run(command, shell=True, check=True)
        print(f"Database backed up successfully to {backup_file}")
    except Exception as e:
        logger.exception(f"Error during backup_database: {e}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def clear_cache(self):
    """Clear the entire cache."""
    try:
        cache.clear()
        print("Cache cleared successfully.")
    except Exception as e:
        logger.exception(f"Error during clear_cache: {e}")
        self.retry(exc=e, countdown=60)


@shared_task(bind=True, max_retries=3)
def load_prediction_model(self):
    """Load the prediction model from the database and save it to the cache."""
    try:
        # Attempt to get the model from the cache
        model = cache.get("prediction_model")
        if model:
            logger.info("Prediction model retrieved from cache")
            return  # Exit early if the model was retrieved from the cache

        # Load the prediction model
        prediction_model = PredictionModel.objects.filter(
            is_active=True).latest("updated_at")
        logger.info(f"Prediction model loaded: {prediction_model.model_name}")

        # Ensure the pickle_file is not None or empty
        if not prediction_model.pickle_file:
            logger.warning("Warning: pickle_file is None or empty")
            return

        model = pickle.loads(prediction_model.pickle_file)  # noqa: S301
        logger.info("Prediction model successfully loaded from pickle")

        # Save the model to cache
        cache.set("prediction_model", model, timeout=3600)
        logger.info("Prediction model saved to cache")
    except PredictionModel.DoesNotExist:
        logger.exception("No active prediction model found.")
    except Exception:
        logger.exception("Error during model loading")
        self.retry(countdown=60)


@shared_task(bind=True, max_retries=3)
def fetch_weather_data(self):
    """Fetch weather data from the Open-Meteo API and store it in the database."""
    api_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 40.7831,  # Latitude for Manhattan
        "longitude": -73.9712,  # Longitude for Manhattan
        "hourly": "temperature_2m,dewpoint_2m,precipitation",
    }

    try:
        logger.info("Sending request to weather API.")
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info("API response received successfully.")

        if "hourly" in data:
            hourly_data = data["hourly"]
            temperature = hourly_data.get("temperature_2m", [None])[0]
            dewpoint = hourly_data.get("dewpoint_2m", [None])[0]
            precipitation = hourly_data.get("precipitation", [None])[0]

            if {temperature, dewpoint, precipitation} != {None}:
                logger.info(
                    f"Fetched weather data: temperature={temperature}, dewpoint={dewpoint}, precipitation={precipitation}"
                )

                weather = WeatherData.objects.create(
                    temperature=temperature,
                    dewpoint=dewpoint,
                    precipitation=precipitation,
                    # Use timezone-aware datetime
                    timestamp=timezone.now(),
                )
                # TODO: id is not used, consider removing this line.
                logger.info(
                    f"Weather data stored in the database with id={weather.id}")

                # Cache the weather data for 6 hours (21600 seconds), open-meteo forecast is updated in every 6 hours
                cache.set("temperature", temperature, timeout=21600)
                cache.set("dewpoint", dewpoint, timeout=21600)
                cache.set("precipitation", precipitation, timeout=21600)

                # Clean up old weather data from database after 7 days
                threshold_date = timezone.now() - timedelta(days=7)
                WeatherData.objects.filter(
                    timestamp__lt=threshold_date).delete()
                logger.info("Old weather data deleted from the database.")

                return temperature, dewpoint, precipitation
            logger.error("Expected keys are missing in the 'hourly' data.")
            return None, None, None
        logger.error("'hourly' key is missing in the response.")
        return None, None, None  # noqa: TRY300

    except requests.exceptions.RequestException:
        logger.exception("Error fetching weather data")
        self.retry(countdown=60)  # Retry after 60 seconds
        return None, None, None
    except ValueError:
        logger.exception("ValueError")
        return None, None, None
    except Exception:
        logger.exception("Unexpected error")
        self.retry(countdown=60)  # Retry after 60 seconds
        return None, None, None
