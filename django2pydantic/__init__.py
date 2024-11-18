"""Super schema packages."""

from django2pydantic.schema import django2pydantic
from django2pydantic.types import Infer, InferExcept, MetaFields, ModelFields

__all__ = ["Infer", "InferExcept", "ModelFields", "MetaFields", "django2pydantic"]
__version__ = "0.0.1"
