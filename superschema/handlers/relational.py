"""Handlers for relational fields."""

from typing import Any, override

from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields.related import RelatedField

from superschema.handlers.base import DjangoFieldHandler
from superschema.registry import FieldTypeRegistry


class RelatedFieldHandler(DjangoFieldHandler[RelatedField[Any, Any]]):
    """Base handler for Related fields."""

    @property
    @override
    def examples(self) -> list[Any] | None:
        """Return the example value(s) of the field."""
        lct = self.field_obj.get_limit_choices_to()
        if self.field_obj.choices:
            return list(
                self.field_obj.get_choices(
                    include_blank=self.field_obj.blank,
                    limit_choices_to=lct,
                ),
            )
        if self.field_obj.has_default():
            if not callable(self.field_obj.default):
                return [self.field_obj.default]
            if callable(self.field_obj.default):
                return [self.field_obj.default()]
        return None


class ForeignKeyHandler(DjangoFieldHandler[models.ForeignKey[models.Model]]):
    """Handler for ForeignKey fields."""

    @override
    @classmethod
    def field(cls) -> type[models.ForeignKey[models.Model]]:
        return models.ForeignKey

    @override
    def get_pydantic_type_raw(self):
        if hasattr(self.field_obj, "to_field") and isinstance(
            self.field_obj.to_field,
            ModelBase,
        ):
            target_field = self.field_obj.related_model._meta.get_field(
                self.field_obj.to_field,
            )
        else:
            target_field = self.field_obj.related_model._meta.pk
        if not target_field:
            msg = f"Related model {self.field_obj.related_model} does not have a primary key field."
            raise ValueError(
                msg,
            )  # This should never happen, but just in case, we raise an error here.
        return (
            FieldTypeRegistry.instance().get_handler(target_field).get_pydantic_type()
        )


class OneToOneFieldHandler(DjangoFieldHandler[models.OneToOneField[models.Model]]):
    """Handler for OneToOne fields."""

    @override
    @classmethod
    def field(cls) -> type[models.OneToOneField[models.Model]]:
        return models.OneToOneField

    @override
    def get_pydantic_type_raw(self):
        if hasattr(self.field_obj, "to_field") and isinstance(
            self.field_obj.to_field,
            ModelBase,
        ):
            target_field = self.field_obj.related_model._meta.get_field(
                self.field_obj.to_field,
            )
        else:
            target_field = self.field_obj.related_model._meta.pk
        if not target_field:
            msg = f"Related model {self.field_obj.related_model} does not have a primary key field."
            raise ValueError(
                msg,
            )  # This should never happen, but just in case, we raise an error here.
        return (
            FieldTypeRegistry.instance().get_handler(target_field).get_pydantic_type()
        )
