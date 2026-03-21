"""Visual Basic (.NET) language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING, Any

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_vb,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_sequence_open,
)
from literalizer._language import (
    HasFormatEnums,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value  # noqa: TC001

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

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

@beartype
class VisualBasic(metaclass=HasFormatEnums):
    """Visual Basic (.NET) language specification.

    VB.NET collection initializers (``New T() { ... }``,
    ``New HashSet(Of T) From { ... }``, etc.) do not support comments
    inside the ``{ ... }`` block.  YAML comments associated with
    collection elements are therefore emitted as standalone comment lines
    *before* the collection — or before the variable declaration when a
    variable name is supplied.
    """

    class DateFormats(enum.Enum):
        """Date format options for VisualBasic."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for VisualBasic."""

        ISO = enum.member(value=format_datetime_iso)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Visual Basic."""

        ARRAY = SequenceFormatConfig(
            open_str="New Object() {",
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="New Object() {}",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Visual Basic."""

        HASH_SET = SetFormatConfig(
            open_str="New HashSet(Of Object) From {",
            close="}",
            empty_set="New HashSet(Of Object)()",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.HASH_SET,
    ) -> None:
        """Initialize VisualBasic language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "Nothing"
        self.true_literal = "True"
        self.false_literal = "False"
        fmt = sequence_format.value
        self.sequence_format_config = fmt
        self.set_format_config = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = typed_sequence_open(
            schema_to_opener=_vb_schema_to_opener,
            fallback=fmt.open_str,
        )
        self.dict_open: Callable[[dict[str, Value]], str] = fixed_dict_open(
            open_str="New Dictionary(Of String, Object) From {",
        )
        self.dict_close = "}"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_vb_dict_entry
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_vb
        self.empty_dict: str | None = None
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
        self.supports_collection_comments = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
