"""Field handlers for network fields."""

from typing import override

from django.db import models
from pydantic import IPvAnyAddress

from django2pydantic.handlers.base import DjangoFieldHandler


class GenericIpAddressFieldHandler(
    DjangoFieldHandler[models.GenericIPAddressField[str]],
):
    """Handler for Generic IP Address fields."""

    @override
    @classmethod
    def field(cls) -> type[models.GenericIPAddressField[str]]:
        return models.GenericIPAddressField

    @override
    def get_pydantic_type_raw(self) -> type[IPvAnyAddress]:
        return IPvAnyAddress
