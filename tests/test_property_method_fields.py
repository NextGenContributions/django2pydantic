"""Test property method based fields."""

from typing import Any

import pytest
from django.db import models

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer
from tests.utils import add_property_method, get_openapi_equivalent

BasicTypes = [
    int,
    str,
    float,
    bool,
    list[int],
    list[str],
    list[float],
    list[bool],
]


@pytest.mark.parametrize("return_type", BasicTypes)
def test_django_model_property_methods_are_supported(return_type: Any) -> None:
    property_name = "some_property"

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)

    add_property_method(
        cls=ModelA,
        name=property_name,
        return_type=return_type,
        value="test",
    )

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig(
            model=ModelA,
            fields={
                property_name: Infer,
            },
        )

    openapi_schema = SchemaA.model_json_schema()
    assert openapi_schema["properties"][property_name][
        "type"
    ] == get_openapi_equivalent(python_native_type=return_type)
