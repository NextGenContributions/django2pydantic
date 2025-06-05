"""Handler for JSON fields."""

import json
from types import UnionType
from typing import Annotated, Any, override

from django.db import models
from pydantic import BeforeValidator, Json

from django2pydantic.handlers.base import DjangoFieldHandler
from django2pydantic.types import GetType, SetType, SupportedPydanticTypes


def ensure_json_str(value: Any) -> str:  # pyright: ignore [reportExplicitAny]
    """Ensure the value being validated is a string.

    Pydantic's Json type expects a string representation of JSON, passing in a python
    object will raise validation error. This function ensures the value is a string.
    """
    if isinstance(value, str):
        return value
    return json.dumps(value)


class JSONFieldHandler(DjangoFieldHandler[models.JSONField[SetType, GetType]]):  # pyright: ignore [reportExplicitAny]
    """Handler for JSON fields."""

    @classmethod
    @override
    def field(cls) -> type[models.JSONField]:
        return models.JSONField

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Json  # type: ignore[no-any-return]

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Annotated[  # type: ignore[return-value]
            super().get_pydantic_type(), BeforeValidator(ensure_json_str)
        ]
