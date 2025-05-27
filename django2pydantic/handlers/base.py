"""Base classes for handling Django model fields."""

import re
from abc import ABC, abstractmethod
from collections.abc import Callable
from enum import Enum, IntEnum
from types import UnionType
from typing import (
    Any,
    Generic,
    Protocol,
    TypeVar,
    Union,
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
from django.db.models import ForeignObjectRel
from django.utils.encoding import force_str
from pydantic import Field
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined, PydanticUndefinedType

from django2pydantic.types import (
    ForwardRel,
    GetType,
    ReverseRel,
    SetType,
    SupportedPydanticTypes,
    TFieldType_co,
)

CallableOutput = TypeVar("CallableOutput", int, str, bool, UUID, float)
DefaultCallable = Callable[..., CallableOutput]


@runtime_checkable
class PydanticConverter(Protocol[TFieldType_co]):
    """Define the interface for a Pydantic field converter."""

    def __init__(self, field_obj: TFieldType_co) -> None:
        """Initialize the field converter.

        Args:
            field_obj (TFieldAndRelType_co): The Django field object.

        """

    @classmethod
    def field(cls) -> type[TFieldType_co]:
        """Return the type of the field.

        Returns:
            type: The type of the field.

        """
        raise NotImplementedError

    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the type of the field.

        Returns:
            type: The type of the field.

        """
        raise NotImplementedError

    def get_pydantic_field(self) -> FieldInfo:
        """Return the Pydantic field information.

        Returns:
            FieldInfo: The Pydantic field information.

        """
        raise NotImplementedError


class FieldTypeHandler(Generic[TFieldType_co], PydanticConverter[TFieldType_co], ABC):  # noqa: WPS214 - Found too many methods
    """Abstract base class for handling generic model fields."""

    @override
    def __init__(self, field_obj: TFieldType_co) -> None:
        pass

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
    def default(self) -> Any:  # noqa: ANN401  # pyright: ignore[reportAny,reportExplicitAny]
        """Return the default value of the field."""
        return PydanticUndefinedType

    @property
    def default_factory(self) -> DefaultCallable[Any] | PydanticUndefinedType:  # pyright: ignore [reportExplicitAny]
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
    def examples(self) -> list[Any] | None:  # pyright: ignore [reportExplicitAny]
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
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return type

    @override
    def get_pydantic_field(self) -> FieldInfo:
        """Return the Pydantic field information."""
        pydantic_field = Field(  # pyright: ignore [reportAny]
            default=self.default,  # pyright: ignore [reportAny]
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
            "FieldInfo",
            pydantic_field,
        )  # Pydantic seems to have marked Field as Any, although it is FieldInfo


TDjangoMainParentFields = (
    models.Field[SetType, GetType]  # pyright: ignore [reportExplicitAny]
    | ForwardRel
    | ReverseRel
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

    Implementations should override the `field` class method to return the Django field
    class they handle.
    """

    @override
    def __init__(self, field_obj: TDjangoField_co) -> None:  # pyright: ignore[reportMissingSuperCall]
        """Initialize the field handler."""
        self.field_obj: models.Field[SetType, GetType] | ForwardRel
        if isinstance(field_obj, ForeignObjectRel):
            if field_obj.related_model == "self":
                related_model = field_obj.model
            else:
                related_model = field_obj.related_model
            self.field_obj = related_model._meta.pk  # noqa: SLF001  # pyright: ignore [reportUnknownMemberType]
        else:
            self.field_obj = field_obj

    @classmethod
    @override
    def field(cls) -> type[TDjangoField_co]:
        """Return the type of the field."""
        return models.Field[SetType, GetType]  # type: ignore[return-value]

    @property
    @override
    def title(self) -> str | None:
        """Return the title of the field."""
        if vn := self.field_obj.verbose_name:
            return force_str(vn)
        if n := self.field_obj.name:
            return n
        if an := self.field_obj.attname:
            return an
        return None

    @property
    @override
    def description(self) -> str | None:
        """Return the description of the field."""
        if ht := self.field_obj.help_text:
            return force_str(ht).strip()
        if vn := self.field_obj.verbose_name:
            return force_str(vn).strip()
        return None

    @property
    @override
    def default(self) -> Any:  # pyright: ignore [reportAny, reportExplicitAny]
        """Return the default value of the field."""
        if self.field_obj.has_default() and not callable(self.field_obj.default):  # pyright: ignore [reportAny]
            return self.field_obj.default  # pyright: ignore [reportAny]
        if self.field_obj.null and self.field_obj.blank:
            # So that the field is not marked as required
            return None
        return PydanticUndefined

    @property
    @override
    def default_factory(self) -> DefaultCallable[Any] | PydanticUndefinedType:  # pyright: ignore [reportExplicitAny]
        """Return the default factory of the field."""
        if self.field_obj.has_default() and callable(self.field_obj.default):  # pyright: ignore [reportAny]
            return cast("DefaultCallable[Any]", self.field_obj.default)  # pyright: ignore [reportExplicitAny]
        return PydanticUndefined

    @property
    @override
    def examples(self) -> list[Any] | None:  # pyright: ignore [reportExplicitAny]
        """Return the example value(s) of the field."""
        if self.field_obj.choices:
            choices = self.field_obj.get_choices(include_blank=self.field_obj.blank)
            return [c[0] for c in choices]
        if self.field_obj.has_default():
            if not callable(self.field_obj.default):  # pyright: ignore [reportAny]
                return [self.field_obj.default]  # pyright: ignore [reportAny]
            if callable(self.field_obj.default):
                return [self.field_obj.default()]
        return None

    @property
    @override
    def ge(self) -> int | None:
        # check if the field has MinValueValidator
        for validator in self.field_obj.validators:
            if isinstance(validator, MinValueValidator):
                return cast("int", validator.limit_value)
        return None

    @property
    @override
    def le(self) -> int | None:
        # check if the field has MaxValueValidator
        for validator in self.field_obj.validators:
            if isinstance(validator, MaxValueValidator):
                return cast("int", validator.limit_value)

        return None

    @property
    @override
    def multiple_of(self) -> int | None:
        for validator in self.field_obj.validators:
            if isinstance(validator, StepValueValidator) and not getattr(
                validator, "offset", None
            ):
                return cast("int", validator.limit_value)

        return None

    @property
    @override
    def max_length(self) -> int | None:
        """Return the max length of the field if it has a MaxLengthValidator."""
        for validator in self.field_obj.validators:
            if isinstance(validator, MaxLengthValidator):
                if callable(validator.limit_value):  # pyright: ignore [reportAny]
                    return cast("int", validator.limit_value())
                return cast("int", validator.limit_value)
        return None

    @property
    @override
    def min_length(self) -> int | None:
        """Return the min length of the field if it has a MinLengthValidator."""
        for validator in self.field_obj.validators:
            if isinstance(validator, MinLengthValidator):
                if callable(validator.limit_value):  # pyright: ignore [reportAny]
                    return cast("int", validator.limit_value())
                return cast("int", validator.limit_value)
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
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the type of the field."""

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field.

        If the field has choices, return an Enum/IntEnum type. Otherwise, return the
        raw type.
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
            return Union[self.get_pydantic_type_raw(), None]  # type: ignore[return-value]
        return self.get_pydantic_type_raw()
