"""Handler for property decorated methods."""

from collections.abc import Callable
from typing import Any, cast, override

from pydantic import Field
from pydantic.fields import FieldInfo

from django2pydantic.handlers.base import FieldTypeHandler

PropertyFunctionReturnTypes = str | int | float | bool | list | dict | None


class PropertyHandler(FieldTypeHandler[type[property]]):
    """Handler for property decorated methods."""

    @classmethod
    @override
    def field(cls):
        return Callable[..., Any]

    @property
    @override
    def deprecated(self) -> bool:
        """Return whether the field is deprecated."""
        if self.field_obj.fget:
            return getattr(self.field_obj.fget, "deprecated", False)
        return False

    @override
    def get_pydantic_type(self) -> PropertyFunctionReturnTypes:
        """Return the type of the property."""
        func = self.field_obj.fget
        return func.__annotations__.get("return", None)

    @override
    def get_pydantic_field(self) -> FieldInfo:
        return cast(FieldInfo, Field(description=self.field_obj.__doc__))
