"""This file is used to configure the user_management app."""

from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    """User management app configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "user_management"
