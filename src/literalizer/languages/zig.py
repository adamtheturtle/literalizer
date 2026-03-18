"""Zig language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._language import Language


@beartype
def _to_val(value: str) -> str:
    """Wrap a pre-formatted value string in a Zig ``ZVal`` union literal.

    Inspects the string representation to determine the appropriate union
    tag: ``.int`` for integers, ``.float`` for floats, ``.str`` for
    strings.  Values that are already tagged (starting with ``.``) are
    returned unchanged.
    """
    if value.startswith("."):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f".{{ .str = {value} }}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f".{{ .int = {value} }}"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f".{{ .float = {value} }}"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_zig_dict_entry(key: str, value: str) -> str:
    """Format a Zig dict entry as a ``ZKV`` anonymous struct literal."""
    return f".{{ .key = {key}, .val = {_to_val(value=value)} }}"


@beartype
def _format_zig_sequence_entry(item: str) -> str:
    """Format a Zig sequence entry as a ``ZVal`` union literal."""
    return _to_val(value=item)


@beartype
def _format_zig_set_entry(item: str) -> str:
    """Format a Zig set entry as a ``ZVal`` union literal."""
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Zig ``const`` declaration with explicit ``ZVal`` type."""
    return f"const {name}: ZVal = {_to_val(value=value)};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Zig assignment to an existing ``ZVal`` variable."""
    return f"{name} = {_to_val(value=value)};"


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
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
