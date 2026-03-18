"""Ada language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
)
from literalizer._language import Language


def _to_ada_val(value: str) -> str:
    """Wrap a pre-formatted value string in an Ada ``A_Val`` constructor.

    Inspects the string representation to determine the appropriate
    constructor: ``AStr``, ``AInt``, ``AFloat``, or passes through
    values that are already ``A_Val`` expressions
    (``ANull``, ``ABool``, ``AList``, ``AMap``, ``ASet``, ``AEntry``).
    """
    _val_prefixes = (
        "ANull",
        "ABool",
        "AInt",
        "AFloat",
        "AStr",
        "AList",
        "AMap",
        "ASet",
        "AEntry",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        ada_escaped = value.replace('\\"', '""').replace("\\\\", "\\")
        return f"AStr ({ada_escaped})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"AInt ({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"AFloat ({value})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_ada_dict_entry(key: str, value: str) -> str:
    """Format an Ada dict/map entry as an ``AEntry (key, AVal value)``
    call.
    """
    return f"AEntry ({key}, {_to_ada_val(value=value)})"


def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Ada object declaration.

    Example: ``"x"`` and ``"AList'(AInt (1))"`` →
    ``"x : A_Val := AList'(AInt (1));"``
    """
    return f"{name} : A_Val := {_to_ada_val(value=value)};"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Ada assignment statement to an existing variable.

    Example: ``"x"`` and ``"AList'(AInt (1))"`` →
    ``"x := AList'(AInt (1));"``
    """
    return f"{name} := {_to_ada_val(value=value)};"


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
    format_string=format_string_backslash,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence="AList'(1 .. 0 => ANull)",
    empty_dict="AMap'(1 .. 0 => ANull)",
    set_open="ASet'(",
    set_close=")",
    empty_set="ASet'(1 .. 0 => ANull)",
    format_sequence_entry=_to_ada_val,
    format_set_entry=_to_ada_val,
    comment_prefix="--",
    comment_suffix="",
    omap_open="AMap'(",
    omap_close=")",
    format_omap_entry=_format_ada_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
