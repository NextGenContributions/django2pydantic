"""Mixin class for the Pydantic model."""

from typing import TYPE_CHECKING, Any, ClassVar, TypeVar, cast

from django.db.models import Model
from pydantic import (
    BaseModel,
    ConfigDict,
    ValidationError,
    ValidationInfo,
    model_validator,
)
from pydantic.functional_validators import ModelWrapValidatorHandler
from pydantic_core.core_schema import ValidatorFunctionWrapHandler

from django2pydantic.getter import DjangoGetter

if TYPE_CHECKING:
    from django2pydantic import BaseSchema

SVar = TypeVar("SVar", bound="BaseSchema")  # type: ignore[type-arg] # pyright: ignore [reportMissingTypeArgument]


class BaseMixins(BaseModel):
    """Base Mixins class."""

    model_config: ClassVar[ConfigDict] = {
        "from_attributes": True,
        "arbitrary_types_allowed": True,
        "use_enum_values": True,
        "validate_default": False,
    }

    @model_validator(mode="wrap")  # pyright: ignore[reportArgumentType]
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

    @staticmethod
    def validate_relation(
        value: Any,  # noqa: ANN401
        handler: ValidatorFunctionWrapHandler,
        info: ValidationInfo,  # noqa: ARG004
    ) -> Any:  # noqa: ANN401
        """Validate the related field.

        If the model requires primary key(s) instead of an instance or list of instances
        then return only the primary key(s).
        """
        try:
            return handler(value)
        except ValidationError as validation_err:
            # Return multiple primary keys if the value is a list of instances
            if (
                isinstance(value, list)
                and len(value) > 0  # pyright: ignore [reportUnknownArgumentType]
                and isinstance(value[0], Model)
            ):
                return handler([o.pk for o in cast(list[Model], value)])

            # Return single primary key if the value is a single instance
            if isinstance(value, Model):
                return handler(value.pk)

            raise ValueError(value) from validation_err  # pyright: ignore[reportUnknownArgumentType]
