"""Formatter contracts for combinations outside the golden corpus."""

from textwrap import dedent

from literalizer import (
    InputFormat,
    NewVariable,
    literalize,
)
from literalizer.languages import (
    Cpp,
    Crystal,
    Elm,
    Java,
    Roc,
    Rust,
)


def test_elm_integer_format_handles_i64_minimum() -> None:
    """The raw format preserves its special minimum-integer spelling."""
    # The public API rejects integers outside Elm's supported range before
    # invoking the formatter, so this spelling needs a direct formatter test.
    assert Elm.integer_formats.DECIMAL(-(2**63)) == (
        "EInt ((-9223372036854775807 - 1))"
    )


def test_crystal_plain_dictionary_entry() -> None:
    """A quoted key does not need the percent-literal spacing escape."""
    result = literalize(
        source='{"a|b": 1}',
        input_format=InputFormat.JSON,
        language=Crystal(string_format=Crystal.string_formats.MULTILINE),
    )
    assert result.code == '{\n    "a|b" => 1,\n}'


def test_roc_wrappers_without_preamble() -> None:
    """Empty preambles do not add separator lines."""
    language = Roc(dict_format=Roc.dict_formats.RECORD)
    result = literalize(
        source="{}",
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="test", modifiers=frozenset()),
        wrap_in_file=True,
    )
    assert result.code == dedent(
        text="""\
        module [test]

        test = {}"""
    )


def test_roc_call_wrapper_without_preamble() -> None:
    """An empty call preamble does not add separator lines."""
    # Wrapped public calls always generate a stub in the body preamble.
    # Only the wrapper itself accepts a call with no stub or declarations.
    language = Roc()
    assert language.wrap_calls_with_declarations(
        declarations=(), calls="call", body_preamble=()
    ) == dedent(
        text="""\
        module [main]

        main =
            dbg (call)
            {}"""
    )


def test_java_boxed_mixed_numeric_annotation() -> None:
    """A set annotation boxes its widened numeric element type."""
    # Keep the formatter contract here: the public renderer currently emits
    # Set<Double> with integer elements that javac rejects, so this combination
    # cannot yet be covered by a compiling golden.
    language = Java(
        variable_type_hints=Java.variable_type_hints_formats.ALWAYS,
    )
    assert (
        language.format_variable_declaration(
            "data", "value", {1, 2.5}, frozenset()
        )
        == "Set<Double> data = value;"
    )


def test_rust_static_datetime_annotation() -> None:
    """Datetime annotations retain time information rather than date
    type.
    """
    language = Rust(
        declaration_style=Rust.declaration_styles.STATIC,
        sequence_format=Rust.sequence_formats.ARRAY,
    )
    result = literalize(
        source="2000-01-01T00:00:00",
        input_format=InputFormat.YAML,
        language=language,
        variable_form=NewVariable(name="value", modifiers=frozenset()),
    )
    assert result.code == (
        "static value: NaiveDateTime = NaiveDateTime::new("
        "NaiveDate::from_ymd_opt(2000, 1, 1).unwrap(), "
        "NaiveTime::from_hms_opt(0, 0, 0).unwrap());"
    )
    assert result.preamble == (
        "use chrono::NaiveDate;",
        "use chrono::NaiveDateTime;",
        "use chrono::NaiveTime;",
    )


def test_rust_mutable_json_declaration() -> None:
    """The ``mut`` modifier applies to JSON-backed local declarations."""
    language = Rust(json_type=Rust.json_types.SERDE_JSON_VALUE)
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(
            name="data", modifiers=frozenset({Rust.modifiers.MUT})
        ),
    )
    assert result.code == (
        "let mut data: serde_json::Value = serde_json::json!(1);"
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
