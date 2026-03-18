"""R language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


@beartype
def _format_r_dict_entry(key: str, value: str) -> str:
    """Format an R named list entry.

    R list syntax does not allow zero-length names (``"" = value`` is a
    parse error), so empty-string keys are emitted as positional (unnamed)
    elements.
    """
    if key == '""':
        return value
    return f"{key} = {value}"


@beartype
def _format_r_omap_entry(key: str, value: str) -> str:
    """Format an R named list entry for an ordered map."""
    return f"{key} = {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an R variable declaration."""
    return f"{name} <- {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an R variable assignment."""
    return f"{name} <- {value}"


R = Language(
    null_literal="NULL",
    true_literal="TRUE",
    false_literal="FALSE",
    sequence_open="list(",
    sequence_close=")",
    dict_open="list(",
    dict_close=")",
    format_dict_entry=_format_r_dict_entry,
    single_element_trailing_comma=False,
    format_string=format_string_backslash,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="list(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="list(",
    omap_close=")",
    format_omap_entry=_format_r_omap_entry,
    multiline_trailing_comma=False,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
