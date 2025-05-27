"""Utility functions for testing."""

import json
from pathlib import Path
from random import randint
from types import UnionType
from typing import TYPE_CHECKING, Annotated, Any, Union, cast, get_args, get_origin

import pydantic
from django.db import models
from django.db.models import Field, ForeignObjectRel
from pydantic.fields import FieldInfo

from django2pydantic import FieldTypeRegistry
from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import (
    GetType,
    Infer,
    SetType,
    SupportedPydanticTypes,
)

if TYPE_CHECKING:
    from django.contrib.contenttypes.fields import GenericForeignKey

DjangoField = models.Field[GetType, SetType]  # pyright: ignore [reportExplicitAny]

JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def debug_json(json_data: JSONValue) -> None:  # pragma: no cover
    """Print pretty the JSON value with indentation."""
    json_str: str = json.dumps(json_data)
    with Path("debug.json").open("w") as file:
        _ = file.write(json_str)


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
    model_name = f"TestModel{randint(0, 10000000)}"  # noqa: S311
    return cast("type[models.Model]", type(model_name, (models.Model,), attrs))


def pydantic_schema_from_field(
    field: Field[GetType, SetType],
) -> type[pydantic.BaseModel]:
    """Create a Pydantic model from a Django model field."""
    field_name: str
    model: type[models.Model]
    if hasattr(field, "model"):  # The field is already attached to a model
        field_name = field.name
        model = field.model
    else:
        field_name = "field"
        model = django_model_factory(fields={field_name: field})

    meta_class_attrs: SchemaConfig = SchemaConfig(  # type: ignore[type-arg]
        model=model,
        fields={field_name: Infer},
    )

    # Call get_fields() to cache model's fields, useful for testing due to dynamic
    # creation of fields during tests. Without this, the model's fields might appear
    # unavailable when accessed later through get_field() (not to be confused with the
    # plural one: get_fields()).
    _ = model._meta.get_fields()  # noqa: SLF001
    return cast(
        "type[pydantic.BaseModel]",
        type(
            "TestSchema",
            (BaseSchema,),
            {
                "config": meta_class_attrs,
            },
        ),
    )


def get_openapi_schema_from_field(
    field: Field[GetType, SetType],
) -> dict[str, Any]:  # pyright: ignore [reportExplicitAny]
    """Get the OpenAPI schema from a Django model field."""
    schema: type[pydantic.BaseModel] = pydantic_schema_from_field(field)
    return schema.model_json_schema()


def add_property_method(
    cls: type[models.Model],
    name: str,
    return_type: type,
    value: Any,  # pyright: ignore [reportExplicitAny, reportAny, reportUnusedParameter]  # noqa: ANN401, ARG001
) -> None:
    """Create a property method on the given class.

    Adds property method to the given class with the given name, return type, and value.

    Args:
        cls (type[models.Model]): The class to add the property method to.
        name (str): The name of the property method.
        return_type (type): The return type of the property method.
        value (Any): The value to return from the property method.

    """

    def property_method(self) -> Any:  # type: ignore[no-untyped-def]  # pyright: ignore [reportExplicitAny]  # noqa: ANN001, ANN401
        """Test method."""

    property_method.__annotations__["return"] = return_type

    setattr(cls, name, property(property_method))


def get_openapi_equivalent(python_native_type: Any) -> Any:  # noqa: ANN401, PLR0911  # pyright: ignore [reportExplicitAny]
    """Get the OpenAPI equivalent of the given Python native type."""
    if python_native_type is int:
        return "integer"
    if python_native_type is str:
        return "string"
    if python_native_type is float:
        return "number"
    if python_native_type is bool:
        return "boolean"
    if python_native_type == list[int]:
        return "array"
    if python_native_type == list[str]:
        return "array"
    if python_native_type == list[float]:
        return "array"
    if python_native_type == list[bool]:
        return "array"
    return "object"


def get_pydantic_type_and_fieldinfo(
    field: DjangoField,
) -> tuple[
    UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes], FieldInfo
]:  # pyright: ignore [reportExplicitAny]
    """Get the Pydantic field for a Django model field."""
    model_field: Field[Any, Any] | ForeignObjectRel | GenericForeignKey  # pyright: ignore [reportExplicitAny]
    if hasattr(field, "model"):  # The field is already attached to a model
        model_field = field
    else:
        field_name = "field"
        model: type[models.Model] = django_model_factory(fields={field_name: field})
        model_field = model._meta.get_field(field_name)  # noqa: SLF001  # pyright: ignore [reportUnknownMemberType, reportUnknownVariableType]  # pylint: disable=no-member

    handler = FieldTypeRegistry.instance().get_handler(model_field)  # pyright: ignore [reportUnknownArgumentType]
    return handler.get_pydantic_type(), handler.get_pydantic_field()


def get_first_non_null_type(openapi_field: dict[Any, Any]) -> dict[Any, Any]:  # pyright: ignore [reportExplicitAny]
    """Get the first non-null type from an 'anyOf' array in OpenAPI field's property.

    If the field has an 'anyOf' property, return the first item with type != 'null'.
    Otherwise, return the original field.

    Args:
        openapi_field: The OpenAPI field

    Returns:
        The first non-null type in 'anyOf' array or the original field
    """
    if "anyOf" in openapi_field:
        for item in openapi_field["anyOf"]:
            if item.get("type") != "null":
                return item  # type: ignore[no-any-return]
    return openapi_field


def has_null_type(openapi_field: dict[Any, Any]) -> bool:  # pyright: ignore [reportExplicitAny]
    """Check if the field has a null type in 'anyOf' array in OpenAPI field's property.

    Args:
        openapi_field: The OpenAPI field
    Returns:
        True if the field has a null type, False otherwise
    """
    if "anyOf" in openapi_field:
        for item in openapi_field["anyOf"]:
            if item.get("type") == "null":
                return True
    return False


def type_is_nullable(
    field_type: UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes],
) -> bool:
    """Check if the type is nullable (Union with None)."""
    if get_origin(field_type) in {Union, UnionType}:  # pyright: ignore [reportDeprecated]
        return type(None) in get_args(field_type)

    if get_origin(field_type) is Annotated:
        # Loop through all the arguments of the Annotated type
        for a in get_args(field_type):
            # Test nullability of the argument, continue if it's not
            if is_nullable := type_is_nullable(a):
                return is_nullable

    return False
