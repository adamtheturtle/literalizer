"""Kotlin language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


@beartype
def _format_kotlin_omap_entry(key: str, value: str) -> str:
    """Format a Kotlin ordered-map entry."""
    return f"{key} to {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Kotlin variable declaration."""
    return f"val {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Kotlin variable assignment."""
    return f"{name} = {value}"


KOTLIN = Language(
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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
    format_string=format_string_backslash,
)
