"""Built-in language specifications for 13 programming languages."""

from __future__ import annotations

from beartype import beartype

__all__ = [
    "CPP",
    "CSHARP",
    "GO",
    "HASKELL",
    "JAVA",
    "JAVASCRIPT",
    "KOTLIN",
    "PHP",
    "PYTHON",
    "RUBY",
    "RUST",
    "SWIFT",
    "TYPESCRIPT",
]

from literalizer._language import LanguageSpec
from literalizer.formatters import (
    format_bytes_hex,
    format_date_iso,
    format_date_php,
    format_datetime_iso,
    format_datetime_php,
    format_variable_declaration_cpp,
    format_variable_declaration_csharp,
    format_variable_declaration_go,
    format_variable_declaration_java,
    format_variable_declaration_js,
    format_variable_declaration_kotlin,
    format_variable_declaration_python,
    format_variable_declaration_ruby,
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
    dict_separator=": ",
    dict_open="{",
    dict_close="}",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="#",
    omap_open="OrderedDict([",
    omap_close="])",
    format_omap_entry=_format_python_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_python,
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
    dict_separator=": ",
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="new Dictionary<string, object> {",
    omap_close="}",
    format_omap_entry=_format_csharp_dict_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_csharp,
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
    dict_separator=": ",
    dict_open="{",
    dict_close="}",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_js_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_js,
)

TYPESCRIPT = LanguageSpec(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    collection_open="[",
    collection_close="]",
    dict_separator=": ",
    dict_open="{",
    dict_close="}",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_js_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_js,
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
    dict_separator=" => ",
    dict_open="{",
    dict_close="}",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="#",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_ruby_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_ruby,
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
    dict_separator=": ",
    dict_open="map[string]any{",
    dict_close="}",
    format_dict_entry=None,
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
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_go,
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
    dict_separator=": ",
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_cpp_dict_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_cpp,
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
    dict_separator=": ",
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="new java.util.ArrayList<>(java.util.Arrays.asList(",
    omap_close="))",
    format_omap_entry=_format_java_dict_entry,
    multiline_close_indent="",
    format_variable_declaration=format_variable_declaration_java,
    skip_null_dict_values=True,
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
    dict_separator=": ",
    dict_open="[",
    dict_close="]",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_swift_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=None,
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
    dict_separator=": ",
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="HashMap::from([",
    omap_close="])",
    format_omap_entry=_format_rust_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=None,
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
    dict_separator=" to ",
    dict_open="mapOf<String, Any?>(",
    dict_close=")",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="linkedMapOf<String, Any?>(",
    omap_close=")",
    format_omap_entry=_format_kotlin_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_kotlin,
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
    dict_separator=" => ",
    dict_open="[",
    dict_close="]",
    format_dict_entry=None,
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
    format_set_entry=None,
    comment_prefix="//",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_php_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=None,
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
    dict_separator=", ",
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
    format_set_entry=None,
    comment_prefix="--",
    omap_open="HMap [",
    omap_close="]",
    format_omap_entry=_format_haskell_omap_entry,
    multiline_close_indent="    ",
    skip_null_dict_values=False,
    format_variable_declaration=None,
)
