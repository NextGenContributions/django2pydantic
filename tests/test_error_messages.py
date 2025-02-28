"""Test error messages."""

import pytest
from django.db import models

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer


def test_defing_a_non_existing_field_raises_exception() -> None:
    """Test that an exception is raised when an included field is not found."""
    with pytest.raises(AttributeError):  # noqa: PT012

        class ModelA(models.Model):  # noqa: DJ008
            id = models.AutoField[int, int](primary_key=True)

        class SchemaA(BaseSchema[ModelA]):
            """SchemaA class."""

            config = SchemaConfig(
                model=ModelA,
                fields={
                    "non_existing_field": Infer,
                },
            )
