"""Nox test configuration.

See: https://nox.thea.codes/en/stable/config.html
"""

from pathlib import Path

import nox

# Allow proper use of different python versions
nox.options.default_venv_backend = "uv"


@nox.session(python=["3.12", "3.13"])
@nox.parametrize("django_version", ["4.2", "5.0", "5.1", "5.2"])
def tests(session: nox.Session, django_version: str) -> None:
    """Run the test suite."""
    # https://nox.thea.codes/en/stable/cookbook.html#using-a-lockfile
    _ = session.run_install(
        "uv",
        "sync",
        "--no-dev",
        "--group=tests",
        f"--python={session.virtualenv.location}",
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )
    # Override django version from lockfile
    session.install(f"django=={django_version}")

    # a fix so .ipynb tests imports succeed:
    session.env["PYTHONPATH"] = str(Path(__file__).parent.resolve())

    _ = session.run("pytest", "-vv")


@nox.session
def lint_with_flake8(session: nox.Session) -> None:
    """Lint the codebase with flake8."""
    session.install("flake8")
    _ = session.run("flake8")


@nox.session
def lint_with_ruff(session: nox.Session) -> None:
    """Lint the codebase with ruff."""
    session.install("ruff")
    _ = session.run("ruff")


@nox.session
def lint_with_pylint(session: nox.Session) -> None:
    """Lint the codebase with pylint."""
    session.install("pylint")
    _ = session.run("pylint")


@nox.session
def type_check_with_mypy(session: nox.Session) -> None:
    """Type-check the codebase with mypy."""
    session.install("mypy")
    _ = session.run("mypy")


@nox.session
def type_check_with_pyright(session: nox.Session) -> None:
    """Type-check the codebase with pyright."""
    session.install("pyright")
    _ = session.run("pyright")


@nox.session
def type_check_with_pytype(session: nox.Session) -> None:
    """Type-check the codebase with pytype."""
    session.install("pytype")
    _ = session.run("pytype")


@nox.session
def type_check_with_pyre(session: nox.Session) -> None:
    """Type-check the codebase with pyre."""
    session.install("pyre-check")
    _ = session.run("pyre")


@nox.session
def type_check_with_basedpyright(session: nox.Session) -> None:
    """Type-check the codebase with basedpyright."""
    session.install("basedpyright")
    _ = session.run("basedpyright")


@nox.session
def lint_imports(session: nox.Session) -> None:
    """Lint the codebase with importlinter."""
    _ = session.run("lint-imports")


@nox.session
def noop(session: nox.Session) -> None:
    """No operation.

    Dummy one just to do nothing.
    """
