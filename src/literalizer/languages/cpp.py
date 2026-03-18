"""C++ language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Literal

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_cpp,
    format_date_iso,
    format_datetime_cpp,
    format_datetime_iso,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._language import Language


@beartype
def _format_cpp_dict_entry(key: str, value: str) -> str:
    """Format a C++ dict entry as a brace-enclosed pair."""
    return f"{{{key}, {value}}}"


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a C++ variable declaration."""
    return f"auto {name} = {value};"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a C++ variable assignment."""
    return f"{name} = {value};"


_DATE_FORMATS: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "cpp": format_date_cpp,
}

_DATETIME_FORMATS: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "cpp": format_datetime_cpp,
}


class Cpp:
    """C++ language specification."""

    def __init__(
        self,
        *,
        date_format: Literal["iso", "cpp"] = "iso",
        datetime_format: Literal["iso", "cpp"] = "iso",
    ) -> None:
        """Initialize Cpp language specification."""
        self.null_literal = "nullptr"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open = "{"
        self.sequence_close = "}"
        self.dict_open = "{"
        self.dict_close = "}"
        self.format_dict_entry = _format_cpp_dict_entry
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes = format_bytes_hex
        self.format_date = _DATE_FORMATS[date_format]
        self.format_datetime = _DATETIME_FORMATS[datetime_format]
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry = passthrough_sequence_entry
        self.format_set_entry = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "{"
        self.omap_close = "}"
        self.format_omap_entry = _format_cpp_dict_entry
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration = _format_variable_declaration
        self.format_variable_assignment = _format_variable_assignment


CPP: Language = Cpp()
