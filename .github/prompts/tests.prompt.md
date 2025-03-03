Your goal is to generate a unit test using pytest.

# Requirements for writing tests:
- Strictly follow the test plan:
    - Use parameterized tests if a test belongs to `Using Parameterized Tests` category.
    - Use hypothesis library for property-based testing if a test belongs to `Using Hypothesis` category.
- Test only publicly exposed components declared in #file:../../django2pydantic/__init__.py __all__ in an end-to-end manner. Verify the outcome from OpenAPI schema.
- Follow the example use cases from #file:../../examples.ipynb
- If a database object is needed, don't create objects using Django's objects manager e.g. `Author.objects.create(name="John Doe")`, since we don't actually have a database running. Instead create an object using this syntax `Author(name="John Doe")`
- Do not use mock/patch.
- Do not modify existing implementation without first asking for permission.
- Do not test private/protected methods/functions such as _get_field_info, has_property, _get_django_field, _get_field_info, _determine_field_type, etc.
- Do not test helper methods/functions.
- Add docstring to explain test functions.
- Utilize utility functions in #file:../../tests/utils.py if necessary.
- You can get FieldTypeRegistry with default field type handlers by importing "from django2pydantic.defaults import field_type_registry" #file:../../django2pydantic/defaults.py
