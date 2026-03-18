"""MATLAB language specification."""

from __future__ import annotations

import json

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
def _format_matlab_dict_entry(key: str, value: str) -> str:
    """Format a MATLAB ``struct`` field as a ``'key', value`` pair.

    MATLAB ``struct`` accepts alternating character-vector keys and values.
    Dictionary keys arrive as double-quoted strings; they are converted to
    single-quoted character vectors as required by ``struct``.  Internal
    single quotes are doubled to produce valid MATLAB char-vector literals.

    Cell-array values are wrapped in an extra layer of braces so that
    ``struct`` stores them as a single cell-array field rather than
    expanding them into a struct array.
    """
    inner = json.loads(s=key).replace("'", "''")
    key = f"'{inner}'"
    if value.startswith("{") and value.endswith("}"):
        value = f"{{{value}}}"
    return f"{key}, {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a MATLAB variable declaration."""
    return f"{name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a MATLAB variable assignment."""
    return f"{name} = {value};"


MATLAB = Language(
    null_literal="[]",
    true_literal="true",
    false_literal="false",
    sequence_open="{",
    sequence_close="}",
    dict_open="struct(",
    dict_close=")",
    format_dict_entry=_format_matlab_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence="{}",
    empty_dict="struct()",
    set_open="{",
    set_close="}",
    empty_set="{}",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="%",
    comment_suffix="",
    omap_open="struct(",
    omap_close=")",
    format_omap_entry=_format_matlab_dict_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_string=format_string_backslash,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
