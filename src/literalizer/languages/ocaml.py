"""OCaml language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    format_string_backslash,
    passthrough_sequence_entry,
    tuple_dict_entry,
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
    TrailingCommaConfig,
    body_preamble_from_scalars,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _format_ocaml_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in the appropriate OCaml ``val_t``
    constructor.
    """
    match original:
        case bool():
            return formatted
        case int():
            negative = formatted.startswith("-")
            return f"OInt ({formatted})" if negative else f"OInt {formatted}"
        case float():
            negative = formatted.startswith("-")
            return (
                f"OFloat ({formatted})" if negative else f"OFloat {formatted}"
            )
        case str() | bytes():
            return f"OStr {formatted}"
        case datetime.date() if formatted.startswith('"'):
            return f"OStr {formatted}"
        case _:
            return formatted


@beartype
def _format_variable_declaration(name: str, value: str, data: Value) -> str:
    """Format an OCaml variable declaration."""
    val_type = "val_t array" if value.lstrip().startswith("[|") else "val_t"
    wrapped = _format_ocaml_entry(original=data, formatted=value)
    return f"let {name} : {val_type} = {wrapped}"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format an OCaml variable assignment."""
    return _format_variable_declaration(name=name, value=value, data=data)


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

        OCAML = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="ODate ({year}, {month}, {day})",
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for OCaml."""

        OCAML = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="ODatetime (({year}, {month}, {day}), "
                "({hour}, {minute}, {second}))",
            ),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
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
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="[|"),
            close="|]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
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
            set_opener_template="",
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

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": format_integer_hex,
                "UNDERSCORE": format_integer_hex,
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": format_integer_binary,
                "UNDERSCORE": format_integer_binary,
            }
        )

        def get_formatter(
            self,
            numeric_separator: enum.Enum,
        ) -> Callable[[int], str]:
            """Return the integer formatter for the given separator."""
            formatter: Callable[[int], str] = self.value[
                numeric_separator.name
            ]
            return formatter

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"
        UNDERSCORE = "underscore"

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

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

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
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
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
            format_entry=tuple_dict_entry(
                format_value=_format_ocaml_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
        )
        self.trailing_comma_config: TrailingCommaConfig = TrailingCommaConfig(
            multiline_trailing_comma=False,
        )
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            _format_ocaml_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="OMap [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=_format_ocaml_entry)
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.element_separator = "; "
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _format_ocaml_entry
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        _h = "type val_t ="
        _date_constructor = (
            "  | OStr of string"
            if date_format.value.type_produced is str
            else "  | ODate of (int * int * int)"
        )
        _datetime_constructor = (
            "  | OStr of string"
            if datetime_format.value.type_produced is str
            else "  | ODatetime of ((int * int * int) * (int * int * int))"
        )
        self.scalar_body_preamble: dict[
            type,
            tuple[str, ...],
        ] = {
            type(None): (_h, "  | ONull"),
            bool: (_h, "  | OBool of bool"),
            int: (_h, "  | OInt of int"),
            float: (_h, "  | OFloat of float"),
            str: (_h, "  | OStr of string"),
            bytes: (_h, "  | OStr of string"),
            datetime.date: (_h, _date_constructor),
            datetime.datetime: (_h, _datetime_constructor),
            list: (_h, "  | OList of val_t list"),
            dict: (_h, "  | OMap of (string * val_t) list"),
            ordereddict: (_h, "  | OMap of (string * val_t) list"),
            set: (_h, "  | OSet of val_t list"),
        }
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
