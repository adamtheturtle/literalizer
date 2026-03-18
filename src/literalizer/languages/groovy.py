"""Groovy language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._language import Language


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Groovy variable declaration."""
    return f"def {name} = {value}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Groovy variable assignment."""
    return f"{name} = {value}"


_BYTES_FORMAT: Callable[[bytes], str] = format_bytes_hex
_DATE_FORMAT: Callable[[datetime.date], str] = format_date_iso
_DATETIME_FORMAT: Callable[[datetime.datetime], str] = format_datetime_iso


class Groovy:
    """Groovy language specification."""

    def __init__(self) -> None:
        """Initialize Groovy language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "["
        self.sequence_close = "]"
        self.dict_open = "["
        self.dict_close = "]"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _BYTES_FORMAT
        self.format_date: Callable[[datetime.date], str] = _DATE_FORMAT
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _DATETIME_FORMAT
        )
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = "[:]"
        self.set_open = "["
        self.set_close = "] as Set<Object>"
        self.empty_set: str | None = "[] as Set<Object>"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
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


GROOVY: Language = Groovy()
