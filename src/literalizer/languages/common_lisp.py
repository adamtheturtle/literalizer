"""Common Lisp language specification."""

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
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_cons_entry(key: str, value: str) -> str:
    """Format a Common Lisp association-list entry as a ``cons`` pair."""
    return f"(cons {key} {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Common Lisp special-variable declaration with earmuffs."""
    return f"(defparameter *{name}* {value})"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Common Lisp special-variable assignment with earmuffs."""
    return f"(setf *{name}* {value})"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class CommonLisp:
    """Common Lisp language specification."""

    @beartype
    def __init__(self) -> None:
        """Initialize Common Lisp language specification."""
        self.null_literal = "nil"
        self.true_literal = "t"
        self.false_literal = "nil"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="(list "
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="(list "
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = _format_cons_entry
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "nil"
        self.empty_dict: str | None = "nil"
        self.set_open = "(list "
        self.set_close = ")"
        self.empty_set: str | None = "nil"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = ";"
        self.comment_suffix = ""
        self.omap_open = "(list "
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = _format_cons_entry
        self.multiline_close_indent = ""
        self.element_separator = " "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
