from typing import Literal

import pytest
from django.db import models
from django_pydantic_field import SchemaField
from pydantic import BaseModel, Field

from django2pydantic.schema import BaseSchema, SchemaConfig
from django2pydantic.types import Infer


def test_django_pydantic_field_SchemaField_works() -> None:
    """Test that schema subclassing works."""

    class SomePydanticModel(BaseModel):
        name: str
        age: int

    class ModelA(models.Model):
        pydantic_field = SchemaField(schema=SomePydanticModel)

    class SchemaA(BaseSchema[ModelA]):
        """SchemaA class."""

        config = SchemaConfig(
            model=ModelA,
            fields={
                "pydantic_field": Infer,
            },
        )

    openapi_schema = SchemaA.model_json_schema()

    # The SchemaField should generate a reference to the Pydantic model schema
    pydantic_field_schema = openapi_schema["properties"]["pydantic_field"]
    assert "$ref" in pydantic_field_schema

    # The referenced schema should be available in $defs
    ref_path = pydantic_field_schema["$ref"]
    assert ref_path.startswith("#/$defs/")

    # Extract the definition name and check it exists
    def_name = ref_path.split("/")[-1]
    assert def_name in openapi_schema["$defs"]

    # The referenced schema should be of type "object"
    referenced_schema = openapi_schema["$defs"][def_name]
    assert referenced_schema["type"] == "object"

    # The referenced schema should have the expected properties
    assert "name" in referenced_schema["properties"]
    assert "age" in referenced_schema["properties"]
    assert referenced_schema["properties"]["name"]["type"] == "string"
    assert referenced_schema["properties"]["age"]["type"] == "integer"

    valid_data = {
        "pydantic_field": {
            "name": "testuser",
            "age": 25,
        }
    }

    validated_data = SchemaA.model_validate(valid_data)
    assert validated_data.pydantic_field.name == "testuser"
    assert validated_data.pydantic_field.age == 25

    invalid_data = {
        "pydantic_field": {
            "name": "testuser",
            "age": "not an integer",  # Invalid age type
        }
    }
    with pytest.raises(ValueError) as exc_info:
        SchemaA.model_validate(invalid_data)
    assert "Input should be a valid integer" in str(exc_info.value)


def test_django_pydantic_field_SchemaField_with_discriminator_works() -> None:
    """Test that SchemaField with discriminator works.

    Ref: https://docs.pydantic.dev/latest/concepts/unions/#discriminated-unions-with-str-discriminators
    """

    class Cat(BaseModel):
        pet_type: Literal["cat"]
        meows: int

    class Dog(BaseModel):
        pet_type: Literal["dog"]
        barks: float

    class Lizard(BaseModel):
        pet_type: Literal["reptile", "lizard"]
        scales: bool

    class Model(BaseModel):
        pet: Cat | Dog | Lizard = Field(discriminator="pet_type")
        n: int

    class MyDjangoModel(models.Model):
        pydantic_field = SchemaField(
            schema=Model,
        )

    class MyDjangoSchema(BaseSchema[MyDjangoModel]):
        """MyDjangoSchema class."""

        config = SchemaConfig(
            model=MyDjangoModel,
            fields={
                "pydantic_field": Infer,
            },
        )

    openapi_schema = MyDjangoSchema.model_json_schema()
    pydantic_field_schema = openapi_schema["properties"]["pydantic_field"]
    assert "$ref" in pydantic_field_schema
    ref_path = pydantic_field_schema["$ref"]
    assert ref_path.startswith("#/$defs/")
    def_name = ref_path.split("/")[-1]
    assert def_name in openapi_schema["$defs"]
    referenced_schema = openapi_schema["$defs"][def_name]
    assert referenced_schema["type"] == "object"
    assert "pet" in referenced_schema["properties"]

    # The pet field should be a discriminated union
    pet_schema = referenced_schema["properties"]["pet"]
    assert "discriminator" in pet_schema
    assert "oneOf" in pet_schema

    # Check discriminator structure
    discriminator = pet_schema["discriminator"]
    assert discriminator["propertyName"] == "pet_type"
    assert "mapping" in discriminator

    # Check that oneOf contains references to the union members
    one_of = pet_schema["oneOf"]
    expected_union_members = 3  # Cat, Dog, Lizard
    assert len(one_of) == expected_union_members

    # All oneOf items should be references
    for item in one_of:
        assert "$ref" in item
        assert item["$ref"].startswith("#/$defs/")

    # Check that the referenced schemas exist in $defs
    expected_schemas = ["Cat", "Dog", "Lizard"]
    for schema_name in expected_schemas:
        assert schema_name in openapi_schema["$defs"]
        schema_def = openapi_schema["$defs"][schema_name]
        assert schema_def["type"] == "object"
        assert "pet_type" in schema_def["properties"]

    valid_data_cat = {
        "pydantic_field": {
            "pet": {
                "pet_type": "cat",
                "meows": 3,
            },
            "n": 42,
        }
    }
    validated_data_cat = MyDjangoSchema.model_validate(valid_data_cat)
    assert validated_data_cat.pydantic_field.pet.pet_type == "cat"
    assert validated_data_cat.pydantic_field.pet.meows == 3
    assert validated_data_cat.pydantic_field.n == 42
    valid_data_dog = {
        "pydantic_field": {
            "pet": {
                "pet_type": "dog",
                "barks": 2.5,
            },
            "n": 42,
        }
    }
    validated_data_dog = MyDjangoSchema.model_validate(valid_data_dog)
    assert validated_data_dog.pydantic_field.pet.pet_type == "dog"
    assert validated_data_dog.pydantic_field.pet.barks == 2.5
    assert validated_data_dog.pydantic_field.n == 42
    valid_data_lizard = {
        "pydantic_field": {
            "pet": {
                "pet_type": "lizard",
                "scales": True,
            },
            "n": 42,
        }
    }
    validated_data_lizard = MyDjangoSchema.model_validate(valid_data_lizard)
    assert validated_data_lizard.pydantic_field.pet.pet_type == "lizard"
    assert validated_data_lizard.pydantic_field.pet.scales is True
    assert validated_data_lizard.pydantic_field.n == 42

    invalid_data_cat = {
        "pydantic_field": {
            "pet": {
                "pet_type": "cat",
                "barks": 2.5,  # Invalid as cats don't bark
            },
            "n": 42,
        }
    }
    with pytest.raises(ValueError) as exc_info:
        MyDjangoSchema.model_validate(invalid_data_cat)
    assert "Field required" in str(exc_info.value)
