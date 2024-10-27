"""Handler for property decorated methods."""

from typing import cast, override

from pydantic import Field
from pydantic.fields import FieldInfo

from superschema.handlers.base import FieldTypeHandler

ReturnType = str


class PropertyHandler(FieldTypeHandler[property]):
    """Handler for property decorated methods."""

    @override
    @classmethod
    def field(cls) -> type[property]:
        return property

    @property
    def deprecated(self) -> bool:
        """Return whether the field is deprecated."""
        if self.field_obj.fget:
            return getattr(self.field_obj.fget, "deprecated", False)

    @override
    def get_pydantic_type(self) -> str:
        """Return the type of the property."""
        func = self.field_obj.fget
        return func.__annotations__.get("return", None)

    @override
    def get_pydantic_field(self) -> FieldInfo:
        return cast(FieldInfo, Field(description=self.field_obj.__doc__))
