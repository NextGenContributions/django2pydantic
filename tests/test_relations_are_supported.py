import uuid
from typing import ClassVar

from django.db import models

from django2pydantic.schema import Schema
from django2pydantic.types import Infer, ModelFields
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
        fields={"someid": models.SmallIntegerField(unique=True)},
    )
    openapi_schema = get_openapi_schema_from_field(
        models.ForeignKey(related_model, on_delete=models.CASCADE, to_field="someid"),
    )
    assert openapi_schema["properties"]["field"]["type"] == "integer"


def test_foreign_key_field() -> None:
    """Test that models can have nested models."""

    class ModelAA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100)

    class ModelBB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelBB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            }

    openapi_schema = SchemaB.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_foreign_key_field_with_to_field_works() -> None:
    """Test that foreign key fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100, unique=True)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ForeignKey(ModelA, on_delete=models.CASCADE, to_field="var")

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            }

    openapi_schema = SchemaB.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_many_to_many_field_works() -> None:
    """Test that many to many fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ManyToManyField(ModelA)

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            }

    openapi_schema = SchemaB.model_json_schema()
    assert openapi_schema["properties"]["rel_a"]["type"] == "array"
    assert (
        openapi_schema["properties"]["rel_a"]["items"]["properties"]["id"]["type"]
        == "integer"
    )
    assert (
        openapi_schema["$defs"]["ModelASchema"]["properties"]["name"]["type"]
        == "string"
    )


def test_one_to_one_field_works() -> None:
    """Test that one to one fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.OneToOneField(ModelA, on_delete=models.CASCADE)

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "var": Infer,
                },
            }

    openapi_schema = SchemaB.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["var"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_many_to_one_relations_work() -> None:
    """Test that many to one relations are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)

        class Meta:
            default_related_name = "rel_b"

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_b": {
                    "id": Infer,
                    "name": Infer,
                },
            }

    openapi_schema = SchemaA.model_json_schema()
    ref = openapi_schema["properties"]["rel_b"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_many_to_many_reverse_relations_work() -> None:
    """Test that many to many relations are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ManyToManyField(ModelA)

        class Meta:
            default_related_name = "rel_b"

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "var": Infer,
                "rel_b": {
                    "id": Infer,
                    "name": Infer,
                },
            }

    openapi_schema = SchemaA.model_json_schema()
    ref = openapi_schema["properties"]["rel_b"]["items"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_one_to_one_reverse_relations_work() -> None:
    """Test that one to one relations are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        var = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.OneToOneField(ModelA, on_delete=models.CASCADE)

        class Meta:
            default_related_name = "rel_b"

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "var": Infer,
                "rel_b": {
                    "id": Infer,
                    "name": Infer,
                },
            }

    openapi_schema = SchemaA.model_json_schema()
    ref = openapi_schema["properties"]["rel_b"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_relational_field_usage_by_id_works() -> None:
    """Test that relational fields can be used by id."""

    class ModelA(models.Model):
        id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ForeignKey(ModelA, on_delete=models.CASCADE)

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a_id": Infer,  # <--- This is the important part
            }

    openapi_schema = SchemaB.model_json_schema()
    assert openapi_schema["properties"]["rel_a_id"]["type"] == "string"
    assert openapi_schema["properties"]["rel_a_id"]["format"] == "uuid4"


def test_symmetrical_many_to_many_fields_are_supported() -> None:
    """Test that symmetrical many to many fields are supported."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ManyToManyField("self", symmetrical=True)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": {
                    "id": Infer,
                    "name": Infer,
                },
            }

    openapi_schema = SchemaA.model_json_schema()
    ref = openapi_schema["properties"]["rel_a"]["items"]["$ref"].split("/")[-1]
    assert openapi_schema["$defs"][ref]["properties"]["name"]["type"] == "string"
    assert openapi_schema["$defs"][ref]["properties"]["id"]["type"] == "integer"


def test_many_to_many_relations_provide_an_array_of_ids() -> None:
    """Test that many to many relations are represented as arrays."""

    class ModelA1(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelB1(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)
        rel_a = models.ManyToManyField(ModelA)

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB1
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
                "rel_a": Infer,  # <--- This is the important part
            }

    openapi_schema = SchemaB.model_json_schema()
    assert openapi_schema["properties"]["rel_a"]["type"] == "array"
    assert openapi_schema["properties"]["rel_a"]["items"]["type"] == "integer"
