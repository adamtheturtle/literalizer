"""Ada language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._language import Language
from literalizer.formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_ada,
    format_variable_declaration_ada,
    to_ada_val,
)


@beartype
def _format_ada_dict_entry(key: str, value: str) -> str:
    """Format an Ada dict/map entry as an ``AEntry (key, AVal value)``
    call.
    """
    return f"AEntry ({key}, {to_ada_val(value=value)})"


ADA = Language(
    null_literal="ANull",
    true_literal="ABool (True)",
    false_literal="ABool (False)",
    sequence_open="AList'(",
    sequence_close=")",
    dict_open="AMap'(",
    dict_close=")",
    format_dict_entry=_format_ada_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence="AList'(1 .. 0 => ANull)",
    empty_dict="AMap'(1 .. 0 => ANull)",
    set_open="ASet'(",
    set_close=")",
    empty_set="ASet'(1 .. 0 => ANull)",
    format_sequence_entry=to_ada_val,
    format_set_entry=to_ada_val,
    comment_prefix="--",
    comment_suffix="",
    omap_open="AMap'(",
    omap_close=")",
    format_omap_entry=_format_ada_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_ada,
    format_variable_assignment=format_variable_assignment_ada,
)
