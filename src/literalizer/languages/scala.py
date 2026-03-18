"""Scala language specification."""

import datetime
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _infer_scala_element_type(values: list[Any]) -> str | None:
    """Recursively infer the Scala element type for a list of values.

    Returns a type string like ``"String"``, ``"Int"``,
    ``"Array[Int]"``, or ``None`` when the type cannot be inferred.
    """
    if not values:
        return None
    if all(isinstance(v, str) for v in values):
        return "String"
    if all(isinstance(v, bool) for v in values):
        return "Boolean"
    if all(isinstance(v, int) and not isinstance(v, bool) for v in values):
        return "Int"
    if all(
        isinstance(v, (int, float)) and not isinstance(v, bool) for v in values
    ) and any(isinstance(v, float) for v in values):
        return "Double"
    if all(isinstance(v, list) for v in values):
        inner_types = {_infer_scala_element_type(values=v) for v in values}
        if len(inner_types) == 1:
            inner_type = inner_types.pop()
            if inner_type is not None:
                return f"Array[{inner_type}]"
    return None


@beartype
def _format_scala_collection_open(values: list[Any]) -> str:
    """Return a typed Scala collection opener inferred from element types.

    Returns ``"Array[String]("`` when all elements are strings,
    ``"Array[Boolean]("`` when all elements are booleans,
    ``"Array[Int]("`` when all elements are non-boolean integers,
    ``"Array[Double]("`` when all elements are non-boolean numeric
    (float, or mixed int and float), ``"Array[Array[Int]]("`` for nested
    homogeneous arrays, and ``"List("`` otherwise.
    """
    element_type = _infer_scala_element_type(values=values)
    if element_type is not None:
        return f"Array[{element_type}]("
    return "List("


@beartype
def _format_scala_omap_entry(key: str, value: str) -> str:
    """Format a Scala ``ListMap`` entry as a ``key -> value`` pair."""
    return f"{key} -> {value}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Scala variable declaration."""
    return f"val {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Scala variable assignment."""
    return f"{name} = {value}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class Scala:
    """Scala language specification."""

    @beartype
    def __init__(self) -> None:
        """Initialize Scala language specification."""
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = (
            _format_scala_collection_open
        )
        self.sequence_close = ")"
        self.dict_open = "Map("
        self.dict_close = ")"
        self.format_dict_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=" -> ")
        )
        self.multiline_trailing_comma = True
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "Set("
        self.set_close = ")"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "//"
        self.comment_suffix = ""
        self.omap_open = "scala.collection.immutable.ListMap("
        self.omap_close = ")"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_scala_omap_entry
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
