"""Handler for JSON fields."""

from typing import Annotated, override

from django.db import models
from pydantic import Json

from superschema.handlers.base import DjangoFieldHandler

JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


class JSONFieldHandler(DjangoFieldHandler[models.JSONField[JSONValue]]):
    """Handler for JSON fields."""

    @override
    @classmethod
    def field(cls) -> type[models.JSONField]:
        return models.JSONField

    @override
    def get_pydantic_type_raw(self) -> type[Annotated]:
        return Json
