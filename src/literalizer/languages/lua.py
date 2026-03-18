"""Lua language specification."""

from __future__ import annotations

from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
)

if TYPE_CHECKING:
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


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Lua variable declaration."""
    return f"local {name} = {value}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Lua variable assignment."""
    return f"{name} = {value}"


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
        self.format_dict_entry = _format_lua_dict_entry
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes = format_bytes_hex
        self.format_date = format_date_iso
        self.format_datetime = format_datetime_iso
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry = passthrough_sequence_entry
        self.format_set_entry = _format_lua_set_entry
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry = _format_lua_dict_entry
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = True
        self.format_variable_declaration = _format_variable_declaration
        self.format_variable_assignment = _format_variable_assignment


LUA: Language = Lua()
