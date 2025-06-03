"""Super schema packages."""

import django_stubs_ext

from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.schema import BaseSchema
from django2pydantic.types import Infer, InferExcept, ModelFields, ModelFieldsCompact

django_stubs_ext.monkeypatch()

__all__ = [
    "BaseSchema",
    "FieldTypeRegistry",
    "Infer",
    "InferExcept",
    "ModelFields",
    "ModelFieldsCompact",
]
__version__ = "0.4.3"
