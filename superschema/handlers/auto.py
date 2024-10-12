"""Auto field handlers."""

from typing import override

from django.db import models

from superschema.handlers.base import DjangoFieldHandler


class SmallAutoFieldHandler(DjangoFieldHandler[models.SmallAutoField]):
    """Handler for Small Auto fields."""

    @override
    @classmethod
    def field(cls) -> type[models.SmallAutoField]:
        return models.SmallAutoField

    @property
    @override
    def ge(self) -> int | None:
        return 1

    @property
    @override
    def le(self) -> int | None:
        return 32767

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class AutoFieldHandler(DjangoFieldHandler[models.AutoField]):
    """Handler for Auto fields."""

    @override
    @classmethod
    def field(cls) -> type[models.AutoField]:
        return models.AutoField

    @property
    @override
    def ge(self) -> int | None:
        return 1

    @property
    @override
    def le(self) -> int | None:
        return 2147483647

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class BigAutoFieldHandler(DjangoFieldHandler[models.BigAutoField]):
    """Handler for Big Auto fields."""

    @override
    @classmethod
    def field(cls) -> type[models.BigAutoField]:
        return models.BigAutoField

    @property
    @override
    def ge(self) -> int | None:
        return 1

    @property
    @override
    def le(self) -> int | None:
        return 9223372036854775807

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int
