"""Test cases for Django models to Pydantic models conversion."""

from typing import Any

from django.db import models

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer

FieldClass = type[models.Field[Any, Any]]


DjangoRelationalFields = [
    models.ForeignKey,
    models.OneToOneField,
    models.ManyToManyField,
]


def test_related_field_description_is_set_from_help_text() -> None:
    """Test that the field description is set from the help text if it exists."""
    help_text = "This is a test help text for the field."

    class TestModel(models.Model):
        field = models.ForeignKey(
            help_text=help_text,
            on_delete=models.CASCADE,
            to="self",
            related_name="related_field",
        )

        class Meta:
            app_label = "test_app"

    class FieldSchema(BaseSchema):
        config = SchemaConfig(model=TestModel, fields={"id": Infer, "field": Infer})

    openapi_schema = FieldSchema.model_json_schema()
    assert (
        openapi_schema["properties"]["field"]["description"].strip()
        == help_text.strip()
    )


def test_related_field_title_is_set_from_verbose_name() -> None:
    """Test that the field title is set from the verbose name if it exists."""
    title = "This is a test title for the field."

    class TestModel(models.Model):
        field = models.ForeignKey(
            verbose_name=title,
            on_delete=models.CASCADE,
            to="self",
            related_name="related_field",
        )

        class Meta:
            app_label = "test_app"

    class FieldSchema(BaseSchema):
        config = SchemaConfig(model=TestModel, fields={"id": Infer, "field": Infer})

    openapi_schema = FieldSchema.model_json_schema()
    assert openapi_schema["properties"]["field"]["title"].strip() == title.strip()
