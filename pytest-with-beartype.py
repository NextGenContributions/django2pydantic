#!/usr/bin/env python
"""Pytest wrapper which instruments it with Beartype's type annotation checks.

Why is this needed?
------------------

Because if you run pytest with the pytest-beartype plugin with command:
`pytest --beartype-packages='src,tests,automation,config'`
it will emit the following type warning:
```
BeartypePytestWarning: Previously imported packages "..." not checkable by beartype.
```

This is because the Beartype plugin is not able to instrument the packages
that are already imported somehow by pytest.
Refs:
- https://github.com/beartype/beartype/issues/322
- https://github.com/beartype/pytest-beartype/issues/3

So this wrapper script provides the workaround for this issue.

"""

import pytest
from beartype import BeartypeConf
from beartype.claw import beartype_package

type_check_instrumented_packages: list[str] = ["superschema", "tests"]

for package in type_check_instrumented_packages:
    beartype_package(package_name=package, conf=BeartypeConf())


# Run all tests in the current directory
pytest.main()
