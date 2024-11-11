from typing import TYPE_CHECKING, Any, TypeVar

from pydantic import BaseModel, ValidationInfo, model_validator
from pydantic.functional_validators import ModelWrapValidatorHandler

from superschema.getter import DjangoGetter

if TYPE_CHECKING:
    from superschema import SuperSchema

SVar = TypeVar("SVar", bound="SuperSchema")


class BaseMixins(BaseModel):
    """Base Mixins class."""

    model_config = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
        "validate_default": True,
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
        print("-----------Root Validator-----------")
        values = DjangoGetter(values, cls, info.context)
        return handler(values)
