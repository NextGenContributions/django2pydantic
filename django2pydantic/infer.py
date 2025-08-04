"""Infer utilities for converting a Django model field to a Pydantic field definition."""

from enum import Enum, IntEnum
from types import UnionType
from typing import TYPE_CHECKING, Annotated

from django.db.models import Field

from django2pydantic.defaults import field_type_registry
from django2pydantic.types import InferExcept

if TYPE_CHECKING:
    from django.db.models.fields import (
        _FieldDescriptor,  # pyright: ignore[reportPrivateUsage]
    )

    type FieldType = _FieldDescriptor[Field[object, object]]
else:
    type FieldType = Field


class InferredField:  # pylint: disable=too-few-public-methods
    """Infer a Pydantic field from a Django model field."""

    @classmethod
    def __class_getitem__(
        cls, django_model_field: FieldType | tuple[FieldType, InferExcept]
    ) -> (
        Enum
        | IntEnum
        | UnionType
        | list[Enum | IntEnum | type[object]]
        | type[object]
        | Annotated[object, ...]
    ):
        """Infer a Pydantic field from a Django model field.

        Args:
            django_model_field: The Django model field to infer from.
            override: Optional override for the inferred Pydantic field.

        Returns:
            FieldInfo: The inferred Pydantic field information.

        Usage example:
        ```python
        from django2pydantic import InferredField
        from pydantic import BaseModel


        class MyDjangoModel(models.Model):
            some_str_field = models.CharField(
                max_length=100, description="A string field"
            )
            some_int_field = models.IntegerField(description="An integer field")


        class MyModel(BaseModel):
            some_str_field: InferredField[MyDjangoModel.some_str_field]
            some_int_field: InferredField[MyDjangoModel.some_int_field]
            ...
        ```
        """
        field, override = (
            (django_model_field[0].field, django_model_field[1])
            if isinstance(django_model_field, tuple)
            else (django_model_field.field, None)
        )

        type_handler = field_type_registry.get_handler(field)  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType, reportAttributeAccessIssue]

        pydantic_type = type_handler.get_pydantic_type()
        pydantic_field_info = type_handler.get_pydantic_field()

        if override:
            for detail_key, detail_value in override.args.items():
                if detail_key == "annotation":
                    pydantic_type = detail_value
                else:
                    setattr(pydantic_field_info, detail_key, detail_value)

        return Annotated[pydantic_type, pydantic_field_info]  # pyre-ignore[6]
