"""Fixtures shared across the integration test modules."""

from pathlib import Path

import pytest
from beartype import beartype


@pytest.fixture(name="cases_dir")
@beartype
def fixture_cases_dir(request: pytest.FixtureRequest) -> Path:
    """Return the absolute path to the integration test cases
    directory.
    """
    return request.config.rootpath / "tests" / "integration" / "cases"
