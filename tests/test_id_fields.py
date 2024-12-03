"""Test that implicit id fields are supported."""

from typing import ClassVar

from django.db import models
from pydantic.v1.fields import ModelField

from django2pydantic.schema import Schema
from django2pydantic.types import Infer


def test_implicit_id_fields_works() -> None:
    """Test that implicit id fields are supported."""

    class ModelA(models.Model):
        name = models.CharField(max_length=100)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelField] = {
                "id": Infer,
                "name": Infer,
            }

    openapi_schema = SchemaA.model_json_schema()
    assert openapi_schema["properties"]["id"]["type"] == "integer"
    assert openapi_schema["properties"]["name"]["type"] == "string"


def test_explicit_id_fields_works() -> None:
    """Test that explicit id fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelField] = {
                "id": Infer,
                "name": Infer,
            }

    openapi_schema = SchemaA.model_json_schema()
    assert openapi_schema["properties"]["id"]["type"] == "integer"
    assert openapi_schema["properties"]["name"]["type"] == "string"
