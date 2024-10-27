"""Tooling to convert Django models and fields to Pydantic native models."""

from typing import ClassVar

from django.db.models import Model
from pydantic import BaseModel

from superschema.base import SuperSchemaResolver
from superschema.types import ModelFields


class SuperSchema(BaseModel, metaclass=SuperSchemaResolver):
    """SuperSchema class."""

    class Meta:
        """Pydantic configuration."""

        name: str | None = None
        models: Model | None = None
        fields: ClassVar[ModelFields | None] = None
