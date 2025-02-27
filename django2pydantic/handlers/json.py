"""Handler for JSON fields."""

from typing import override

from django.db import models
from pydantic import Json

from django2pydantic.handlers.base import DjangoFieldHandler
from django2pydantic.types import GetType, SetType


class JSONFieldHandler(DjangoFieldHandler[models.JSONField[SetType, GetType]]):
    """Handler for JSON fields."""

    @classmethod
    @override
    def field(cls) -> type[models.JSONField]:
        return models.JSONField

    @override
    def get_pydantic_type_raw(
        self,
    ):
        return Json
