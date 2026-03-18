"""PHP language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_sequence_open,
    format_bytes_hex,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)


@beartype
def _format_php_omap_entry(key: str, value: str) -> str:
    """Format one PHP array entry as a ``key => value`` pair."""
    return f"{key} => {value}"


@beartype
def _format_date(value: datetime.date) -> str:
    """Format a date as a PHP DateTime object."""
    return f'new DateTime("{value.isoformat()}")'


@beartype
def _format_datetime(value: datetime.datetime) -> str:
    """Format a datetime as a PHP DateTime object."""
    return f'new DateTime("{value.isoformat()}")'


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a PHP variable declaration."""
    return f"${name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a PHP variable assignment."""
    return f"${name} = {value};"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = _format_date
_datetime_format: Callable[[datetime.datetime], str] = _format_datetime
_string_format: Callable[[str], str] = format_string_backslash


if TYPE_CHECKING:
    from literalizer._types import Value


class Php:
    """PHP language specification."""

    @beartype
    def __init__(self) -> None:
        """Initialize Php language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="["
        )
        self.sequence_close = "]"
        self.dict_open = "["
        self.dict_close = "]"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" => ")
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
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_php_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
