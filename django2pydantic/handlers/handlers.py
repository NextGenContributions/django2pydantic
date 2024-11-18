"""Tooling to convert Django models and fields to Pydantic native models."""

from collections.abc import Callable
from typing import Any, TypeVar
from uuid import UUID

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from pydantic_core import PydanticUndefinedType

SupportedParentFields = (
    models.Field[Any, Any]
    | models.ForeignObjectRel
    | GenericForeignKey
    | Callable[[], type]
)

TFieldType_co = TypeVar("TFieldType_co", bound=SupportedParentFields, covariant=True)

CallableOutput = TypeVar("CallableOutput", int, str, bool, UUID, float)
DefaultCallable = Callable[..., CallableOutput]

Undefined = PydanticUndefinedType
