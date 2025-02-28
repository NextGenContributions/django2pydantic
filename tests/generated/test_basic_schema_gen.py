# """Tests for basic schema generation functionality of django2pydantic."""

# from decimal import Decimal
# from typing import Any

# import pytest
# from django.db import models
# from hypothesis import given
# from hypothesis import strategies as st
# from pydantic import ValidationError

# from django2pydantic import BaseSchema, Infer, InferExcept
# from django2pydantic.schema import SchemaConfig


# def test_should_generate_valid_schema_when_model_has_simple_fields() -> None:
#     """Test that a valid schema is generated from a Django model with simple fields."""

#     class SimpleModel(models.Model):
#         name = models.CharField(max_length=100)
#         description = models.TextField()
#         is_active = models.BooleanField(default=True)

#         class Meta:
#             app_label = "tests"

#     class SimpleModelSchema(BaseSchema[SimpleModel]):
#         config = SchemaConfig[SimpleModel](
#             model=SimpleModel,
#             fields={
#                 "name": Infer,
#                 "description": Infer,
#                 "is_active": Infer,
#             },
#         )

#     # Generate the schema
#     schema = SimpleModelSchema.model_json_schema()

#     # Validate the schema structure
#     assert schema["title"] == "SimpleModelSchema"
#     assert schema["type"] == "object"
#     assert set(schema["properties"].keys()) == {"name", "description", "is_active"}

#     # Validate field types
#     assert schema["properties"]["name"]["type"] == "string"
#     assert schema["properties"]["name"]["maxLength"] == 100
#     assert schema["properties"]["description"]["type"] == "string"
#     assert schema["properties"]["is_active"]["type"] == "boolean"


# class ComplexModel(models.Model):
#     """A complex model with various field types for testing."""

#     # Text fields
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     email = models.EmailField()

#     # Numeric fields
#     count = models.IntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     # Boolean field
#     is_active = models.BooleanField(default=True)

#     # Date/time fields
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         app_label = "tests"


# @pytest.mark.parametrize(
#     "field_name,expected_type,expected_format,expected_constraints",
#     [
#         ("name", "string", None, {"maxLength": 50}),
#         ("description", "string", None, {}),
#         ("email", "string", "email", {}),
#         ("count", "integer", None, {}),
#         ("amount", "number", None, {"multipleOf": 0.01}),
#         ("is_active", "boolean", None, {}),
#         ("created_at", "string", "date-time", {}),
#     ],
# )
# def test_should_infer_correct_field_types_when_using_infer(
#     field_name: str,
#     expected_type: str,
#     expected_format: str | None,
#     expected_constraints: dict[str, Any],
# ) -> None:
#     """Test that field types are correctly inferred when using Infer marker."""

#     class ComplexModelSchema(BaseSchema[ComplexModel]):
#         config = SchemaConfig[ComplexModel](
#             model=ComplexModel,
#             fields={
#                 "name": Infer,
#                 "description": Infer,
#                 "email": Infer,
#                 "count": Infer,
#                 "amount": Infer,
#                 "is_active": Infer,
#                 "created_at": Infer,
#             },
#         )

#     schema = ComplexModelSchema.model_json_schema()

#     # Check field type
#     assert schema["properties"][field_name]["type"] == expected_type

#     # Check field format if expected
#     if expected_format:
#         assert schema["properties"][field_name]["format"] == expected_format
#     elif "format" in schema["properties"][field_name]:
#         pytest.fail(
#             f"Unexpected format found: {schema['properties'][field_name]['format']}"
#         )

#     # Check constraints
#     for constraint_name, constraint_value in expected_constraints.items():
#         assert schema["properties"][field_name][constraint_name] == constraint_value


# @pytest.mark.parametrize(
#     "custom_fields,expected_title,expected_description",
#     [
#         (
#             {"name": InferExcept(title="Custom Name")},
#             "Custom Name",
#             "name",
#         ),
#         (
#             {"name": InferExcept(description="Custom description")},
#             "name",
#             "Custom description",
#         ),
#         (
#             {
#                 "name": InferExcept(
#                     title="Custom Name", description="Custom description"
#                 )
#             },
#             "Custom Name",
#             "Custom description",
#         ),
#     ],
# )
# def test_should_use_custom_field_definitions_when_using_infer_except(
#     custom_fields: dict[str, InferExcept],
#     expected_title: str,
#     expected_description: str,
# ) -> None:
#     """Test that custom field definitions are used when using InferExcept."""

#     class CustomModel(models.Model):
#         name = models.CharField(max_length=100)

#         class Meta:
#             app_label = "tests"

#     class CustomModelSchema(BaseSchema[CustomModel]):
#         config = SchemaConfig[CustomModel](
#             model=CustomModel,
#             fields=custom_fields,
#         )

#     schema = CustomModelSchema.model_json_schema()

#     assert schema["properties"]["name"]["title"] == expected_title
#     assert schema["properties"]["name"]["description"] == expected_description


# @pytest.mark.parametrize(
#     "model_config,expected_title,expected_description",
#     [
#         (
#             {"title": "CustomName"},
#             "CustomName",
#             None,
#         ),
#         (
#             {"description": "Custom model description"},
#             "CustomNameSchema",
#             "Custom model ,
#         ),
#         (
#             {"title": "FullyCustom", "description": "Fully customized schema"},
#             "FullyCustom",
#             "Fully customized schema",
#         ),
#     ],
# )
# def test_should_apply_schema_naming_when_config_is_provided(
#     model_config: dict[str, str],
#     expected_title: str,
#     expected_description: str | None,
# ) -> None:
#     """Test that schema naming is applied when config is provided."""

#     class NamedModel(models.Model):
#         value = models.CharField(max_length=100)

#         class Meta:
#             app_label = "tests"

#     class CustomNameSchema(BaseSchema[NamedModel]):
#         model_config = model_config

#         config = SchemaConfig[NamedModel](
#             model=NamedModel,
#             fields={"value": Infer},
#         )

#     schema = CustomNameSchema.model_json_schema()

#     assert schema["title"] == expected_title

#     if expected_description:
#         assert schema["description"] == expected_description
#     elif "description" in schema:
#         assert schema["description"] is None


# def test_should_include_field_metadata_when_title_and_description_exist() -> None:
#     """Test that field metadata is included in the schema when title and description exist."""

#     class MetadataModel(models.Model):
#         name = models.CharField(max_length=100, help_text="The name field")
#         description = models.TextField(verbose_name="Item Description")

#         class Meta:
#             app_label = "tests"

#     class MetadataSchema(BaseSchema[MetadataModel]):
#         config = SchemaConfig[MetadataModel](
#             model=MetadataModel,
#             fields={
#                 "name": Infer,
#                 "description": Infer,
#             },
#         )

#     schema = MetadataSchema.model_json_schema()

#     assert schema["properties"]["name"]["description"] == "The name field"
#     assert schema["properties"]["description"]["title"] == "Item Description"


# class ValidationModel(models.Model):
#     """A model with validation rules for testing."""

#     name = models.CharField(max_length=10)
#     email = models.EmailField()
#     count = models.IntegerField(default=0)

#     class Meta:
#         app_label = "tests"


# class ValidationSchema(BaseSchema[ValidationModel]):
#     """Schema for ValidationModel with inferred fields."""

#     config = SchemaConfig[ValidationModel](
#         model=ValidationModel,
#         fields={
#             "name": Infer,
#             "email": Infer,
#             "count": Infer,
#         },
#     )


# @pytest.mark.parametrize(
#     "data,is_valid,error_field,error_contains",
#     [
#         (
#             {"name": "Test", "email": "test@example.com", "count": 5},
#             True,
#             None,
#             None,
#         ),
#         (
#             {"name": "ThisNameIsTooLong", "email": "test@example.com", "count": 5},
#             False,
#             "name",
#             "longer than the maximum allowed length",
#         ),
#         (
#             {"name": "Test", "email": "not-an-email", "count": 5},
#             False,
#             "email",
#             "value is not a valid email address",
#         ),
#         (
#             {"name": "Test", "email": "test@example.com", "count": "not-a-number"},
#             False,
#             "count",
#             "Input should be a valid integer",
#         ),
#     ],
# )
# def test_should_validate_model_when_data_is_provided(
#     data: dict[str, Any],
#     is_valid: bool,
#     error_field: str | None,
#     error_contains: str | None,
# ) -> None:
#     """Test that a schema validates data according to the model's constraints."""
#     if is_valid:
#         valid_instance = ValidationSchema(**data)
#         for key, value in data.items():
#             assert getattr(valid_instance, key) == value
#     else:
#         with pytest.raises(ValueError) as exc_info:
#             ValidationSchema(**data)
#         assert error_field in str(exc_info.value)
#         assert error_contains in str(exc_info.value)


# @pytest.mark.parametrize(
#     "name,email",
#     [
#         ("Test", "valid@example.com"),
#         ("Short", "short@test.io"),
#         ("A", "a@b.com"),
#     ],
# )
# def test_should_validate_model_with_valid_data(name: str, email: str) -> None:
#     """Test that valid data passes validation with various valid inputs."""
#     valid_data = {
#         "name": name,
#         "email": email,
#         "count": 10,
#     }

#     valid_instance = ValidationSchema(**valid_data)
#     assert valid_instance.name == name
#     assert valid_instance.email == email
#     assert valid_instance.count == 10


# # Property-based testing with Hypothesis
# @given(
#     name=st.text(min_size=1, max_size=10),
#     email=st.emails(),
#     count=st.integers(min_value=-1000, max_value=1000),
# )
# def test_should_validate_model_with_generated_data(
#     name: str, email: str, count: int
# ) -> None:
#     """Test that a schema validates generated data correctly."""
#     try:
#         instance = ValidationSchema(name=name, email=email, count=count)
#         assert instance.name == name
#         assert instance.email == email
#         assert instance.count == count
#     except ValidationError:
#         # If validation error occurs, ensure it's because of constraints
#         if len(name) > 10:
#             pytest.fail("Name should be valid since Hypothesis ensures max_size=10")
#         # Other validation errors should not occur with Hypothesis-generated data


# def test_should_convert_model_to_dict_when_instance_exists() -> None:
#     """Test that a Django model instance can be converted to a Pydantic model."""

#     class ConversionModel(models.Model):
#         title = models.CharField(max_length=100)
#         description = models.TextField(blank=True)
#         is_featured = models.BooleanField(default=False)

#         class Meta:
#             app_label = "tests"

#     class ConversionSchema(BaseSchema[ConversionModel]):
#         config = SchemaConfig[ConversionModel](
#             model=ConversionModel,
#             fields={
#                 "title": Infer,
#                 "description": Infer,
#                 "is_featured": Infer,
#             },
#         )

#     # Create a Django model instance
#     model_instance = ConversionModel(
#         title="Test Title",
#         description="Test Description",
#         is_featured=True,
#     )

#     # Convert to Pydantic model
#     schema_instance = ConversionSchema.model_validate(model_instance)

#     # Check values
#     assert schema_instance.title == "Test Title"
#     assert schema_instance.description == "Test Description"
#     assert schema_instance.is_featured is True

#     # Convert to dict
#     data_dict = schema_instance.model_dump()
#     assert data_dict == {
#         "title": "Test Title",
#         "description": "Test Description",
#         "is_featured": True,
#     }


# @given(
#     title=st.text(min_size=1, max_size=100),
#     description=st.text(),
#     is_featured=st.booleans(),
# )
# def test_should_convert_model_to_dict_with_generated_data(
#     title: str, description: str, is_featured: bool
# ) -> None:
#     """Test that a Django model instance with generated data can be converted to a Pydantic model."""

#     class ConversionModel(models.Model):
#         title = models.CharField(max_length=100)
#         description = models.TextField(blank=True)
#         is_featured = models.BooleanField(default=False)

#         class Meta:
#             app_label = "tests"

#     class ConversionSchema(BaseSchema[ConversionModel]):
#         config = SchemaConfig[ConversionModel](
#             model=ConversionModel,
#             fields={
#                 "title": Infer,
#                 "description": Infer,
#                 "is_featured": Infer,
#             },
#         )

#     # Create a Django model instance with generated data
#     model_instance = ConversionModel(
#         title=title,
#         description=description,
#         is_featured=is_featured,
#     )

#     # Convert to Pydantic model
#     schema_instance = ConversionSchema.model_validate(model_instance)

#     # Check values
#     assert schema_instance.title == title
#     assert schema_instance.description == description
#     assert schema_instance.is_featured is is_featured

#     # Convert to dict
#     data_dict = schema_instance.model_dump()
#     assert data_dict == {
#         "title": title,
#         "description": description,
#         "is_featured": is_featured,
#     }


# def test_should_generate_openapi_schema_when_model_is_processed() -> None:
#     """Test that an OpenAPI schema is generated when a model is processed."""

#     class OpenAPIModel(models.Model):
#         name = models.CharField(max_length=100)
#         age = models.IntegerField()
#         email = models.EmailField()

#         class Meta:
#             app_label = "tests"

#     class OpenAPISchema(BaseSchema[OpenAPIModel]):
#         config = SchemaConfig[OpenAPIModel](
#             model=OpenAPIModel,
#             fields={
#                 "name": Infer,
#                 "age": Infer,
#                 "email": Infer,
#             },
#         )

#     schema = OpenAPISchema.model_json_schema()

#     # Check OpenAPI schema structure
#     assert "title" in schema
#     assert "type" in schema
#     assert "properties" in schema
#     assert "required" in schema

#     # Check that it contains all fields
#     assert "name" in schema["properties"]
#     assert "age" in schema["properties"]
#     assert "email" in schema["properties"]

#     # Check field formats and constraints
#     assert schema["properties"]["name"]["type"] == "string"
#     assert schema["properties"]["age"]["type"] == "integer"
#     assert schema["properties"]["email"]["type"] == "string"
#     assert schema["properties"]["email"]["format"] == "email"


# def test_should_handle_required_and_optional_fields_when_generating_schema() -> None:
#     """Test that required and optional fields are correctly identified in the schema."""

#     class RequiredOptionalModel(models.Model):
#         required_field = models.CharField(max_length=100)
#         optional_field = models.CharField(max_length=100, blank=True, null=True)
#         default_field = models.IntegerField(default=42)

#         class Meta:
#             app_label = "tests"

#     class RequiredOptionalSchema(BaseSchema[RequiredOptionalModel]):
#         config = SchemaConfig[RequiredOptionalModel](
#             model=RequiredOptionalModel,
#             fields={
#                 "required_field": Infer,
#                 "optional_field": Infer,
#                 "default_field": Infer,
#             },
#         )

#     schema = RequiredOptionalSchema.model_json_schema()

#     # Check required fields
#     assert "required" in schema
#     assert "required_field" in schema["required"]
#     assert "optional_field" not in schema["required"]
#     assert "default_field" not in schema["required"]

#     # Check nullable fields
#     assert schema["properties"]["optional_field"].get("nullable", False) is True

#     # Test validation
#     # This should pass as optional_field is optional
#     instance1 = RequiredOptionalSchema(required_field="test")
#     assert instance1.required_field == "test"
#     assert instance1.optional_field is None
#     assert instance1.default_field == 42

#     # This should fail as required_field is required
#     with pytest.raises(ValueError) as exc_info:
#         RequiredOptionalSchema(optional_field="test")
#     assert "required_field" in str(exc_info.value)
#     assert "Field required" in str(exc_info.value)


# @pytest.mark.parametrize(
#     "model_fields,schema_fields,expected_fields_in_schema",
#     [
#         # Include all fields
#         (
#             ["name", "age", "is_active"],
#             ["name", "age", "is_active"],
#             ["name", "age", "is_active"],
#         ),
#         # Subset of fields
#         (["name", "age", "is_active"], ["name", "age"], ["name", "age"]),
#         # Single field
#         (["name", "age", "is_active"], ["name"], ["name"]),
#     ],
# )
# def test_should_include_only_specified_fields_when_generating_schema(
#     model_fields: list[str],
#     schema_fields: list[str],
#     expected_fields_in_schema: list[str],
# ) -> None:
#     """Test that only specified fields are included in the schema."""
#     # Dynamic creation of model with specified fields
#     model_attrs = {
#         field: models.CharField(max_length=100)
#         if field == "name"
#         else models.IntegerField()
#         if field == "age"
#         else models.BooleanField(default=True)
#         for field in model_fields
#     }
#     model_attrs["Meta"] = type("Meta", (), {"app_label": "tests"})

#     PartialModel = type("PartialModel", (models.Model,), model_attrs)

#     # Dynamic creation of schema with specified fields
#     schema_config = SchemaConfig[PartialModel](
#         model=PartialModel,
#         fields={field: Infer for field in schema_fields},
#     )

#     PartialSchema = type(
#         "PartialSchema", (BaseSchema[PartialModel],), {"config": schema_config}
#     )

#     schema = PartialSchema.model_json_schema()

#     # Check that only expected fields are in schema
#     assert set(schema["properties"].keys()) == set(expected_fields_in_schema)


# @given(
#     model_data=st.dictionaries(
#         keys=st.text(
#             min_size=1,
#             max_size=20,
#             alphabet=st.characters(whitelist_categories=("Lu", "Ll")),
#         ),
#         values=st.one_of(
#             st.text(max_size=50),
#             st.integers(-1000, 1000),
#             st.booleans(),
#             st.decimals(min_value=-100, max_value=100),
#         ),
#         min_size=1,
#     )
# )
# def test_should_handle_dynamic_model_creation_with_generated_data(
#     model_data: dict[str, Any],
# ) -> None:
#     """Test that dynamic model creation and schema generation works with generated data."""
#     # Skip test if all values are not serializable
#     # Pydantic requires all values to be JSON serializable
#     for key, value in model_data.items():
#         if not isinstance(value, (str, int, bool, float)) and value is not None:
#             pytest.skip("Skipping test with non-serializable values")

#     # Create a Django model dynamically
#     class DynamicModel(models.Model):
#         class Meta:
#             app_label = "tests"

#     # Setup schema config
#     fields_dict = {}

#     # Create schema model
#     class DynamicSchema(BaseSchema[DynamicModel]):
#         config = SchemaConfig[DynamicModel](
#             model=DynamicModel,
#             fields=fields_dict,
#         )

#     # Create model instance
#     instance = DynamicModel()

#     # Set attributes on instance
#     for key, value in model_data.items():
#         setattr(instance, key, value)

#     # Create dynamic fields for each attribute
#     for key in model_data:
#         fields_dict[key] = Infer

#     # This should work without errors when getting data from model
#     schema_instance = DynamicSchema.model_validate(instance)

#     # Verify values
#     for key, value in model_data.items():
#         assert hasattr(schema_instance, key)
#         attr_value = getattr(schema_instance, key)

#         # For Decimal, convert to float for comparison
#         if isinstance(value, Decimal):
#             assert float(attr_value) == pytest.approx(float(value))
#         else:
#             assert attr_value == value
