"""Go language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Literal

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_go,
    format_date_iso,
    format_datetime_go,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_go_collection_open(values: list[Any]) -> str:
    """Return a typed Go slice opener inferred from element types.

    Returns ``"[]string{"`` when all elements are strings,
    ``"[]bool{"`` when all elements are booleans,
    ``"[]int{"`` when all elements are non-boolean integers,
    ``"[]float64{"`` when all elements are non-boolean numeric
    (float, or mixed int and float), and ``"[]any{"`` otherwise.
    """
    if values and all(isinstance(v, str) for v in values):
        return "[]string{"
    if values and all(isinstance(v, bool) for v in values):
        return "[]bool{"
    if values and all(
        isinstance(v, int) and not isinstance(v, bool) for v in values
    ):
        return "[]int{"
    if (
        values
        and all(
            isinstance(v, (int, float)) and not isinstance(v, bool)
            for v in values
        )
        and any(isinstance(v, float) for v in values)
    ):
        return "[]float64{"
    return "[]any{"


@beartype
def _format_go_set_entry(item: str) -> str:
    """Format a Go set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple": struct{}{}``.
    """
    return f"{item}: struct{{}}{{}}"


@beartype
def _format_go_omap_entry(key: str, value: str) -> str:
    """Format a Go ordered-map entry as a ``{key, value}`` pair."""
    return f"{{{key}, {value}}}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Go variable declaration."""
    return f"{name} := {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Go variable assignment."""
    return f"{name} = {value}"


_date_formats: dict[str, Callable[[datetime.date], str]] = {
    "iso": format_date_iso,
    "go": format_date_go,
}

_datetime_formats: dict[str, Callable[[datetime.datetime], str]] = {
    "iso": format_datetime_iso,
    "go": format_datetime_go,
}
_string_format: Callable[[str], str] = format_string_backslash


class Go:
    """Go language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``"iso"`` (default) — ISO 8601 string, e.g. ``"2024-01-15"``.
            * ``"go"`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 0, 0, 0, 0, time.UTC)``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``"iso"`` (default) — ISO 8601 string,
              e.g. ``"2024-01-15T12:30:00"``.
            * ``"go"`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 12, 30, 0, 0,
              time.UTC)``.
    """

    @beartype
    def __init__(
        self,
        *,
        date_format: Literal["iso", "go"] = "iso",
        datetime_format: Literal["iso", "go"] = "iso",
    ) -> None:
        """Initialize Go language specification."""
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = (
            _format_go_collection_open
        )
        self.sequence_close = "}"
        self.dict_open = "map[string]any{"
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
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
        self.set_open = "map[any]struct{}{"
        self.set_close = "}"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = _format_go_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "[][2]any{"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_go_omap_entry
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
