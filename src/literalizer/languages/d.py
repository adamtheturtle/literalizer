"""D language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_d,
    format_variable_declaration_d,
    to_d_val,
)
from literalizer._language import Language


@beartype
def _format_d_dict_entry(key: str, value: str) -> str:
    """Format a D associative-array entry as ``key: JSONValue(value)``."""
    return f"{key}: {to_d_val(value=value)}"


@beartype
def _format_d_sequence_entry(item: str) -> str:
    """Format a D array entry as a ``JSONValue(item)`` call."""
    return to_d_val(value=item)


@beartype
def _format_d_set_entry(item: str) -> str:
    """Format a D set entry (represented as array) as
    ``JSONValue(item)``.
    """
    return to_d_val(value=item)


@beartype
def _format_d_omap_entry(key: str, value: str) -> str:
    """Format a D ordered-map entry as a two-element ``JSONValue``
    array.
    """
    return f"JSONValue([JSONValue({key}), {to_d_val(value=value)}])"


D = Language(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="JSONValue([",
    sequence_close="])",
    dict_open="JSONValue([",
    dict_close="])",
    format_dict_entry=_format_d_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence='parseJSON("[]")',
    empty_dict='parseJSON("{}")',
    set_open="JSONValue([",
    set_close="])",
    empty_set='parseJSON("[]")',
    format_sequence_entry=_format_d_sequence_entry,
    format_set_entry=_format_d_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="JSONValue([",
    omap_close="])",
    format_omap_entry=_format_d_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_d,
    format_variable_assignment=format_variable_assignment_d,
)
