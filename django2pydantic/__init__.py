"""Super schema packages."""

import django_stubs_ext

from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer, InferExcept, ModelFields, ModelFieldsCompact

django_stubs_ext.monkeypatch()

__all__ = [
    "BaseSchema",
    "FieldTypeRegistry",
    "Infer",
    "InferExcept",
    "ModelFields",
    "ModelFieldsCompact",
    "SchemaConfig",
]
__version__ = "0.5.1"
