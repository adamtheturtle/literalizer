"""Haskell language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@beartype
def _format_haskell_dict_entry(key: str, value: str) -> str:
    """Format a Haskell dict entry as a tuple pair."""
    return f"({key}, {value})"


@beartype
def _format_haskell_omap_entry(key: str, value: str) -> str:
    """Format a Haskell ordered-map entry as a tuple pair."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Haskell variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Haskell variable assignment."""
    return f"{name} = {value}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class Haskell:
    """Haskell language specification."""

    def __init__(self) -> None:
        """Initialize Haskell language specification."""
        self.null_literal = "HNull"
        self.true_literal = "HBool True"
        self.false_literal = "HBool False"
        self.sequence_open = "HList ["
        self.sequence_close = "]"
        self.dict_open = "HMap ["
        self.dict_close = "]"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_haskell_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "HSet ["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "HMap ["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_haskell_omap_entry
        )
        self.multiline_close_indent = "    "
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
