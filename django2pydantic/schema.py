"""Tooling to convert Django models and fields to Pydantic native models."""

from typing import Any, ClassVar, TypeVar

from django.db.models import Model
from pydantic import BaseModel, ValidationInfo, model_validator
from pydantic.functional_validators import ModelWrapValidatorHandler

from django2pydantic.base import SuperSchemaResolver
from django2pydantic.getter import DjangoGetter
from django2pydantic.types import ModelFields

SType = TypeVar("SType", bound=BaseModel)

DictStrAny = dict[str, Any]


class Schema(BaseModel, metaclass=SuperSchemaResolver):
    """django2pydantic class."""

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        arbitrary_types_allowed = True

    class Meta:
        """Pydantic configuration."""

        name: str | None = None
        model: type[Model] | None = None
        fields: ClassVar[ModelFields | None] = None

    @model_validator(mode="wrap")
    @classmethod
    def _run_root_validator(
        cls,
        values: Any,
        handler: ModelWrapValidatorHandler[SType],
        info: ValidationInfo,
    ) -> SType:
        forbids_extra = cls.model_config.get("extra") == "forbid"
        should_validate_assignment = cls.model_config.get("validate_assignment", False)
        if forbids_extra or should_validate_assignment:
            handler(values)
        values = DjangoGetter(obj=values, schema_cls=cls, context=info.context)
        return handler(values)
