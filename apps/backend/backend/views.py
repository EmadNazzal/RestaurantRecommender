"""
This is the main view for the backend app.

It returns a simple "Hello, world!" to indicate that the app is running, and the backend is set up
correctly.
"""

from django.http import HttpResponse


def home(request):  # noqa: ARG001
    """Main view for the backend app."""
    return HttpResponse("Hello, world!")
