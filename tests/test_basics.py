"""Test cases for Django models to Pydantic models conversion."""

import uuid
from string import printable
from typing import Any

import pytest
from django.db import models
from django.utils.translation import gettext_lazy as _
from hypothesis import given
from hypothesis import strategies as st

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer
from tests.utils import debug_json, get_openapi_schema_from_field

FieldClass = type[models.Field[Any, Any]]

AutoFields: list[FieldClass] = [models.AutoField, models.BigAutoField]

DjangoFieldTypes: list[FieldClass] = [
    models.BigIntegerField,
    models.BooleanField,
    models.CharField,
    models.DateField,
    models.DateTimeField,
    models.DecimalField,
    models.DurationField,
    models.EmailField,
    models.FileField,
    models.FilePathField,
    models.FloatField,
    models.ImageField,
    models.IntegerField,
    models.GenericIPAddressField,
    models.PositiveIntegerField,
    models.PositiveSmallIntegerField,
    models.PositiveBigIntegerField,
    models.SlugField,
    models.SmallIntegerField,
    models.TextField,
    models.TimeField,
    models.URLField,
    models.UUIDField,
    models.BinaryField,
    models.JSONField,
]

DjangoRelationalFields = [
    models.ForeignKey,
    models.OneToOneField,
    models.ManyToManyField,
]


def get_test_data_for_field(
    field: FieldClass,
) -> str | int | float | bool | uuid.UUID | bytes | dict[str, str]:
    """Get the test data for the given field."""
    datas = {
        models.CharField: "test",
        models.TextField: "test",
        models.IntegerField: 100,
        models.FloatField: 100.0,
        models.BooleanField: True,
        models.DateField: "2021-01-01",
        models.DateTimeField: "2021-01-01T00:00:00",
        models.DecimalField: 100.0,
        models.DurationField: "1 day",
        models.EmailField: "test@test.com",
        models.FileField: "test.txt",
        models.FilePathField: "test.txt",
        models.ImageField: "test.jpg",
        models.GenericIPAddressField: "192.168.0.1",
        models.PositiveIntegerField: 100,
        models.PositiveSmallIntegerField: 100,
        models.PositiveBigIntegerField: 100,
        models.SlugField: "test",
        models.TimeField: "00:00:00",
        models.URLField: "http://example.com",
        models.UUIDField: str(uuid.uuid4()),
        models.BinaryField: b"test",
        models.JSONField: {"test": "test"},
        models.BigIntegerField: 100,
        models.SmallIntegerField: 100,
    }
    return datas[field]


def is_correct_field_type_and_format(
    field: FieldClass,
    type_: str,
    format: str | None,
) -> bool:
    """Check the given field type and format whether they match the desired OpenAPI types."""
    datas = {
        models.CharField: {"type": "string", "format": None},
        models.TextField: {"type": "string", "format": None},
        models.IntegerField: {"type": "integer", "format": None},
        models.FloatField: {"type": "number", "format": None},
        models.BooleanField: {"type": "boolean", "format": None},
        models.DateField: {"type": "string", "format": "date"},
        models.DateTimeField: {"type": "string", "format": "date-time"},
        models.DecimalField: {"type": "number", "format": None},
        models.DurationField: {"type": "string", "format": "duration"},
        models.BinaryField: {"type": "string", "format": "binary"},
        models.FileField: {"type": "string", "format": "file"},
        models.FilePathField: {"type": "string", "format": "file-path"},
        models.ImageField: {"type": "string", "format": "image"},
        models.GenericIPAddressField: {"type": "string", "format": "ipvanyaddress"},
        models.IPAddressField: {"type": "string", "format": "ipv4"},
        models.PositiveIntegerField: {"type": "integer", "format": None},
        models.PositiveSmallIntegerField: {"type": "integer", "format": None},
        models.PositiveBigIntegerField: {"type": "integer", "format": None},
        models.SlugField: {"type": "string", "format": None},
        models.TimeField: {"type": "string", "format": "time"},
        models.URLField: {"type": "string", "format": "uri"},
        models.UUIDField: {"type": "string", "format": "uuid"},
        models.BigIntegerField: {"type": "integer", "format": None},
        models.SmallIntegerField: {"type": "integer", "format": None},
        models.EmailField: {"type": "string", "format": "email"},
        models.JSONField: {"type": "object", "format": None},
        models.SmallAutoField: {"type": "integer", "format": None},
        models.AutoField: {"type": "integer", "format": None},
        models.BigAutoField: {"type": "integer", "format": None},
    }
    return datas[field]["type"] == type_ and datas[field]["format"] == format


@pytest.mark.skip(reason="WOOF")
@pytest.mark.parametrize("field", DjangoFieldTypes)
@given(
    help_text=st.text(alphabet=printable).filter(
        condition=lambda help_text: help_text != "",
    ),
)
def test_field_description_is_set_from_help_text(
    field: FieldClass,
    help_text: str,
) -> None:
    """Test that the field description is set from the help text if it exists."""
    openapi_schema = get_openapi_schema_from_field(field(help_text=help_text))
    assert (
        openapi_schema["properties"]["field"]["description"].strip()
        == help_text.strip()
    )


@pytest.mark.skip(reason="WOOF")
@pytest.mark.parametrize("field", DjangoFieldTypes)
def test_field_type_and_format_is_correct_openapi_equivalent(field: FieldClass) -> None:
    """Test that the field type and format is correct OpenAPI equivalent."""
    openapi_schema = get_openapi_schema_from_field(field())
    field_format = openapi_schema["properties"]["field"].get("format", None)
    debug_json(openapi_schema)
    assert is_correct_field_type_and_format(
        field=field,
        type_=openapi_schema["properties"]["field"]["type"],
        format=field_format,
    )


@pytest.mark.skip(reason="WOOF")
@pytest.mark.parametrize("field", DjangoFieldTypes)
@given(
    help_text=st.text(alphabet=printable).filter(
        condition=lambda help_text: help_text != "",
    ),
)
def test_field_description_is_set_from_lazy_translated_help_text(
    field: FieldClass,
    help_text: str,
) -> None:
    """Test that the OpenAPI field description is set from the Django field's help text if it exists."""
    openapi_schema = get_openapi_schema_from_field(field(help_text=_(help_text)))
    assert openapi_schema["properties"]["field"]["description"].strip().replace(
        "\r",
        "",
    ).replace("\n", "") == help_text.strip().replace("\r", "").replace("\n", "")


@pytest.mark.skip(reason="WOOF")
@pytest.mark.parametrize("field", DjangoFieldTypes)
@given(
    verbose_name=st.text(alphabet=printable).filter(
        condition=lambda verbose_name: verbose_name != "",
    ),
)
def test_field_description_is_set_from_verbose_name_if_no_help_text(
    field: FieldClass,
    verbose_name: str,
) -> None:
    """Test that the field description is set from the verbose name if it exists."""
    openapi_schema = get_openapi_schema_from_field(field(verbose_name=verbose_name))
    assert (
        openapi_schema["properties"]["field"]["description"].strip().lower()
        == verbose_name.strip().lower()
    )


@pytest.mark.skip(reason="WOOF")
@pytest.mark.parametrize("field", DjangoFieldTypes)
@given(
    verbose_name=st.text(alphabet=printable).filter(
        condition=lambda verbose_name: verbose_name != "",
    ),
)
def test_field_description_is_set_from_lazy_translated_verbose_name_if_no_help_text(
    field: FieldClass,
    verbose_name: str,
) -> None:
    """Test that the field description is set from the verbose name if it exists."""
    openapi_schema = get_openapi_schema_from_field(field(verbose_name=_(verbose_name)))
    assert openapi_schema["properties"]["field"][
        "description"
    ].strip().lower().strip().replace("\r", "").replace(
        "\n",
        "",
    ) == verbose_name.strip().lower().strip().replace("\r", "").replace("\n", "")


@pytest.mark.skip(reason="WOOF")
@pytest.mark.parametrize("field", DjangoFieldTypes)
def test_default_value_is_set(field: FieldClass) -> None:
    """Test that the default value is set."""
    default_value = get_test_data_for_field(field)
    openapi_schema = get_openapi_schema_from_field(field(default=default_value))
    assert openapi_schema["properties"]["field"]["default"] == default_value


@pytest.mark.parametrize("field", DjangoFieldTypes)
def test_null_field_sets_field_as_not_required(field: FieldClass) -> None:
    """Test that null fields are not required."""
    openapi_schema = get_openapi_schema_from_field(field(null=True))
    assert openapi_schema.get("required", []) == []


@pytest.mark.parametrize("field", DjangoFieldTypes)
def test_non_null_field_sets_as_required(field: FieldClass) -> None:
    """Test that non-null fields are required."""
    openapi_schema = get_openapi_schema_from_field(field(null=False))
    assert openapi_schema.get("required", []) == ["field"]


def test_schema_subclassing_works() -> None:
    """Test that schema subclassing works."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig(
            model=ModelA,
            fields={
                "id": Infer,
                "name": Infer,
            },
        )

    class SchemaB(SchemaA):
        """SchemaB class."""

    openapi_schema = SchemaB.model_json_schema()
    assert openapi_schema["properties"]["name"]["type"] == "string"
