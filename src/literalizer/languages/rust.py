"""Rust language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Literal

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_date_rust,
    format_datetime_iso,
    format_datetime_rust,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._language import Language


@beartype
def _format_rust_dict_entry(key: str, value: str) -> str:
    """Format a Rust HashMap entry as a tuple ``(key, value)``."""
    return f"({key}, {value})"


@beartype
def _format_rust_omap_entry(key: str, value: str) -> str:
    """Format a Rust ordered-map entry as a tuple ``(key, value)``."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Rust variable declaration."""
    return f"let {name} = {value};"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Rust variable assignment."""
    return f"{name} = {value};"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "rust": format_date_rust,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "rust": format_datetime_rust,
}
_string_format: Callable[[str], str] = format_string_backslash


class Rust:
    """Rust language specification."""

    def __init__(
        self,
        *,
        date_format: Literal["iso", "rust"] = "iso",
        datetime_format: Literal["iso", "rust"] = "iso",
    ) -> None:
        """Initialize Rust language specification."""
        self.null_literal = "None"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "vec!["
        self.sequence_close = "]"
        self.dict_open = "HashMap::from(["
        self.dict_close = "])"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_rust_dict_entry
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        self.format_date: Callable[[datetime.date], str] = _date_formats[
            date_format
        ]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_formats[datetime_format]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "HashSet::from(["
        self.set_close = "])"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "HashMap::from(["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_rust_omap_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )


RUST: Language = Rust()
