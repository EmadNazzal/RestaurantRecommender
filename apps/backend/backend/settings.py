"""
Django settings for backend project.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/

For quick-start development, see
https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Environment Variables ---

# Load environment variables from a .env.local file. .env.local
env_path = (BASE_DIR / "../../local.env").resolve()
print(f"Checking for env file at: {env_path}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print("No .env.local file found. Skipping...")

# CONFIGCAT_SDK_KEY = os.getenv('CONFIGCAT_SDK_KEY')
# print(f"CONFIGCAT_SDK_KEY: {CONFIGCAT_SDK_KEY}")

# Django environment variables.
DJANGO_SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "default_secret_key")
DJANGO_SUPERUSER_EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL", "default_email")
DJANGO_SUPERUSER_PASSWORD = os.getenv(
    "DJANGO_SUPERUSER_PASSWORD", "default_password")
DJANGO_SUPERUSER_FIRST_NAME = os.getenv(
    "DJANGO_SUPERUSER_FIRST_NAME", "default_first_name")
DJANGO_SUPERUSER_SURNAME = os.getenv(
    "DJANGO_SUPERUSER_SURNAME", "default_surname")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "your-default-secret-key")

# Postgres environment variables.
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

print("Database Name:", POSTGRES_DB)
print("Database User:", POSTGRES_USER)

# --- Basic Settings ---

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv("DEBUG", "False") == "True"
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Example to print the DEBUG value to ensure it's set correctly
print("DEBUG:", DEBUG)

HOST = os.getenv("HOST", "localhost")
ALLOWED_HOSTS = ["*"]

# --- Application Definition ---

INSTALLED_APPS = [
    "corsheaders",
    "custom_commands",
    "debug_toolbar",
    "django_celery_beat",
    "django_celery_results",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "rest_framework_simplejwt.token_blacklist",
    "rest_framework_simplejwt",
    "rest_framework",
    "restaurant_recommender",
    "user_management",
]

# --- Middleware ---

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.cache.UpdateCacheMiddleware",
    "django.middleware.cache.FetchFromCacheMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

# --- URL Configuration ---

ROOT_URLCONF = "backend.urls"
INTERNAL_IPS = [
    "127.0.0.1",
]

# --- Template Configuration ---

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# --- WSGI Configuration ---

WSGI_APPLICATION = "backend.wsgi.application"

# --- Database Configuration ---
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


if all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    print("Using PostgreSQL")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_DB,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": 'db',
            "PORT": 5432,
            # Keep connections open for 600 seconds (10 minutes) for connection spooling.
            "CONN_MAX_AGE": 600,
        }
    }

# else:
#     print("Using SQLite")
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             # "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }

# --- Password Validation ---
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# --- Internationalization ---
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static and Media Files ---
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static/"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# --- Cookies ---

# Set the default session expiration to two weeks, for "remember me" option.
SESSION_COOKIE_AGE = 1209600  # 14 days in seconds.
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS in production.
# Allow JavaScript access to the cookie
SESSION_COOKIE_HTTPONLY = False
# Works for most cases without cross-site issues.
SESSION_COOKIE_SAMESITE = "None"


# --- REST Framework ---

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    # Uncomment these lines if you want to enable throttling
    # TODO(RiinKal): disabling throttling rules for development
    # "DEFAULT_THROTTLE_CLASSES": [
    #     "rest_framework.throttling.AnonRateThrottle",
    #     "rest_framework.throttling.UserRateThrottle",
    # ],
    # "DEFAULT_THROTTLE_RATES": {
    #     "anon": "100/hour",  # 100 requests per hour for anonymous users.
    #     "user": "1000/hour",  # 1000 requests per hour for authenticated users.
    # },
}


# --- JWT Settings ---

# This setup will enforce authentication for all endpoints that are covered by these default settings,
# requiring users to provide valid credentials (username and password) to access protected resources.
SIMPLE_JWT = {
    # Default values, these can be overridden in view.py
    # TODO(RiinKal): have to modify these for remember me functionality
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SIGNING_KEY": SECRET_KEY,
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# --- Email Configuration ---

# Gmail SMTP email service configuration for password reset with email confirmation
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS') == 'True'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

# --- Cache Configuration ---

# Optional: This is to ensure Django sessions are stored in Redis.
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

# --- Celery Configuration ---

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_TIMEZONE = "UTC"
CELERY_IMPORTS = (
    "restaurant_recommender.tasks",
    "user_management.tasks",
)
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# --- CORS Configuration ---

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# --- CRSF Configuration ---

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]

# --- Logging Configuration ---

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/django.log",
            "formatter": "standard",
        },
        "celery_worker": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/celery_worker.log",
            "formatter": "standard",
            # 5 MB
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
        },
        "celery_beat": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": BASE_DIR / "logs/celery_beat.log",
            "formatter": "standard",
            # 5 MB
            "maxBytes": 1024 * 1024 * 5,
            "backupCount": 5,
        },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["default", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "celery.worker": {
            "handlers": ["celery_worker", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "celery.beat": {
            "handlers": ["celery_beat", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# --- Model Configuration ---
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

AUTH_USER_MODEL = "user_management.User"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Drivers Configuration ---

# TODO(RiinKal): add chrome and edge driver
# SELENIUM_DRIVER_OPTS = {"executable_path": "/path/to/chromedriver", "options": {"profile": "/path/to/custom/profile"}}
