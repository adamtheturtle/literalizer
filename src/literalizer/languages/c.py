"""C language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_c,
    format_variable_declaration_c,
    to_c_val,
)
from literalizer._language import Language


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


C = Language(
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
