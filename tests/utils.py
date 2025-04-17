"""Utility functions for testing."""

import json
from pathlib import Path
from random import randint
from typing import Any, cast

import pydantic
from django.db import models

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import GetType, Infer, ModelFields, SetType

DjangoField = models.Field[GetType, SetType]  # pyright: ignore [reportExplicitAny]

JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def debug_json(json_data: JSONValue) -> None:  # pragma: no cover
    """Print pretty the JSON value with indentation."""
    json_str: str = json.dumps(json_data)
    # print_json(data=json_str, indent=4)
    with Path("debug.json").open("w") as file:
        file.write(json_str)


def django_model_factory(
    fields: dict[str, DjangoField],
) -> type[models.Model]:
    """Create a Django model with the given fields."""
    meta_attrs: dict[str, str] = {
        "app_label": "tests",
    }

    attrs = {
        "__module__": "django.db.models",
        **fields,
        "Meta": type("Meta", (), meta_attrs),
    }
    model_name = f"TestModel{randint(0, 10000000)}"
    return cast(type[models.Model], type(model_name, (models.Model,), attrs))


def pydantic_schema_from_field(field: DjangoField) -> type[pydantic.BaseModel]:
    """Create a Pydantic model from a Django model field."""
    field_name = "field"
    model: type[models.Model] = django_model_factory(fields={field_name: field})
    fields_def: ModelFields = {field_name: Infer}
    meta_class_attrs: SchemaConfig = SchemaConfig(  # type: ignore[type-arg]
        model=model,
        fields=fields_def,
    )

    return cast(
        type[pydantic.BaseModel],
        type(
            "TestSchema",
            (BaseSchema,),
            {
                "config": meta_class_attrs,
            },
        ),
    )


def get_openapi_schema_from_field(field: DjangoField) -> dict[str, Any]:
    """Get the OpenAPI schema from a Django model field."""
    schema: type[pydantic.BaseModel] = pydantic_schema_from_field(field)
    return schema.model_json_schema()


def add_property_method(
    cls: type[models.Model],
    name: str,
    return_type: type,
    value: Any,  # pyright: ignore [reportExplicitAny, reportAny, reportUnusedParameter]
) -> None:
    """Create a property method on the given class.

    Adds a property method to the given class with the given name, return type, and value.

    Args:
        cls (type[models.Model]): The class to add the property method to.
        name (str): The name of the property method.
        return_type (type): The return type of the property method.
        value (Any): The value to return from the property method.

    """

    def property_method(self) -> Any:  # type: ignore[no-untyped-def]  # pyright: ignore [reportExplicitAny]
        """Test method."""

    property_method.__annotations__["return"] = return_type

    setattr(cls, name, property(property_method))


def get_openapi_equivalent(python_native_type: Any) -> Any:
    """Get the OpenAPI equivalent of the given Python native type."""
    if python_native_type == int:
        return "integer"
    if python_native_type == str:
        return "string"
    if python_native_type == float:
        return "number"
    if python_native_type == bool:
        return "boolean"
    if python_native_type == list[int]:
        return "array"
    if python_native_type == list[str]:
        return "array"
    if python_native_type == list[float]:
        return "array"
    if python_native_type == list[bool]:
        return "array"
