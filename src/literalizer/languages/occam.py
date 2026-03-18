"""Occam-pi language specification."""

from __future__ import annotations

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_occam,
    format_variable_declaration_occam,
    to_occam_val,
)
from literalizer._language import Language


def _format_occam_dict_entry(key: str, value: str) -> str:
    """Format an occam-pi dict or omap entry as a ``MOBILE LIT(lit.pair;
    ...)`` constructor.
    """
    val = to_occam_val(value=value)
    return f"MOBILE LIT(lit.pair; MOBILE []BYTE {key}; {val})"


def _format_occam_list_entry(item: str) -> str:
    """Format an occam-pi list entry with the appropriate ``LIT``
    constructor.
    """
    return to_occam_val(value=item)


def _format_occam_set_entry(item: str) -> str:
    """Format an occam-pi set entry with the appropriate ``LIT``
    constructor.
    """
    return to_occam_val(value=item)


OCCAM = Language(
    null_literal="MOBILE LIT(lit.null)",
    true_literal="MOBILE LIT(lit.bool; TRUE)",
    false_literal="MOBILE LIT(lit.bool; FALSE)",
    sequence_open="MOBILE LIT(lit.list; MOBILE []MOBILE LIT [",
    sequence_close="])",
    dict_open="MOBILE LIT(lit.map; MOBILE []MOBILE LIT [",
    dict_close="])",
    format_dict_entry=_format_occam_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="MOBILE LIT(lit.set; MOBILE []MOBILE LIT [",
    set_close="])",
    empty_set=None,
    format_sequence_entry=_format_occam_list_entry,
    format_set_entry=_format_occam_set_entry,
    comment_prefix="--",
    comment_suffix="",
    omap_open="MOBILE LIT(lit.map; MOBILE []MOBILE LIT [",
    omap_close="])",
    format_omap_entry=_format_occam_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_occam,
    format_variable_assignment=format_variable_assignment_occam,
)
