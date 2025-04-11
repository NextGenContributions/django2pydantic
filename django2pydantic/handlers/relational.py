"""Handlers for relational fields."""

from abc import ABC
from typing import Annotated, Any, Generic, TypeVar, override, Sequence

from django.db import models
from pydantic.fields import FieldInfo

from django2pydantic.handlers.base import DjangoFieldHandler
from django2pydantic.types import (
    ForwardRel,
    ReverseRel,
    SupportedPydanticTypes,
)

TDjangoReverseField = TypeVar(
    "TDjangoReverseField",
    bound=ReverseRel,
)

TDjangoRelatedField = TypeVar(
    "TDjangoRelatedField",
    bound=ForwardRel | ReverseRel,
)


class RelatedFieldHandler(
    Generic[TDjangoRelatedField], DjangoFieldHandler[TDjangoRelatedField], ABC
):
    """Base handler for Related fields."""

    @property
    @override
    def ge(self) -> int | None:
        return None

    @property
    @override
    def gt(self) -> int | None:
        return None

    @property
    @override
    def le(self) -> int | None:
        return None

    @property
    @override
    def lt(self) -> int | None:
        return None

    @override
    def get_pydantic_type_raw(self) -> SupportedPydanticTypes:
        """Return the Pydantic type of the field."""
        from django2pydantic.registry import FieldTypeRegistry

        return (
            FieldTypeRegistry.instance().get_handler(self.field_obj).get_pydantic_type()
        )

    # TODO(phuongfi91): https://github.com/NextGenContributions/django2pydantic/issues/50
    # @property
    # def _examples(
    #     self,
    # ) -> list[Any] | None:  # PRAGMA: NO COVER  # pyright: ignore [reportExplicitAny]
    #     """Return the example value(s) of the field.
    #
    #     Currently disabled as marked as protected method.
    #
    #     There might be some use case to provide example values for the fields,
    #     by using limit_choices_to or default values.
    #     """
    #     lct = self.field_obj.get_limit_choices_to()
    #     if self.field_obj.choices:
    #         return list(
    #             self.field_obj.get_choices(
    #                 include_blank=self.field_obj.blank,
    #                 limit_choices_to=lct,
    #             ),
    #         )
    #     if self.field_obj.has_default():
    #         if not callable(self.field_obj.default):
    #             return [self.field_obj.default]
    #         if callable(self.field_obj.default):
    #             return [self.field_obj.default()]
    #     return None


class ForeignKeyHandler(
    RelatedFieldHandler[models.ForeignKey[models.Model, models.Model]]
):
    """Handler for ForeignKey fields."""

    @classmethod
    @override
    def field(cls) -> type[models.ForeignKey[models.Model, models.Model]]:
        return models.ForeignKey

    @override
    def get_pydantic_type(self) -> Annotated[SupportedPydanticTypes, Any]:
        """Return the Pydantic type of the field."""
        from django2pydantic.registry import FieldTypeRegistry

        field_info: FieldInfo = (
            FieldTypeRegistry.instance()
            .get_handler(self.field_obj)
            .get_pydantic_field()
        )
        return Annotated[self.get_pydantic_type_raw(), field_info]  # type: ignore[return-value]


class OneToOneFieldHandler(
    RelatedFieldHandler[models.OneToOneField[models.Model, models.Model]]
):
    """Handler for OneToOne fields."""

    @classmethod
    @override
    def field(cls) -> type[models.OneToOneField[models.Model, models.Model]]:
        return models.OneToOneField


class ManyToManyFieldHandler(
    RelatedFieldHandler[models.ManyToManyField[models.Model, models.Model]],
):
    """Handler for ManyToMany fields."""

    @classmethod
    @override
    def field(cls) -> type[models.ManyToManyField[models.Model, models.Model]]:
        return models.ManyToManyField

    @override
    def get_pydantic_type(self) -> Sequence[Annotated[SupportedPydanticTypes, Any]]:
        """Return the Pydantic type of the field."""
        from django2pydantic.registry import FieldTypeRegistry

        field_info: FieldInfo = (
            FieldTypeRegistry.instance()
            .get_handler(self.field_obj)
            .get_pydantic_field()
        )
        return list[Annotated[self.get_pydantic_type_raw(), field_info]]  # type: ignore[return-value,misc]


class ReverseRelHandler(
    Generic[TDjangoReverseField], RelatedFieldHandler[TDjangoReverseField]
):
    """Base handler for reverse relation fields."""

    @property
    @override
    def default(self) -> None:
        return None  # So that the field is not marked as required

    @override
    def get_pydantic_type_raw(self) -> SupportedPydanticTypes:
        """Return the Pydantic type of the field."""
        from django2pydantic.registry import FieldTypeRegistry

        return (
            FieldTypeRegistry.instance().get_handler(self.field_obj).get_pydantic_type()
        )


class ManyToManyRelHandler(ReverseRelHandler[models.ManyToManyRel]):
    """Handler for ManyToMany reverse relation."""

    @classmethod
    @override
    def field(cls) -> type[models.ManyToManyRel]:
        return models.ManyToManyRel

    @override
    def get_pydantic_type(self) -> list[Annotated[SupportedPydanticTypes, Any]]:
        """Return the Pydantic type of the field."""
        from django2pydantic.registry import FieldTypeRegistry

        field_info: FieldInfo = (
            FieldTypeRegistry.instance()
            .get_handler(self.field_obj)
            .get_pydantic_field()
        )
        return list[Annotated[self.get_pydantic_type_raw(), field_info]]  # type: ignore[return-value,misc]


class OneToOneRelHandler(ReverseRelHandler[models.OneToOneRel]):
    """Handler for OneToOne reverse relation."""

    @classmethod
    @override
    def field(cls) -> type[models.OneToOneRel]:
        return models.OneToOneRel

    @override
    def get_pydantic_type(self) -> SupportedPydanticTypes:
        return self.get_pydantic_type_raw() | None


class ManyToOneRelHandler(ReverseRelHandler[models.ManyToOneRel]):
    """Handler for ManyToOne reverse relation."""

    @classmethod
    @override
    def field(cls) -> type[models.ManyToOneRel]:
        return models.ManyToOneRel

    @override
    def get_pydantic_type(self) -> type[Annotated[Any, Any]]:
        """Return the Pydantic type of the field."""
        from django2pydantic.registry import FieldTypeRegistry

        field_info: FieldInfo = (
            FieldTypeRegistry.instance()
            .get_handler(self.field_obj)
            .get_pydantic_field()
        )
        return list[Annotated[self.get_pydantic_type_raw(), field_info]]
