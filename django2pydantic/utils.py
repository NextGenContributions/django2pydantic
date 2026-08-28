"""Utility functions for django2pydantic."""

from types import UnionType
from typing import TYPE_CHECKING

from pydantic.fields import FieldInfo

from django2pydantic.types import SupportedPydanticTypes

if TYPE_CHECKING:
    from django2pydantic import InferExcept


def override_type_and_meta(
    pydantic_type: UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes],
    field_info: FieldInfo,
    overrides: "InferExcept | None",
) -> tuple[
    UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes], FieldInfo
]:
    """Override the type and meta of a field using the provided overrides."""
    if not overrides:
        return pydantic_type, field_info

    # Create a field info with the values used from the original field and overrides
    # TODO(phuongfi91): Mutating FieldInfo's attrs is not reliable since mutations have
    #  to be also tracked in _attributes_set.
    #  Ideally there should be a way to construct another copy of FieldInfo based on the
    #  original (with potential overrides).
    #  Discussion is ongoing to determine the best approach in future pydantic after the
    #  breaking change in pydantic 2.12.0.
    #  Ref: https://github.com/pydantic/pydantic/issues/12374
    #  https://github.com/NextGenContributions/django-ninja-crudl/issues/35
    field_info_copy = field_info._copy()  # noqa: SLF001 # pyright: ignore[reportPrivateUsage]
    field_info_copy._attributes_set.update(overrides.args)  # noqa: SLF001 # pyright: ignore [reportCallIssue, reportArgumentType, reportPrivateUsage]
    for key, value in overrides.args.items():
        if key == "annotation":
            pydantic_type = value  # pyright: ignore[reportAssignmentType]
        else:
            setattr(field_info_copy, key, value)
    return pydantic_type, field_info_copy
