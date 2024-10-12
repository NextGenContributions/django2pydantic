from decimal import Decimal
from typing import override

from django.db import models

from superschema.handlers.base import DjangoFieldHandler


class IntegerFieldHandler(DjangoFieldHandler[models.IntegerField[int]]):
    """Handler for Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.IntegerField[int]]:
        return models.IntegerField

    @property
    @override
    def ge(self) -> int | None:
        return -2147483648

    @property
    def le(self) -> int | None:
        return 2147483647

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class SmallIntegerFieldHandler(DjangoFieldHandler[models.SmallIntegerField[int]]):
    """Handler for Small Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.SmallIntegerField[int]]:
        return models.SmallIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return -32768

    @property
    @override
    def le(self) -> int | None:
        return 32767

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class PositiveSmallIntegerFieldHandler(
    DjangoFieldHandler[models.PositiveSmallIntegerField[int]],
):
    """Handler for Positive Small Integer fields.

    Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#positivesmallintegerfield
    """

    @override
    @classmethod
    def field(cls) -> type[models.PositiveSmallIntegerField[int]]:
        return models.PositiveSmallIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return 0

    @property
    @override
    def le(self) -> int | None:
        return 32767

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class PositiveIntegerFieldHandler(DjangoFieldHandler[models.PositiveIntegerField[int]]):
    """Handler for Positive Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.PositiveIntegerField[int]]:
        return models.PositiveIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return 0

    @property
    @override
    def le(self) -> int | None:
        return 2147483647

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class BigIntegerFieldHandler(DjangoFieldHandler[models.BigIntegerField[int]]):
    """Handler for Big Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.BigIntegerField[int]]:
        return models.BigIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return -9223372036854775808

    @property
    @override
    def le(self) -> int | None:
        return 9223372036854775807

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class PositiveBigIntegerFieldHandler(
    DjangoFieldHandler[models.PositiveBigIntegerField[int]],
):
    """Handler for Positive Big Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.PositiveBigIntegerField[int]]:
        return models.PositiveBigIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return 0

    @property
    @override
    def le(self) -> int | None:
        return 9223372036854775807

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class DecimalFieldHandler(DjangoFieldHandler[models.DecimalField[Decimal]]):
    """Handler for Decimal fields."""

    @override
    @classmethod
    def field(cls) -> type[models.DecimalField[Decimal]]:
        return models.DecimalField

    @property
    @override
    def max_digits(self) -> int | None:
        return self.field_obj.max_digits

    @property
    @override
    def decimal_places(self) -> int | None:
        return self.field_obj.decimal_places

    @override
    def get_pydantic_type_raw(self) -> type[float]:
        return float


class FloatFieldHandler(DjangoFieldHandler[models.FloatField[float]]):
    """Handler for Float fields."""

    @override
    @classmethod
    def field(cls) -> type[models.FloatField[float]]:
        return models.FloatField

    @override
    def get_pydantic_type_raw(self) -> type[float]:
        return float
