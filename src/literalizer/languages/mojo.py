"""Mojo language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_mojo_omap_entry(key: str, value: str) -> str:
    """Format one Mojo ordered-map entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Mojo variable declaration in Python-compatible script
    style.
    """
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Mojo variable assignment."""
    return f"{name} = {value}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class Mojo:
    """Mojo language specification.

    Mojo does not support heterogeneous collections — every element in a
    list or set must share a single type.  When a collection contains
    scalar values of mixed types (e.g. ``[1, 2.5, 3]``), **all values
    are coerced to their string representations** so that the resulting
    literal is valid Mojo (e.g. ``["1", "2.5", "3"]``).

    For sets, coercion is skipped when it would reduce the element count.
    This can happen when distinct values of different types coerce to the
    same string (e.g. ``{1, "1"}`` would both become ``"1"``).  In that
    case the original uncoerced values are kept.
    """

    @beartype
    def __init__(self) -> None:
        """Initialize Mojo language specification."""
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="["
        )
        self.sequence_close = "]"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="{"
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_mojo_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.coerce_heterogeneous_to_strings = True
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
