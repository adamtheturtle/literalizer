"""Bash language specification."""

from __future__ import annotations

import re

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_set_entry,
)
from literalizer._language import Language


def _to_bash_value(item: str) -> str:
    """Quote an item if it is a nested array or dict expression.

    Bash does not support nested array literals, so any value that is
    itself an array or associative-array expression (starting with
    ``(``) is collapsed to a single line and double-quoted.
    """
    if item.startswith("("):
        collapsed = re.sub(pattern=r"[ \t]*\n[ \t]*", repl=" ", string=item)
        escaped = collapsed.replace("\\", "\\\\").replace('"', '\\"')
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
    return f"declare {name}={value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Bash variable assignment."""
    return f"{name}={value}"


@beartype
def _format_bash_set_entry(item: str) -> str:
    """Format a Bash indexed-array set element."""
    return passthrough_set_entry(item=item)


BASH = Language(
    null_literal='""',
    true_literal="true",
    false_literal="false",
    sequence_open="(",
    sequence_close=")",
    dict_open="(",
    dict_close=")",
    format_dict_entry=_format_bash_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_string=format_string_backslash,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=_format_bash_sequence_entry,
    format_set_entry=_format_bash_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="(",
    omap_close=")",
    format_omap_entry=_format_bash_dict_entry,
    multiline_close_indent="",
    element_separator=" ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
