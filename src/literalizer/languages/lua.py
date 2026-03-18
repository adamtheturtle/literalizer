"""Lua language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._language import Language


@beartype
def _format_lua_dict_entry(key: str, value: str) -> str:
    """Format a Lua table entry with a string key.

    Example: ``'"name"'`` and ``'"Alice"'`` → ``'["name"] = "Alice"'``.
    """
    return f"[{key}] = {value}"


@beartype
def _format_lua_set_entry(item: str) -> str:
    """Format a Lua set entry as a table key with a ``true`` value.

    Example: ``'"apple"'`` → ``'["apple"] = true'``.
    """
    return f"[{item}] = true"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Lua variable declaration."""
    return f"local {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Lua variable assignment."""
    return f"{name} = {value}"


_BYTES_FORMAT: Callable[[bytes], str] = format_bytes_hex
_DATE_FORMAT: Callable[[datetime.date], str] = format_date_iso
_DATETIME_FORMAT: Callable[[datetime.datetime], str] = format_datetime_iso
_STRING_FORMAT: Callable[[str], str] = format_string_backslash


class Lua:
    """Lua language specification."""

    def __init__(self) -> None:
        """Initialize Lua language specification."""
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "{"
        self.sequence_close = "}"
        self.dict_open = "{"
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_lua_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _BYTES_FORMAT
        self.format_date: Callable[[datetime.date], str] = _DATE_FORMAT
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _DATETIME_FORMAT
        )
        self.format_string: Callable[[str], str] = _STRING_FORMAT
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_lua_set_entry
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_lua_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )


LUA: Language = Lua()
