from decimal import Decimal
from typing import override

from django.db import connection, models

from django2pydantic.handlers.base import DjangoFieldHandler


class IntegerFieldHandler(DjangoFieldHandler[models.IntegerField[int, int]]):
    """Handler for Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.IntegerField[int, int]]:
        return models.IntegerField

    # TODO(phuongfi91): Revisit all the potential None values in mix and max params
    @property
    @override
    def ge(self) -> int | None:
        return max(connection.ops.integer_field_range("IntegerField")[0], super().ge)

    @property
    @override
    def le(self) -> int | None:
        return min(connection.ops.integer_field_range("IntegerField")[1], super().le)

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class SmallIntegerFieldHandler(DjangoFieldHandler[models.SmallIntegerField[int, int]]):
    """Handler for Small Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.SmallIntegerField[int, int]]:
        return models.SmallIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return max(
            connection.ops.integer_field_range("SmallIntegerField")[0],
            super().ge,
        )

    @property
    @override
    def le(self) -> int | None:
        return min(
            connection.ops.integer_field_range("SmallIntegerField")[1],
            super().le,
        )

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class PositiveSmallIntegerFieldHandler(
    DjangoFieldHandler[models.PositiveSmallIntegerField[int, int]],
):
    """Handler for Positive Small Integer fields.

    Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#positivesmallintegerfield
    """

    @override
    @classmethod
    def field(cls) -> type[models.PositiveSmallIntegerField[int, int]]:
        return models.PositiveSmallIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return max(
            connection.ops.integer_field_range("PositiveSmallIntegerField")[0],
            super().ge,
        )

    @property
    @override
    def le(self) -> int | None:
        return min(
            connection.ops.integer_field_range("PositiveSmallIntegerField")[1],
            super().le,
        )

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class PositiveIntegerFieldHandler(
    DjangoFieldHandler[models.PositiveIntegerField[int, int]]
):
    """Handler for Positive Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.PositiveIntegerField[int, int]]:
        return models.PositiveIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return max(
            connection.ops.integer_field_range("PositiveIntegerField")[0],
            super().ge,
        )

    @property
    @override
    def le(self) -> int | None:
        return min(
            connection.ops.integer_field_range("PositiveIntegerField")[1],
            super().le,
        )

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class BigIntegerFieldHandler(DjangoFieldHandler[models.BigIntegerField[int, int]]):
    """Handler for Big Integer fields."""

    @override
    @classmethod
    def field(cls) -> type[models.BigIntegerField[int, int]]:
        return models.BigIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return max(connection.ops.integer_field_range("BigIntegerField")[0], super().ge)

    @property
    @override
    def le(self) -> int | None:
        return min(connection.ops.integer_field_range("BigIntegerField")[1], super().le)

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class PositiveBigIntegerFieldHandler(
    DjangoFieldHandler[models.PositiveBigIntegerField[int, int]],
):
    """Handler for Positive Big Integer fields."""

    @classmethod
    @override
    def field(cls) -> type[models.PositiveBigIntegerField[int, int]]:
        return models.PositiveBigIntegerField

    @property
    @override
    def ge(self) -> int | None:
        return max(
            connection.ops.integer_field_range("PositiveBigIntegerField")[0],
            super().ge or 0,
        )

    @property
    @override
    def le(self) -> int | None:
        return min(
            connection.ops.integer_field_range("PositiveBigIntegerField")[1],
            super().le or 9223372036854775808,
        )

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class DecimalFieldHandler(DjangoFieldHandler[models.DecimalField[Decimal, Decimal]]):
    """Handler for Decimal fields."""

    @classmethod
    @override
    def field(cls) -> type[models.DecimalField[Decimal, Decimal]]:
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
    def get_pydantic_type_raw(self) -> type[Decimal]:
        return Decimal


class FloatFieldHandler(DjangoFieldHandler[models.FloatField[float, float]]):
    """Handler for Float fields."""

    @classmethod
    @override
    def field(cls) -> type[models.FloatField[float, float]]:
        return models.FloatField

    @override
    def get_pydantic_type_raw(self) -> type[float]:
        return float
