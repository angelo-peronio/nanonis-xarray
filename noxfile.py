"""Nox configuration."""

import re
from pathlib import Path
from tempfile import gettempdir
from typing import Any

import nox
from nox.sessions import Session

nox.needs_version = ">=2024.3.2"
nox.options.default_venv_backend = "uv"
nox.options.envdir = Path(gettempdir()) / "nox"
nox.options.error_on_missing_interpreters = True
nox.options.error_on_external_run = True

pyproject = nox.project.load_toml("pyproject.toml")


def version_tuple(version: str) -> tuple[int, ...]:
    """'1.24' --> (1, 24)."""
    return tuple(int(s) for s in version.split("."))


def get_python_versions(pyproject: dict[str, Any]) -> list[str]:
    """Extract a sorted list of supported Python versions from the Trove classifiers."""
    classifiers = pyproject["project"]["classifiers"]
    match_classifier = re.compile(
        r"Programming Language :: Python :: (?P<version>\d+\.\d+)"
    ).fullmatch
    python_versions = [
        m.group("version")
        for classifier in classifiers
        if (m := match_classifier(classifier))
    ]
    return sorted(python_versions, key=version_tuple)


python_versions = get_python_versions(pyproject)

# TODO: read from pyproject.
oldest_numpy = "1.24"
oldest_xarray = "2022.11"


@nox.session(python=python_versions)
def test_python(session: Session) -> None:
    """Test the supported Python versions."""
    session.install(".[test]")
    session.run("pytest")


@nox.session(python=python_versions[0])
def test_oldest(session: Session) -> None:
    """Test the oldest supported versions of Python and the dependencies."""
    session.install(
        f"numpy=={oldest_numpy}",
        f"xarray=={oldest_xarray}",
        ".[test]",
    )
    session.run("pytest")


@nox.session()
def coverage(session: Session) -> None:
    """Generate test coverage report."""
    # We generate XML because Codecov would convert it to XML anyway.
    # Coverage analysis slows down the testing, so we do it only once.
    session.install(".[test]")
    session.run("pytest", "--cov=gsffile", "--cov-report=xml")
