"""D language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
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


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a D ``auto`` variable declaration using ``JSONValue``."""
    return f"auto {name} = {_to_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a D assignment to an existing variable."""
    return f"{name} = {_to_val(value=value)};"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class D:
    """D language specification."""

    def __init__(self) -> None:
        """Initialize D language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="JSONValue(["
        )
        self.sequence_close = "])"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="JSONValue(["
        )
        self.dict_close = "])"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_d_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = 'parseJSON("[]")'
        self.empty_dict: str | None = 'parseJSON("{}")'
        self.set_open = "JSONValue(["
        self.set_close = "])"
        self.empty_set: str | None = 'parseJSON("[]")'
        self.format_sequence_entry: Callable[[str], str] = (
            _format_d_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_d_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "JSONValue(["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_d_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
