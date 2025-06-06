"""Tooling to convert Django models and fields to Pydantic native models."""

import logging
from collections.abc import Callable
from typing import ClassVar, TypeVar, override
from uuid import UUID

from django.db.models import ForeignObjectRel
from pydantic_core import PydanticUndefinedType

from django2pydantic.handlers.base import PydanticConverter
from django2pydantic.types import SupportedParentFields

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
        field: SupportedParentFields | ForeignObjectRel,
    ) -> PydanticConverter[SupportedParentFields]:
        """Get the handler for a Django field."""
        # Primarily use a handler that is registered for the exact Django field class:
        type_handler = self.handlers.get(type(field), None)
        if type_handler is not None:
            return type_handler(field)

        # Secondary, use a handler that is registered for a superclass of the
        # Django field class:
        # TODO(maintainer): Implement inheritance-based handler lookup
        # https://github.com/NextGenContributions/django2pydantic/issues/TBD

        msg = (
            f"No handler registered for {field} for Django field type {type(field)}. "
            f"Currently registered handlers are for: {self.handlers}"
        )
        raise ValueError(msg)

    def register_if_module_installed(
        self,
        fq_field_class: str,
        fq_handler_class: str,
    ) -> None:
        """Register a handler class if the module is installed.

        This is useful for optional dependencies where the handler should only be
        registered if the corresponding package is installed.

        Args:
            fq_field_class (str): Fully qualified field class name to check for
                installation.
            fq_handler_class (str): Fully qualified handler class name to register.
        """
        try:
            import importlib

            # Extract module and class name from the field class
            field_module_name, field_class_name = fq_field_class.rsplit(".", 1)

            # Try to import the module containing the field class to check if
            # it's available
            field_module = importlib.import_module(field_module_name)
            getattr(field_module, field_class_name)

            # Extract module and class name from the handler class
            handler_module_name, handler_class_name = fq_handler_class.rsplit(".", 1)

            # Import the handler class from our own module
            handler_module = importlib.import_module(handler_module_name)
            handler_class = getattr(handler_module, handler_class_name)

            # Verify the handler class is properly configured
            handler_class.field()

            # Register the handler
            self.register(handler_class)  # pyright: ignore[reportUnknownMemberType]
        except ImportError:
            logger = logging.getLogger(__name__)
            logger.debug(
                "Module '%s' not installed, skipping handler '%s' registration",
                fq_field_class,
                fq_handler_class,
            )
