"""Base classes for handling Django model fields."""

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum, IntEnum
from types import UnionType
from typing import (
    Annotated,
    Any,
    Generic,
    Optional,  # pyright: ignore[reportDeprecated]
    Protocol,
    TypeVar,
    cast,
    override,
    runtime_checkable,
)
from uuid import UUID

from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
    StepValueValidator,
)
from django.db import models
from django.db.models.fields.related import RelatedField
from django.utils.encoding import force_str
from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from django2pydantic.types import GetType, SetType, TFieldType_co

CallableOutput = TypeVar("CallableOutput", int, str, bool, UUID, float)
DefaultCallable = Callable[..., CallableOutput]


@runtime_checkable
class PydanticConverter(Protocol[TFieldType_co]):
    """Define the interface for a Pydantic field converter."""

    def __init__(self, field_obj: TFieldType_co) -> None:
        """Initialize the field converter.

        Args:
            field_obj (TFieldType_co): The Django field object.

        """

    @classmethod
    def field(cls) -> type[TFieldType_co]:
        """Return the type of the field.

        Returns:
            type: The type of the field.

        """
        return NotImplemented

    def get_pydantic_type(self) -> IntEnum | Enum | type[object] | UnionType:
        """Return the type of the field.

        Returns:
            type: The type of the field.

        """
        return NotImplemented

    def get_pydantic_field(self) -> FieldInfo:
        """Return the Pydantic field information.

        Returns:
            FieldInfo: The Pydantic field information.

        """
        return NotImplemented


class FieldTypeHandler(Generic[TFieldType_co], PydanticConverter[TFieldType_co], ABC):  # noqa: WPS214 - Found too many methods
    """Abstract base class for handling Django model fields."""

    field_obj: TFieldType_co

    @override
    def __init__(self, field_obj: TFieldType_co) -> None:
        """Initialize the field handler."""
        super().__init__(field_obj)
        self.field_obj = field_obj

    @classmethod
    @abstractmethod
    @override
    def field(cls) -> type[TFieldType_co]:
        """Return the type of the field."""

    @property
    def description(self) -> str | None:
        """Return the description of the field."""
        return None

    @property
    def default(self) -> Any:
        """Return the default value of the field."""
        return PydanticUndefinedType

    @property
    def default_factory(self) -> DefaultCallable[Any] | PydanticUndefinedType:
        """Return the default factory of the field."""
        return PydanticUndefined

    @property
    def title(self) -> str | None:
        """Return the title of the field."""
        return None

    @property
    def ge(self) -> int | None:
        """Return the greater than or equal to value of the field."""
        return None

    @property
    def gt(self) -> int | None:
        """Return the greater than value of the field."""
        return None

    @property
    def le(self) -> int | None:
        """Return the less than or equal to value of the field."""
        return None

    @property
    def lt(self) -> int | None:
        """Return the less than value of the field."""
        return None

    @property
    def max_digits(self) -> int | None:
        """Return the maximum number of digits of the field."""
        return None

    @property
    def decimal_places(self) -> int | None:
        """Return the number of decimal places of the field."""
        return None

    @property
    def min_length(self) -> int | None:
        """Return the minimum length of the field."""
        return None

    @property
    def max_length(self) -> int | None:
        """Return the maximum length of the field."""
        return None

    @property
    def pattern(self) -> re.Pattern[str] | str | None:
        """Return the regex pattern of the field."""
        return None

    @property
    def alias(self) -> str | None:
        """Return the alias of the field."""
        return None

    @property
    def examples(self) -> list[Any] | None:
        """Return the example values of the field."""
        return None

    @property
    def deprecated(self) -> bool | str:
        """Return whether the field is deprecated."""
        return False

    @property
    def multiple_of(self) -> int | float | None:
        """Return the multiple of the field."""
        return None

    @abstractmethod
    @override
    def get_pydantic_type(self) -> IntEnum | Enum | type[object] | UnionType:
        """Return the Pydantic type of the field."""
        return type

    @override
    def get_pydantic_field(self) -> FieldInfo:
        """Return the Pydantic field information."""
        pydantic_field = Field(
            default=self.default,
            title=self.title,
            description=self.description,
            alias=self.alias,
            examples=self.examples,
            ge=self.ge,
            gt=self.gt,
            le=self.le,
            lt=self.lt,
            pattern=self.pattern,
            max_digits=self.max_digits,
            decimal_places=self.decimal_places,
            min_length=self.min_length,
            max_length=self.max_length,
            multiple_of=self.multiple_of,
            deprecated=self.deprecated,
        )

        return cast(
            FieldInfo,
            pydantic_field,
        )  # Pydantic seems have marked Field as Any although it is FieldInfo


TDjangoMainParentFields = (
    models.Field[SetType, GetType] | RelatedField[models.Model, models.Model]
)

TDjangoField_co = TypeVar(
    "TDjangoField_co",
    bound=TDjangoMainParentFields,
    covariant=True,
)


class DjangoFieldHandler(  # noqa: WPS214
    Generic[TDjangoField_co], FieldTypeHandler[TDjangoField_co], ABC
):
    """Base class for handling Django fields.

    Implementations should override the `field` class method to return the Django field class they handle.
    """

    @classmethod
    @override
    def field(cls) -> type[TDjangoField_co]:
        """Return the type of the field."""
        return models.Field[SetType, GetType]

    @property
    def is_required(self) -> bool:
        """Return whether the field is required."""
        return not self.field_obj.null and not self.field_obj.blank

    @property
    @override
    def title(self) -> str | None:
        """Return the title of the field."""
        if getattr(self.field_obj, "verbose_name", None):
            return force_str(self.field_obj.verbose_name)
        if getattr(self.field_obj, "name", None):
            return self.field_obj.name
        if getattr(self.field_obj, "attname", None):
            return self.field_obj.attname
        return None

    @property
    @override
    def description(self) -> str | None:
        """Return the description of the field."""
        if self.field_obj.help_text:
            return force_str(self.field_obj.help_text).strip()
        if self.field_obj.verbose_name:
            return force_str(self.field_obj.verbose_name).strip()
        return None

    @property
    @override
    def default(self) -> Any:
        """Return the default value of the field."""
        if self.field_obj.has_default() and not callable(self.field_obj.default):
            return self.field_obj.default
        if self.field_obj.null:  # So that the field is not marked as required
            return None
        return PydanticUndefined

    @property
    @override
    def default_factory(self) -> DefaultCallable[Any] | PydanticUndefinedType:
        """Return the default factory of the field."""
        if self.field_obj.has_default() and callable(self.field_obj.default):
            return cast(DefaultCallable[Any], self.field_obj.default)
        return PydanticUndefined

    @property
    @override
    def examples(self) -> list[Any] | None:
        """Return the example value(s) of the field."""
        if self.field_obj.choices:
            choices = self.field_obj.get_choices(include_blank=self.field_obj.blank)
            return [c[0] for c in choices]
        if self.field_obj.has_default():
            if not callable(self.field_obj.default):
                return [self.field_obj.default]
            if callable(self.field_obj.default):
                return [self.field_obj.default()]
        return None

    @property
    @override
    def ge(self) -> int | None:
        # check if the field has MinValueValidator
        if self.field_obj.validators:
            for validator in self.field_obj.validators:
                if isinstance(validator, MinValueValidator):
                    return cast(int, validator.limit_value)
        return None

    @property
    @override
    def le(self) -> int | None:
        if self.field_obj.validators:
            for validator in self.field_obj.validators:
                if isinstance(validator, MaxValueValidator):
                    return cast(int, validator.limit_value)

        return None

    @property
    @override
    def multiple_of(self) -> int | None:
        if self.field_obj.validators:
            for validator in self.field_obj.validators:
                if isinstance(validator, StepValueValidator):
                    if not getattr(validator, "offset", None):
                        return cast(int, validator.limit_value)
        return None

    @property
    @override
    def max_length(self) -> int | None:
        """Return the max length of the field if it has a MaxLengthValidator."""
        for validator in self.field_obj.validators:
            if isinstance(validator, MaxLengthValidator):
                if callable(validator.limit_value):
                    return cast(int, validator.limit_value())
                return cast(int, validator.limit_value)
        return None

    @property
    @override
    def min_length(self) -> int | None:
        """Return the min length of the field if it has a MinLengthValidator."""
        for validator in self.field_obj.validators:
            if isinstance(validator, MinLengthValidator):
                if callable(validator.limit_value):
                    return cast(int, validator.limit_value())
                return cast(int, validator.limit_value)
        return None

    @property
    @override
    def pattern(self) -> re.Pattern[str] | str | None:
        """Return the pattern of the field if it has a RegexValidator."""
        # Check if the Django field has any RegexValidator
        for validator in self.field_obj.validators:
            if isinstance(validator, RegexValidator):
                return validator.regex
        return None

    @abstractmethod
    def get_pydantic_type_raw(
        self,
    ) -> type[object] | UnionType | Annotated[SetType, GetType]:
        """Return the type of the field."""

    @override
    def get_pydantic_type(self) -> IntEnum | Enum | type[object] | UnionType:
        """Return the Pydantic type of the field.

        If the field has choices, return an Enum/IntEnum type. Otherwise, return the raw type.
        """
        if self.field_obj.choices:
            ch = self.field_obj.get_choices(include_blank=False)
            # We need to reverse the choices tuples to make the enum work correctly:
            named_choices = [(force_str(c[1]), c[0]) for c in ch]

            # We need to create a unique name for the Enum type:
            model_name = self.field_obj.model.__name__
            field_name = self.field_obj.name.title().replace("_", "")
            enum_name = f"{model_name}{field_name}Enum"

            # If all choices are integers, we can use IntEnum:
            if all(isinstance(c[0], int) for c in ch):
                return IntEnum(
                    enum_name,
                    named_choices,
                    module=__name__,
                )

            # Otherwise, we use a regular Enum:
            return Enum(
                enum_name,
                named_choices,
                module=__name__,
            )

        if self.field_obj.null:
            return Optional[self.get_pydantic_type_raw()]  # noqa: UP007
        return self.get_pydantic_type_raw()
