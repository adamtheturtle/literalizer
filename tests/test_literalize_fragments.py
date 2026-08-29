"""Tests for intentionally incomplete literal fragments."""

# pylint: disable=import-private-name,protected-access,useless-suppression,wrong-spelling-in-comment
# ruff: noqa: SLF001

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

import literalizer
from literalizer import (
    InputFormat,
    _literalize,
    literalize,
    literalize_call,
)
from literalizer.languages import OCaml, PureScript, Python, Rust

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


@pytest.mark.parametrize(
    argnames=("lang_cls", "expected"),
    ids=["OCaml", "PureScript"],
    argvalues=[
        (
            OCaml,
            (
                "type val_t =\n"
                "  | OInt of int\n"
                "  | OList of val_t list\n"
                "let _ = Module.func(OInt 1)"
            ),
        ),
        (
            PureScript,
            (
                "data Val\n"
                "    = PInt Int\n"
                "    | PList (Array Val)\n"
                "Module.func (PInt 1)"
            ),
        ),
    ],
)
def test_unwrapped_qualified_call_target(
    *,
    lang_cls: literalizer.LanguageCls,
    expected: str,
) -> None:
    """A module-qualified call target renders as a bare fragment.

    These languages spell a module with an initial capital, which their
    declaration grammar refuses, so a wrapped file cannot declare the
    target -- but the call itself is what the caller places in a module
    that already imports it.  Elm is absent because it flattens a
    dotted target into one identifier, and the flattened name is
    capitalized and so not a value name at all (issue #4525).
    """
    result = literalize_call(
        source="- - 1\n",
        input_format=InputFormat.YAML,
        language=lang_cls(),
        target_function="Module.func",
        parameter_names=["a"],
    )
    assert result.code == expected


@pytest.mark.parametrize(
    argnames="ref_values",
    argvalues=[
        pytest.param(None, id="none"),
        pytest.param({"zzz": 5}, id="unrelated"),
    ],
)
def test_unresolved_ref_marker_leaves_no_preamble(
    ref_values: dict[str, int] | None,
) -> None:
    """A marker with no value supplied asks for nothing of its own.

    An unresolved marker is a bare identifier in the rendered code, so
    the mapping it is written as must not reach preamble inference; and
    an entry naming something else must not change what identical code
    asks for (issue #4480).
    """
    result = literalize(
        source='[{"$ref": "a"}, 1]',
        input_format=InputFormat.JSON,
        language=Rust(),
        ref_key="$ref",
        ref_values=ref_values,
    )
    assert result.bare_code == "vec![\n    a,\n    1,\n]"
    assert not result.preamble
