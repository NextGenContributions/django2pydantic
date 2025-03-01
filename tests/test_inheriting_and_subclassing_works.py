"""Test that inheriting and subclassing works."""


@pytest.mark.skip(reason="Placeholder test")
def test_models_can_have_abstract_base_classes() -> None:
    """Test that models can have abstract base classes."""

    class Base(models.Model):
        id = models.AutoField(primary_key=True)

        class Meta:
            abstract = True

    class ModelA(Base):
        name = models.CharField(max_length=100)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
            }

    openapi_schema = SchemaA.model_json_schema()
    assert openapi_schema["properties"]["name"]["type"] == "string"


@pytest.mark.skip(reason="Placeholder test")
def test_foreign_key_fields_can_have_string_reference_to_related_model() -> None:
    """Test that foreign key fields can have a string reference to the related model."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        model_a = models.ForeignKey(
            "ModelA", on_delete=models.CASCADE
        )  # <-- string reference

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
            }

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "model_a": Infer,
            }

    openapi_schema = SchemaB.model_json_schema()
    assert (
        openapi_schema["properties"]["model_a"]["$ref"] == "#/components/schemas/ModelA"
    )


@pytest.mark.skip(reason="Placeholder test")
def test_many_to_many_fields_can_have_string_reference_to_related_model() -> None:
    """Test that many to many fields can have a string reference to the related model."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        model_a = models.ManyToManyField("ModelA")

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
            }

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "model_a": Infer,
            }

    openapi_schema = SchemaB.model_json_schema()
    assert (
        openapi_schema["properties"]["model_a"]["items"]["$ref"]
        == "#/components/schemas/ModelA"
    )


@pytest.mark.skip(reason="Placeholder test")
def test_one_to_one_fields_can_have_string_reference_to_related_model() -> None:
    """Test that one to one fields can have a string reference to the related model."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class ModelB(models.Model):
        id = models.AutoField(primary_key=True)
        model_a = models.OneToOneField("ModelA", on_delete=models.CASCADE)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
            }

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelB
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "model_a": Infer,
            }

    openapi_schema = SchemaB.model_json_schema()
    assert (
        openapi_schema["properties"]["model_a"]["$ref"] == "#/components/schemas/ModelA"
    )


@pytest.mark.skip(reason="Placeholder test")
def test_there_can_be_multiple_schemas_for_one_model() -> None:
    """Test that there can be multiple schemas for one model."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=100)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "name": Infer,
            }

    class SchemaB(Schema):
        """SchemaB class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
            }

    openapi_schema_a = SchemaA.model_json_schema()
    openapi_schema_b = SchemaB.model_json_schema()
    assert openapi_schema_a["properties"]["name"]["type"] == "string"
    assert "name" not in openapi_schema_b["properties"]


@pytest.mark.skip(reason="Placeholder test")
def test_there_can_be_self_referencing_fields() -> None:
    """Test that there can be self-referencing fields."""

    class ModelA(models.Model):
        id = models.AutoField(primary_key=True)
        parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)

    class SchemaA(Schema):
        """SchemaA class."""

        class Meta(Schema.Meta):
            """Meta class."""

            model = ModelA
            fields: ClassVar[ModelFields] = {
                "id": Infer,
                "parent": Infer,
            }

    openapi_schema = SchemaA.model_json_schema()
    assert (
        openapi_schema["properties"]["parent"]["$ref"] == "#/components/schemas/ModelA"
    )
