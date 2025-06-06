"""Handler for django-pydantic-field SchemaField.

Ref: https://github.com/surenkov/django-pydantic-field
"""

from types import UnionType
from typing import override

from django_pydantic_field.v2.fields import PydanticSchemaField

from django2pydantic.handlers.base import DjangoFieldHandler
from django2pydantic.types import SupportedPydanticTypes


class SchemaFieldHandler(DjangoFieldHandler[PydanticSchemaField]):  # pyright: ignore [reportExplicitAny]
    """Handler for django-pydantic-field SchemaField."""

    @classmethod
    @override
    def field(cls) -> type[PydanticSchemaField]:
        return PydanticSchemaField

    @override
    def get_pydantic_type_raw(
        self,
    ) -> UnionType | SupportedPydanticTypes | list[SupportedPydanticTypes]:
        """Return the Pydantic type of the field.

        Extract the schema from the PydanticSchemaField and return it as the type.
        """
        # Get the schema from the adapter
        schema = self.field_obj.adapter.prepared_schema
        if schema is not None:
            return schema  # type: ignore[return-value]

        # Fallback to the raw schema if prepared_schema is not available
        if hasattr(self.field_obj, "schema") and self.field_obj.schema is not None:
            return self.field_obj.schema  # type: ignore[return-value]

        # If no schema is available, return dict as a fallback
        return dict  # type: ignore[return-value]
