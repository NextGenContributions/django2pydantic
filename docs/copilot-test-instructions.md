- Project's test coverage should be 100%.
- Use Pytest for testing.
- Tests are located in the [tests](../tests) directory.
- Eagerly look for opportunities to unite tests by using the `@pytest.mark.parametrize` decorator to write parametrized tests.


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
