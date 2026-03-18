"""Lua language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._language import Language
from literalizer.formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_lua,
    format_variable_declaration_lua,
    passthrough_sequence_entry,
)


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


LUA = Language(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="{",
    sequence_close="}",
    dict_open="{",
    dict_close="}",
    format_dict_entry=_format_lua_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="{",
    set_close="}",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=_format_lua_set_entry,
    comment_prefix="--",
    comment_suffix="",
    omap_open="{",
    omap_close="}",
    format_omap_entry=_format_lua_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=True,
    format_variable_declaration=format_variable_declaration_lua,
    format_variable_assignment=format_variable_assignment_lua,
)
