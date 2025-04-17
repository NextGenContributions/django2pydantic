# TODO(phuongfi91): pylint disable for all tests
# pylint: disable=too-few-public-methods

import uuid

import pytest
from django.db import models

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer
from tests.utils import django_model_factory, get_openapi_schema_from_field


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
        fields={"someid": models.CharField(unique=True)},
    )
    openapi_schema = get_openapi_schema_from_field(
        models.ForeignKey(related_model, on_delete=models.CASCADE, to_field="someid"),
    )
    assert openapi_schema["properties"]["field"]["type"] == "string"


def test_foreign_key_field() -> None:
    """Test that models can have nested models."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ForeignKey[ModelA, ModelA](ModelA, on_delete=models.CASCADE)

    class SchemaB(BaseSchema[ModelB]):
        """SchemaB class."""

        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            },
        )

    openapi_schema = SchemaB.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_foreign_key_field_with_to_field_works() -> None:
    """Test that foreign key fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100, unique=True)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ForeignKey[ModelA, ModelA](
            ModelA, on_delete=models.CASCADE, to_field="var"
        )

    class SchemaB(BaseSchema[ModelB]):
        """SchemaB class."""

        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            },
        )

    openapi_schema = SchemaB.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_many_to_many_field_works() -> None:
    """Test that many to many fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ManyToManyField[ModelA, ModelA](ModelA)

    class SchemaB(BaseSchema[ModelB]):
        """SchemaB class."""

        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            },
        )

    openapi_schema = SchemaB.model_json_schema()

    # 'rel_a' should either be an 'array' or 'null'
    rel_a_types = openapi_schema["properties"]["rel_a"]["anyOf"]
    assert sorted([item["type"] for item in rel_a_types]) == ["array", "null"]

    # 'rel_a' array item's properties should be defined
    array_type = next(
        r
        for r in openapi_schema["properties"]["rel_a"]["anyOf"]
        if r["type"] == "array"
    )
    ref = array_type["items"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"


def test_one_to_one_field_works() -> None:
    """Test that one to one fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.OneToOneField[ModelA, ModelA](ModelA, on_delete=models.CASCADE)

    class SchemaB(BaseSchema[ModelB]):
        """SchemaB class."""

        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            },
        )

    openapi_schema = SchemaB.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_many_to_one_relations_works() -> None:
    """Test that many-to-one relations are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ForeignKey[ModelA, ModelA](
            ModelA, related_name="rel_b", on_delete=models.CASCADE
        )

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "id": Infer,
                "var": Infer,
                "rel_b": {
                    "id": Infer,
                    "name": Infer,
                },
            },
        )

    openapi_schema = SchemaA.model_json_schema()

    # 'rel_b' should either be an 'array' or 'null'
    rel_a_types = openapi_schema["properties"]["rel_b"]["anyOf"]
    assert sorted([item["type"] for item in rel_a_types]) == ["array", "null"]

    # 'rel_b' array item's properties should be defined
    array_type = next(
        r
        for r in openapi_schema["properties"]["rel_b"]["anyOf"]
        if r["type"] == "array"
    )
    ref = array_type["items"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"


def test_many_to_many_reverse_relations_works() -> None:
    """Test that many-to-many relations are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ManyToManyField[ModelA, ModelA](ModelA, related_name="rel_b")

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "id": Infer,
                "var": Infer,
                "rel_b": {
                    "id": Infer,
                    "name": Infer,
                },
            },
        )

    openapi_schema = SchemaA.model_json_schema()

    # 'rel_b' should either be an 'array' or 'null'
    rel_a_types = openapi_schema["properties"]["rel_b"]["anyOf"]
    assert sorted([item["type"] for item in rel_a_types]) == ["array", "null"]

    # 'rel_b' array item's properties should be defined
    array_type = next(
        r
        for r in openapi_schema["properties"]["rel_b"]["anyOf"]
        if r["type"] == "array"
    )
    ref = array_type["items"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"


def test_one_to_one_reverse_relations_works() -> None:
    """Test that one-to-one relations are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        var = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):  # pyright: ignore[reportUnusedClass]
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.OneToOneField[ModelA, ModelA](
            ModelA,
            on_delete=models.CASCADE,
            related_name="rel_b",
        )

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "id": Infer,
                "var": Infer,
                "rel_b": {
                    "id": Infer,
                    "name": Infer,
                },
            },
        )

    openapi_schema = SchemaA.model_json_schema()

    # 'rel_b' should either be None (direct type ref) or 'null'
    rel_a_types = openapi_schema["properties"]["rel_b"]["anyOf"]
    assert sorted([i.get("type", "") for i in rel_a_types]) == ["", "null"]

    # 'rel_b' item's properties should be defined
    ref_type = next(r for r in rel_a_types if r.get("type") is None)
    ref = ref_type["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_relational_field_usage_by_id_works() -> None:
    """Test that relational fields can be used by id."""

    class ModelA(models.Model):
        id = models.UUIDField[uuid.UUID, uuid.UUID](
            primary_key=True, editable=False, default=uuid.uuid4
        )
        name = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ForeignKey[ModelA, ModelA](ModelA, on_delete=models.CASCADE)

    class SchemaB(BaseSchema[ModelB]):
        """SchemaB class."""

        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a_id": Infer,  # <--- This is the important part
            },
        )

    openapi_schema = SchemaB.model_json_schema()
    assert openapi_schema["properties"]["rel_a_id"]["type"] == "string"
    assert openapi_schema["properties"]["rel_a_id"]["format"] == "uuid4"


def test_symmetrical_many_to_many_fields_are_supported() -> None:
    """Test that symmetrical many to many fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ManyToManyField["ModelA", "ModelA"]("self", symmetrical=True)

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "name": Infer,
                },
            },
        )

    class SchemaB(SchemaA):
        """SchemaB class."""

    openapi_schema = SchemaA.model_json_schema()

    # 'rel_a' should either be 'array' or 'null'
    rel_a_types = openapi_schema["properties"]["rel_a"]["anyOf"]
    assert sorted([i.get("type", "") for i in rel_a_types]) == ["array", "null"]

    # 'rel_a' item's properties should be defined
    ref_type = next(r for r in rel_a_types if r.get("type") == "array")
    ref = ref_type["items"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"


def test_many_to_many_relations_provide_an_array_of_ids() -> None:
    """Test that many-to-many relations are represented as arrays."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ManyToManyField[ModelA, ModelA](ModelA)

    class SchemaB(BaseSchema[ModelB]):
        """SchemaB class."""

        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": Infer,  # <--- This is the important part
            },
        )

    openapi_schema = SchemaB.model_json_schema()
    assert openapi_schema["properties"]["rel_a"]["type"] == "array"
    assert openapi_schema["properties"]["rel_a"]["items"]["type"] == "integer"


# TODO(phuongfi91): Related to the experimental django validators
#  https://github.com/NextGenContributions/django2pydantic/issues/41
# def test_random_thing():
#     """Test that random things are supported."""
#     from django.core.validators import MaxLengthValidator, MinLengthValidator
#
#     class ModelA(models.Model):
#         id = models.AutoField[int, int](primary_key=True)
#         name = models.CharField[str, str](max_length=100, validators=[
#             MinLengthValidator(1),
#             MaxLengthValidator(100),
#         ])
#
#     class SchemaA(BaseSchema[ModelA]):
#         """SchemaA class."""
#
#         config = SchemaConfig[ModelA](
#             model=ModelA,
#             fields={
#                 # "id": Infer,
#                 "name": Infer,
#             },
#         )
#
#     a = SchemaA.model_validate({
#         # "id": 1,
#         "name": "a",
#     })


def test_inferred_many_to_many_field_should_be_list_of_ids() -> None:
    """Inferred many-to-many field should return only a list of related object IDs."""

    class ModelA1(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelA2(models.Model):
        id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a1 = models.ManyToManyField(ModelA1)  # pyright: ignore[reportUnknownVariableType]
        rel_a2 = models.ManyToManyField(ModelA2)  # pyright: ignore[reportUnknownVariableType]

    class SchemaB(BaseSchema[ModelB]):
        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a1": Infer,
                "rel_a2": Infer,
            },
        )

    # int IDs
    a11 = ModelA1(id=1, name="a11")
    a12 = ModelA1(id=2, name="a12")
    # UUIDs
    a21 = ModelA2(name="a21")
    a22 = ModelA2(name="a22")

    b = SchemaB.model_validate(
        {
            "id": 10,
            "name": "b",
            "rel_a1": [a11, a12],
            "rel_a2": [a21, a22],
        },
    )
    assert b.model_dump() == {
        "id": 10,
        "name": "b",
        "rel_a1": [
            1,
            2,
        ],
        "rel_a2": [
            a21.pk,
            a22.pk,
        ],
    }


def test_specified_many_to_many_field_should_be_list_of_objects() -> None:
    """Specified many-to-many field.

    When specified with related-object fields, a list of related-objects with specified
     fields should be returned accordingly.
    """

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ManyToManyField(ModelA)  # pyright: ignore[reportUnknownVariableType]

    class SchemaB(BaseSchema[ModelB]):
        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "name": Infer,
                },
            },
        )

    a1 = ModelA(id=1, name="a1")
    a2 = ModelA(id=2, name="a2")
    b = SchemaB.model_validate(
        {
            "id": 11,
            "name": "b",
            "rel_a": [a1, a2],
        },
    )
    assert b.model_dump() == {
        "id": 11,
        "name": "b",
        "rel_a": [
            {
                "id": 1,
                "name": "a1",
            },
            {
                "id": 2,
                "name": "a2",
            },
        ],
    }


# TODO(phuongfi91): This is failing due to missing handler for reverse relations
@pytest.mark.skip(reason="WIP")
def test_inferred_fk_field_should_be_an_id() -> None:
    """Inferred FK field (many-to-one) should return only an ID."""

    class ModelA(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)

    class ModelB(models.Model):
        id = models.AutoField[int, int](primary_key=True)
        name = models.CharField[str, str](max_length=100)
        rel_a = models.ForeignKey[ModelA, ModelA](
            ModelA,
            on_delete=models.CASCADE,
            related_name="rel_b",
        )

    class SchemaA(BaseSchema[ModelA]):
        config = SchemaConfig[ModelA](
            model=ModelA,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_b": Infer,
            },
        )

    class SchemaB(BaseSchema[ModelB]):
        config = SchemaConfig[ModelB](
            model=ModelB,
            fields={
                "id": Infer,
                "name": Infer,
                "rel_a": Infer,
            },
        )

    a = ModelA(id=1, name="a")

    # b1
    b1 = SchemaB.model_validate(
        {
            "id": 11,
            "name": "b1",
            "rel_a": a,
        },
    )
    assert b1.model_dump() == {
        "id": 11,
        "name": "b1",
        "rel_a": 1,
    }

    # b2
    b2 = SchemaB.model_validate(
        {
            "id": 12,
            "name": "b2",
            "rel_a": a,
        },
    )
    assert b2.model_dump() == {
        "id": 12,
        "name": "b2",
        "rel_a": 1,
    }

    # a
    a = SchemaA.model_validate(
        {
            "id": 1,
            "name": "a",
            "rel_b": [b1, b2],
        },
    )
    assert a.model_dump() == {
        "id": 1,
        "name": "a",
        "rel_b": [
            11,
            12,
        ],
    }
