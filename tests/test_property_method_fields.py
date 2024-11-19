"""Test property method based fields."""

from typing import Any, ClassVar

import pytest
from django.db import models

from django2pydantic.schema import Schema
from django2pydantic.types import Infer, ModelFields
from tests.utils import add_property_method, debug_json, get_openapi_equivalent

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
        id = models.AutoField(primary_key=True)

    add_property_method(
        cls=ModelA,
        name=property_name,
        return_type=return_type,
        value="test",
    )

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                property_name: Infer,
            }

    openapi_schema = SchemaA.model_json_schema()
    debug_json(openapi_schema)
    assert openapi_schema["properties"][property_name][
        "type"
    ] == get_openapi_equivalent(python_native_type=return_type)
