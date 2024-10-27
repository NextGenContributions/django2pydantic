"""Nox test configuration.

See: https://nox.thea.codes/en/stable/config.html
"""

import nox


@nox.session(python=["3.12", "3.13"], reuse_venv=True)
def tests(session: nox.Session) -> None:
    """Run the test suite."""
    session.run("poetry", "install", "--only=test", external=True)
    session.run("pytest")


@nox.session
def lint(session: nox.Session) -> None:
    session.install("flake8")
    session.run("flake8")


@nox.session
def type_check_with_mypy(session: nox.Session) -> None:
    session.install("mypy")
    session.run("mypy")


@nox.session
def type_check_with_pyright(session: nox.Session) -> None:
    session.install("pyright")
    session.run("pyright")


@nox.session
def type_check_with_pytype(session: nox.Session) -> None:
    session.install("pytype")
    session.run("pytype")


@nox.session
def type_check_with_pyre(session: nox.Session) -> None:
    session.install("pyre-check")
    session.run("pyre")


@nox.session
def type_check_with_basedpyright(session: nox.Session) -> None:
    session.install("basedpyright")
    session.run("basedpyright")
