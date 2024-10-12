"""Example of using superschema.schema.ApiFields."""

from ast import TypeVar
from typing import Any, TypedDict, Union, reveal_type

from pydantic import BaseModel, Field

from superschema.types import Infer, InferExcept

SubClassOfPydanticBaseModel_co = TypeVar(
    "SubClassOfPydanticBaseModel_co",
    bound=BaseModel,
    covariant=True,
)


class ApiSchema:
    def __new__(cls, *args, **kwargs) -> BaseModel:
        """Create a new ApiSchema class."""
        print("args", args)
        print("kwargs", kwargs)

        class SomeModel(BaseModel):
            id: int

        return SomeModel()


FieldType = dict[
    str,
    Union[
        InferExcept,
        type[Infer],
        Any,
        list[type[BaseModel]],
        type[BaseModel],
        "FieldType",
    ],
]

create_fields: FieldType = {
    "id": InferExcept(title="some name"),
    "name": Infer,
    "description": Field(None, title="some name"),
    "organization": {"id": Infer, "name": Infer},
    "applications": [BaseModel],
    "account": BaseModel,
}

reveal_type(create_schema)

In python why does this not work?

class Model(TypedDict):
    attr: str


m: Model = {"attr": "value"}

t: dict[str, Any] = m

Incompatible types in assignment (expression has type "Model", variable has type "dict[str, Any]") Mypy assignment
Type "Model" is not assignable to declared type "dict[str, Any]"
  "Model" is not assignable to "dict[str, Any]" Pylance reportAssignmentType