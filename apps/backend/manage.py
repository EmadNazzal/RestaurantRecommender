#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line  # noqa: PLC0415
    except ImportError as exc:
        msg = (
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        )
        raise ImportError(msg) from exc

    # Ensure that the execute_from_command_line is called first
    execute_from_command_line(sys.argv)

    # Call the superuser command only if 'runserver' is in the arguments
    if "runserver" in sys.argv:
        try:
            from django.core.management import call_command  # noqa: PLC0415

            print("Running runserver command, attempting to create superuser...")
            call_command("superuser")
        except ValueError as e:
            print(f"Error creating superuser: {e!s}")


if __name__ == "__main__":
    main()
