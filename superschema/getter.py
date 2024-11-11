"""Getter for Pydantic related Django models."""

from typing import Any, reveal_type

from django.db.models import Manager, QuerySet
from django.db.models.fields.files import FieldFile

__all__ = [
    "DjangoGetter",
]

Result = list[Any] | list[Any] | None | str | Any


class DjangoGetterMixin:
    """Mixin for DjangoGetter."""

    def _convert_result(
        self,
        result: Any,
    ) -> Result:
        """Convert the result to a serializable format."""
        if isinstance(result, Manager):
            print("MANAGER", result)
            return list(result.all())

        if isinstance(result, getattr(QuerySet, "__origin__", QuerySet)):
            print("QUERYSET")
            return list(result)

        if callable(result):
            return result()

        if isinstance(result, FieldFile):
            if not result:
                return None
            return result.url

        return result


class DjangoGetter(DjangoGetterMixin):
    """Getter for Pydantic related Django models."""

    __slots__ = ("_obj", "_schema_cls", "_context")

    def _get_prefetched_values(self, key: str) -> Result:
        """Get the prefetched values.

        Example:
        key = some_key
        self._obj = {
            "some_key__id": 1,
            "some_key__name": "Some Name",
        }
        """
        values = {}
        for k, v in self._obj.items():
            if k.startswith(f"{key}__"):
                values[k[len(key) + 2 :]] = v

        return values

    def __init__(self, obj: Any, schema_cls: Any, context: Any = None) -> None:
        self._obj = obj
        self._schema_cls = schema_cls
        self._context = context
        print("OBJ", self._obj)
        reveal_type(self._obj)
        print(type(self._obj))
        print("SCHEMA", self._schema_cls)
        reveal_type(self._schema_cls)
        print(type(self._schema_cls))

    def __getattr__(self, key: str) -> Result:
        """Get the attribute from the object."""
        if key.startswith("__pydantic"):
            return getattr(self._obj, key)

        # If the model_dump attribute is called
        if key == "model_dump":
            # we need to return the pydantic schema .model_dump method
            return self._schema_cls(**self._obj).model_dump

        if isinstance(self._obj, dict):
            if key not in self._obj:
                return self._get_prefetched_values(key)
                print(f"Key {key} not found in {self._obj}")
                raise AttributeError(key)
            value = self._obj[key]
        else:
            try:
                value = getattr(self._obj, key)
            except AttributeError as e:
                print(f"AttributeError: {e}")
                raise AttributeError(key) from e

        print(f"{key} -> {value}")

        return self._convert_result(value)
