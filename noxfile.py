"""Nox test configuration.

See: https://nox.thea.codes/en/stable/config.html
"""

import nox


@nox.session(python=["3.12", "3.13"], reuse_venv=True)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.run("pytest")


@nox.session
def lint_with_flake8(session: nox.Session) -> None:
    """Lint the codebase with flake8."""
    session.install("flake8")
    session.run("flake8")


@nox.session
def lint_with_ruff(session: nox.Session) -> None:
    """Lint the codebase with ruff."""
    session.install("ruff")
    session.run("ruff")


@nox.session
def lint_with_pylint(session: nox.Session) -> None:
    """Lint the codebase with pylint."""
    session.install("pylint")
    session.run("pylint")


@nox.session
def type_check_with_mypy(session: nox.Session) -> None:
    """Type-check the codebase with mypy."""
    session.install("mypy")
    session.run("mypy")


@nox.session
def type_check_with_pyright(session: nox.Session) -> None:
    """Type-check the codebase with pyright."""
    session.install("pyright")
    session.run("pyright")


@nox.session
def type_check_with_pytype(session: nox.Session) -> None:
    """Type-check the codebase with pytype."""
    session.install("pytype")
    session.run("pytype")


@nox.session
def type_check_with_pyre(session: nox.Session) -> None:
    """Type-check the codebase with pyre."""
    session.install("pyre-check")
    session.run("pyre")


@nox.session
def type_check_with_basedpyright(session: nox.Session) -> None:
    """Type-check the codebase with basedpyright."""
    session.install("basedpyright")
    session.run("basedpyright")


@nox.session
def lint_imports(session: nox.Session) -> None:
    """Lint the codebase with importlinter."""
    session.run("lint-imports")


@nox.session
def noop(session: nox.Session) -> None:
    """No operation.

    Dummy one just to do nothing.
    """
