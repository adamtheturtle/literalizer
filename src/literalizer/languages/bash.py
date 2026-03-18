"""Bash language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@beartype
def _to_bash_value(item: str) -> str:
    """Quote an item if it is a nested array or dict expression.

    Bash does not support nested array literals, so any value that is
    itself an array or associative-array expression (starting with
    ``(``) is double-quoted with special characters escaped.
    """
    if item.startswith("("):
        escaped = (
            item.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("$", "\\$")
            .replace("`", "\\`")
        )
        return f'"{escaped}"'
    return item


@beartype
def _format_bash_sequence_entry(item: str) -> str:
    """Format a Bash indexed-array element, quoting nested collections."""
    return _to_bash_value(item=item)


@beartype
def _format_bash_dict_entry(key: str, value: str) -> str:
    """Format a Bash associative-array entry as ``[key]=value``."""
    return f"[{key}]={_to_bash_value(item=value)}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Bash ``declare`` variable declaration."""
    flag = (
        " -A"
        if any(line.lstrip().startswith("[") for line in value.splitlines())
        else ""
    )
    return f"declare{flag} {name}={value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Bash variable assignment."""
    return f"{name}={value}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class Bash:
    """Bash language specification."""

    @beartype
    def __init__(self) -> None:
        """Initialize Bash language specification."""
        self.null_literal = '""'
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = fixed_sequence_open(delimiter="(")
        self.sequence_close = ")"
        self.dict_open = "("
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_bash_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            _format_bash_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_bash_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = " "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
