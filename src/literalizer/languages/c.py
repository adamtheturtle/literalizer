"""C language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._language import Language


def _to_val(value: str) -> str:
    """Convert a value to a C union cast expression."""
    if value.startswith("((_CVal)"):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"((_CVal){{.s = {value}}})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"((_CVal){{.i = {value}}})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"((_CVal){{.f = {value}}})"
    except ValueError:
        pass
    if float_result is not None:
        return float_result
    return value


@beartype
def _format_c_dict_entry(key: str, value: str) -> str:
    """Format a C dict entry as a ``_CKV`` compound literal."""
    return f"{{{key}, {_to_val(value=value)}}}"


@beartype
def _format_c_list_entry(item: str) -> str:
    """Format a C list entry as a ``_CVal`` compound literal."""
    return _to_val(value=item)


@beartype
def _format_c_set_entry(item: str) -> str:
    """Format a C set entry as a ``_CVal`` compound literal."""
    return _to_val(value=item)


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a C variable declaration."""
    return f"_CVal {name} = {_to_val(value=value)};"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a C variable assignment."""
    return f"{name} = {_to_val(value=value)};"


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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
