"""Tooling to convert Django models and fields to Pydantic native models."""

from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Generic, TypeVar, override

from beartype import beartype
from pydantic import BaseModel, ConfigDict
from pydantic._internal._model_construction import ModelMetaclass

from django2pydantic.base import create_pydantic_model
from django2pydantic.defaults import field_type_registry
from django2pydantic.mixin import BaseMixins
from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.types import (
    DictStrAny,
    ModelFields,
    ModelFieldsCompact,
    TDjangoModel_co,
)

SType = TypeVar("SType", bound=BaseModel)


@beartype
def has_property(cls: type[object], property_name: str) -> bool:
    """Check if a class has a property."""
    return hasattr(cls, property_name) and isinstance(
        getattr(cls, property_name),
        property,
    )


Bases = tuple[type[BaseModel]]


class SchemaResolver(ModelMetaclass):
    """Metaclass for django2pydantic."""

    @override
    def __new__(
        mcs: type[ModelMetaclass],
        cls_name: str,
        bases: Bases,
        namespace: DictStrAny,
        **kwargs: DictStrAny,
    ) -> type[BaseModel]:
        """Create a new Schema class."""
        # Python calls the metaclass with the BaseSchema class too
        # so we need to check if the class is the BaseSchema class
        # and return it as is as we are only interested in the
        # classes that inherit from it.
        is_final_or_not_specified = bool(getattr(namespace, "__final__", True))
        is_abstract_or_not_specified = bool(getattr(namespace, "__abstract__", False))
        is_base_schema_by_name = (
            cls_name.startswith("BaseSchema")
            and namespace.get("__module__") == "django2pydantic.schema"
        )
        has_config = "config" in namespace
        if (
            not has_config
            or is_base_schema_by_name
            or not is_final_or_not_specified
            or is_abstract_or_not_specified
        ):
            return super().__new__(mcs, cls_name, bases, namespace)  # pyright: ignore[reportUnknownVariableType]

        config = namespace.get("config")

        if config is None or not isinstance(config, SchemaConfig):
            fully_qualified_name = f"{namespace.get('__module__')}.{cls_name}"
            required_config_fqn = (
                f"{SchemaConfig.__module__}.{SchemaConfig.__qualname__}"
            )
            msg = (
                f"Schema configuration is required for class '{fully_qualified_name}'. "
                f"Expected an instance of '{required_config_fqn}', got '{config}'."
            )
            raise ValueError(msg)

        if config.field_type_registry is None:
            config.field_type_registry = field_type_registry

        return create_pydantic_model(
            config.model,
            config.field_type_registry,
            fields=config.fields,
            model_name=config.name,
            bases=(BaseMixins, BaseModel),
        )


@dataclass(init=True, kw_only=True)
class SchemaConfig(Generic[TDjangoModel_co]):
    """Schema configuration."""

    model: type[TDjangoModel_co]
    """Django model class."""

    fields: ModelFields | ModelFieldsCompact
    """Model's fields to be included in the schema."""

    field_type_registry: FieldTypeRegistry | None = None
    """Field type registry to be used.

    Field type registry is used to resolve Django model fields to Pydantic field types.

    If not provided, the default field type registry will be used.
    """

    name: str | None = None
    """Schema name.

    If not provided, the schema name will be automatically generated.
    """


class BaseSchema(BaseModel, Generic[TDjangoModel_co], ABC, metaclass=SchemaResolver):
    """django2pydantic BaseSchema class."""

    config: SchemaConfig[TDjangoModel_co]
    """Schema configuration."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
    """Pydantic model configuration.

    See:
    https://docs.pydantic.dev/2.10/concepts/config/
    """

    """
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
    """
