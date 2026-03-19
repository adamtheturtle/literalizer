"""Visual Basic (.NET) language specification."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from beartype import beartype

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_vb,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)
from literalizer._types import Value  # noqa: TC001

_VB_SCALAR_TYPES: dict[str, str] = {
    "string": "String",
    "boolean": "Boolean",
    "integer": "Integer",
    "number": "Double",
}


@beartype
def _vb_schema_to_type(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a VB.NET type name, recursively."""
    schema_type = item_schema.get("type")
    if isinstance(schema_type, str):
        if schema_type in _VB_SCALAR_TYPES:
            return _VB_SCALAR_TYPES[schema_type]
        if schema_type == "array":
            nested = item_schema.get("items", {})
            inner = _vb_schema_to_type(item_schema=nested)
            return f"{inner}()" if inner is not None else None
        return None
    if (
        isinstance(schema_type, list)
        and set(schema_type) == {"integer", "number"}  # pyright: ignore[reportUnknownArgumentType]
    ):
        return "Double"
    return None


@beartype
def _vb_schema_to_opener(item_schema: dict[str, Any]) -> str | None:
    """Map a JSON Schema item type to a VB.NET array opener."""
    type_name = _vb_schema_to_type(item_schema=item_schema)
    if type_name is None:
        return None
    return f"New {type_name}() {{"


@beartype
def _format_vb_dict_entry(key: str, value: str) -> str:
    """Format a VB.NET dictionary initializer entry."""
    return f"{{{key}, {value}}}"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a VB.NET variable declaration."""
    return f"Dim {name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a VB.NET variable assignment."""
    return f"{name} = {value}"


class VisualBasic:
    """Visual Basic (.NET) language specification."""

    @beartype
    def __init__(self) -> None:
        """Initialize VisualBasic language specification."""
        self.null_literal = "Nothing"
        self.true_literal = "True"
        self.false_literal = "False"
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_vb_schema_to_opener,
            fallback="New Object() {",
        )
        self.sequence_close = "}"
        self.dict_open = "New Dictionary(Of String, Object) From {"
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_vb_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = format_bytes_hex
        self.format_date: Callable[[datetime.date], str] = format_date_iso
        self.format_datetime: Callable[[datetime.datetime], str] = (
            format_datetime_iso
        )
        self.format_string: Callable[[str], str] = format_string_vb
        self.empty_sequence: str | None = "New Object() {}"
        self.empty_dict: str | None = None
        self.set_open = "New HashSet(Of Object) From {"
        self.set_close = "}"
        self.empty_set: str | None = "New HashSet(Of Object)()"
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "'"
        self.comment_suffix = ""
        self.omap_open = "New Dictionary(Of String, Object) From {"
        self.omap_close = "}"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_vb_dict_entry
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
