"""R language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING, Literal

from beartype import beartype

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_date_r,
    format_datetime_iso,
    format_datetime_r,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


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


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "r": format_date_r,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "r": format_datetime_r,
}
_string_format: Callable[[str], str] = format_string_backslash


class R:
    """R language specification.

    Dicts are represented as named ``list()`` calls where each entry is
    written as ``"key" = value``.  R's parser rejects zero-length names, so
    **dict keys that are empty strings are emitted as positional (unnamed)
    list elements** rather than as ``"" = value``.  The name is lost in the
    output; if you need to round-trip empty-string keys, use a different
    target language.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``"iso"`` (default) — ISO 8601 string, e.g. ``"2024-01-15"``.
            * ``"r"`` — ``as.Date(...)`` call,
              e.g. ``as.Date("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``"iso"`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``"r"`` — ``as.POSIXct(...)`` call,
              e.g. ``as.POSIXct("2024-01-15T12:30:00")``.
    """

    @beartype
    def __init__(
        self,
        *,
        date_format: Literal["iso", "r"] = "iso",
        datetime_format: Literal["iso", "r"] = "iso",
    ) -> None:
        """Initialize R language specification."""
        self.null_literal = "NULL"
        self.true_literal = "TRUE"
        self.false_literal = "FALSE"
        self.sequence_open = "list("
        self.sequence_close = ")"
        self.dict_open = "list("
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_r_dict_entry
        )
        self.multiline_trailing_comma = False
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
        self.set_open = "list("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "#"
        self.comment_suffix = ""
        self.omap_open = "list("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_r_omap_entry
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
