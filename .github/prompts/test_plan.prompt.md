Your goal is to generate a test plan for the project.

# Requirements for writing tests:
- List all the possible tests that should be done and organize them into categories
- For each category, further define 3 subcategories and put the tests in the appropriate subcategory:
    - `Using Parameterized Tests`: If a test can benefit from using parameterized testing.
    - `Using Hypothesis`: If a test can benefit from using property-based testing.
    - `General`: If a test does not benefit from either of the above.
- Test only publicly exposed components declared in #file:../../django2pydantic/__init__.py __all__ in an end-to-end manner. Verify the outcome from OpenAPI schema.
- Follow the example use cases from #file:../../examples.ipynb
- Do not use mock/patch.
- Do not test private/protected methods/functions such as _get_field_info, has_property, _get_django_field, _get_field_info, _determine_field_type, etc.
- Do not test helper methods/functions.

# The test case names should be descriptive and should follow a consistent naming convention:

* test_should_<expected result>_when_<condition>
* test_should_<expected result>_when_<action>
* test_should_<expected result>_when_<condition>_<action>
* test_when_<condition>_then_<expected result>
* test_given_<precondition>_when_<action>_then_<expected result>

Examples:

* test_should_display_error_message_when_login_fails
* test_should_display_success_message_when_login_succeeds
* test_when_login_fails_then_display_error_message
