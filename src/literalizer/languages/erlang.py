"""Erlang language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


@beartype
def _format_erlang_omap_entry(key: str, value: str) -> str:
    """Format an Erlang ordered-map entry as a ``{key, value}`` tuple."""
    return f"{{{key}, {value}}}"


@beartype
def _format_bytes(value: bytes) -> str:
    """Format bytes as an Erlang binary literal."""
    parts = ", ".join(f"{b}" for b in value)
    return f"<<{parts}>>"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an Erlang variable declaration."""
    erlang_name = name[0].upper() + name[1:]
    return f"{erlang_name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an Erlang variable assignment."""
    erlang_name = name[0].upper() + name[1:]
    return f"{erlang_name} = {value}"


ERLANG = Language(
    null_literal="undefined",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="#{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" => "),
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=_format_bytes,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="sets:from_list([",
    set_close="])",
    empty_set="sets:from_list([])",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="%",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_erlang_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
    format_string=format_string_backslash,
)
