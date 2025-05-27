"""Text-related field handlers for Django models."""
# pylint: disable=too-few-public-methods

import uuid
from types import UnionType
from typing import Annotated, Any, Generic, override
from uuid import UUID

from django.db import models
from pydantic import (
    UUID1,
    UUID3,
    UUID4,
    UUID5,
    AnyUrl,
    EmailStr,
    WrapValidator,
)
from pydantic_core import PydanticUndefined
from pydantic_core.core_schema import ValidatorFunctionWrapHandler

from django2pydantic.handlers.base import DjangoFieldHandler, TDjangoField_co
from django2pydantic.types import GetType, SetType, SupportedPydanticTypes


def handle_empty_string(value: Any, handler: ValidatorFunctionWrapHandler) -> str:  # noqa: ANN401  # pyright: ignore [reportExplicitAny]
    """Handle empty string, which can fail Pydantic validation e.g. Email/URL."""
    if value == "":
        # Bypass validation error for empty string
        return ""
    return handler(value)  # type: ignore[no-any-return]


class DjangoStringBasedFieldHandler(
    Generic[TDjangoField_co], DjangoFieldHandler[TDjangoField_co]
):
    """Base handler for Django string-based fields."""

    @property
    @override
    def default(self) -> Any:  # pyright: ignore [reportAny, reportExplicitAny]
        """Return the default value of the field."""
        if self.field_obj.has_default() and not callable(self.field_obj.default):  # pyright: ignore [reportAny]
            return self.field_obj.default  # pyright: ignore [reportAny]
        if self.field_obj.blank:  # So that the field is not marked as required
            # Depending on the field null constraint, return None or empty string
            if self.field_obj.null:
                return None
            return ""
        return PydanticUndefined

    @property
    @override
    def max_length(self) -> int | None:
        if self.field_obj.choices:
            return None
        return self.field_obj.max_length

    @property
    @override
    def min_length(self) -> int | None:
        if super().min_length is None and not self.field_obj.blank:
            return 1
        return None

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return str


class CharFieldHandler(
    DjangoStringBasedFieldHandler[models.CharField[SetType, GetType]]  # pyright: ignore [reportExplicitAny]
):
    """Handler for Char fields."""

    @classmethod
    @override
    def field(cls) -> type[models.CharField[SetType, GetType]]:
        return models.CharField


class TextFieldHandler(
    DjangoStringBasedFieldHandler[models.TextField[SetType, GetType]]  # pyright: ignore [reportExplicitAny]
):
    """Handler for Text fields."""

    @classmethod
    @override
    def field(cls) -> type[models.TextField[SetType, GetType]]:
        return models.TextField


class SlugFieldHandler(
    DjangoStringBasedFieldHandler[models.SlugField[SetType, GetType]]  # pyright: ignore [reportExplicitAny]
):
    """Handler for Slug fields."""

    @classmethod
    @override
    def field(cls) -> type[models.SlugField[SetType, GetType]]:
        return models.SlugField


class EmailFieldHandler(DjangoStringBasedFieldHandler[models.EmailField[str, str]]):
    """Handler for email fields."""

    @classmethod
    @override
    def field(cls) -> type[models.EmailField[str, str]]:
        """Return the type of the field."""
        return models.EmailField

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the type of the field."""
        return EmailStr  # pyright: ignore [reportReturnType]

    @property
    @override
    def pattern(self) -> None:
        return None

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Annotated[  # type: ignore[return-value]
            super().get_pydantic_type(),
            WrapValidator(handle_empty_string),
        ]


class UrlFieldHandler(DjangoStringBasedFieldHandler[models.URLField[str, str]]):
    """Handler for URL fields."""

    @classmethod
    @override
    def field(cls) -> type[models.URLField[str, str]]:
        return models.URLField

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return AnyUrl

    @property
    @override
    def pattern(self) -> None:
        return None

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Annotated[  # type: ignore[return-value]
            super().get_pydantic_type(),
            WrapValidator(handle_empty_string),
        ]

    @property
    @override
    def min_length(self) -> int | None:
        # TODO(phuongfi91): Investigate if this can be changed
        # URLField is special case - always has min_length=1 - defined by Ninja OpenAPI
        return 1  # to match the generated OpenAPI spec


class UUIDFieldHandler(DjangoFieldHandler[models.UUIDField[SetType, GetType]]):  # pyright: ignore [reportExplicitAny]
    """Handler for UUID fields."""

    @classmethod
    @override
    def field(cls) -> type[models.UUIDField[UUID, UUID]]:
        return models.UUIDField

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        # Find out uuid version from Django field by examining the default value
        if self.field_obj.default is uuid.uuid1:
            return UUID1  # pyright: ignore [reportReturnType]
        if self.field_obj.default is uuid.uuid3:
            return UUID3  # pyright: ignore [reportReturnType]
        if self.field_obj.default is uuid.uuid4:
            return UUID4  # pyright: ignore [reportReturnType]
        if self.field_obj.default is uuid.uuid5:
            return UUID5  # pyright: ignore [reportReturnType]

        # If not determinable, default to just generic UUID
        return UUID
