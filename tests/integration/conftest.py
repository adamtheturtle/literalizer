"""Fixtures shared across the integration test modules."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session", name="cases_dir")
def fixture_cases_dir() -> Path:
    """Return the absolute path to the integration test cases
    directory.
    """
    return Path(__file__).resolve().with_name(name="cases")
