"""Time-related field handlers."""

import datetime
from typing import override

from django.db import models

from superschema.handlers.base import DjangoFieldHandler


class TimeFieldHandler(DjangoFieldHandler[models.TimeField[datetime.time]]):
    """Handler for Time fields."""

    @override
    @classmethod
    def field(cls) -> type[models.TimeField[datetime.time]]:
        return models.TimeField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.time]:
        return datetime.time


class DateFieldHandler(DjangoFieldHandler[models.DateField[datetime.date]]):
    """Handler for Date fields."""

    @override
    @classmethod
    def field(cls) -> type[models.DateField[datetime.date]]:
        return models.DateField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.date]:
        return datetime.date


class DateTimeFieldHandler(DjangoFieldHandler[models.DateTimeField[datetime.datetime]]):
    """Handler for DateTime fields."""

    @override
    @classmethod
    def field(cls) -> type[models.DateTimeField[datetime.datetime]]:
        return models.DateTimeField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.datetime]:
        return datetime.datetime


class DurationFieldHandler(
    DjangoFieldHandler[models.DurationField[datetime.timedelta]],
):
    """Handler for Duration fields."""

    @override
    @classmethod
    def field(cls) -> type[models.DurationField[datetime.timedelta]]:
        return models.DurationField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.timedelta]:
        return datetime.timedelta
