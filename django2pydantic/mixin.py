from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel, ValidationInfo, model_validator
from pydantic.functional_validators import ModelWrapValidatorHandler

from django2pydantic.getter import DjangoGetter

if TYPE_CHECKING:
    from django2pydantic import django2pydantic

SVar = TypeVar("SVar", bound="django2pydantic")


class BaseMixins(BaseModel):
    """Base Mixins class."""

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
        "validate_default": False,
    }

    @model_validator(mode="wrap")
    @classmethod
    def _run_root_validator(
        cls,
        values: Any,
        handler: ModelWrapValidatorHandler[SVar],
        info: ValidationInfo,
    ) -> SVar:
        """Run the root validator."""
        values = DjangoGetter(values, cls, info.context)
        return handler(values)
