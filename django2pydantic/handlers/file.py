"""File-related field handlers."""

from typing import override

from django.db import models
from pydantic import FilePath

from django2pydantic.handlers.base import DjangoFieldHandler


class FileFieldHandler(DjangoFieldHandler[models.FileField]):
    """Handler for File fields."""

    @classmethod
    @override
    def field(cls) -> type[models.FileField]:
        return models.FileField

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str


class FilePathFieldHandler(DjangoFieldHandler[models.FilePathField[str, str]]):
    """Handler for FilePath fields."""

    @classmethod
    @override
    def field(cls) -> type[models.FilePathField[str, str]]:
        return models.FilePathField

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return FilePath


class ImageFieldHandler(DjangoFieldHandler[models.ImageField]):
    """Handler for Image fields."""

    @classmethod
    @override
    def field(cls) -> type[models.ImageField]:
        return models.ImageField

    @property
    @override
    def max_length(self) -> int | None:
        return self.field_obj.max_length or 100

    @override
    def get_pydantic_type_raw(self) -> type[str]:
        return str


class BinaryFieldHandler(DjangoFieldHandler[models.BinaryField[bytes, bytes]]):
    """Handler for Binary fields."""

    @classmethod
    @override
    def field(cls) -> type[models.BinaryField[bytes, bytes]]:
        return models.BinaryField

    @property
    @override
    def max_length(self) -> int | None:
        return self.field_obj.max_length

    @override
    def get_pydantic_type_raw(self) -> type[bytes]:
        return bytes
