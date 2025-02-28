"""Auto field handlers."""

from typing import override

from django.db import models

from django2pydantic.handlers.base import DjangoFieldHandler


class SmallAutoFieldHandler(DjangoFieldHandler[models.SmallAutoField[int, int]]):
    """Handler for Small Auto fields."""

    @classmethod
    @override
    def field(cls) -> type[models.SmallAutoField[int, int]]:
        return models.SmallAutoField

    @property
    @override
    def ge(self) -> int | None:
        validator_min = super().ge
        return max(1, validator_min) if validator_min is not None else 1

    @property
    @override
    def le(self) -> int | None:
        validator_max = super().le
        return min(32767, validator_max) if validator_max is not None else 32767

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class AutoFieldHandler(DjangoFieldHandler[models.AutoField[int, int]]):
    """Handler for Auto fields."""

    @classmethod
    @override
    def field(cls) -> type[models.AutoField[int, int]]:
        return models.AutoField

    @property
    @override
    def ge(self) -> int | None:
        validator_min = super().ge
        return max(1, validator_min) if validator_min is not None else 1

    @property
    @override
    def le(self) -> int | None:
        validator_max = super().le
        return (
            min(2147483647, validator_max) if validator_max is not None else 2147483647
        )

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int


class BigAutoFieldHandler(DjangoFieldHandler[models.BigAutoField[int, int]]):
    """Handler for Big Auto fields."""

    @classmethod
    @override
    def field(cls) -> type[models.BigAutoField[int, int]]:
        return models.BigAutoField

    @property
    @override
    def ge(self) -> int | None:
        validator_min = super().ge
        return max(1, validator_min) if validator_min is not None else 1

    @property
    @override
    def le(self) -> int | None:
        validator_max = super().le
        return (
            min(9223372036854775807, validator_max)
            if validator_max is not None
            else 9223372036854775807
        )

    @property
    @override
    def examples(self) -> list[int]:
        if self.ge is not None and self.le is not None:
            return [self.ge, self.le]
        if self.ge is not None:
            return [self.ge]
        if self.le is not None:
            return [self.le]
        return []

    @override
    def get_pydantic_type_raw(self) -> type[int]:
        return int
