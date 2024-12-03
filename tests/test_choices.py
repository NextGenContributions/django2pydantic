"""Test choices are set as enum."""

from django.db import models
from django.utils.translation import gettext as _

from tests.utils import get_openapi_schema_from_field


def test_field_tuple_choices_are_set_as_enum() -> None:
    """Test that field choices are set as enum."""
    choices = [("a", "A"), ("b", "B"), ("c", "C")]
    openapi_schema = get_openapi_schema_from_field(models.CharField(choices=choices))
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
    assert openapi_schema["properties"]["field"]["enum"] == Choices.values
    assert openapi_schema["properties"]["field"]["type"] == "integer"
