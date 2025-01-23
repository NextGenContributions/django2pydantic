"""Boolean field handler."""

from typing import override

from django.db import models

from django2pydantic.handlers.base import DjangoFieldHandler


class BooleanFieldHandler(DjangoFieldHandler[models.BooleanField[bool, bool]]):
    """Handler for Boolean fields."""

    @classmethod
    @override
    def field(cls) -> type[models.BooleanField[bool, bool]]:
        return models.BooleanField

    @override
    def get_pydantic_type_raw(self) -> type[bool]:
        return bool
