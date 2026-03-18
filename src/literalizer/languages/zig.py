"""Zig language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_zig,
    format_variable_declaration_zig,
    to_zig_val,
)
from literalizer._language import Language


@beartype
def _format_zig_dict_entry(key: str, value: str) -> str:
    """Format a Zig dict entry as a ``ZKV`` anonymous struct literal."""
    return f".{{ .key = {key}, .val = {to_zig_val(value=value)} }}"


@beartype
def _format_zig_sequence_entry(item: str) -> str:
    """Format a Zig sequence entry as a ``ZVal`` union literal."""
    return to_zig_val(value=item)


@beartype
def _format_zig_set_entry(item: str) -> str:
    """Format a Zig set entry as a ``ZVal`` union literal."""
    return to_zig_val(value=item)


ZIG = Language(
    null_literal=".nil",
    true_literal=".{ .bool = true }",
    false_literal=".{ .bool = false }",
    sequence_open=".{ .arr = &.{",
    sequence_close="}}",
    dict_open=".{ .map = &.{",
    dict_close="}}",
    format_dict_entry=_format_zig_dict_entry,
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open=".{ .set = &.{",
    set_close="}}",
    empty_set=None,
    format_sequence_entry=_format_zig_sequence_entry,
    format_set_entry=_format_zig_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open=".{ .map = &.{",
    omap_close="}}",
    format_omap_entry=_format_zig_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_zig,
    format_variable_assignment=format_variable_assignment_zig,
)
