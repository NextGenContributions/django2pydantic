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
    TDjangoModel,
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
    """Metaclass for BaseSchema."""

    @override
    def __new__(  # pylint: disable=signature-differs
        mcs: type[ModelMetaclass],  # noqa: N804
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
            return super().__new__(  # type: ignore[no-any-return,misc]
                mcs,
                cls_name,  # pyright: ignore [reportCallIssue]
                bases,
                namespace,
            )

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
            config.model,  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
            config.field_type_registry,
            fields=config.fields,
            model_name=config.name,
            bases=(BaseMixins, BaseModel),
        )


@dataclass(init=True, kw_only=True)
class SchemaConfig(Generic[TDjangoModel]):
    """Schema configuration."""

    model: type[TDjangoModel]
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


class BaseSchema(BaseModel, Generic[TDjangoModel], ABC, metaclass=SchemaResolver):
    """django2pydantic BaseSchema class."""

    config: SchemaConfig[TDjangoModel]
    """Schema configuration."""

    model_config: ClassVar[ConfigDict] = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
    """Pydantic model configuration.

    See:
    https://docs.pydantic.dev/2.10/concepts/config/
    """
