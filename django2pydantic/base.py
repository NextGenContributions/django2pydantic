"""Tooling to convert Django models and fields to Pydantic native models."""

from enum import Enum, IntEnum
from types import UnionType
from typing import TYPE_CHECKING, Any, cast

from beartype import beartype
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import FieldDoesNotExist
from django.db.models import (
    Field,
    ForeignKey,
    ForeignObjectRel,
    ManyToManyField,
    ManyToManyRel,
    ManyToOneRel,
    Model,
    OneToOneField,
    OneToOneRel,
)
from pydantic import BaseModel, create_model, field_validator
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined

from django2pydantic.mixin import BaseMixins
from django2pydantic.registry import FieldTypeRegistry
from django2pydantic.types import (
    GetType,
    Infer,
    InferExcept,
    ModelFields,
    ModelFieldsCompact,
    SetType,
    TDjangoModel,
)

if TYPE_CHECKING:
    from collections.abc import Callable

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
    django_model: type[TDjangoModel],
    field_type_registry: FieldTypeRegistry,
    fields: ModelFields | ModelFieldsCompact,
    bases: tuple[type[BaseModel], ...] | None = None,
    model_name: str | None = None,
) -> type[BaseModel]:
    """Create a Pydantic model from a Django model.

    Args:
        django_model (type[models.Model]): The Django model class.
        field_type_registry (FieldTypeRegistry): The field type registry.
        fields (ModelFields | ModelFieldsCompact): The included fields.
        bases (tuple[type[BaseModel], ...], optional): The base classes for the Pydantic
            model. Defaults to None.
        model_name (str, optional): The name of the Pydantic model. Defaults to None.

    Returns:
        type[BaseModel]: The Pydantic model.

    Raises:
        ValueError: If included_fields is None.
        AttributeError: If there are errors creating the Pydantic model.
    """
    model_name = model_name or f"{django_model.__name__}Schema"

    pydantic_fields: PydanticFields = {}

    validators: dict[str, Callable[..., Any]] = {}  # pyright: ignore [reportExplicitAny]

    errors: list[str] = []

    if fields is None:
        msg = "The 'fields' argument is required."
        raise ValueError(msg)

    # for field_name, field_def in fields.items():
    field_name: str
    field_def: (
        type[Infer | BaseModel]
        | InferExcept
        | FieldInfo
        | list[type[BaseModel]]
        | ModelFields
        | ModelFieldsCompact
    )
    for field in fields:
        field_name, field_def = _get_field_info(field, fields)

        pydantic_fields[field_name] = (
            Infer,
            FieldInfo(title=field_name, description=field_name),
        )

        # Get django field if exists in the Django model:
        try:
            django_field = _get_django_field(
                django_model=django_model, field_name=field_name
            )
        except ValueError as e:
            errors.append(str(e))
            continue

        # TODO(jhassine): Make this works and move to function
        #  https://github.com/NextGenContributions/django2pydantic/issues/41
        # # Register the Django field's validators as field validators in Pydantic models
        # if use_django_validators and isinstance(django_field, Field):
        #     for validator in django_field.validators:
        #         if callable(validator):
        #             validators[f"{field_name}_{validator.__str__()}"] = field_validator(
        #                 field_name,
        #                 mode="after",
        #             )(validator)

        pydantic_field_info: FieldInfo
        if field_def is Infer:
            type_handler = field_type_registry.get_handler(django_field)
            python_type = type_handler.get_pydantic_type()
            pydantic_field_info = type_handler.get_pydantic_field()
            pydantic_fields[field_name] = (python_type, pydantic_field_info)

            if type(django_field) in {  # noqa: WPS516
                ForeignKey,
                ManyToOneRel,
                ManyToManyField,
                ManyToManyRel,
                OneToOneField,
                OneToOneRel,
            }:
                validators[f"{field_name}_relation"] = field_validator(
                    field_name,
                    mode="wrap",
                )(BaseMixins.validate_relation)

        elif isinstance(field_def, InferExcept):
            type_handler = field_type_registry.get_handler(django_field)
            python_type = type_handler.get_pydantic_type()
            pydantic_field_info = type_handler.get_pydantic_field()

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
            if not isinstance(field_def[0], type(BaseModel)):
                errors.append(
                    f"Invalid field '{field_def}' definition for '{field_name}' "
                    f"in the Django model '{django_model.__name__}'"
                    f"Expected a Pydantic model class.",
                )
                continue
            related_schema = field_def[0]
            pydantic_fields[field_name] = (
                list[related_schema],  # type: ignore[valid-type]
                FieldInfo(
                    title=field_name,
                    description=field_name,
                ),
            )

        elif isinstance(field_def, dict):
            related_django_model_name = field_name
            related_model_fields = field_def

            # Create related model if it's a valid Django model:
            try:
                related_schema = _recursively_create_related_schema(
                    django_model=django_model,
                    field_type_registry=field_type_registry,
                    field_name=field_name,
                    bases=bases,
                    model_name=model_name,
                    related_django_model_name=related_django_model_name,
                    related_model_fields=related_model_fields,
                )
            except ValueError as e:
                errors.append(str(e))
                continue

            # Determine the field type based on the relationship type:
            try:
                field_type, field_info = _determine_field_type(  # pyright: ignore [reportAny]
                    django_field=django_field,
                    related_django_model_name=related_django_model_name,
                    related_schema=related_schema,
                    field_type_registry=field_type_registry,
                )
                pydantic_fields[related_django_model_name] = (field_type, field_info)
            except ValueError as e:
                errors.append(str(e))
                continue

        else:
            errors.append(
                f"Invalid field definition for '{field_name}' "
                f"which does not exists in the Django model '{django_model.__name__}'. "
                f"The field definition was: {field_def} "
            )

    if errors:
        msg = (
            f"Error creating Pydantic model from '{django_model.__name__}' "
            "Django model:"
            "\n\t❌ "
            "\n\t❌ ".join(errors)
        )
        raise AttributeError(msg)

    # Finally, create the Pydantic model:
    # https://docs.pydantic.dev/2.9/concepts/models/#dynamic-model-creation
    return create_model(
        model_name,
        __base__=bases,
        __config__=None,
        __doc__=None,
        __module__=__name__,
        __validators__=validators,
        __cls_kwargs__=None,
        **pydantic_fields,
    )


def _get_django_field(
    *,
    django_model: type[Model],
    field_name: str,
) -> Field[GetType, SetType] | ForeignObjectRel | GenericForeignKey | property:
    # Check if the field is a property function:
    if has_property(django_model, field_name):
        return cast("property", getattr(django_model, field_name))
    try:
        return django_model._meta.get_field(  # noqa: SLF001, WPS437 # pyright: ignore[reportUnknownVariableType,reportUnknownMemberType]
            field_name=field_name,
        )
    except FieldDoesNotExist as e:
        available_fields = django_model._meta.get_fields(  # noqa: SLF001
            include_hidden=True, include_parents=True
        )
        available_field_names = [
            field.name for field in available_fields if field.name != field_name
        ]

        msg = (
            f"The fields definition includes field '{field_name}' which "
            f"is not found in the Django model '{django_model.__name__}'. "
            f"The available fields are: "
            f"{', '.join(available_field_names) if available_field_names else 'None'}."
        )
        raise ValueError(msg) from e


def _get_field_info(
    field: str | tuple[str, Any],  # pyright: ignore [reportExplicitAny]
    fields: ModelFields | ModelFieldsCompact,
) -> tuple[str, Any]:  # pyright: ignore [reportExplicitAny]
    """Retrieve field information from the given fields."""
    if isinstance(field, str):
        field_name = field
        if isinstance(fields, dict):
            try:
                # In case of a dict
                field_def = fields[field]
            except KeyError:
                # Key doesn't exist
                field_def = Infer
        else:
            # We're dealing with a non-dict iterable
            field_def = Infer
    else:
        field_name, field_def = field  # pyright: ignore [reportAny]
    return field_name, field_def


def _recursively_create_related_schema(  # noqa: PLR0913
    *,
    django_model: type[Model],
    field_type_registry: FieldTypeRegistry,
    field_name: str,
    bases: tuple[type[BaseModel], ...] | None,
    model_name: str,
    related_django_model_name: str,
    related_model_fields: ModelFields | ModelFieldsCompact,
) -> type[BaseModel]:
    related_django_model = django_model._meta.get_field(  # noqa: SLF001, WPS437 # pyright: ignore[reportUnknownMemberType]
        field_name=related_django_model_name,
    ).related_model

    if related_django_model is None:
        msg = (
            f"The fields definition includes "
            f"related model '{related_django_model_name}' "
            f"which is not found in the Django model '{django_model.__name__}'"
        )
        raise ValueError(msg)

    nested_dj_model: type[Model]
    if isinstance(related_django_model, type) and issubclass(
        related_django_model, Model
    ):
        nested_dj_model = related_django_model
    elif related_django_model == "self":
        # If the related model is "self", then we use the current model
        # Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#recursive
        nested_dj_model = django_model
    else:
        msg = (
            f"The related model '{related_django_model_name}' "
            f"for field '{field_name}' in the Django model "
            f"'{django_model.__name__}' "
            f"is not a valid Django model."
        )
        raise ValueError(msg)

    return create_pydantic_model(
        nested_dj_model,
        field_type_registry,
        related_model_fields,
        model_name=f"{model_name}_{related_django_model_name}",
        bases=bases,
    )


def _determine_field_type(
    *,
    django_field: Field[SetType, GetType]
    | ForeignObjectRel
    | GenericForeignKey
    | property,
    related_django_model_name: str,
    related_schema: type[BaseModel],
    field_type_registry: FieldTypeRegistry,
) -> tuple[Any, FieldInfo]:  # pyright: ignore [reportExplicitAny]
    """Determine the field type and create a FieldInfo for related models."""
    default: PydanticUndefined | None = PydanticUndefined  # type: ignore[valid-type]
    field_type: Any  # noqa: F821  # pyright: ignore [reportExplicitAny]

    dj_field_type = type(django_field)
    if dj_field_type in {ForeignKey, OneToOneField, OneToOneRel}:
        if django_field.null:  # type: ignore[union-attr]  # type narrowing doesn't work
            field_type = related_schema | None  # noqa: UP007  # pyright: ignore [reportAny]
            default = None  # pyright: ignore [reportUnknownVariableType]
        else:
            field_type = related_schema  # pyright: ignore [reportAny]
    elif dj_field_type in {ManyToManyField, ManyToManyRel, ManyToOneRel}:
        # TODO(jhassine): Check if through model is set and if it defines the foreign
        #   key as unique then the return type should not be a list
        #   Ref: https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ManyToManyField.through_fields
        #   https://github.com/NextGenContributions/django2pydantic/issues/41
        field_type = list[related_schema] | None  # type: ignore[valid-type]
        default = None  # pyright: ignore [reportUnknownVariableType]
    else:
        msg = (
            f"Unknown field type {django_field} for "
            f"related model {related_django_model_name}"
        )
        raise TypeError(msg)

    type_handler = field_type_registry.get_handler(django_field)
    title = type_handler.title
    description = type_handler.description

    return (
        field_type,
        FieldInfo(
            default=default,
            title=title,
            description=description,
        ),
    )
