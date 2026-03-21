"""Configuration for pytest."""

import pytest
from beartype import beartype


def pytest_collection_modifyitems(items: list[pytest.Function]) -> None:
    """Apply the beartype decorator to all collected test functions."""
    for item in items:
        item.obj = beartype(obj=item.obj)
