"""Tooling to convert Django models and fields to Pydantic native models."""

from collections.abc import Callable
from enum import Enum, IntEnum
from types import UnionType
from typing import Any, Optional, TypeVar, override
from uuid import UUID

from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from pydantic import BaseModel, create_model
from pydantic._internal._model_construction import ModelMetaclass
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from django2pydantic.defaults import field_type_registry
from django2pydantic.mixin import BaseMixins
from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.types import Infer, InferExcept, ModelFields

SupportedParentFields = (
    models.Field[Any, Any]
    | models.ForeignObjectRel
    | GenericForeignKey
    | Callable[[], type]
)

CallableOutput = TypeVar("CallableOutput", int, str, bool, UUID, float)
DefaultCallable = Callable[..., CallableOutput]


DjangoModelFieldName = str
RelatedModelFields = tuple[str, set[str]]
RelatedModelListFieldsSchema = tuple[str, type[list[BaseModel]]]
RelatedModelFieldsSchema = tuple[str, type[BaseModel]]
ApiFields = set[
    DjangoModelFieldName
    | RelatedModelFields
    | RelatedModelListFieldsSchema
    | RelatedModelFieldsSchema
]


def has_property(cls: type, property_name: str) -> bool:
    return hasattr(cls, property_name) and isinstance(
        getattr(cls, property_name),
        property,
    )


def create_pydantic_model(
    django_model: type[models.Model],
    field_type_registry: FieldTypeRegistry,
    included_fields: ModelFields,
    bases: tuple[type[BaseModel], ...] | None = None,
    model_name: str | None = None,
) -> type[BaseModel]:
    """Create a Pydantic model from a Django model.

    included_fields: ModelFields = {
        "id": InferExcept(title="some name"),
        "name": Infer,
        "description": Field(None, title="some name"),
        "organization": {"id": Infer, "name": Infer},
        "applications": [BaseModel],
        "account": BaseModel,
    }

    Args:
        django_model (type[models.Model]): The Django model class.
        field_type_registry (FieldTypeRegistry): The field type registry.
        included_fields (ApiFields): The included fields.

    Returns:
        type[BaseModel]: The Pydantic model.

    """
    pydantic_fields: dict[
        str,
        tuple[
            type[BaseModel | list[BaseModel]] | type | Enum | IntEnum | UnionType,
            FieldInfo,
        ],
    ] = {}

    errors: list[str] = []

    for field_name, field_def in included_fields.items():
        # Check if the field is a property function:
        if has_property(django_model, field_name):
            django_field = getattr(django_model, field_name)
        else:
            try:
                django_field = django_model._meta.get_field(  # noqa: SLF001, WPS437
                    field_name=field_name,
                )
            except FieldDoesNotExist:
                errors.append(
                    f"The fields definition includes field '{field_name}' "
                    f"which is not found in the Django model '{django_model.__name__}'.",
                )
                continue

        if field_def is Infer:
            type_handler = field_type_registry.get_handler(django_field)
            python_type = type_handler.get_pydantic_type()
            pydantic_field_info: FieldInfo = type_handler.get_pydantic_field()

            pydantic_fields[field_name] = (python_type, pydantic_field_info)
        elif isinstance(field_def, InferExcept):
            type_handler = field_type_registry.get_handler(django_field)
            python_type = type_handler.get_pydantic_type()
            pydantic_field_info: FieldInfo = type_handler.get_pydantic_field()

            # Override the field values
            for detail_key, detail_value in field_def.args.items():
                setattr(pydantic_field_info, detail_key, detail_value)

            pydantic_fields[field_name] = (python_type, pydantic_field_info)
        # If the extracted fields is a type[pydantic.BaseModel]:
        elif isinstance(field_def, type) and issubclass(field_def, BaseModel):
            related_schema = field_def
            pydantic_fields[field_name] = (
                related_schema,
                FieldInfo(
                    title=field_name,
                    description=field_name,
                ),
            )
        elif isinstance(field_def, list):
            if not isinstance(field_def[0], BaseModel):
                errors.append(
                    f"Invalid field '{field_def}' definition for '{field_name}' "
                    f"in the Django model '{django_model.__name__}'"
                    f"Expected a Pydantic model class.",
                )
                continue
            related_schema = field_def[0]
            pydantic_fields[field_name] = (
                list[related_schema],
                FieldInfo(
                    title=field_name,
                    description=field_name,
                ),
            )
        elif isinstance(field_def, dict):
            related_django_model_name = field_name
            related_model_fields = field_def

            related_django_model = django_model._meta.get_field(  # noqa: SLF001, WPS437
                field_name=related_django_model_name,
            ).related_model

            if related_django_model is None:
                msg = (
                    f"The fields definition includes "
                    f"related model '{related_django_model_name}' "
                    f"which is not found in the Django model '{django_model.__name__}'"
                )
                errors.append(msg)
                continue

            related_schema = create_pydantic_model(
                related_django_model,
                field_type_registry,
                related_model_fields,
                model_name=f"{model_name}_{related_django_model_name}",
                bases=bases,
            )

            default = PydanticUndefined

            if isinstance(django_field, models.ManyToManyField):
                # TODO: Check if through model is set
                #   and if it defines the foreign key as unique
                #   then the return type should not be a list

                field_type = Optional[list[related_schema]]  # noqa: UP007
                default = None
            elif isinstance(django_field, models.OneToOneField):
                # 1
                field_type = related_schema
                if django_field.null:
                    field_type = Optional[related_schema]  # noqa: UP007
                    default = None
                else:
                    field_type = related_schema
            elif isinstance(django_field, models.ForeignKey):
                # 2
                if django_field.null:
                    field_type = Optional[related_schema]  # noqa: UP007
                    default = None
                else:
                    field_type = related_schema
            elif isinstance(django_field, models.OneToOneRel):
                # 3
                field_type = Optional[related_schema]  # noqa: UP007
                default = None
            elif isinstance(django_field, models.ManyToManyRel):
                # 4
                field_type = Optional[list[related_schema]]  # noqa: UP007
                default = None
            elif isinstance(django_field, models.ManyToOneRel):
                # 5
                field_type = Optional[list[related_schema]]  # noqa: UP007
                default = None
            else:
                errors.append(
                    "Unknown field type for related model ",
                )
                continue

            pydantic_fields[related_django_model_name] = (
                field_type,
                FieldInfo(
                    default=default,
                    title=related_django_model_name,
                    description=related_django_model_name,
                ),
            )
        else:
            errors.append(
                f"Invalid field definition for '{field_name}' "
                f"in the Django model '{django_model.__name__}'. Did not match any of the expected types."
                f"The field definition was: {field_def}"
                f"Expected one of: Infer, InferExcept, pydantic.BaseModel, list[pydantic.BaseModel], dict[str, str]",
            )

    if errors:
        msg = (
            f"Error creating Pydantic model from '{django_model.__name__}' Django model:"
            "\n\t❌ "
            "\n\t❌ ".join(errors)
        )
        raise AttributeError(msg)

    # Finally, create the Pydantic model:
    # https://docs.pydantic.dev/2.9/concepts/models/#dynamic-model-creation
    model_name = model_name or f"{django_model.__name__}Schema"
    return create_model(
        model_name,
        __base__=bases,
        **pydantic_fields,
    )


Bases = tuple[type[BaseModel]]
Namespace = dict[str, Any]
Kwargs = dict[str, Any]


class SuperSchemaResolver(ModelMetaclass):
    """Metaclass for django2pydantic."""

    @override
    def __new__(  # pylint: disable=W0222,C0204
        cls: type,
        name: str,
        bases: Bases,
        namespace: Namespace,
        **kwargs: Kwargs,
    ) -> type[BaseModel]:
        """Create a new django2pydantic class."""
        if name == "django2pydantic":
            return super().__new__(cls, name, bases, namespace, **kwargs)

        if "Meta" not in namespace:
            msg = f"Meta class is required for {name}"
            raise ValueError(msg)

        if getattr(namespace["Meta"], "model", None) is None:
            msg = f"model class is required in Meta class for {name}"
            raise ValueError(msg)

        model_class = namespace["Meta"].model
        if not issubclass(model_class, models.Model):
            msg = f"model_class must be a Django model, got {model_class}"
            raise TypeError(msg)

        # Check that included fields are present in the model Meta class
        if getattr(namespace["Meta"], "fields", None) is None:
            msg = f"model field is required in Meta class for {name}"
            raise ValueError(msg)

        model_name = getattr(namespace["Meta"], "name", None)

        return create_pydantic_model(
            model_class,
            field_type_registry,
            included_fields=namespace["Meta"].fields,
            model_name=model_name,
            bases=(BaseMixins, BaseModel),
        )
