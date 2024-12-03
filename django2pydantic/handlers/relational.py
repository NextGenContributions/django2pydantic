"""Handlers for relational fields."""

from abc import ABC
from typing import Annotated, Any, override

from django.apps import apps
from django.db import models
from django.db.models.base import ModelBase
from django.db.models.fields.related import RelatedField
from pydantic.fields import FieldInfo

from django2pydantic.handlers.base import DjangoFieldHandler
from django2pydantic.registry import FieldTypeRegistry


class RelatedFieldHandler[TDjangoModel: RelatedField[Any, Any]](
    DjangoFieldHandler[TDjangoModel], ABC
):
    """Base handler for Related fields."""

    @override
    def get_pydantic_type_raw(self):
        """Return the Pydantic type of the field."""
        return (
            FieldTypeRegistry.instance()
            .get_handler(self._get_target_field())
            .get_pydantic_type()
        )

    def _get_target_field(self) -> models.Field[Any, Any]:
        """Return the target field of the relation."""
        if getattr(self.field_obj, "to_field", False) and isinstance(
            self.field_obj.to_field,
            ModelBase,
        ):
            target_field = self.field_obj.related_model._meta.get_field(
                self.field_obj.to_field,
            )
        elif isinstance(self.field_obj.related_model, str):
            if "." in self.field_obj.related_model:
                app_label = self.field_obj.related_model.split(".")[0]
                model_name = self.field_obj.related_model.split(".")[1]
                target_field = apps.get_model(  # noqa: SLF001
                    app_label=app_label, model_name=model_name
                )._meta.pk
            elif self.field_obj.related_model != "self":
                app_label = self.field_obj.model._meta.app_label  # type: ignore[unreachable]  # noqa: SLF001, WPS437
                model_name = self.field_obj.related_model
                try:
                    target_field = apps.get_model(  # noqa: SLF001
                        app_label=app_label, model_name=model_name
                    )._meta.pk
                except LookupError as lookup_exception:
                    msg = (
                        f"{lookup_exception}\n"
                        f"For field '{self.field_obj.name}'"
                        f" in model '{self.field_obj.model.__name__}',"
                        f" did not find related model {self.field_obj.related_model}. "
                        "If you are using string references to models,"
                        " use the format 'app_label.ModelName'.\n"
                        "More information: https://docs.djangoproject.com/en/5.1/ref/models/fields/#absolute-relationships"
                    )
                    raise ValueError(
                        msg,
                    ) from lookup_exception

            if self.field_obj.related_model == "self":
                target_field = self.field_obj.model._meta.pk
        else:
            target_field = self.field_obj.related_model._meta.pk
        if not target_field:
            msg = f"Related model {self.field_obj.related_model} does not have a primary key field."
            raise ValueError(
                msg,
            )  # This should never happen, but just in case, we raise an error here.
        return target_field

    @property
    def _examples(self) -> list[Any] | None:  # PRAGMA: NO COVER
        """Return the example value(s) of the field.

        Currently disabled as marked as protected method.

        There might be some use case to provide example values for the fields,
        by using limit_choices_to or default values.
        """
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


class ForeignKeyHandler(RelatedFieldHandler[models.ForeignKey[models.Model]]):
    """Handler for ForeignKey fields."""

    @override
    @classmethod
    def field(cls) -> type[models.ForeignKey[models.Model]]:
        return models.ForeignKey


class OneToOneFieldHandler(RelatedFieldHandler[models.OneToOneField[models.Model]]):
    """Handler for OneToOne fields."""

    @override
    @classmethod
    def field(cls) -> type[models.OneToOneField[models.Model]]:
        return models.OneToOneField


class ManyToManyFieldHandler(
    RelatedFieldHandler[models.ManyToManyField[models.Model, models.Model]],
):
    """Handler for ManyToMany fields."""

    @override
    @classmethod
    def field(cls) -> type[models.ManyToManyField[models.Model, models.Model]]:
        return models.ManyToManyField

    @override
    def get_pydantic_type(self) -> type[list[Annotated[Any, Any]]]:
        """Return the Pydantic type of the field."""
        field_info: FieldInfo = (
            FieldTypeRegistry.instance()
            .get_handler(self._get_target_field())
            .get_pydantic_field()
        )
        return list[Annotated[self.get_pydantic_type_raw(), field_info]]
