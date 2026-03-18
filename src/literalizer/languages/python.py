"""Python language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING, Literal

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_bytes_python,
    format_date_iso,
    format_date_python,
    format_datetime_epoch,
    format_datetime_iso,
    format_datetime_python,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_python_omap_entry(key: str, value: str) -> str:
    """Format one Python ``OrderedDict`` entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Python variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Python variable assignment."""
    return f"{name} = {value}"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "python": format_date_python,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "python": format_datetime_python,
    "epoch": format_datetime_epoch,
}
_string_format: Callable[[str], str] = format_string_backslash

_bytes_formats: dict[str, Callable[[bytes], str]] = {
    "hex": format_bytes_hex,
    "python": format_bytes_python,
}


class Python:
    """Python language specification."""

    def __init__(
        self,
        *,
        date_format: Literal["iso", "python"] = "iso",
        datetime_format: Literal["iso", "python", "epoch"] = "iso",
        bytes_format: Literal["hex", "python"] = "hex",
    ) -> None:
        """Initialize Python language specification."""
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        self.sequence_open = "("
        self.sequence_close = ")"
        self.dict_open = "{"
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = True
        self.format_bytes: Callable[[bytes], str] = _bytes_formats[
            bytes_format
        ]
        self.format_date: Callable[[datetime.date], str] = _date_formats[
            date_format
        ]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_formats[datetime_format]
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "{"
        self.set_close = "}"
        self.empty_set: str | None = "set()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "OrderedDict(["
        self.omap_close = "])"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_python_omap_entry
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
        self.format_collection_open: Callable[[list[Value]], str] | None = None
