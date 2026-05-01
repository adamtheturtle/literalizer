"""Focused tests for collection-layout formatting."""

from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING

import pytest

import literalizer
from literalizer._literalize import (
    _collection_open_for_multiline_value,  # pyright: ignore[reportPrivateUsage]
)
from literalizer.languages import Python

if TYPE_CHECKING:
    from literalizer._types import Value


@pytest.mark.parametrize(
    argnames=("source", "expected"),
    argvalues=[
        (
            "outer:\n  inner:\n    x: 1\n",
            """\
            {
                "outer": {
                    "inner": {
                        "x": 1,
                    },
                },
            }""",
        ),
        (
            "outer:\n  !!set\n  ? a\n  ? b\n",
            """\
            {
                "outer": {
                    "a",
                    "b",
                },
            }""",
        ),
        (
            "outer: !!omap\n  - a: 1\n  - b: 2\n",
            """\
            {
                "outer": OrderedDict([
                    ("a", 1),
                    ("b", 2),
                ]),
            }""",
        ),
    ],
)
def test_multiline_nested_collection_delimiters(
    source: str,
    expected: str,
) -> None:
    """Nested collection delimiters are emitted on their own lines."""
    result = literalizer.literalize(
        source=source,
        input_format=literalizer.InputFormat.YAML,
        language=Python(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
        collection_layout=literalizer.CollectionLayout.MULTILINE,
    )

    assert result.code == textwrap.dedent(text=expected)


def test_multiline_open_overrides_take_precedence() -> None:
    """Widened collection openers override language defaults."""
    sequence_open = _collection_open_for_multiline_value(
        data=[1],
        spec=Python(),
        is_ordered_map=False,
        dict_open_override=None,
        sequence_open_override="override(",
        expand_refs=False,
        ref_key="$ref",
    )
    dict_open = _collection_open_for_multiline_value(
        data={"x": 1},
        spec=Python(),
        is_ordered_map=False,
        dict_open_override="override{",
        sequence_open_override=None,
        expand_refs=False,
        ref_key="$ref",
    )

    assert sequence_open == "override("
    assert dict_open == "override{"


def test_multiline_collection_open_filters_expanded_refs() -> None:
    """Ref-expanded nested collections compute openers without ref
    items.
    """
    spec = Python()
    ref_marker: dict[str, Value] = {"$ref": "existing"}
    dict_data: dict[str, Value] = {"keep": 1, "skip": ref_marker}
    list_data: list[Value] = [1, ref_marker]

    dict_open = _collection_open_for_multiline_value(
        data=dict_data,
        spec=spec,
        is_ordered_map=False,
        dict_open_override=None,
        sequence_open_override=None,
        expand_refs=True,
        ref_key="$ref",
    )
    sequence_open = _collection_open_for_multiline_value(
        data=list_data,
        spec=spec,
        is_ordered_map=False,
        dict_open_override=None,
        sequence_open_override=None,
        expand_refs=True,
        ref_key="$ref",
    )

    assert dict_open == "{"
    assert sequence_open == "("


def test_multiline_collection_open_uses_plain_list_items() -> None:
    """Non-ref-expanded list openers use all list items."""
    ref_marker: dict[str, Value] = {"$ref": "existing"}
    list_data: list[Value] = [1, ref_marker]

    result = _collection_open_for_multiline_value(
        data=list_data,
        spec=Python(),
        is_ordered_map=False,
        dict_open_override=None,
        sequence_open_override=None,
        expand_refs=False,
        ref_key="$ref",
    )

    assert result == "("
