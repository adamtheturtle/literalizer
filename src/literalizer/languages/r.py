"""R language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_date_r,
    format_datetime_iso,
    format_datetime_r,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer.exceptions import EmptyDictKeyError

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value


@beartype
def _format_r_dict_entry_positional(key: str, value: str) -> str:
    """Format an R named list entry.

    R list syntax does not allow zero-length names (``"" = value`` is a
    parse error), so empty-string keys are emitted as positional (unnamed)
    elements.
    """
    if key == '""':
        return value
    return f"{key} = {value}"


@beartype
def _format_r_dict_entry_error(key: str, value: str) -> str:
    """Format an R named list entry, raising on empty-string keys."""
    if key == '""':
        msg = (
            "R does not support empty-string dict keys. "
            "Use empty_dict_key=R.EmptyDictKey.POSITIONAL to emit them "
            "as unnamed list elements instead."
        )
        raise EmptyDictKeyError(msg)
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


@beartype
class R:
    """R language specification.

    Dicts are represented as named ``list()`` calls where each entry is
    written as ``"key" = value``.  R's parser rejects zero-length names, so
    by default **dict keys that are empty strings are emitted as positional
    (unnamed) list elements** rather than as ``"" = value``.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``DateFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15"``.
            * ``DateFormat.R`` — ``as.Date(...)`` call,
              e.g. ``as.Date("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``DatetimeFormat.ISO`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``DatetimeFormat.R`` — ``as.POSIXct(...)`` call,
              e.g. ``as.POSIXct("2024-01-15T12:30:00")``.

        empty_dict_key: How to handle empty-string dict keys.

            * ``EmptyDictKey.POSITIONAL`` (default) — emit as an unnamed
              positional list element.
            * ``EmptyDictKey.ERROR`` — raise
              :class:`~literalizer.exceptions.EmptyDictKeyError`.
    """

    class DateFormat(enum.Enum):
        """Date formatting options for R."""

        ISO = enum.member(value=format_date_iso)
        R = enum.member(value=format_date_r)

    class DatetimeFormat(enum.Enum):
        """Datetime formatting options for R."""

        ISO = enum.member(value=format_datetime_iso)
        R = enum.member(value=format_datetime_r)

    class EmptyDictKey(enum.Enum):
        """How to handle empty-string dict keys in R.

        R's parser rejects zero-length names (``"" = value`` is a parse
        error).
        """

        POSITIONAL = enum.member(value=_format_r_dict_entry_positional)
        ERROR = enum.member(value=_format_r_dict_entry_error)

    def __init__(
        self,
        *,
        date_format: DateFormat,
        datetime_format: DatetimeFormat,
        empty_dict_key: EmptyDictKey,
    ) -> None:
        """Initialize R language specification."""
        self.null_literal = "NULL"
        self.true_literal = "TRUE"
        self.false_literal = "FALSE"
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str="list("
        )
        self.sequence_close = ")"
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="list("
        )
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            empty_dict_key.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        self.format_date: Callable[[datetime.date], str] = date_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value  # ty: ignore[invalid-assignment]  # pyrefly: ignore[bad-assignment]
        )
        self.format_string: Callable[[str], str] = format_string_backslash
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
        self.coerce_heterogeneous_to_strings = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
