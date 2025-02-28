"""Number fields tests."""

import pydantic
import pytest
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    StepValueValidator,
)
from django.db import models

from tests.utils import pydantic_schema_from_field

IntegerField = type[
    models.SmallIntegerField[int, int]
    | models.IntegerField[int, int]
    | models.BigIntegerField[int, int]
    | models.PositiveBigIntegerField[int, int]
    | models.PositiveIntegerField[int, int]
    | models.PositiveSmallIntegerField[int, int]
    | models.SmallAutoField[int, int]
    | models.AutoField[int, int]
    | models.BigAutoField[int, int]
]

IntegerFields: list[IntegerField] = [
    models.SmallIntegerField[int, int],
    models.IntegerField[int, int],
    models.BigIntegerField[int, int],
    models.PositiveBigIntegerField[int, int],
    models.PositiveIntegerField[int, int],
    models.PositiveSmallIntegerField[int, int],
    models.SmallAutoField[int, int],
    models.AutoField[int, int],
    models.BigAutoField[int, int],
]


@pytest.mark.parametrize("django_field", IntegerFields)
def test_integer_field_min_value_validator_is_supported(
    django_field: IntegerField,
) -> None:
    """Test that the minimum value of an integer field is set."""
    field = django_field(
        validators=[MinValueValidator(10)],
    )

    pydantic_model = pydantic_schema_from_field(field)
    openapi_schema = pydantic_model.model_json_schema()
    assert openapi_schema["properties"]["field"]["minimum"] == 10
    with pytest.raises(pydantic.ValidationError):
        assert pydantic_model(field=9)


@pytest.mark.parametrize("django_field", IntegerFields)
def test_integer_field_max_value_validator_is_supported(
    django_field: IntegerField,
) -> None:
    """Test that the maximum value of an integer field is set."""
    field = django_field(
        validators=[MaxValueValidator(10)],
    )

    pydantic_model = pydantic_schema_from_field(field)
    openapi_schema = pydantic_model.model_json_schema()
    assert openapi_schema["properties"]["field"]["maximum"] == 10
    with pytest.raises(pydantic.ValidationError):
        assert pydantic_model(field=11)


@pytest.mark.parametrize("django_field", IntegerFields)
def test_step_value_validator_is_supported(
    django_field: IntegerField,
) -> None:
    """Test that the step value of an integer field is set."""
    field = django_field(
        validators=[StepValueValidator(2, offset=0)],
    )

    pydantic_model = pydantic_schema_from_field(field)
    openapi_schema = pydantic_model.model_json_schema()
    assert openapi_schema["properties"]["field"]["multipleOf"] == 2


@pytest.mark.parametrize("django_field", IntegerFields)
def test_example_value_is_set_based_on_le_and_or_ge(
    django_field: IntegerField,
) -> None:
    """Test that the example value is set based on the le and or ge values."""
    field = django_field(
        validators=[MinValueValidator(11), MaxValueValidator(20)],
    )

    pydantic_model = pydantic_schema_from_field(field)
    openapi_schema = pydantic_model.model_json_schema()
    assert openapi_schema["properties"]["field"]["example"] == [11, 20]
    assert pydantic_model(field=15)
