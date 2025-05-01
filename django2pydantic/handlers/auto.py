"""Auto field handlers."""
# pylint: disable=too-few-public-methods

from typing import override

from django.db import models

from django2pydantic.handlers.numbers import DjangoIntegerFieldHandler


class SmallAutoFieldHandler(DjangoIntegerFieldHandler[models.SmallAutoField[int, int]]):
    """Handler for Small Auto fields."""

    @classmethod
    @override
    def field(cls) -> type[models.SmallAutoField[int, int]]:
        return models.SmallAutoField


class AutoFieldHandler(DjangoIntegerFieldHandler[models.AutoField[int, int]]):
    """Handler for Auto fields."""

    @classmethod
    @override
    def field(cls) -> type[models.AutoField[int, int]]:
        return models.AutoField


class BigAutoFieldHandler(DjangoIntegerFieldHandler[models.BigAutoField[int, int]]):
    """Handler for Big Auto fields."""

    @classmethod
    @override
    def field(cls) -> type[models.BigAutoField[int, int]]:
        return models.BigAutoField
