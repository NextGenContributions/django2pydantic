"""Handlers for relational fields."""

from abc import ABC
from types import UnionType
from typing import Annotated, Any, Generic, TypeVar, Union, override

from django.db import models
from django.db.models.fields.related import RelatedField
from django.utils.encoding import force_str
from pydantic_core import PydanticUndefined

from django2pydantic.handlers.base import DjangoFieldHandler, PydanticConverter
from django2pydantic.types import (
    ForwardRel,
    GetType,
    ReverseRel,
    SetType,
    SupportedParentFields,
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
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        if not isinstance(self.field_obj, RelatedField):
            msg = (
                f"Expected 'field_obj' to be of type 'RelatedField', "
                f"got {type(self.field_obj)} instead"
            )
            raise TypeError(msg)

        pydantic_type = self._get_field_type_handler(
            self.field_obj.target_field  # pyright: ignore [reportUnknownMemberType, reportUnknownArgumentType]
        ).get_pydantic_type()

        # ManyToManyField: null has no effect since there is no way to require a
        # relationship at the database level.
        # Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#manytomanyfield
        if not self.field_obj.many_to_many and self.field_obj.null:
            return Union[pydantic_type, None]  # type: ignore[return-value]  # noqa: UP007
        return pydantic_type

    def _get_field_type_handler(
        self, field: models.Field[GetType, SetType]
    ) -> PydanticConverter[SupportedParentFields]:
        """Return the field type handler."""
        from django2pydantic.registry import FieldTypeRegistry

        return FieldTypeRegistry.instance().get_handler(field)

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
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return Annotated[self.get_pydantic_type_raw(), self.get_pydantic_field()]  # type: ignore[return-value]


class OneToOneFieldHandler(
    RelatedFieldHandler[models.OneToOneField[models.Model, models.Model]]
):
    """Handler for OneToOne fields."""

    @classmethod
    @override
    def field(cls) -> type[models.OneToOneField[models.Model, models.Model]]:
        return models.OneToOneField

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return Annotated[self.get_pydantic_type_raw(), self.get_pydantic_field()]  # type: ignore[return-value]


class ManyToManyFieldHandler(
    RelatedFieldHandler[models.ManyToManyField[models.Model, models.Model]],
):
    """Handler for ManyToMany fields."""

    @classmethod
    @override
    def field(cls) -> type[models.ManyToManyField[models.Model, models.Model]]:
        return models.ManyToManyField

    @property
    @override
    def default(self) -> Any:  # pyright: ignore [reportAny, reportExplicitAny]
        """Return the default value of the field."""
        if self.field_obj.has_default() and not callable(self.field_obj.default):  # pyright: ignore [reportAny]
            return self.field_obj.default  # pyright: ignore [reportAny]
        if self.field_obj.blank:
            # ManyToManyField: null has no effect since there is no way to require a
            # relationship at the database level.
            # Ref: https://docs.djangoproject.com/en/5.1/ref/models/fields/#manytomanyfield
            return None
        return PydanticUndefined

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return (
            list[Annotated[self.get_pydantic_type_raw(), self.get_pydantic_field()]]  # type: ignore[misc]
            | None
        )


class ReverseRelatedFieldHandler(
    Generic[TDjangoReverseField], RelatedFieldHandler[TDjangoReverseField]
):
    """Base handler for reverse relation fields."""

    @property
    @override
    def default(self) -> None:
        return None  # So that the field is not marked as required

    @property
    @override
    def description(self) -> None:
        # TODO(jhassine): https://github.com/NextGenContributions/django2pydantic/issues/88
        return None

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return self._get_field_type_handler(self.field_obj).get_pydantic_type()


class ManyToManyRelHandler(ReverseRelatedFieldHandler[models.ManyToManyRel]):
    """Handler for ManyToMany reverse relation."""

    @classmethod
    @override
    def field(cls) -> type[models.ManyToManyRel]:
        return models.ManyToManyRel

    @property
    @override
    def title(self) -> str | None:
        if vn := self.related_model._meta.verbose_name_plural:  # noqa: SLF001 # pyright: ignore [reportOptionalMemberAccess]
            return force_str(vn)
        return super().title

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return (
            list[Annotated[self.get_pydantic_type_raw(), self.get_pydantic_field()]]  # type: ignore[misc]
            | None
        )


class OneToOneRelHandler(ReverseRelatedFieldHandler[models.OneToOneRel]):
    """Handler for OneToOne reverse relation."""

    @classmethod
    @override
    def field(cls) -> type[models.OneToOneRel]:
        return models.OneToOneRel

    @property
    @override
    def title(self) -> str | None:
        if vn := self.related_model._meta.verbose_name:  # noqa: SLF001  # pyright: ignore [reportOptionalMemberAccess]
            return force_str(vn)
        return super().title

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        return Annotated[self.get_pydantic_type_raw() | None, self.get_pydantic_field()]  # type: ignore[return-value,operator]


class ManyToOneRelHandler(ReverseRelatedFieldHandler[models.ManyToOneRel]):
    """Handler for ManyToOne reverse relation."""

    @classmethod
    @override
    def field(cls) -> type[models.ManyToOneRel]:
        return models.ManyToOneRel

    @property
    @override
    def title(self) -> str | None:
        if vn := self.related_model._meta.verbose_name_plural:  # noqa: SLF001  # pyright: ignore [reportOptionalMemberAccess]
            return force_str(vn)
        return super().title

    @override
    def get_pydantic_type(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field."""
        return (
            list[Annotated[self.get_pydantic_type_raw(), self.get_pydantic_field()]]  # type: ignore[misc]
            | None
        )
