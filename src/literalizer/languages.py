"""Built-in language specifications for 14 programming languages."""

from __future__ import annotations

from beartype import beartype

__all__ = [
    "CLOJURE",
    "CPP",
    "CSHARP",
    "DART",
    "ELIXIR",
    "FSHARP",
    "GO",
    "HASKELL",
    "JAVA",
    "JAVASCRIPT",
    "JULIA",
    "KOTLIN",
    "PHP",
    "PYTHON",
    "RUBY",
    "RUST",
    "SCALA",
    "SWIFT",
    "TYPESCRIPT",
    "R",
]

from literalizer._language import LanguageSpec
from literalizer.formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_date_php,
    format_datetime_iso,
    format_datetime_php,
    format_variable_assignment_clojure,
    format_variable_assignment_cpp,
    format_variable_assignment_csharp,
    format_variable_assignment_dart,
    format_variable_assignment_elixir,
    format_variable_assignment_fsharp,
    format_variable_assignment_go,
    format_variable_assignment_haskell,
    format_variable_assignment_java,
    format_variable_assignment_js,
    format_variable_assignment_kotlin,
    format_variable_assignment_php,
    format_variable_assignment_python,
    format_variable_assignment_r,
    format_variable_assignment_ruby,
    format_variable_assignment_rust,
    format_variable_assignment_scala,
    format_variable_assignment_swift,
    format_variable_declaration_clojure,
    format_variable_declaration_cpp,
    format_variable_declaration_csharp,
    format_variable_declaration_dart,
    format_variable_declaration_elixir,
    format_variable_declaration_fsharp,
    format_variable_declaration_go,
    format_variable_declaration_haskell,
    format_variable_declaration_java,
    format_variable_declaration_js,
    format_variable_declaration_julia,
    format_variable_declaration_kotlin,
    format_variable_declaration_php,
    format_variable_declaration_python,
    format_variable_declaration_r,
    format_variable_declaration_ruby,
    format_variable_declaration_rust,
    format_variable_declaration_scala,
    format_variable_declaration_swift,
    passthrough_list_entry,
    passthrough_set_entry,
    to_fsharp_val,
)


def _format_python_omap_entry(key: str, value: str) -> str:
    """Format one Python ``OrderedDict`` entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


PYTHON = LanguageSpec(
    null_literal="None",
    true_literal="True",
    false_literal="False",
    collection_open="(",
    collection_close=")",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=True,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set="set()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    omap_open="OrderedDict([",
    omap_close="])",
    format_omap_entry=_format_python_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_python,
    format_variable_assignment=format_variable_assignment_python,
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_csharp_dict_entry(key: str, value: str) -> str:
    """Format a C# dictionary indexer entry."""
    return f"[{key}] = {value}"


CSHARP = LanguageSpec(
    null_literal="(object?)null",
    true_literal="true",
    false_literal="false",
    collection_open="(",
    collection_close=")",
    dict_open="new Dictionary<string, object> {",
    dict_close="}",
    format_dict_entry=_format_csharp_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection="ValueTuple.Create()",
    empty_dict=None,
    set_open="new HashSet<object> {",
    set_close="}",
    empty_set="new HashSet<object>()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="new Dictionary<string, object> {",
    omap_close="}",
    format_omap_entry=_format_csharp_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_csharp,
    format_variable_assignment=format_variable_assignment_csharp,
    format_list_entry=passthrough_list_entry,
)


def _format_dart_omap_entry(key: str, value: str) -> str:
    """Format a Dart map entry."""
    return f"{key}: {value}"


DART = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set="<dynamic>{}",
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_dart_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_dart,
    format_variable_assignment=format_variable_assignment_dart,
    format_list_entry=passthrough_list_entry,
)


def _format_js_omap_entry(key: str, value: str) -> str:
    """Format a JavaScript/TypeScript ordered-map entry."""
    return f"{key}: {value}"


JAVASCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="new Set([",
    set_close="])",
    empty_set="new Set()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_js_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_js,
    format_variable_assignment=format_variable_assignment_js,
    format_list_entry=passthrough_list_entry,
)

TYPESCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="new Set([",
    set_close="])",
    empty_set="new Set()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_js_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_js,
    format_variable_assignment=format_variable_assignment_js,
    format_list_entry=passthrough_list_entry,
)


def _format_ruby_omap_entry(key: str, value: str) -> str:
    """Format a Ruby ordered-map entry."""
    return f"{key} => {value}"


RUBY = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="Set.new([",
    set_close="])",
    empty_set="Set.new",
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_ruby_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_ruby,
    format_variable_assignment=format_variable_assignment_ruby,
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_go_set_entry(item: str) -> str:
    """Format a Go set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple": struct{}{}``.
    """
    return f"{item}: struct{{}}{{}}"


def _format_go_omap_entry(key: str, value: str) -> str:
    """Format a Go ordered-map entry as a ``{key, value}`` pair."""
    return f"{{{key}, {value}}}"


GO = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[]any{",
    collection_close="}",
    dict_open="map[string]any{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="map[any]struct{}{",
    set_close="}",
    empty_set=None,
    format_set_entry=_format_go_set_entry,
    comment_prefix="//",
    omap_open="[][2]any{",
    omap_close="}",
    format_omap_entry=_format_go_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_go,
    format_variable_assignment=format_variable_assignment_go,
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_cpp_dict_entry(key: str, value: str) -> str:
    """Format a C++ dict entry as a brace-enclosed pair."""
    return f"{{{key}, {value}}}"


CPP = LanguageSpec(
    null_literal="nullptr",
    true_literal="true",
    false_literal="false",
    collection_open="{",
    collection_close="}",
    dict_open="{",
    dict_close="}",
    format_dict_entry=_format_cpp_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_cpp_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_cpp,
    format_variable_assignment=format_variable_assignment_cpp,
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_java_dict_entry(key: str, value: str) -> str:
    """Format a Java ``Map.entry(key, value)`` call."""
    return f"Map.entry({key}, {value})"


JAVA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="new Object[]{",
    collection_close="}",
    dict_open="Map.ofEntries(",
    dict_close=")",
    format_dict_entry=_format_java_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="Set.of(",
    set_close=")",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="new java.util.ArrayList<>(java.util.Arrays.asList(",
    omap_close="))",
    format_omap_entry=_format_java_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    format_variable_declaration=format_variable_declaration_java,
    format_variable_assignment=format_variable_assignment_java,
    skip_null_dict_values=True,
    format_list_entry=passthrough_list_entry,
)


def _format_swift_omap_entry(key: str, value: str) -> str:
    """Format a Swift dictionary entry."""
    return f"{key}: {value}"


SWIFT = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection="[Any]()",
    empty_dict="[String: Any]()",
    set_open="Set<AnyHashable>([",
    set_close="])",
    empty_set="Set<AnyHashable>()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_swift_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_swift,
    format_variable_assignment=format_variable_assignment_swift,
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_rust_dict_entry(key: str, value: str) -> str:
    """Format a Rust HashMap entry as a tuple ``(key, value)``."""
    return f"({key}, {value})"


def _format_rust_omap_entry(key: str, value: str) -> str:
    """Format a Rust ordered-map entry as a tuple ``(key, value)``."""
    return f"({key}, {value})"


RUST = LanguageSpec(
    null_literal="None",
    true_literal="true",
    false_literal="false",
    collection_open="vec![",
    collection_close="]",
    dict_open="HashMap::from([",
    dict_close="])",
    format_dict_entry=_format_rust_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="HashSet::from([",
    set_close="])",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="HashMap::from([",
    omap_close="])",
    format_omap_entry=_format_rust_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_rust,
    format_variable_assignment=format_variable_assignment_rust,
    format_list_entry=passthrough_list_entry,
)


def _format_kotlin_omap_entry(key: str, value: str) -> str:
    """Format a Kotlin ordered-map entry."""
    return f"{key} to {value}"


KOTLIN = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="listOf<Any?>(",
    collection_close=")",
    dict_open="mapOf<String, Any?>(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" to "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="setOf<Any?>(",
    set_close=")",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="linkedMapOf<String, Any?>(",
    omap_close=")",
    format_omap_entry=_format_kotlin_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_kotlin,
    format_variable_assignment=format_variable_assignment_kotlin,
    format_list_entry=passthrough_list_entry,
)


def _format_php_omap_entry(key: str, value: str) -> str:
    """Format one PHP array entry as a ``key => value`` pair."""
    return f"{key} => {value}"


PHP = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_php,
    format_datetime=format_datetime_php,
    empty_collection=None,
    empty_dict=None,
    set_open="[",
    set_close="]",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_php_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_php,
    format_variable_assignment=format_variable_assignment_php,
    format_list_entry=passthrough_list_entry,
)


def _format_julia_omap_entry(key: str, value: str) -> str:
    """Format a Julia ordered-map entry as a pair arrow expression."""
    return f"{key} => {value}"


JULIA = LanguageSpec(
    null_literal="nothing",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="Dict(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict="Dict()",
    set_open="Set([",
    set_close="])",
    empty_set="Set()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_julia_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_julia,
    format_variable_assignment=format_variable_declaration_julia,
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_elixir_omap_entry(key: str, value: str) -> str:
    """Format an Elixir ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


ELIXIR = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="%{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="MapSet.new([",
    set_close="])",
    empty_set="MapSet.new()",
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_elixir_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_elixir,
    format_variable_assignment=format_variable_assignment_elixir,
    element_separator=", ",
    format_list_entry=passthrough_list_entry,
)


@beartype
def _format_haskell_dict_entry(key: str, value: str) -> str:
    """Format a Haskell dict entry as a tuple pair."""
    return f"({key}, {value})"


def _format_haskell_omap_entry(key: str, value: str) -> str:
    """Format a Haskell ordered-map entry as a tuple pair."""
    return f"({key}, {value})"


HASKELL = LanguageSpec(
    null_literal="HNull",
    true_literal="HBool True",
    false_literal="HBool False",
    collection_open="HList [",
    collection_close="]",
    dict_open="HMap [",
    dict_close="]",
    format_dict_entry=_format_haskell_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="HSet [",
    set_close="]",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="--",
    omap_open="HMap [",
    omap_close="]",
    format_omap_entry=_format_haskell_omap_entry,
    multiline_close_indent="    ",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_haskell,
    format_variable_assignment=format_variable_assignment_haskell,
    format_list_entry=passthrough_list_entry,
)


def _format_fsharp_dict_entry(key: str, value: str) -> str:
    """Format an F# dict entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {to_fsharp_val(value)})"  # type: ignore[misc]


def _format_fsharp_omap_entry(key: str, value: str) -> str:
    """Format an F# ordered-map entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {to_fsharp_val(value)})"  # type: ignore[misc]


def _format_fsharp_set_entry(item: str) -> str:
    """Format an F# set entry with the appropriate ``Val`` constructor."""
    return to_fsharp_val(item)  # type: ignore[misc]


def _format_fsharp_list_entry(item: str) -> str:
    """Format an F# list entry with the appropriate ``Val``
    constructor.
    """
    return to_fsharp_val(item)  # type: ignore[misc]


FSHARP = LanguageSpec(
    null_literal="FNull",
    true_literal="FBool true",
    false_literal="FBool false",
    collection_open="FList [",
    collection_close="]",
    dict_open="FMap [",
    dict_close="]",
    format_dict_entry=_format_fsharp_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="FSet [",
    set_close="]",
    empty_set=None,
    format_set_entry=_format_fsharp_set_entry,
    comment_prefix="//",
    omap_open="FMap [",
    omap_close="]",
    format_omap_entry=_format_fsharp_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_fsharp,
    format_variable_assignment=format_variable_assignment_fsharp,
    element_separator="; ",
    format_list_entry=_format_fsharp_list_entry,
)


CLOJURE = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" "),
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="#{",
    set_close="}",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix=";",
    omap_open="{",
    omap_close="}",
    format_omap_entry=dict_entry_with_separator(separator=" "),
    multiline_close_indent="",
    element_separator=" ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_clojure,
    format_variable_assignment=format_variable_assignment_clojure,
    format_list_entry=passthrough_list_entry,
)


def _format_scala_omap_entry(key: str, value: str) -> str:
    """Format a Scala ``ListMap`` entry as a ``key -> value`` pair."""
    return f"{key} -> {value}"


SCALA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="List(",
    collection_close=")",
    dict_open="Map(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" -> "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="Set(",
    set_close=")",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    omap_open="scala.collection.immutable.ListMap(",
    omap_close=")",
    format_omap_entry=_format_scala_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_scala,
    format_variable_assignment=format_variable_assignment_scala,
    format_list_entry=passthrough_list_entry,
)


def _format_r_omap_entry(key: str, value: str) -> str:
    """Format an R named list entry for an ordered map."""
    return f"{key} = {value}"


R = LanguageSpec(
    null_literal="NULL",
    true_literal="TRUE",
    false_literal="FALSE",
    collection_open="list(",
    collection_close=")",
    dict_open="list(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" = "),
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_collection=None,
    empty_dict=None,
    set_open="list(",
    set_close=")",
    empty_set=None,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    omap_open="list(",
    omap_close=")",
    format_omap_entry=_format_r_omap_entry,
    multiline_trailing_comma=False,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_r,
    format_variable_assignment=format_variable_assignment_r,
    format_list_entry=passthrough_list_entry,
)
