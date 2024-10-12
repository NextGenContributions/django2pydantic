"""Test cases for Django models to Pydantic models conversion."""

import json
import uuid
from pathlib import Path
from random import randint
from string import printable
from typing import Any, ClassVar

import pydantic
import pytest
from django.db import models
from django.utils.translation import gettext_lazy as _
from hypothesis import given
from hypothesis import strategies as st
from rich import print_json

from superschema.schema import SuperSchema
from superschema.types import Infer, MetaFields, ModelFields

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
    # models.EmailField,
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

"""
Tests
choices are set as enum
choices are set as examples
Different choice definitions are supported
decimal values are set correctly
Charfield max_length is set correctly
Charfield, etc pattern is set correctly
exception is raised on included field that is not found
Default value is set
Default factory is set
Foreignkey and One-to-one field column names are included
Related fields are included
Property methods are included
Property setters are included
Related fields primary key type is
EmailStr is set
Ipaddress
Urlfield
Jsonfield
Is extensible with custom type handler
Model documentation is used as schema documentation
"""

DjangoField = models.Field[Any, Any]

JSONValue = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def debug_json(json_data: JSONValue) -> None:  # pragma: no cover
    """Print pretty the JSON value with indentation."""
    json_str: str = json.dumps(json_data)
    print_json(data=json_str, indent=4)
    with Path("debug.json").open("w") as file:
        file.write(json_str)


def django_model_factory(
    fields: dict[str, DjangoField],
) -> type[models.Model]:
    """Create a Django model with the given fields."""
    meta_attrs: dict[str, str] = {
        "app_label": "tests",
    }

    attrs = {
        "__module__": "django.db.models",
        **fields,
        "Meta": type("Meta", (), meta_attrs),
    }
    model_name = f"TestModel{randint(0, 10000000)}"
    return type(model_name, (models.Model,), attrs)


def pydantic_schema_from_field(field: DjangoField) -> type[pydantic.BaseModel]:
    """Create a Pydantic model from a Django model field."""
    field_name = "field"
    model: type[models.Model] = django_model_factory(fields={field_name: field})
    fields_def: ModelFields = {field_name: Infer}
    meta_class_attrs: MetaFields = {
        "model": model,
        "fields": fields_def,
    }
    meta_class = type("Meta", (), dict(meta_class_attrs))

    return type(
        "Schema",
        (SuperSchema,),
        {
            "Meta": meta_class,
        },
    )


def get_openapi_schema_from_field(field: DjangoField) -> dict[str, Any]:
    """Get the OpenAPI schema from a Django model field."""
    schema: type[pydantic.BaseModel] = pydantic_schema_from_field(field)
    return schema.model_json_schema()


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
    """Test that the field description is set from the help text if it exists."""
    openapi_schema = get_openapi_schema_from_field(field(help_text=_(help_text)))
    assert openapi_schema["properties"]["field"]["description"].strip().replace(
        "\r",
        "",
    ).replace("\n", "") == help_text.strip().replace("\r", "").replace("\n", "")


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


def test_uuid_field_is_supported() -> None:
    """Test that UUID fields are supported."""
    openapi_schema = get_openapi_schema_from_field(models.UUIDField())
    assert openapi_schema["properties"]["field"]["type"] == "string"
    assert openapi_schema["properties"]["field"]["format"] == "uuid"


def test_uuid1_field_is_supported() -> None:
    """Test that UUID fields are supported."""
    openapi_schema = get_openapi_schema_from_field(models.UUIDField(default=uuid.uuid1))
    assert openapi_schema["properties"]["field"]["type"] == "string"
    assert openapi_schema["properties"]["field"]["format"] == "uuid1"


def test_uuid4_field_is_supported() -> None:
    """Test that UUID fields are supported."""
    openapi_schema = get_openapi_schema_from_field(models.UUIDField(default=uuid.uuid4))
    assert openapi_schema["properties"]["field"]["type"] == "string"
    assert openapi_schema["properties"]["field"]["format"] == "uuid4"


def test_field_tuple_choices_are_set_as_enum() -> None:
    """Test that field choices are set as enum."""
    choices = [("a", "A"), ("b", "B"), ("c", "C")]
    openapi_schema = get_openapi_schema_from_field(models.CharField(choices=choices))
    debug_json(openapi_schema)
    assert openapi_schema["$defs"]["FieldEnum"]["enum"] == [
        choice[0] for choice in choices
    ]
    assert openapi_schema["properties"]["field"]["$ref"] == "#/$defs/FieldEnum"
    assert openapi_schema["$defs"]["FieldEnum"]["type"] == "string"


def test_field_enum_choices_are_set_as_enum() -> None:
    """Test that field's enum choices are set as enum."""

    class Choices(models.TextChoices):
        AA = "a"
        BB = "b"
        CC = "c"

    openapi_schema = get_openapi_schema_from_field(
        models.CharField(choices=Choices.choices),
    )
    debug_json(openapi_schema)
    assert openapi_schema["$defs"]["FieldEnum"]["enum"] == Choices.values
    assert openapi_schema["properties"]["field"]["$ref"] == "#/$defs/FieldEnum"
    assert openapi_schema["$defs"]["FieldEnum"]["type"] == "string"


def test_field_enum_choices_with_label_are_set_as_enum() -> None:
    """Test that field's enum choices are set as enum."""

    class Choices(models.TextChoices):
        AA = "a", "Aaa"
        BB = "b", "Bee"
        CC = "c", "Cee"

    openapi_schema = get_openapi_schema_from_field(
        models.CharField(choices=Choices.choices),
    )
    debug_json(openapi_schema)
    assert openapi_schema["$defs"]["FieldEnum"]["enum"] == Choices.values
    assert openapi_schema["properties"]["field"]["$ref"] == "#/$defs/FieldEnum"
    assert openapi_schema["$defs"]["FieldEnum"]["type"] == "string"


def test_field_enum_choices_with_translated_label_are_set_as_enum() -> None:
    """Test that field's enum choices are set as enum."""

    class Choices(models.TextChoices):
        A = "a", _("Aaa")
        B = "b", _("Bee")
        C = "c", _("Cee")

    openapi_schema = get_openapi_schema_from_field(
        models.CharField(choices=Choices.choices),
    )
    debug_json(openapi_schema)
    assert openapi_schema["$defs"]["FieldEnum"]["enum"] == Choices.values
    assert openapi_schema["properties"]["field"]["$ref"] == "#/$defs/FieldEnum"
    assert openapi_schema["$defs"]["FieldEnum"]["type"] == "string"


def test_field_integer_enum_choices_are_set_as_enum() -> None:
    """Test that field's enum choices are set as enum."""

    class Choices(models.IntegerChoices):
        A = 1, "Aaa"
        B = 2, "Bee"
        C = 3, "Cee"

    openapi_schema = get_openapi_schema_from_field(
        models.IntegerField(choices=Choices.choices),
    )
    # print(openapi_schema)
    debug_json(openapi_schema)
    assert openapi_schema["properties"]["field"]["enum"] == Choices.values
    assert openapi_schema["properties"]["field"]["type"] == "integer"


def test_foreign_key_field_to_primary_key_is_supported() -> None:
    """Test that foreign key fields are supported."""
    related_model = django_model_factory(fields={})
    openapi_schema = get_openapi_schema_from_field(
        models.ForeignKey(related_model, on_delete=models.CASCADE),
    )
    assert openapi_schema["properties"]["field"]["type"] == "integer"


def test_foreign_key_field_with_to_field_is_supported() -> None:
    """Test that foreign key fields are supported."""
    related_model = django_model_factory(
        fields={"someid": models.SmallIntegerField(unique=True)},
    )
    openapi_schema = get_openapi_schema_from_field(
        models.ForeignKey(related_model, on_delete=models.CASCADE, to_field="someid"),
    )
    assert openapi_schema["properties"]["field"]["type"] == "integer"


def test_models_can_have_nested_models() -> None:
    """Test that models can have nested models."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)

    class SchemaB(SuperSchema):
        """SchemaB class."""

        class Meta(SuperSchema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "name": Infer,
                },
            }

    openapi_schema = SchemaB.model_json_schema()
    debug_json(openapi_schema)
    assert openapi_schema["properties"]["rel_a"]["type"] == "object"
    assert (
        openapi_schema["properties"]["rel_a"]["properties"]["id"]["type"] == "integer"
    )
    assert (
        openapi_schema["$defs"]["ModelASchema"]["properties"]["name"]["type"]
        == "string"
    )
