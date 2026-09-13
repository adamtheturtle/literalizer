"""Formatter contracts for combinations outside the golden corpus."""

import datetime

import pytest

from literalizer import (
    CollectionLayout,
    InputFormat,
    StubReturn,
    literalize,
    literalize_call,
)
from literalizer._language import Language
from literalizer._types import Scalar, Value
from literalizer.languages import (
    Cpp,
    Crystal,
    Elm,
    Java,
    JavaScript,
    Kotlin,
    Nim,
    Python,
    Roc,
    Ruby,
    Rust,
    Sml,
    TypeScript,
)


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[
        JavaScript(string_format=JavaScript.string_formats.MULTILINE),
        TypeScript(string_format=TypeScript.string_formats.MULTILINE),
    ],
)
def test_multiline_strings_in_ordered_map(language: Language) -> None:
    """Template string keys use computed property syntax in ordered
    maps.
    """
    result = literalize(
        source="!!omap\n- a: 1\n",
        input_format=InputFormat.YAML,
        language=language,
    )
    assert result.bare_code == "{\n  [`a`]: 1,\n}"


def test_negative_timezone_offset() -> None:
    """Negative hours and minutes retain their signs in native
    literals.
    """
    offset = datetime.timezone(
        offset=datetime.timedelta(hours=-5, minutes=-30)
    )
    value = datetime.datetime(year=2000, month=1, day=1, tzinfo=offset)
    assert Python().format_datetime(value) == (
        "datetime.datetime(year=2000, month=1, day=1, hour=0, minute=0, "
        "second=0, tzinfo=datetime.timezone(offset=datetime.timedelta("
        "hours=-5, minutes=-30)))"
    )
    assert Ruby().format_datetime(value) == (
        'Time.new(2000, 1, 1, 0, 0, 0, "-05:30")'
    )


def test_elm_integer_format_handles_i64_minimum() -> None:
    """The raw format preserves its special minimum-integer spelling."""
    assert Elm.integer_formats.DECIMAL(-(2**63)) == (
        "EInt ((-9223372036854775807 - 1))"
    )


def test_sml_negative_epoch_constructor() -> None:
    """Epoch dates before 1970 use SML's signed integer syntax."""
    language = Sml(datetime_format=Sml.datetime_formats.EPOCH)
    value = datetime.datetime(year=1960, month=1, day=1, tzinfo=datetime.UTC)
    formatted = language.format_datetime(value)
    assert language.format_sequence_entry(value, formatted) == (
        "SInt (~315619200)"
    )


def test_nim_zero_argument_value_method_stub() -> None:
    """A value-returning method with no arguments needs only self."""
    assert Nim().format_call_stub(
        ("thing", "go"), (), StubReturn.VALUE, []
    ) == (
        "type ThingType = object",
        "proc go(self: ThingType): int {.discardable.} = 0",
        "var thing: ThingType",
    )


def test_nim_iso_date_variant_needs_no_json_import() -> None:
    """String dates do not inherit the native date's JSON import."""
    language = Nim(
        heterogeneous_strategy=Nim.heterogeneous_strategies.OBJECT_VARIANT,
        date_format=Nim.date_formats.ISO,
    )
    assert language.scalar_preamble[datetime.date] == ()
    assert language.scalar_preamble[datetime.datetime] == ("import json",)


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
    record: dict[Scalar, Value] = {"a": 1}
    assert language.sequence_open([record, 2]) == "listOf<Any?>("


def test_roc_wrappers_without_preamble() -> None:
    """Empty preambles do not add separator lines."""
    language = Roc()
    assert (
        language.wrap_in_file(
            content="test", variable_name="test", body_preamble=()
        )
        == "module [test]\n\ntest"
    )
    assert (
        language.wrap_calls_with_declarations(
            declarations=(), calls="call", body_preamble=()
        )
        == "module [main]\n\nmain =\n    dbg (call)\n    {}"
    )


def test_bound_call_transform_consumes_return_value() -> None:
    """A call transform composes with declarations for bound arguments."""
    result = literalize_call(
        source='[{"$ref":"x"}]',
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="f",
        parameter_names=["a"],
        bound_refs={"x": 1},
        ref_key="$ref",
        call_transform=lambda context: f"print({context.call})",
        wrap_in_file=True,
    )
    assert "print(f(a=x))" in result.code
    assert "x = 1" in result.code


def test_whole_call_comment() -> None:
    """A whole-input call receives its single source comment."""
    result = literalize_call(
        source="[1]",
        input_format=InputFormat.JSON,
        language=Python(),
        target_function="f",
        parameter_names=["a"],
        per_element=False,
        comment_source=["note"],
    )
    assert result.code == "f(a=(1,))  # note"


def test_cpp_positional_empty_lists_share_element_type() -> None:
    """Empty positional cousins inherit the common nested list type."""
    empty: list[Value] = [list[Value](), list[Value]()]
    populated: list[Value] = [list[Value]([1]), list[Value]([1])]
    assert Cpp().sequence_open([empty, populated]) == (
        "std::vector<std::vector<std::vector<int>>>{"
    )


def test_cpp14_tuple_preamble() -> None:
    """C++14 tuple values require the tuple header without
    std::variant.
    """
    language = Cpp(
        language_version=Cpp.version_formats.CPP14,
        heterogeneous_strategy=Cpp.heterogeneous_strategies.TUPLE,
    )
    data: list[Value] = [1, "two"]
    assert language.data_dependent_preamble(data) == ("#include <tuple>",)


def test_java_boxed_mixed_numeric_annotation() -> None:
    """A set annotation boxes its widened numeric element type."""
    language = Java(
        variable_type_hints=Java.variable_type_hints_formats.ALWAYS,
    )
    data: Value = set[Scalar]({1, 2.5})
    assert (
        language.format_variable_declaration(
            "data", "value", data, frozenset()
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


def test_python_list_of_records_field_annotation() -> None:
    """List-form record fields use list annotations without tuple ellipses."""
    result = literalize(
        source='{"items":[{"a":1}]}',
        input_format=InputFormat.JSON,
        language=Python(
            sequence_format=Python.sequence_formats.LIST,
            heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
        ),
    )
    assert "items: list[Record1]" in "\n".join(result.preamble)


def test_kotlin_nested_dictionary_array_fallback() -> None:
    """Nested arrays with map elements retain the general map value
    type.
    """
    nested_map: dict[Scalar, Value] = {"b": 1}
    inner: list[Value] = [nested_map]
    outer: list[Value] = [inner]
    assert Kotlin().dict_format_config.dict_open({"a": outer}) == (
        "mapOf<String, Any?>("
    )


def test_java_nested_sibling_sequence_overrides() -> None:
    """Matching positions across sibling maps share widened array
    openers.
    """
    result = literalize(
        source='{"a":[[1],[2]],"b":[["x"],["y"]]}',
        input_format=InputFormat.JSON,
        language=Java(),
    )
    assert result.bare_code == (
        "Map.ofEntries(\n"
        '    Map.entry("a", new Object[]{new Object[]{1}, new Object[]{2}}),\n'
        '    Map.entry("b", new Object[]{new Object[]{"x"}, '
        'new Object[]{"y"}})\n'
        ")"
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


def test_multiline_sibling_integer_widening() -> None:
    """Multiline sibling lists retain their shared widened integer
    format.
    """
    result = literalize(
        source='{"a":[1],"b":[1099511627776]}',
        input_format=InputFormat.JSON,
        language=Java(),
        collection_layout=CollectionLayout.MULTILINE,
    )
    assert result.bare_code == (
        "Map.ofEntries(\n"
        '    Map.entry("a", new Object[]{\n'
        "        1L\n"
        "    }),\n"
        '    Map.entry("b", new Object[]{\n'
        "        1099511627776L\n"
        "    })\n"
        ")"
    )
