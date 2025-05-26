"""Test string/non-string-based fields along with forward/reverse relational fields.

Default values, whether field is required and min-length (for string) are tested based
on a combination of Django field parameters: `null` and `blank`.

Expected outcomes are checked against pydantic fields and corresponding OpenAPI schema.
"""

# pyright: reportUnannotatedClassAttribute=false, reportUnknownVariableType=false, reportUnknownArgumentType=false
from collections.abc import Sequence
from typing import Any

import pytest
from django.db import models
from pydantic_core import PydanticUndefined

from tests.models import ForeignModel, M2MOptional, M2MRequired
from tests.utils import (
    DjangoField,
    django_model_factory,
    get_first_non_null_type,
    get_openapi_schema_from_field,
    get_pydantic_type_and_fieldinfo,
    has_null_type,
    type_is_nullable,
)


def generate_string_field_test_cases() -> Sequence[tuple[Any, bool, Any, int | None]]:  # pyright: ignore [reportExplicitAny]
    """Generate test cases for string-based Django fields.

    Returns:
        List of tuples containing
            (field, expected_is_required, expected_default, expected_min_length)
    """
    string_fields = [
        models.CharField,
        models.TextField,
        models.EmailField,
        models.SlugField,
    ]

    # Generate cases for regular string fields
    test_cases: list[tuple[Any, bool, Any, int | None]] = [  # pyright: ignore [reportExplicitAny]
        # URLField is special case - always has min_length=1 - defined by Ninja OpenAPI
        (models.URLField(null=True, blank=True), False, None, 1),
        (models.URLField(null=True, blank=False), True, PydanticUndefined, 1),
        (models.URLField(null=False, blank=True), False, "", 1),
        (models.URLField(null=False, blank=False), True, PydanticUndefined, 1),
    ]
    for field in string_fields:
        test_cases.extend(  # pyright: ignore [reportUnknownMemberType]
            [
                (field(null=True, blank=True), False, None, None),
                (field(null=True, blank=False), True, PydanticUndefined, 1),
                (field(null=False, blank=True), False, "", None),
                (field(null=False, blank=False), True, PydanticUndefined, 1),
            ]
        )
    return test_cases


def generate_non_string_field_test_cases() -> Sequence[
    tuple[Any, bool, Any, int | None]  # pyright: ignore [reportExplicitAny]
]:
    """Generate test cases for number-based Django fields.

    Returns:
        List of tuples containing
            (field, expected_is_required, expected_default, expected_min_length)
    """
    non_string_fields: list[
        type[models.Field[Any, Any]]  # pyright: ignore [reportExplicitAny]
        | tuple[type[models.Field[Any, Any]], dict[str, Any]]  # pyright: ignore [reportExplicitAny]
    ] = [
        # Number fields
        models.SmallIntegerField,
        models.IntegerField,
        models.BigIntegerField,
        models.PositiveSmallIntegerField,
        models.PositiveIntegerField,
        models.PositiveBigIntegerField,
        models.FloatField,
        (
            models.DecimalField,
            {
                "max_digits": 10,
                "decimal_places": 2,
            },
        ),
        # Miscellaneous fields
        models.BinaryField,
        models.BooleanField,
        models.DateField,
        models.DateTimeField,
        models.DurationField,
        models.FileField,
        models.FilePathField,
        models.GenericIPAddressField,
        models.ImageField,
        models.JSONField,
        models.TimeField,
        models.UUIDField,
    ]

    # Generate test cases
    test_cases = []
    for f in non_string_fields:
        field: type[models.Field[Any, Any]]  # pyright: ignore [reportExplicitAny]
        args: dict[str, Any] = {}  # pyright: ignore [reportExplicitAny]
        if isinstance(f, type):
            field = f
        else:
            field, args = f  # pyright: ignore [reportGeneralTypeIssues, reportExplicitAny]

        test_cases.extend(  # pyright: ignore [reportUnknownMemberType]
            [
                (field(null=True, blank=True, **args), False, None, None),
                (field(null=True, blank=False, **args), True, PydanticUndefined, None),
                (field(null=False, blank=True, **args), True, PydanticUndefined, None),
                (field(null=False, blank=False, **args), True, PydanticUndefined, None),
            ]
        )
    return test_cases


def generate_relational_field_test_cases() -> Sequence[
    tuple[Any, bool, Any, int | None]  # pyright: ignore [reportExplicitAny]
]:
    """Generate test cases for relational Django fields.

    Returns:
        List of tuples containing
            (field, expected_is_required, expected_default, expected_min_length)
    """
    relational_fields: list[
        type[models.Field[Any, Any]]  # pyright: ignore [reportExplicitAny]
        | tuple[type[models.Field[Any, Any]], dict[str, Any]]  # pyright: ignore [reportExplicitAny]
    ] = [
        (
            models.ForeignKey,
            {
                "to": ForeignModel,
                "on_delete": models.CASCADE,
            },
        ),
        (
            models.OneToOneField,
            {
                "to": ForeignModel,
                "on_delete": models.CASCADE,
            },
        ),
    ]

    # Include models.ManyToManyField cases, where only 'blank=X' matters
    test_cases: list[tuple[Any, bool, Any, int | None]] = [  # pyright: ignore [reportExplicitAny]
        (M2MOptional._meta.get_field("field"), False, None, None),  # noqa: SLF001  # pylint: disable=no-member  # pyright: ignore [reportUnknownMemberType]
        (M2MRequired._meta.get_field("field"), True, PydanticUndefined, None),  # noqa: SLF001  # pylint: disable=no-member  # pyright: ignore [reportUnknownMemberType]
    ]
    # Generate test cases
    for f in relational_fields:
        field: type[models.Field[Any, Any]]  # pyright: ignore [reportExplicitAny]
        args: dict[str, Any] = {}  # pyright: ignore [reportExplicitAny]
        if isinstance(f, type):
            field = f
        else:
            field, args = f  # pyright: ignore [reportGeneralTypeIssues, reportExplicitAny]

        test_cases.extend(  # pyright: ignore [reportUnknownMemberType]
            [
                (field(null=True, blank=True, **args), False, None, None),
                (field(null=True, blank=False, **args), True, PydanticUndefined, None),
                (field(null=False, blank=True, **args), True, PydanticUndefined, None),
                (field(null=False, blank=False, **args), True, PydanticUndefined, None),
            ]
        )

    # Add reverse cases, corresponding to forward relation cases, this includes:
    # - ManyToOneRel - ForeignKey
    # - OneToOneRel - OneToOneField
    # - ManyToManyRel - ManyToManyField
    reverse_rel_cases = []
    for case_field, _, _, _ in test_cases:  # pyright: ignore [reportUnknownMemberType]
        # Attach field to a model
        _ = django_model_factory(fields={"field": case_field})
        reverse_rel_cases.append((case_field.remote_field, False, None, None))  # pyright: ignore [reportUnknownMemberType]
    test_cases.extend(reverse_rel_cases)

    return test_cases


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("field", "expected_is_required", "expected_default", "expected_min_length"),
    [
        *generate_string_field_test_cases(),
        *generate_non_string_field_test_cases(),
        *generate_relational_field_test_cases(),
    ],
)
def test_fields(
    field: DjangoField,  # pyright: ignore [reportExplicitAny]
    expected_is_required: bool,  # noqa: FBT001
    expected_default: Any,  # noqa: ANN401  # pyright: ignore [reportExplicitAny]
    expected_min_length: int | None,
) -> None:
    """Test that a text field is required."""
    # Assert Pydantic's FieldInfo
    field_type, field_info = get_pydantic_type_and_fieldinfo(field)
    assert field_info.is_required() == expected_is_required
    assert field_info.default == expected_default
    assert field_info._attributes_set.get("min_length") == expected_min_length  # noqa: SLF001  # pyright: ignore [reportPrivateUsage]
    is_nullable = type_is_nullable(field_type)
    assert is_nullable == field.null, (
        f"Expected Optional: {field.null}, got: {is_nullable}"
    )

    # Assert OpenAPI schema
    openapi_schema = get_openapi_schema_from_field(field)
    assert openapi_schema.get("required", []) == (
        [field.name] if expected_is_required else []
    )
    assert (
        # "default" is not set if the pydantic field has PydanticUndefined as default
        openapi_schema["properties"][field.name].get("default", PydanticUndefined)
        == expected_default
    )
    not_null_type = get_first_non_null_type(openapi_schema["properties"][field.name])
    assert (
        # "minLength" is not set if the pydantic field has PydanticUndefined as default
        not_null_type.get("minLength") == expected_min_length
    )
    has_null = has_null_type(openapi_schema["properties"][field.name])
    assert has_null == field.null, f"Expected Optional: {field.null}, got: {has_null}"
