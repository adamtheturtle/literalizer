"""OCaml language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value


@beartype
def _format_date_ocaml(value: datetime.date) -> str:
    """Format a date as an OCaml ``ODate`` constructor."""
    return f"ODate ({value.year}, {value.month}, {value.day})"


@beartype
def _format_datetime_ocaml(value: datetime.datetime) -> str:
    """Format a datetime as an OCaml ``ODatetime`` constructor."""
    return (
        f"ODatetime (({value.year}, {value.month}, {value.day}), "
        f"({value.hour}, {value.minute}, {value.second}))"
    )


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
        "ODate",
        "ODatetime",
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
    float(rest)
    return f"OFloat ({value})" if negative else f"OFloat {value}"


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
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format an OCaml variable declaration."""
    return f"let {name} : val_t = {_to_val(value=value)}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format an OCaml variable assignment."""
    return _format_variable_declaration(name=name, value=value, _data=_data)


_string_format: Callable[[str], str] = format_string_backslash


@beartype
class OCaml(metaclass=LanguageCls):
    """OCaml language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.OCAML`` — tuple literal,
              e.g. ``(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.OCAML`` — pair of tuples,
              e.g. ``((2024, 1, 15), (12, 30, 0))``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".ml"
    pygments_name = "ocaml"

    class DateFormats(enum.Enum):
        """Date format options for OCaml."""

        OCAML = DateFormatConfig(formatter=_format_date_ocaml)
        ISO = DateFormatConfig(formatter=format_date_iso, produces_string=True)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for OCaml."""

        OCAML = DatetimeFormatConfig(formatter=_format_datetime_ocaml)
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            produces_string=True,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for OCaml."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="OList ["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
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
            set_open=fixed_set_open(open_str="OSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        PAREN_STAR = CommentConfig(
            prefix="(*",
            suffix=" *)",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = "let"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = "no"

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
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    integer_formats = IntegerFormats
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.OCAML,
        datetime_format: DatetimeFormats = DatetimeFormats.OCAML,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.PAREN_STAR,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
    ) -> None:
        """Initialize OCaml language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "ONull"
        self.true_literal = "OBool true"
        self.false_literal = "OBool false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="OMap ["),
            close="]",
            format_entry=_format_ocaml_dict_entry,
            empty_dict=None,
            preamble_lines=(),
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_integer: Callable[[int], str] = str
        self.format_set_entry: Callable[[str], str] = _format_ocaml_set_entry
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="OMap [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_ocaml_ordered_map_entry
        )
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[str], str] = (
            _format_ocaml_sequence_entry
        )
        self.static_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
