"""PHP language specification."""

from __future__ import annotations

import datetime  # noqa: TC003

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


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


PHP = Language(
    null_literal="null",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=_format_date,
    format_datetime=_format_datetime,
    empty_sequence=None,
    empty_dict=None,
    set_open="[",
    set_close="]",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_php_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
    format_string=format_string_backslash,
)
