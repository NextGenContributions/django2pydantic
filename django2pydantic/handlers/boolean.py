"""Boolean field handler."""

from typing import override

from django.db import models

from django2pydantic.handlers.base import DjangoFieldHandler


class BooleanFieldHandler(DjangoFieldHandler[models.BooleanField[bool]]):
    """Handler for Boolean fields."""

    @override
    @classmethod
    def field(cls) -> type[models.BooleanField[bool]]:
        return models.BooleanField

    @override
    def get_pydantic_type_raw(self) -> type[bool]:
        return bool
