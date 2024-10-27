"""Tests for UUID fields."""

import uuid

from django.db import models

from tests.utils import get_openapi_schema_from_field


def test_uuid_field_is_supported() -> None:
    """Test that UUID fields are supported."""
    openapi_schema = get_openapi_schema_from_field(models.UUIDField())
    assert openapi_schema["properties"]["field"]["type"] == "string"
    assert openapi_schema["properties"]["field"]["format"] == "uuid"


def test_uuid1_field_is_supported() -> None:
    """Test that UUID fields are supported."""
    openapi_schema = get_openapi_schema_from_field(models.UUIDField(default=uuid.uuid1))
    assert openapi_schema["properties"]["field"]["type"] == "string"
    assert openapi_schema["properties"]["field"]["format"] == "uuid1"


def test_uuid4_field_is_supported() -> None:
    """Test that UUID fields are supported."""
    openapi_schema = get_openapi_schema_from_field(models.UUIDField(default=uuid.uuid4))
    assert openapi_schema["properties"]["field"]["type"] == "string"
    assert openapi_schema["properties"]["field"]["format"] == "uuid4"
