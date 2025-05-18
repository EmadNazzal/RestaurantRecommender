"""This module is the entry point for the Django application."""
from __future__ import absolute_import, unicode_literals
from backend.celery import app as celery_app

__all__ = ('celery_app',)


# pylint: disable=unused-import
