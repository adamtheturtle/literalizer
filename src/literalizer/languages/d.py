"""D language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._language import Language


def _to_val(value: str) -> str:
    """Wrap a pre-formatted value string in a D ``JSONValue(...)`` call.

    Inspects the string representation to determine whether wrapping is
    needed.  Values that are already ``JSONValue(...)`` or ``parseJSON(...)``
    expressions are returned unchanged; ``null``, ``true``, and ``false``
    literals and numeric and string literals are all wrapped.
    """
    if value.startswith(("JSONValue(", 'parseJSON("')):
        return value
    if value in {"null", "true", "false"}:
        return f"JSONValue({value})"
    if value.startswith('"') and value.endswith('"'):
        return f"JSONValue({value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"JSONValue({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"JSONValue({value})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_d_dict_entry(key: str, value: str) -> str:
    """Format a D associative-array entry as ``key: JSONValue(value)``."""
    return f"{key}: {_to_val(value=value)}"


@beartype
def _format_d_sequence_entry(item: str) -> str:
    """Format a D array entry as a ``JSONValue(item)`` call."""
    return _to_val(value=item)


@beartype
def _format_d_set_entry(item: str) -> str:
    """Format a D set entry (represented as array) as
    ``JSONValue(item)``.
    """
    return _to_val(value=item)


@beartype
def _format_d_omap_entry(key: str, value: str) -> str:
    """Format a D ordered-map entry as a two-element ``JSONValue``
    array.
    """
    return f"JSONValue([JSONValue({key}), {_to_val(value=value)}])"


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a D ``auto`` variable declaration using ``JSONValue``."""
    return f"auto {name} = {_to_val(value=value)};"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a D assignment to an existing variable."""
    return f"{name} = {_to_val(value=value)};"


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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
