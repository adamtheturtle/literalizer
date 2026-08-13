"""Identifier-case conversion tests."""

import pytest

from literalizer import IdentifierCase


@pytest.mark.parametrize(
    argnames=("name", "expected"),
    argvalues=[("a_b_c", "ABC"), ("a1_b2", "A1B2")],
)
def test_pascal_case_collapses_all_snake_separators(
    name: str,
    expected: str,
) -> None:
    """PascalCase and camelCase use the same normalized word
    boundaries.
    """
    assert IdentifierCase.PASCAL.convert(name=name) == expected
