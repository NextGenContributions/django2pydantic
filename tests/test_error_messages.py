"""Test error messages."""

from typing import ClassVar

import pytest
from django.db import models

from django2pydantic.schema import django2pydantic
from django2pydantic.types import Infer, ModelFields


def test_defing_a_non_existing_field_raises_exception() -> None:
    """Test that an exception is raised when an included field is not found."""
    with pytest.raises(AttributeError):  # noqa: PT012

        class ModelA(models.Model):  # noqa: DJ008
            id = models.AutoField(primary_key=True)

        class SchemaA(django2pydantic):
            """SchemaA class."""

            class Meta(django2pydantic.Meta):
                """Meta class."""

                model = ModelA
                fields: ClassVar[ModelFields] = {
                    "non_existing_field": Infer,
                }
