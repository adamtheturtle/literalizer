"""F# language specification."""

from __future__ import annotations

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_fsharp,
    format_variable_declaration_fsharp,
    to_fsharp_val,
)
from literalizer._language import Language


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


FSHARP = Language(
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
    format_collection_open=None,
)
