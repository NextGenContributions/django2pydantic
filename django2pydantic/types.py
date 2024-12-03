"""Public types for django2pydantic."""

from typing import TypedDict, Union, Unpack, override

from django.db.models import Model
from pydantic import BaseModel
from pydantic.fields import FieldInfo, _FromFieldInfoInputs


class Infer:
    """Used as a marker for inferring the type of a field."""


_InferExceptArgs = Unpack[_FromFieldInfoInputs]


class InferExcept:
    """Used as a marker for inferring the type of a field but overriding some field values."""

    @override
    def __init__(self, **kwargs: Unpack[_FromFieldInfoInputs]) -> None:
        """Initialize the InferExcept class."""
        super().__init__()
        self.args: _FromFieldInfoInputs = kwargs


ModelFields = (
    dict[
        str,
        Union[
            type[Infer],
            InferExcept,
            FieldInfo,
            type[BaseModel],
            list[type[BaseModel]],
            "ModelFields",
        ],
    ]
    | None
)


class MetaFields(TypedDict):
    """TypedDict for meta fields."""

    model: type[Model]
    fields: ModelFields
