from django.db import models

from django2pydantic import BaseSchema, Infer
from django2pydantic.schema import SchemaConfig


def test_schema_with_jsonfield_should_accept_python_object() -> None:
    """Python object should not raise validation error."""

    class ModelA(models.Model):
        config = models.JSONField(default=dict)

    class SchemaA(BaseSchema[ModelA]):  # pylint: disable=too-few-public-methods
        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "config": Infer,
            },
        )

    _ = SchemaA(config={"name": "test"})
    _ = SchemaA(config=["test", 1, 2.0, True, None])
    _ = SchemaA(config="123")
    _ = SchemaA(config=123)
    _ = SchemaA(config=123.0)
    _ = SchemaA(config=True)
