"""Numbers field handlers."""
# pylint: disable=too-few-public-methods

from decimal import Decimal
from typing import Generic, cast, override

from django.db import connection, models

from django2pydantic.handlers.base import DjangoFieldHandler, TDjangoField_co


class DjangoIntegerFieldHandler(
    Generic[TDjangoField_co], DjangoFieldHandler[TDjangoField_co]
):
    """Base handler for Django Integer fields."""

    @property
    @override
    def ge(self) -> int | None:
        validator_min = super().ge
        db_min = connection.ops.integer_field_range(self.field().__name__)[0]
        return max(db_min, validator_min) if validator_min is not None else db_min

    @property
    @override
    def le(self) -> int | None:
        validator_max = super().le
        db_max = connection.ops.integer_field_range(self.field().__name__)[1]
        return min(db_max, validator_max) if validator_max is not None else db_max

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int

    # TODO(phuongfi91): This might cause issue with schemathesis test
    #  https://github.com/NextGenContributions/django-ninja-crudl/issues/35
    # examples = [-9223372036854775808, 9223372036854775807]
    # unresolved_definition = [-9223372036854775808, 9223372036854775807]
    #
    #     def extract_inner_examples(
    #         examples: dict[str, Any], unresolved_definition: dict[str, Any]
    #     ) -> Generator[Any, None, None]:
    #         """Extract exact examples values from the `examples` dictionary."""
    # >       for name, example in examples.items():
    # E       AttributeError: 'list' object has no attribute 'items'
    #
    # ../.venv/lib/python3.12/site-packages/schemathesis/specs/openapi/examples.py:209: AttributeError
    #
    # @property
    # @override
    # def examples(self) -> list[int]:
    #     if self.ge is not None and self.le is not None:
    #         return [self.ge, self.le]
    #     if self.ge is not None:
    #         return [self.ge]
    #     if self.le is not None:
    #         return [self.le]
    #     return []


class IntegerFieldHandler(DjangoIntegerFieldHandler[models.IntegerField[int, int]]):
    """Handler for Integer fields."""

    @classmethod
    @override
    def field(cls) -> type[models.IntegerField[int, int]]:
        return models.IntegerField


class SmallIntegerFieldHandler(
    DjangoIntegerFieldHandler[models.SmallIntegerField[int, int]]
):
    """Handler for Small Integer fields."""

    @classmethod
    @override
    def field(cls) -> type[models.SmallIntegerField[int, int]]:
        return models.SmallIntegerField


class PositiveSmallIntegerFieldHandler(
    DjangoIntegerFieldHandler[models.PositiveSmallIntegerField[int, int]],
):
    """Handler for Positive Small Integer fields.

    Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#positivesmallintegerfield
    """

    @classmethod
    @override
    def field(cls) -> type[models.PositiveSmallIntegerField[int, int]]:
        return models.PositiveSmallIntegerField


class PositiveIntegerFieldHandler(
    DjangoIntegerFieldHandler[models.PositiveIntegerField[int, int]]
):
    """Handler for Positive Integer fields."""

    @classmethod
    @override
    def field(cls) -> type[models.PositiveIntegerField[int, int]]:
        return models.PositiveIntegerField


class BigIntegerFieldHandler(
    DjangoIntegerFieldHandler[models.BigIntegerField[int, int]]
):
    """Handler for Big Integer fields."""

    @classmethod
    @override
    def field(cls) -> type[models.BigIntegerField[int, int]]:
        return models.BigIntegerField


class PositiveBigIntegerFieldHandler(
    DjangoIntegerFieldHandler[models.PositiveBigIntegerField[int, int]],
):
    """Handler for Positive Big Integer fields."""

    @classmethod
    @override
    def field(cls) -> type[models.PositiveBigIntegerField[int, int]]:
        return models.PositiveBigIntegerField


class DecimalFieldHandler(DjangoFieldHandler[models.DecimalField[Decimal, Decimal]]):
    """Handler for Decimal fields."""

    @classmethod
    @override
    def field(cls) -> type[models.DecimalField[Decimal, Decimal]]:
        return models.DecimalField

    @property
    @override
    def max_digits(self) -> int | None:
        return cast("models.DecimalField[Decimal, Decimal]", self.field_obj).max_digits

    @property
    @override
    def decimal_places(self) -> int | None:
        return cast(
            "models.DecimalField[Decimal, Decimal]", self.field_obj
        ).decimal_places

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
