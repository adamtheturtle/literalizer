"""Fixtures shared across the integration test modules."""

from pathlib import Path

import pytest
from pyprojroot import find_root, has_file


@pytest.fixture(name="cases_dir")
def fixture_cases_dir() -> Path:
    """Return the absolute path to the integration test cases
    directory.
    """
    return (
        find_root(
            criterion=has_file(file="pyproject.toml"),
            start=Path(__file__).resolve(),
        )
        / "tests"
        / "integration"
        / "cases"
    )
