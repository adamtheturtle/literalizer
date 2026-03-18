"""OCaml language specification."""

from __future__ import annotations

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_ocaml,
    format_variable_declaration_ocaml,
    to_ocaml_val,
)
from literalizer._language import Language


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


OCAML = Language(
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
    comment_suffix=" *)",
    omap_open="OMap [",
    omap_close="]",
    format_omap_entry=_format_ocaml_omap_entry,
    multiline_close_indent="",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_ocaml,
    format_variable_assignment=format_variable_assignment_ocaml,
    element_separator="; ",
    format_sequence_entry=_format_ocaml_sequence_entry,
    format_collection_open=None,
)
