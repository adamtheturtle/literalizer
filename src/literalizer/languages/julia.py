"""Julia language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    dict_entry_with_separator,
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
    passthrough_set_entry,
    variable_formatter,
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
    date_scalar_preamble,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from literalizer._types import Value


@beartype
class Julia(metaclass=LanguageCls):
    """Julia language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JULIA`` — ``Date(...)`` constructor call,
              e.g. ``Date(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.JULIA`` — ``DateTime(...)`` constructor
              call, e.g. ``DateTime(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which Julia sequence type to use.

            * ``sequence_formats.ARRAY`` — array literal,
              e.g. ``[1, 2, 3]``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
    """

    extension = ".jl"
    pygments_name = "julia"

    class DateFormats(enum.Enum):
        """Date formatting options for Julia."""

        JULIA = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="Date({year}, {month}, {day})",
            ),
            preamble_lines=("using Dates",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Julia."""

        JULIA = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="DateTime({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
            preamble_lines=("using Dates",),
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
        """Sequence type options for Julia."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            supports_trailing_comma=True,
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
        """Set type options for Julia."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="Set(["),
            close="])",
            empty_set="Set()",
            preamble_lines=(),
            set_opener_template="",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="#=",
            suffix=" =#",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = "assign"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DICT = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="Dict("),
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" => ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="Dict()",
            preamble_lines=(),
            narrowed_open=None,
        )
        ORDERED = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="OrderedDict("),
            close=")",
            format_entry=dict_entry_with_separator(
                separator=" => ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict="OrderedDict()",
            preamble_lines=("using DataStructures",),
            narrowed_open=None,
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = "allow"

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

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        AUTO = "auto"

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
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
        date_format: DateFormats = DateFormats.JULIA,
        datetime_format: DatetimeFormats = DatetimeFormats.JULIA,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.HASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_format: DictFormats = DictFormats.DICT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Julia language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self._null_literal = "nothing"
        self._true_literal = "true"
        self._false_literal = "false"
        fmt = sequence_format.value
        self._sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self._set_format_config: SetFormatConfig = set_format.value
        self._sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self._dict_format_config: DictFormatConfig = dict_format.value
        self._trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self._format_bytes: Callable[[bytes], str] = bytes_format
        self._format_date: Callable[[datetime.date], str] = date_format
        self._format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self._format_string: Callable[[str], str] = format_string_backslash
        self._format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
        self._format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self._format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self._comment_config: CommentConfig = comment_format.value
        self._ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="[",
                close="]",
                preamble_lines=(),
            )
        )
        self._format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=" => ",
                format_value=passthrough_sequence_entry,
            )
        )
        self._indent = indent
        self._indent_closing_delimiter = False
        self._element_separator = ", "
        self._skip_null_dict_values = False
        self._supports_collection_comments = True
        self._format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self._format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self._static_preamble: Sequence[str] = ()
        self._static_body_preamble: Sequence[str] = ()
        self._scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self._scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self._compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self._scalar_body_preamble,
        )

        self._type_hint_collection_preamble_lines: tuple[str, ...] = ()
