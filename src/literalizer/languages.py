"""Built-in language specifications for common programming languages."""

from __future__ import annotations

from beartype import beartype

__all__ = [
    "CLOJURE",
    "CPP",
    "CSHARP",
    "DART",
    "ELIXIR",
    "ERLANG",
    "FSHARP",
    "GO",
    "GROOVY",
    "HASKELL",
    "JAVA",
    "JAVASCRIPT",
    "JULIA",
    "KOTLIN",
    "OCAML",
    "PERL",
    "PHP",
    "PYTHON",
    "RUBY",
    "RUST",
    "SCALA",
    "SWIFT",
    "TYPESCRIPT",
    "C",
    "R",
]

from literalizer._language import LanguageSpec
from literalizer.formatters import (
    dict_entry_with_separator,
    format_bytes_erlang,
    format_bytes_hex,
    format_date_iso,
    format_date_php,
    format_datetime_iso,
    format_datetime_php,
    format_variable_assignment_c,
    format_variable_assignment_clojure,
    format_variable_assignment_cpp,
    format_variable_assignment_csharp,
    format_variable_assignment_dart,
    format_variable_assignment_elixir,
    format_variable_assignment_erlang,
    format_variable_assignment_fsharp,
    format_variable_assignment_go,
    format_variable_assignment_groovy,
    format_variable_assignment_haskell,
    format_variable_assignment_java,
    format_variable_assignment_js,
    format_variable_assignment_kotlin,
    format_variable_assignment_ocaml,
    format_variable_assignment_perl,
    format_variable_assignment_php,
    format_variable_assignment_python,
    format_variable_assignment_r,
    format_variable_assignment_ruby,
    format_variable_assignment_rust,
    format_variable_assignment_scala,
    format_variable_assignment_swift,
    format_variable_declaration_c,
    format_variable_declaration_clojure,
    format_variable_declaration_cpp,
    format_variable_declaration_csharp,
    format_variable_declaration_dart,
    format_variable_declaration_elixir,
    format_variable_declaration_erlang,
    format_variable_declaration_fsharp,
    format_variable_declaration_go,
    format_variable_declaration_groovy,
    format_variable_declaration_haskell,
    format_variable_declaration_java,
    format_variable_declaration_js,
    format_variable_declaration_julia,
    format_variable_declaration_kotlin,
    format_variable_declaration_ocaml,
    format_variable_declaration_perl,
    format_variable_declaration_php,
    format_variable_declaration_python,
    format_variable_declaration_r,
    format_variable_declaration_ruby,
    format_variable_declaration_rust,
    format_variable_declaration_scala,
    format_variable_declaration_swift,
    passthrough_sequence_entry,
    passthrough_set_entry,
    to_c_val,
    to_fsharp_val,
    to_ocaml_val,
)


def _format_python_omap_entry(key: str, value: str) -> str:
    """Format one Python ``OrderedDict`` entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


PYTHON = LanguageSpec(
    null_literal="None",
    true_literal="True",
    false_literal="False",
    sequence_open="(",
    sequence_close=")",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=True,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set="set()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="OrderedDict([",
    omap_close="])",
    format_omap_entry=_format_python_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_python,
    format_variable_assignment=format_variable_assignment_python,
)


@beartype
def _format_csharp_dict_entry(key: str, value: str) -> str:
    """Format a C# dictionary indexer entry."""
    return f"[{key}] = {value}"


CSHARP = LanguageSpec(
    null_literal="(object?)null",
    true_literal="true",
    false_literal="false",
    sequence_open="(",
    sequence_close=")",
    dict_open="new Dictionary<string, object> {",
    dict_close="}",
    format_dict_entry=_format_csharp_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence="ValueTuple.Create()",
    empty_dict=None,
    set_open="new HashSet<object> {",
    set_close="}",
    empty_set="new HashSet<object>()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="new Dictionary<string, object> {",
    omap_close="}",
    format_omap_entry=_format_csharp_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_csharp,
    format_variable_assignment=format_variable_assignment_csharp,
)


def _format_dart_omap_entry(key: str, value: str) -> str:
    """Format a Dart map entry."""
    return f"{key}: {value}"


DART = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set="<dynamic>{}",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_dart_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_dart,
    format_variable_assignment=format_variable_assignment_dart,
)


def _format_js_omap_entry(key: str, value: str) -> str:
    """Format a JavaScript/TypeScript ordered-map entry."""
    return f"{key}: {value}"


JAVASCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="new Set([",
    set_close="])",
    empty_set="new Set()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_js_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_js,
    format_variable_assignment=format_variable_assignment_js,
)

TYPESCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="new Set([",
    set_close="])",
    empty_set="new Set()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_js_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_js,
    format_variable_assignment=format_variable_assignment_js,
)


def _format_ruby_omap_entry(key: str, value: str) -> str:
    """Format a Ruby ordered-map entry."""
    return f"{key} => {value}"


RUBY = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="Set.new([",
    set_close="])",
    empty_set="Set.new",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_ruby_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_ruby,
    format_variable_assignment=format_variable_assignment_ruby,
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
    sequence_open="[]any{",
    sequence_close="}",
    dict_open="map[string]any{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="map[any]struct{}{",
    set_close="}",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=_format_go_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[][2]any{",
    omap_close="}",
    format_omap_entry=_format_go_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_go,
    format_variable_assignment=format_variable_assignment_go,
)


@beartype
def _format_cpp_dict_entry(key: str, value: str) -> str:
    """Format a C++ dict entry as a brace-enclosed pair."""
    return f"{{{key}, {value}}}"


CPP = LanguageSpec(
    null_literal="nullptr",
    true_literal="true",
    false_literal="false",
    sequence_open="{",
    sequence_close="}",
    dict_open="{",
    dict_close="}",
    format_dict_entry=_format_cpp_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_cpp_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_cpp,
    format_variable_assignment=format_variable_assignment_cpp,
)


@beartype
def _format_c_dict_entry(key: str, value: str) -> str:
    """Format a C dict entry as a ``_CKV`` compound literal."""
    return f"{{{key}, {to_c_val(value=value)}}}"


@beartype
def _format_c_list_entry(item: str) -> str:
    """Format a C list entry as a ``_CVal`` compound literal."""
    return to_c_val(value=item)


@beartype
def _format_c_set_entry(item: str) -> str:
    """Format a C set entry as a ``_CVal`` compound literal."""
    return to_c_val(value=item)


C = LanguageSpec(
    null_literal="((_CVal){.s = NULL})",
    true_literal="((_CVal){.b = true})",
    false_literal="((_CVal){.b = false})",
    sequence_open="((_CVal){.a = (_CVal[]){",
    sequence_close="}})",
    dict_open="((_CVal){.m = (_CKV[]){",
    dict_close="}})",
    format_dict_entry=_format_c_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="((_CVal){.a = (_CVal[]){",
    set_close="}})",
    empty_set=None,
    format_sequence_entry=_format_c_list_entry,
    format_set_entry=_format_c_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="((_CVal){.m = (_CKV[]){",
    omap_close="}})",
    format_omap_entry=_format_c_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_c,
    format_variable_assignment=format_variable_assignment_c,
)


@beartype
def _format_java_dict_entry(key: str, value: str) -> str:
    """Format a Java ``Map.entry(key, value)`` call."""
    return f"Map.entry({key}, {value})"


JAVA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="new Object[]{",
    sequence_close="}",
    dict_open="Map.ofEntries(",
    dict_close=")",
    format_dict_entry=_format_java_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="Set.of(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="new java.util.ArrayList<>(java.util.Arrays.asList(",
    omap_close="))",
    format_omap_entry=_format_java_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    format_variable_declaration=format_variable_declaration_java,
    format_variable_assignment=format_variable_assignment_java,
    skip_null_dict_values=True,
)


def _format_swift_omap_entry(key: str, value: str) -> str:
    """Format a Swift dictionary entry."""
    return f"{key}: {value}"


SWIFT = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence="[Any]()",
    empty_dict="[String: Any]()",
    set_open="Set<AnyHashable>([",
    set_close="])",
    empty_set="Set<AnyHashable>()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_swift_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_swift,
    format_variable_assignment=format_variable_assignment_swift,
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
    sequence_open="vec![",
    sequence_close="]",
    dict_open="HashMap::from([",
    dict_close="])",
    format_dict_entry=_format_rust_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="HashSet::from([",
    set_close="])",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="HashMap::from([",
    omap_close="])",
    format_omap_entry=_format_rust_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_rust,
    format_variable_assignment=format_variable_assignment_rust,
)


def _format_kotlin_omap_entry(key: str, value: str) -> str:
    """Format a Kotlin ordered-map entry."""
    return f"{key} to {value}"


KOTLIN = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="listOf<Any?>(",
    sequence_close=")",
    dict_open="mapOf<String, Any?>(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" to "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="setOf<Any?>(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="linkedMapOf<String, Any?>(",
    omap_close=")",
    format_omap_entry=_format_kotlin_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_kotlin,
    format_variable_assignment=format_variable_assignment_kotlin,
)


def _format_php_omap_entry(key: str, value: str) -> str:
    """Format one PHP array entry as a ``key => value`` pair."""
    return f"{key} => {value}"


PHP = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_php,
    format_datetime=format_datetime_php,
    empty_sequence=None,
    empty_dict=None,
    set_open="[",
    set_close="]",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_php_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_php,
    format_variable_assignment=format_variable_assignment_php,
)


PERL = LanguageSpec(
    null_literal="undef",
    true_literal="1",
    false_literal="0",
    sequence_open="[",
    sequence_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="[",
    set_close="]",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=dict_entry_with_separator(separator=" => "),
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_perl,
    format_variable_assignment=format_variable_assignment_perl,
)


def _format_julia_omap_entry(key: str, value: str) -> str:
    """Format a Julia ordered-map entry as a pair arrow expression."""
    return f"{key} => {value}"


JULIA = LanguageSpec(
    null_literal="nothing",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="Dict(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict="Dict()",
    set_open="Set([",
    set_close="])",
    empty_set="Set()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_julia_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_julia,
    format_variable_assignment=format_variable_declaration_julia,
)


@beartype
def _format_elixir_omap_entry(key: str, value: str) -> str:
    """Format an Elixir ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


ELIXIR = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="%{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="MapSet.new([",
    set_close="])",
    empty_set="MapSet.new()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_elixir_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_elixir,
    format_variable_assignment=format_variable_assignment_elixir,
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
    sequence_open="HList [",
    sequence_close="]",
    dict_open="HMap [",
    dict_close="]",
    format_dict_entry=_format_haskell_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="HSet [",
    set_close="]",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="--",
    comment_suffix="",
    omap_open="HMap [",
    omap_close="]",
    format_omap_entry=_format_haskell_omap_entry,
    multiline_close_indent="    ",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_haskell,
    format_variable_assignment=format_variable_assignment_haskell,
)


def _format_fsharp_dict_entry(key: str, value: str) -> str:
    """Format an F# dict entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {to_fsharp_val(value=value)})"


def _format_fsharp_omap_entry(key: str, value: str) -> str:
    """Format an F# ordered-map entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {to_fsharp_val(value=value)})"


def _format_fsharp_set_entry(item: str) -> str:
    """Format an F# set entry with the appropriate ``Val`` constructor."""
    return to_fsharp_val(value=item)


def _format_fsharp_sequence_entry(item: str) -> str:
    """Format an F# sequence entry with the appropriate ``Val``
    constructor.
    """
    return to_fsharp_val(value=item)


FSHARP = LanguageSpec(
    null_literal="FNull",
    true_literal="FBool true",
    false_literal="FBool false",
    sequence_open="FList [",
    sequence_close="]",
    dict_open="FMap [",
    dict_close="]",
    format_dict_entry=_format_fsharp_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="FSet [",
    set_close="]",
    empty_set=None,
    format_set_entry=_format_fsharp_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="FMap [",
    omap_close="]",
    format_omap_entry=_format_fsharp_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_fsharp,
    format_variable_assignment=format_variable_assignment_fsharp,
    element_separator="; ",
    format_sequence_entry=_format_fsharp_sequence_entry,
)


CLOJURE = LanguageSpec(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" "),
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="#{",
    set_close="}",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix=";",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=dict_entry_with_separator(separator=" "),
    multiline_close_indent="",
    element_separator=" ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_clojure,
    format_variable_assignment=format_variable_assignment_clojure,
)


def _format_scala_omap_entry(key: str, value: str) -> str:
    """Format a Scala ``ListMap`` entry as a ``key -> value`` pair."""
    return f"{key} -> {value}"


SCALA = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="List(",
    sequence_close=")",
    dict_open="Map(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" -> "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="Set(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="scala.collection.immutable.ListMap(",
    omap_close=")",
    format_omap_entry=_format_scala_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_scala,
    format_variable_assignment=format_variable_assignment_scala,
)


def _format_ocaml_dict_entry(key: str, value: str) -> str:
    """Format an OCaml dict entry as a ``(key, OXxx value)`` tuple."""
    return f"({key}, {to_ocaml_val(value=value)})"


def _format_ocaml_omap_entry(key: str, value: str) -> str:
    """Format an OCaml ordered-map entry as a ``(key, OXxx value)``
    tuple.
    """
    return f"({key}, {to_ocaml_val(value=value)})"


def _format_ocaml_set_entry(item: str) -> str:
    """Format an OCaml set entry with the appropriate ``val_t``
    constructor.
    """
    return to_ocaml_val(value=item)


def _format_ocaml_sequence_entry(item: str) -> str:
    """Format an OCaml list entry with the appropriate ``val_t``
    constructor.
    """
    return to_ocaml_val(value=item)


OCAML = LanguageSpec(
    null_literal="ONull",
    true_literal="OBool true",
    false_literal="OBool false",
    sequence_open="OList [",
    sequence_close="]",
    dict_open="OMap [",
    dict_close="]",
    format_dict_entry=_format_ocaml_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="OSet [",
    set_close="]",
    empty_set=None,
    format_set_entry=_format_ocaml_set_entry,
    comment_prefix="(*",
    comment_suffix="",
    omap_open="OMap [",
    omap_close="]",
    format_omap_entry=_format_ocaml_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_ocaml,
    format_variable_assignment=format_variable_assignment_ocaml,
    element_separator="; ",
    format_sequence_entry=_format_ocaml_sequence_entry,
)


GROOVY = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict="[:]",
    set_open="[",
    set_close="] as Set<Object>",
    empty_set="[] as Set<Object>",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=dict_entry_with_separator(separator=": "),
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_groovy,
    format_variable_assignment=format_variable_assignment_groovy,
)


def _format_r_omap_entry(key: str, value: str) -> str:
    """Format an R named list entry for an ordered map."""
    return f"{key} = {value}"


R = LanguageSpec(
    null_literal="NULL",
    true_literal="TRUE",
    false_literal="FALSE",
    sequence_open="list(",
    sequence_close=")",
    dict_open="list(",
    dict_close=")",
    format_dict_entry=dict_entry_with_separator(separator=" = "),
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="list(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="list(",
    omap_close=")",
    format_omap_entry=_format_r_omap_entry,
    multiline_trailing_comma=False,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_r,
    format_variable_assignment=format_variable_assignment_r,
)


@beartype
def _format_erlang_omap_entry(key: str, value: str) -> str:
    """Format an Erlang ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


ERLANG = LanguageSpec(
    null_literal="undefined",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="#{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_erlang,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="sets:from_list([",
    set_close="])",
    empty_set="sets:from_list([])",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="%",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_erlang_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_erlang,
    format_variable_assignment=format_variable_assignment_erlang,
)
