"""OCaml language specification."""

import datetime
import enum
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    HasFormatEnums,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _to_val(value: str) -> str:
    """Convert a value to an OCaml union type expression."""
    _val_prefixes = (
        "ONull",
        "OBool",
        "OList",
        "OMap",
        "OSet",
        "OStr",
        "OInt",
        "OFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"OStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"OInt ({value})" if negative else f"OInt {value}"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"OFloat ({value})" if negative else f"OFloat {value}"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


@beartype
def _format_ocaml_dict_entry(key: str, value: str) -> str:
    """Format an OCaml dict entry as a ``(key, OXxx value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_ocaml_ordered_map_entry(key: str, value: str) -> str:
    """Format an OCaml ordered-map entry as a ``(key, OXxx value)``
    tuple.
    """
    return f"({key}, {_to_val(value=value)})"


@beartype
def _format_ocaml_set_entry(item: str) -> str:
    """Format an OCaml set entry with the appropriate ``val_t``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_ocaml_sequence_entry(item: str) -> str:
    """Format an OCaml list entry with the appropriate ``val_t``
    constructor.
    """
    return _to_val(value=item)


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format an OCaml variable declaration."""
    return f"let {name} : val_t = {_to_val(value=value)}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format an OCaml variable assignment."""
    return _format_variable_declaration(name=name, value=value)


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class OCaml(metaclass=HasFormatEnums):
    """OCaml language specification."""

    extension = ".ml"

    class DateFormats(enum.Enum):
        """Date format options for OCaml."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for OCaml."""

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
        """Sequence type options for OCaml."""

        LIST = SequenceFormatConfig(
            open_str="OList [",
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
        )
        ARRAY = SequenceFormatConfig(
            open_str="[|",
            close="|]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for OCaml."""

        SET = SetFormatConfig(
            open_str="OSet [",
            close="]",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        PAREN_STAR = CommentConfig(
            prefix="(*",
            suffix=" *)",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NONE = "none"

    variable_type_hints_formats = VariableTypeHints

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        comment_format: CommentFormats = CommentFormats.PAREN_STAR,
    ) -> None:
        """Initialize OCaml language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "ONull"
        self.true_literal = "OBool true"
        self.false_literal = "OBool false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="OMap ["),
            close="]",
            format_entry=_format_ocaml_dict_entry,
            empty_dict=None,
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_set_entry: Callable[[str], str] = _format_ocaml_set_entry
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="OMap [",
                close="]",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_ocaml_ordered_map_entry
        )
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[str], str] = (
            _format_ocaml_sequence_entry
        )
