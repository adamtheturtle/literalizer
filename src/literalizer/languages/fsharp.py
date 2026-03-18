"""F# language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._language import Language


@beartype
def _to_val(value: str) -> str:
    """Convert a value to an F# union type expression."""
    _val_prefixes = (
        "FNull",
        "FBool",
        "FList",
        "FMap",
        "FSet",
        "FStr",
        "FInt",
        "FFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"FStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"FInt({value}L)" if negative else f"FInt {value}L"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"FFloat({value})" if negative else f"FFloat {value}"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_fsharp_dict_entry(key: str, value: str) -> str:
    """Format an F# dict entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_fsharp_omap_entry(key: str, value: str) -> str:
    """Format an F# ordered-map entry as a ``(key, FVal value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_fsharp_set_entry(item: str) -> str:
    """Format an F# set entry with the appropriate ``Val`` constructor."""
    return _to_val(value=item)


@beartype
def _format_fsharp_sequence_entry(item: str) -> str:
    """Format an F# sequence entry with the appropriate ``Val``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an F# variable declaration."""
    return f"let {name}: Val = {_to_val(value=value)}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an F# variable assignment."""
    return f"let {name}: Val = {_to_val(value=value)}"


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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
    element_separator="; ",
    format_sequence_entry=_format_fsharp_sequence_entry,
)
