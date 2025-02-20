"""Tooling to convert Django models and fields to Pydantic native models."""

from enum import Enum, IntEnum
from types import UnionType
from typing import Optional

from beartype import beartype
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.types import Infer, InferExcept, ModelFields

type PydanticFields = dict[
    str,
    tuple[
        type[BaseModel | list[BaseModel] | object] | Enum | IntEnum | UnionType,
        FieldInfo,
    ],
]


@beartype
def has_property(cls: type[object], property_name: str) -> bool:
    """Check if a class has a property."""
    return hasattr(cls, property_name) and isinstance(
        getattr(cls, property_name),
        property,
    )


def create_pydantic_model(  # noqa: C901, PLR0912, PLR0915, WPS210, WPS231 # NOSONAR
    django_model: type[models.Model],
    field_type_registry: FieldTypeRegistry,
    fields: ModelFields,
    bases: tuple[type[BaseModel], ...] | None = None,
    model_name: str | None = None,
) -> type[BaseModel]:
    """Create a Pydantic model from a Django model.

    Args:
        django_model (type[models.Model]): The Django model class.
        field_type_registry (FieldTypeRegistry): The field type registry.
        fields (ModelFields): The included fields.
        bases (tuple[type[BaseModel], ...], optional): The base classes for the Pydantic model. Defaults to None.
        model_name (str, optional): The name of the Pydantic model. Defaults to None.

    Returns:
        type[BaseModel]: The Pydantic model.

    Raises:
        ValueError: If included_fields is None.
        AttributeError: If there are errors creating the Pydantic model.
    """
    model_name = model_name or f"{django_model.__name__}Schema"

    pydantic_fields: PydanticFields = {}

    errors: list[str] = []

    for field in fields:
        if isinstance(field, str):
            field_name = field
            field_def = Infer
        else:
            field_name, field_def = field

        pydantic_fields[field_name] = (
            Infer,
            FieldInfo(title=field_name, description=field_name),
        )

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
            pydantic_field_info = type_handler.get_pydantic_field()
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
                f"which does not exists in the Django model '{django_model.__name__}'. "
                f"The field definition was: {field_def} "
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
    return create_model(
        model_name,
        __base__=bases,
        **pydantic_fields,
    )  # pyright: ignore[reportCallIssue]
