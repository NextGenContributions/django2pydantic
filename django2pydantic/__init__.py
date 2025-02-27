"""Super schema packages."""

import django_stubs_ext

from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.schema import BaseSchema
from django2pydantic.types import Infer, InferExcept, ModelFields

django_stubs_ext.monkeypatch()

__all__ = ["BaseSchema", "FieldTypeRegistry", "Infer", "InferExcept", "ModelFields"]
__version__ = "0.2.0"
