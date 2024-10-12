"""Handler for property decorated methods."""

from collections.abc import Callable
from typing import cast, override

from pydantic import Field
from pydantic.fields import FieldInfo

from superschema.handlers.base import FieldTypeHandler


class PropertyHandler(FieldTypeHandler[Callable[[], type]]):
    """Handler for property decorated methods."""

    field_obj: Callable[[], type]

    @override
    @classmethod
    def field(cls) -> Callable:
        return Callable

    @override
    def get_pydantic_type_raw(self):
        """Return the type of the property."""

    @override
    def get_pydantic_field(self) -> FieldInfo:
        return cast(FieldInfo, Field(description=self.field_obj.__doc__))
