"""This sets up the Django environment for testing purposes.

It configures the Django settings module and initializes Django.
This is useful for running tests or scripts that require Django's ORM and other features.
"""

import os

import django
from django.conf import settings


def setup_django_environment() -> None:
    """Set up the Django environment for testing."""
    # Only setup Django if it hasn't been configured yet
    if not settings.configured:
        # Set the default settings module for Django
        _: str = os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
        # Setup Django
        django.setup()
