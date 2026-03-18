"""Groovy language specification."""

from __future__ import annotations

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Groovy variable declaration."""
    return f"def {name} = {value}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Groovy variable assignment."""
    return f"{name} = {value}"


GROOVY = Language(
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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
