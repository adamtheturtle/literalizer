"""Java language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


@beartype
def _format_java_dict_entry(key: str, value: str) -> str:
    """Format a Java ``Map.entry(key, value)`` call."""
    return f"Map.entry({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Java variable declaration."""
    return f"var {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Java variable assignment."""
    return f"{name} = {value};"


JAVA = Language(
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
    format_string=format_string_backslash,
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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
    skip_null_dict_values=True,
)
