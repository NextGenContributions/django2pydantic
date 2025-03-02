"""Shared types within the package."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, TypeVar, Union, Unpack, override

from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models.fields.related import RelatedField
from pydantic import BaseModel
from pydantic.fields import (  # noqa: WPS450
    FieldInfo,
    _FromFieldInfoInputs,  # pyright: ignore[reportPrivateUsage]
)


@dataclass(unsafe_hash=True)
class Infer:
    """Used as a marker for inferring the details of a field."""


@dataclass(unsafe_hash=True)
class InferExcept:
    """Infer except override some values.

    Example:
    ```
    InferExcept(title="My Title", description="My Description")
    ```
    """

    @override
    def __init__(self, **kwargs: Unpack[_FromFieldInfoInputs]) -> None:
        """Initialize the InferExcept class."""
        super().__init__()
        self.args: _FromFieldInfoInputs = kwargs


type ModelFields = (
    dict[
        str,
        type[Infer | BaseModel]
        | InferExcept
        | FieldInfo
        | list[type[BaseModel]]
        | ModelFields,
    ]
    | None
)

type ModelFieldsCompact = list[
    str
    | tuple[
        str,
        type[Infer | BaseModel]
        | InferExcept
        | FieldInfo
        | list[type[BaseModel]]
        | ModelFieldsCompact,
    ]
]
"""Field definition for the schema.

Example:
>>> my_fields: ModelFields = [
...     "name",
...     (
...         "description",
...         InferExcept(
...             title="My better title", description="My better description", max_length=100
...         ),
...     ),
...     "organization_id",
...     ("some_field_to_be_inferred", Infer),
...     ("with_base_model", pydantic.BaseModel),
...     ("with_list_of_base_model", [pydantic.BaseModel]),
...     ("with_pydantic_field_info", FieldInfo(description="My description")),
...     ("some_related_model", ["related_model_id", "related_model_description"]),
... ]

NOTE:

When used with pyre type checker it will raise an error:
`Undefined or invalid type [11]: Annotation ModelFields is not defined as a type.`

This is a known issue with pyre not supporting recursive type aliases:
https://github.com/facebook/pyre-check/issues/813

You need to comment the line with the error in order to make it work: pyre-ignore[11]
"""


# Defining some variables to be used with django-stubs generics
# in order to avoid using typing.Any:
# __set__ value type
type SetType = Any  # pyright: ignore[reportExplicitAny] # pyre-ignore[33]
"""Type for the set value of a field.

To be used with the Django Stubs library for field _ST annotations.

Ref: https://github.com/typeddjango/django-stubs/blob/9d6c8f49e271935832509b108dbeb20b9ce9af3f/django-stubs/db/models/fields/__init__.pyi#L47-L52
"""

type GetType = Any  # pyright: ignore[reportExplicitAny] # pyre-ignore[33]
"""Type for the get value of a field.

To be used with the Django Stubs library for field _GT annotations.

Ref: https://github.com/typeddjango/django-stubs/blob/9d6c8f49e271935832509b108dbeb20b9ce9af3f/django-stubs/db/models/fields/__init__.pyi#L47-L52
"""

# Field types supported by the library
type SupportedParentFields = Union[  # pyright: ignore[reportDeprecated] # noqa: UP007
    models.Field[SetType, GetType],
    RelatedField[models.Model, models.Model],
    GenericForeignKey,
    models.ForeignObjectRel,
    Callable[[], type[object]],
    property,
    type[property],
]
"""This type is used to define the parent field types that are supported by the library.

This includes Django's fields such as:
* regular fields,
* related fields and
* property decorators.
"""

TFieldType_co = TypeVar("TFieldType_co", bound=SupportedParentFields, covariant=True)
"""Represents the supported parent field types to be used with library's generics."""

TDjangoModel_co = TypeVar("TDjangoModel_co", bound=models.Model, covariant=True)

type DictStrAny = dict[str, Any]  # pyright: ignore[reportExplicitAny]
"""Type for a dictionary with string keys and any values."""
