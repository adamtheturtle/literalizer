"""Clojure language specification."""

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._language import Language


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Clojure variable declaration."""
    return f"(def {name} {value})"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Clojure variable assignment."""
    return f"(def {name} {value})"


class Clojure:
    """Clojure language specification."""

    def __init__(self) -> None:
        """Initialize Clojure language specification."""
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "["
        self.sequence_close = "]"
        self.dict_open = "{"
        self.dict_close = "}"
        self.format_dict_entry = dict_entry_with_separator(separator=" ")
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes = format_bytes_hex
        self.format_date = format_date_iso
        self.format_datetime = format_datetime_iso
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "#{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry = passthrough_sequence_entry
        self.format_set_entry = passthrough_set_entry
        self.comment_prefix = ";"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry = dict_entry_with_separator(separator=" ")
        self.multiline_close_indent = ""
        self.element_separator = " "
        self.skip_null_dict_values = False
        self.format_variable_declaration = _format_variable_declaration
        self.format_variable_assignment = _format_variable_assignment


CLOJURE: Language = Clojure()
