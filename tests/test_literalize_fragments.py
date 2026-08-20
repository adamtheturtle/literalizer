"""Tests for intentionally incomplete literal fragments."""

# pylint: disable=import-private-name,protected-access,useless-suppression,wrong-spelling-in-comment
# ruff: noqa: SLF001

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer import (
    InputFormat,
    _literalize,
    literalize,
)
from literalizer.languages import Python

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


def test_binary_without_sequence_delimiters() -> None:
    """YAML binary renders when the enclosing sequence is omitted."""
    result = literalize(
        source="- !!binary SGVsbG8=\n",
        input_format=InputFormat.YAML,
        language=Python(),
        pre_indent_level=0,
        include_delimiters=False,
        variable_form=None,
    )
    assert result.code == '"48656c6c6f",'


def test_ref_marker_search_covers_nested_sequences_and_scalars() -> None:
    """Nested lists are searched and scalar leaves terminate recursion."""
    marker: dict[Scalar, Value] = {"$ref": "existing"}
    present_nested: list[Value] = []
    present_nested.append(marker)
    present: list[Value] = [0]
    present.append(present_nested)
    absent_nested: list[Value] = []
    absent_nested.append("plain")
    absent: list[Value] = [0]
    absent.append(absent_nested)
    mapping: dict[Scalar, Value] = {"nested": present}
    assert _literalize._contains_ref_marker(  # pyright: ignore[reportPrivateUsage]
        value=present, ref_key="$ref"
    )
    assert not _literalize._contains_ref_marker(  # pyright: ignore[reportPrivateUsage]
        value=absent, ref_key="$ref"
    )
    assert _literalize._contains_ref_marker(  # pyright: ignore[reportPrivateUsage]
        value=mapping, ref_key="$ref"
    )
