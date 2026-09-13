"""Contracts for shared formatter fallback selection."""

from typing import TYPE_CHECKING

import pytest

from literalizer._formatters.fallbacks import (
    collection_or_default,
    nonempty_or_default,
    value_or_default,
)

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


@pytest.mark.parametrize(
    argnames=("value", "optional_expected", "nonempty_expected"),
    argvalues=[
        (None, "default", "default"),
        ("", "", "default"),
        ("configured", "configured", "configured"),
    ],
)
def test_optional_and_empty_fallbacks(
    value: str | None, optional_expected: str, nonempty_expected: str
) -> None:
    """Absent and empty settings retain their distinct meanings."""
    assert (
        value_or_default(value=value, default="default") == optional_expected
    )
    assert (
        nonempty_or_default(value=value, default="default")
        == nonempty_expected
    )


def test_collection_fallback_preserves_identity() -> None:
    """Only collection-valued inference may replace the source opener data."""
    source: list[Value] = [1]
    mapping: dict[Scalar, Value] = {"a": 2}
    sequence: list[Value] = [3]
    scalar_set: set[Scalar] = {4}
    assert collection_or_default(value=mapping, default=source) is mapping
    assert collection_or_default(value=sequence, default=source) is sequence
    assert (
        collection_or_default(value=scalar_set, default=source) is scalar_set
    )
    assert collection_or_default(value=None, default=source) is source
    assert collection_or_default(value=5, default=source) is source
