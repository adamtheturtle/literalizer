"""Focused Bash variable-declaration tests."""

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer.languages import Bash

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


def test_newline_bracket_in_scalar_is_not_associative_array() -> None:
    """Rendered string contents do not determine the declaration type."""
    rendered = Bash().format_variable_declaration(
        "my_data",
        '"first\n[key]"',
        "first\n[key]",
        frozenset(),
    )

    assert rendered == 'declare my_data="first\n[key]"'


def test_dict_uses_associative_array_declaration() -> None:
    """Dict data selects Bash's associative-array flag."""
    data: dict[Scalar, Value] = {"key": "value"}
    rendered = Bash().format_variable_declaration(
        "my_data",
        '(["key"]="value")',
        data,
        frozenset(),
    )

    assert rendered == 'declare -A my_data=(["key"]="value")'


def test_dict_reference_uses_scalar_declaration() -> None:
    """A mapping reference is an identifier, not an array initializer."""
    data: dict[Scalar, Value] = {"key": "value"}
    rendered = Bash().format_variable_declaration(
        "my_data",
        "my_var",
        data,
        frozenset(),
    )

    assert rendered == "declare my_data=my_var"


def test_empty_dict_uses_untyped_declaration() -> None:
    """An empty Bash array does not need an associative-array flag."""
    data: dict[Scalar, Value] = {}
    rendered = Bash().format_variable_declaration(
        "my_data",
        "()",
        data,
        frozenset(),
    )

    assert rendered == "declare my_data=()"
