"""Time-related field handlers."""

import datetime
from typing import override

from django.db import models

from django2pydantic.handlers.base import DjangoFieldHandler


class TimeFieldHandler(
    DjangoFieldHandler[models.TimeField[datetime.time, datetime.time]]
):
    """Handler for Time fields."""

    @classmethod
    @override
    def field(cls) -> type[models.TimeField[datetime.time, datetime.time]]:
        return models.TimeField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.time]:
        return datetime.time


class DateFieldHandler(
    DjangoFieldHandler[models.DateField[datetime.date, datetime.date]]
):
    """Handler for Date fields."""

    @classmethod
    @override
    def field(cls) -> type[models.DateField[datetime.date, datetime.date]]:
        return models.DateField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.date]:
        return datetime.date


class DateTimeFieldHandler(
    DjangoFieldHandler[models.DateTimeField[datetime.datetime, datetime.date]]
):
    """Handler for DateTime fields."""

    @classmethod
    @override
    def field(cls) -> type[models.DateTimeField[datetime.datetime, datetime.date]]:
        return models.DateTimeField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.datetime]:
        return datetime.datetime


class DurationFieldHandler(
    DjangoFieldHandler[models.DurationField[datetime.timedelta, datetime.timedelta]],
):
    """Handler for Duration fields."""

    @classmethod
    @override
    def field(
        cls,
    ) -> type[models.DurationField[datetime.timedelta, datetime.timedelta]]:
        return models.DurationField

    @override
    def get_pydantic_type_raw(self) -> type[datetime.timedelta]:
        return datetime.timedelta
