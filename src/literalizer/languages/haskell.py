"""Haskell language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


@beartype
def _format_haskell_dict_entry(key: str, value: str) -> str:
    """Format a Haskell dict entry as a tuple pair."""
    return f"({key}, {value})"


def _format_haskell_omap_entry(key: str, value: str) -> str:
    """Format a Haskell ordered-map entry as a tuple pair."""
    return f"({key}, {value})"


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Haskell variable declaration."""
    return f"{name} = {value}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Haskell variable assignment."""
    return f"{name} = {value}"


HASKELL = Language(
    null_literal="HNull",
    true_literal="HBool True",
    false_literal="HBool False",
    sequence_open="HList [",
    sequence_close="]",
    dict_open="HMap [",
    dict_close="]",
    format_dict_entry=_format_haskell_dict_entry,
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="HSet [",
    set_close="]",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="--",
    comment_suffix="",
    omap_open="HMap [",
    omap_close="]",
    format_omap_entry=_format_haskell_omap_entry,
    multiline_close_indent="    ",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
)
