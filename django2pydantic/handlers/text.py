"""Text-related field handlers for Django models."""

import re
import uuid
from typing import Annotated, cast, override
from uuid import UUID

from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from pydantic import UUID1, UUID3, UUID4, UUID5, AnyUrl, EmailStr

from django2pydantic.handlers.base import DjangoFieldHandler


class CharFieldHandler(DjangoFieldHandler[models.CharField[str]]):
    """Handler for Char fields."""

    @override
    @classmethod
    def field(cls) -> type[models.CharField[str]]:
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

    @override
    def get_pydantic_type_raw(self) -> type:
        return str


class TextFieldHandler(DjangoFieldHandler[models.TextField[str]]):
    """Handler for Text fields."""

    @override
    @classmethod
    def field(cls) -> type[models.TextField[str]]:
        return models.TextField

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str


class SlugFieldHandler(DjangoFieldHandler[models.SlugField[str]]):
    """Handler for Slug fields."""

    @override
    @classmethod
    def field(cls) -> type[models.SlugField[str]]:
        return models.SlugField

    @property
    @override
    def max_length(self) -> int | None:
        return self.field_obj.max_length or 50

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str


class UUIDFieldHandler(DjangoFieldHandler[models.UUIDField[UUID]]):
    """Handler for UUID fields."""

    @override
    @classmethod
    def field(cls) -> type[models.UUIDField[UUID]]:
        return models.UUIDField

    @override
    def get_pydantic_type_raw(self) -> type[Annotated] | UUID:
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

    @override
    @classmethod
    def field(cls) -> type[models.EmailField[str, str]]:
        """Return the type of the field."""
        return models.EmailField

    @override
    def get_pydantic_type_raw(self) -> Annotated:
        """Return the type of the field."""
        return EmailStr


class UrlFieldHandler(DjangoFieldHandler[models.URLField[str]]):
    """Handler for URL fields."""

    @override
    @classmethod
    def field(cls) -> type[models.URLField[str]]:
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
