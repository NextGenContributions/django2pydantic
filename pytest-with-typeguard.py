#!/usr/bin/env python
"""Pytest wrapper which instruments it with Typeguard's type annotation checks.

Why is this needed?
------------------

Because if you run pytest with the pytest-typeguard plugin with command:
`pytest typeguard-packages=src,tests,automation,config`
it will emit the following type warning:
```
InstrumentationWarning:
typeguard cannot check these packages because they are already imported: config, ...
````

This is because the Typeguard plugin is not able to instrument the packages
that are already imported somehow by pytest.

So this wrapper script provides the workaround for this issue.

"""

import pytest
from typeguard import install_import_hook

type_check_instrumented_packages: list[str] = ["superschema", "tests"]

install_import_hook(packages=type_check_instrumented_packages)

# Run all tests in the current directory
pytest.main()
