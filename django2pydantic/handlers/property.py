"""Handler for property decorated methods."""

from typing import cast, override

from pydantic import Field
from pydantic.fields import FieldInfo

from django2pydantic.handlers.base import FieldTypeHandler

PropertyFunctionReturnTypes = type


class PropertyHandler(FieldTypeHandler[property]):
    """Handler for property decorated methods."""

    @override
    def __init__(self, field_obj: property) -> None:
        self.field_obj: property = field_obj

    @classmethod
    @override
    def field(cls) -> type[property]:
        return property

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
        return cast("type", func.__annotations__.get("return", None))

    @override
    def get_pydantic_field(self) -> FieldInfo:
        return cast("FieldInfo", Field(description=self.field_obj.__doc__))
