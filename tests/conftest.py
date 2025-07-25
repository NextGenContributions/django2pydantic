"""Pytest configuration file."""

import django_stubs_ext
import pytest
from _pytest.config import Config
from _pytest.fixtures import SubRequest
from django import setup
from django.apps import apps
from django.conf import settings
from hypothesis import settings as hypothesis_settings

django_stubs_ext.monkeypatch()

# Disable Hypothesis deadline to avoid issues with long-running tests
hypothesis_settings.register_profile("no_timing", deadline=None)
hypothesis_settings.load_profile("no_timing")


def pytest_configure(
    config: Config,  # noqa: ARG001
) -> None:
    """Configure Django settings for pytest."""
    settings.configure(
        ALLOWED_HOSTS=["*"],
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
        },
        SITE_ID=1,
        SECRET_KEY="not very secret in tests",  # noqa: S106
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "DIRS": [],
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
        ],
        MIDDLEWARE=(
            "django.middleware.security.SecurityMiddleware",
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
            "django.contrib.messages.middleware.MessageMiddleware",
            "django.middleware.clickjacking.XFrameOptionsMiddleware",
        ),
        INSTALLED_APPS=(
            "django.contrib.admin",
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "tests",
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
        AUTHENTICATION_BACKENDS=("django.contrib.auth.backends.ModelBackend",),
        LANGUAGE_CODE="en-us",
        TIME_ZONE="UTC",
    )

    setup()


@pytest.fixture(autouse=True)
def teardown_after_each_test(request: SubRequest) -> None:
    """Clear cached django models to avoid issue with reusing model name."""

    def clear_django_models_cache() -> None:
        test_app = apps.get_app_config("tests")
        test_app.models.clear()

    request.addfinalizer(clear_django_models_cache)  # noqa: PT021
