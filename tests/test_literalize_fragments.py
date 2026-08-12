"""Tests for intentionally incomplete literal fragments."""

# pylint: disable=import-private-name,protected-access,wrong-spelling-in-comment
# ruff: noqa: SLF001

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer import (
    CollectionLayout,
    InputFormat,
    NewVariable,
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


def test_ref_markers_are_opt_in() -> None:
    """A ``$ref`` object remains data unless marker handling is
    enabled.
    """
    source = '{"value":{"$ref":"foo"}}'
    variable_form = NewVariable(name="my_data", modifiers=frozenset())

    assert literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=variable_form,
    ).code == ('my_data = {\n    "value": {"$ref": "foo"},\n}')
    assert literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=variable_form,
        ref_key="$ref",
    ).code == ('my_data = {\n    "value": foo,\n}')


def test_ref_markers_preserve_multiline_collection_openers() -> None:
    """Ref-aware nested dicts and lists keep their multiline openers."""
    result = literalize(
        source=(
            '{"mapping":{"value":1,"ref":{"$ref":"foo"}},'
            '"sequence":[1,{"$ref":"bar"},2]}'
        ),
        input_format=InputFormat.JSON,
        language=Python(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        ref_key="$ref",
        collection_layout=CollectionLayout.MULTILINE,
    )

    assert result.code == (
        "my_data = {\n"
        '    "mapping": {\n'
        '        "value": 1,\n'
        '        "ref": foo,\n'
        "    },\n"
        '    "sequence": (\n'
        "        1,\n"
        "        bar,\n"
        "        2,\n"
        "    ),\n"
        "}"
    )
