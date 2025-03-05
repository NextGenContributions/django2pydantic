"""Package's public API."""

import django_stubs_ext

# This needs to be called before importing anything from django2pydantic
django_stubs_ext.monkeypatch()

from django2pydantic.registry import FieldTypeRegistry  # noqa: E402, I001
from django2pydantic.schema import BaseSchema, SchemaConfig  # noqa: E402
from django2pydantic.types import Infer  # noqa: E402
from django2pydantic.types import InferExcept  # noqa: E402
from django2pydantic.types import ModelFields  # noqa: E402
from django2pydantic.types import ModelFieldsCompact  # noqa: E402

__all__ = [
    "BaseSchema",
    "FieldTypeRegistry",
    "Infer",
    "InferExcept",
    "ModelFields",
    "ModelFieldsCompact",
    "SchemaConfig",
]
__version__ = "0.2.0"
