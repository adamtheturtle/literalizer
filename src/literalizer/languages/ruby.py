"""Ruby language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Literal

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_date_ruby,
    format_datetime_iso,
    format_datetime_ruby,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._language import Language


def _format_ruby_omap_entry(key: str, value: str) -> str:
    """Format a Ruby ordered-map entry."""
    return f"{key} => {value}"


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Ruby variable declaration."""
    return f"{name} = {value}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Ruby variable assignment."""
    return f"{name} = {value}"


_DATE_FORMATS: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "ruby": format_date_ruby,
}

_DATETIME_FORMATS: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "ruby": format_datetime_ruby,
}


class Ruby:
    """Ruby language specification."""

    def __init__(
        self,
        *,
        date_format: Literal["iso", "ruby"] = "iso",
        datetime_format: Literal["iso", "ruby"] = "iso",
    ) -> None:
        """Initialize Ruby language specification."""
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "["
        self.sequence_close = "]"
        self.dict_open = "{"
        self.dict_close = "}"
        self.format_dict_entry = dict_entry_with_separator(separator=" => ")
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes = format_bytes_hex
        self.format_date = _DATE_FORMATS[date_format]
        self.format_datetime = _DATETIME_FORMATS[datetime_format]
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "Set.new(["
        self.set_close = "])"
        self.empty_set: str | None = "Set.new"
        self.format_sequence_entry = passthrough_sequence_entry
        self.format_set_entry = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry = _format_ruby_omap_entry
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration = _format_variable_declaration
        self.format_variable_assignment = _format_variable_assignment


RUBY: Language = Ruby()
