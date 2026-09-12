"""Tests for intentionally incomplete literal fragments.

Every golden case wraps its value in a whole file, so a fragment
rendered without its delimiters has no golden surface (issue #4699,
and #3557 for the same gap on ``LiteralizeResult``).
"""

from __future__ import annotations

import pytest

import literalizer
from literalizer import (
    InputFormat,
    literalize,
    literalize_call,
)
from literalizer.languages import Cpp, OCaml, PureScript, Python, Rust


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


@pytest.mark.parametrize(
    argnames=("source", "expected"),
    argvalues=[
        (
            '[0, [[{"\\u0024ref": "existing"}]]]',
            "(\n    0,\n    ((existing,),),\n)",
        ),
        (
            '[0, [["\\u0070lain"]]]',
            '(\n    0,\n    (("plain",),),\n)',
        ),
        (
            '{"nested": [0, {"\\u0024ref": "existing"}]}',
            '{\n    "nested": (0, existing),\n}',
        ),
    ],
)
def test_escaped_ref_marker_search_covers_nested_values(
    source: str,
    expected: str,
) -> None:
    """Escaped keys are found through nested lists and mappings."""
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=Python(),
        ref_key="$ref",
        ref_values={"existing": 1},
    )

    assert result.bare_code == expected


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
    assert len(result.preamble) == 0


def test_ordered_map_argument_types_from_its_reference() -> None:
    """An ordered map takes the type its reference holds.

    A marker stands for a value declared elsewhere, so the ordered map
    around it is written with that value's type rather than with the
    marker's own mapping shape (issue #4732).  A golden would have to
    wrap the call in a file, where the generated stub's parameter type
    for an ordered map is a separate gap, so this stays an ordinary
    test.
    """
    result = literalize_call(
        source="- - !!omap\n    - m:\n        $ref: big_list\n",
        input_format=InputFormat.YAML,
        language=Cpp(),
        target_function="process",
        parameter_names=["a"],
        per_element=True,
        ref_key="$ref",
        ref_values={"big_list": ["x"]},
    )
    assert result.bare_code == (
        "process(std::vector<std::pair<std::string, "
        'std::vector<std::string>>>{{"m", big_list}});'
    )
