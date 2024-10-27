"""Tooling to convert Django models and fields to Pydantic native models."""

from collections.abc import Callable
from typing import Any, ClassVar, TypeVar, override
from uuid import UUID

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from pydantic_core import PydanticUndefinedType

from superschema.handlers.base import PydanticConverter

SupportedParentFields = (
    models.Field[Any, Any]
    | models.ForeignObjectRel
    | GenericForeignKey
    | Callable[[], type[Any]]
)

TFieldType_co = TypeVar("TFieldType_co", bound=SupportedParentFields, covariant=True)

CallableOutput = TypeVar("CallableOutput", int, str, bool, UUID, float)
DefaultCallable = Callable[..., CallableOutput]

Undefined = PydanticUndefinedType


class FieldTypeRegistry:
    """Registry for Django field type handlers."""

    _instance: "ClassVar[FieldTypeRegistry | None]" = None

    @override
    def __init__(self) -> None:
        super().__init__()
        self.handlers: dict[
            type[SupportedParentFields],
            type[PydanticConverter[SupportedParentFields]],
        ] = {}

    @classmethod
    def instance(cls) -> "FieldTypeRegistry":
        """Return the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register(
        self,
        handler_class: type[PydanticConverter[SupportedParentFields]],
    ) -> None:
        """Register a handler class for a Django field class."""
        self.handlers[handler_class.field()] = handler_class

    def get_handler(
        self,
        field: SupportedParentFields,
    ) -> PydanticConverter[SupportedParentFields]:
        """Get the handler for a Django field."""
        # Primarily use a handler that is registered for the exact Django field class:
        for django_field_class, type_handler in self.handlers.items():
            if type(field) is django_field_class:
                return type_handler(field)

        # Secondary, use a handler that is registered for a superclass of the Django field class:
        # for django_field_class, type_handler in self.handlers.items():
        #    if issubclass(type(field), django_field_class):
        #        return type_handler(field)

        msg = (
            f"No handler registered for {field} for Django field type {type(field)}. "
            f"Currently registered handlers are for: {self.handlers}"
        )
        raise ValueError(msg)
