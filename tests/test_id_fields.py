"""Test that implicit id fields are supported."""

from django.db import models

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer


def test_implicit_id_fields_works() -> None:
    """Test that implicit id fields are supported."""

    class ModelA(models.Model):
        name = models.CharField[str, str](max_length=100)

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig(
            model=ModelA,
            fields={
                "id": Infer,
                "name": Infer,
            },
        )

    openapi_schema = SchemaA.model_json_schema()
    assert openapi_schema["properties"]["id"]["type"] == "integer"
    assert openapi_schema["properties"]["name"]["type"] == "string"


def test_explicit_id_fields_works() -> None:
    """Test that explicit id fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "id": Infer,
                "name": Infer,
            },
        )

    openapi_schema = SchemaA.model_json_schema()
    assert openapi_schema["properties"]["id"]["type"] == "integer"
    assert openapi_schema["properties"]["name"]["type"] == "string"
