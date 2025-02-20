"""Mixin class for Pydantic models."""

from typing import Any, ClassVar, TypeVar

from pydantic import BaseModel, ConfigDict, ValidationInfo, model_validator
from pydantic.functional_validators import ModelWrapValidatorHandler

from django2pydantic.getter import DjangoGetter

SVar = TypeVar("SVar")


class BaseMixins(BaseModel):
    """Base Mixins class."""

    model_config: ClassVar[ConfigDict] = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
        "validate_default": False,
    }

    @model_validator(mode="wrap")
    @classmethod
    def _run_root_validator(
        cls,
        values: Any,  # noqa: ANN401
        handler: ModelWrapValidatorHandler[SVar],
        info: ValidationInfo,
    ) -> SVar:
        """Run the root validator."""
        values = DjangoGetter(values, cls, info.context)
        return handler(values)
