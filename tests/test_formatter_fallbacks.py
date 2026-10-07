"""Formatter contracts for combinations outside the golden corpus."""

import datetime
from textwrap import dedent

from literalizer import (
    InputFormat,
    literalize,
)
from literalizer.languages import (
    Cpp,
    Crystal,
    Elm,
    Kotlin,
    Roc,
    Rust,
)


def test_elm_integer_format_handles_i64_minimum() -> None:
    """The raw format preserves its special minimum-integer spelling."""
    assert Elm.integer_formats.DECIMAL(-(2**63)) == (
        "EInt ((-9223372036854775807 - 1))"
    )


def test_crystal_plain_dictionary_entry() -> None:
    """A quoted key does not need the percent-literal spacing escape."""
    assert Crystal(
        string_format=Crystal.string_formats.MULTILINE
    ).dict_format_config.format_entry('"a"', 1, "1") == ('"a" => 1')


def test_kotlin_unresolved_record_list_opener() -> None:
    """A record mixed with a scalar retains the general element type."""
    language = Kotlin(
        heterogeneous_strategy=Kotlin.heterogeneous_strategies.RECORD,
    )
    assert language.sequence_open([{"a": 1}, 2]) == "listOf<Any?>("


def test_roc_wrappers_without_preamble() -> None:
    """Empty preambles do not add separator lines."""
    language = Roc()
    assert language.wrap_in_file(
        content="test", variable_name="test", body_preamble=()
    ) == dedent(
        text="""\
        module [test]

        test"""
    )
    assert language.wrap_calls_with_declarations(
        declarations=(), calls="call", body_preamble=()
    ) == dedent(
        text="""\
        module [main]

        main =
            dbg (call)
            {}"""
    )


def test_cpp_positional_empty_lists_share_element_type() -> None:
    """Empty positional cousins inherit the common nested list type."""
    assert Cpp().sequence_open([[[], []], [[1], [1]]]) == (
        "std::vector<std::vector<std::vector<int>>>{"
    )


def test_rust_static_datetime_annotation() -> None:
    """Datetime annotations retain time information rather than date
    type.
    """
    language = Rust(
        declaration_style=Rust.declaration_styles.STATIC,
        sequence_format=Rust.sequence_formats.ARRAY,
    )
    assert (
        language.format_variable_declaration(
            "value",
            "stamp",
            datetime.datetime(year=2000, month=1, day=1, tzinfo=datetime.UTC),
            frozenset(),
        )
        == "static value: NaiveDateTime = stamp;"
    )


def test_rust_mutable_json_declaration() -> None:
    """The ``mut`` modifier applies to JSON-backed local declarations."""
    language = Rust(json_type=Rust.json_types.SERDE_JSON_VALUE)
    assert (
        language.format_variable_declaration(
            "data", "1", 1, frozenset({Rust.Modifiers["MUT"]})
        )
        == "let mut data: serde_json::Value = serde_json::json!(1);"
    )


def test_unknown_reference_ignores_unrelated_preamble_values() -> None:
    """An unbound fragment does not infer types from unrelated
    bindings.
    """
    result = literalize(
        source='{"$ref":"missing"}',
        input_format=InputFormat.JSON,
        language=Cpp(),
        ref_key="$ref",
        ref_values={"other": 1},
    )
    assert result.bare_code == "std::move(missing)"
