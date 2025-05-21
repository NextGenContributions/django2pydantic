"""Text-related field handlers for Django models."""

import re
import uuid
from types import UnionType
from typing import Annotated, Any, override
from uuid import UUID

from django.core.validators import RegexValidator
from django.db import models
from pydantic import UUID1, UUID3, UUID4, UUID5, AnyUrl, BeforeValidator, EmailStr

from django2pydantic.handlers.base import DjangoFieldHandler
from django2pydantic.types import GetType, SetType, SupportedPydanticTypes


def ensure_not_empty_string(value: Any) -> Any | None:  # noqa: ANN401  # pyright: ignore [reportExplicitAny]
    """Ensure string is not empty, which can fail Pydantic validation e.g. Email/URL."""
    if isinstance(value, str) and len(value) == 0:
        return None
    return value


class CharFieldHandler(DjangoFieldHandler[models.CharField[SetType, GetType]]):
    """Handler for Char fields."""

    @classmethod
    @override
    def field(cls) -> type[models.CharField[SetType, GetType]]:
        return models.CharField

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

    @property
    @override
    def pattern(self) -> re.Pattern[str] | str | None:
        """Return the pattern of the field if it has a RegexValidator."""
        # Check if the Django field has any RegexValidator
        for validator in self.field_obj.validators:
            if isinstance(validator, RegexValidator):
                return validator.regex
        return None

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str


class TextFieldHandler(DjangoFieldHandler[models.TextField[SetType, GetType]]):
    """Handler for Text fields."""

    @classmethod
    @override
    def field(cls) -> type[models.TextField[SetType, GetType]]:
        return models.TextField

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str

    @property
    @override
    def min_length(self) -> int | None:
        if super().min_length is None and not self.field_obj.blank:
            return 1
        return None


class SlugFieldHandler(DjangoFieldHandler[models.SlugField[SetType, GetType]]):
    """Handler for Slug fields."""

    @classmethod
    @override
    def field(cls) -> type[models.SlugField[SetType, GetType]]:
        return models.SlugField

    @property
    @override
    def max_length(self) -> int | None:
        return self.field_obj.max_length or 50

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str


class UUIDFieldHandler(DjangoFieldHandler[models.UUIDField[SetType, GetType]]):
    """Handler for UUID fields."""

    @classmethod
    @override
    def field(cls) -> type[models.UUIDField[UUID, UUID]]:
        return models.UUIDField

    @override
    def get_pydantic_type_raw(self) -> type[Annotated[SetType, GetType]] | UUID:
        # Find out the uuid version from the Django field by examining the default value function:
        if self.field_obj.default is uuid.uuid1:
            return UUID1
        if self.field_obj.default is uuid.uuid3:
            return UUID3
        if self.field_obj.default is uuid.uuid4:
            return UUID4
        if self.field_obj.default is uuid.uuid5:
            return UUID5

        # If not determinable, default to just generic UUID
        return UUID


class EmailFieldHandler(DjangoFieldHandler[models.EmailField[str, str]]):
    """Handler for email fields."""

    @classmethod
    @override
    def field(cls) -> type[models.EmailField[str, str]]:
        """Return the type of the field."""
        return models.EmailField

    @override
    def get_pydantic_type_raw(self) -> Annotated:
        """Return the type of the field."""
        return EmailStr

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Annotated[  # type: ignore[return-value]
            super().get_pydantic_type(), BeforeValidator(ensure_not_empty_string)
        ]


class UrlFieldHandler(DjangoFieldHandler[models.URLField[str, str]]):
    """Handler for URL fields."""

    @classmethod
    @override
    def field(cls) -> type[models.URLField[str, str]]:
        return models.URLField

    @property
    @override
    def max_length(self) -> int | None:
        return self.field_obj.max_length or 200

    @property
    @override
    def pattern(self) -> None:
        return None

    @override
    def get_pydantic_type_raw(self) -> type[AnyUrl]:
        return AnyUrl

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Annotated[  # type: ignore[return-value]
            super().get_pydantic_type(), BeforeValidator(ensure_not_empty_string)
        ]
