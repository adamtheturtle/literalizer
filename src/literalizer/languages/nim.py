"""Nim language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
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
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
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
def _format_date_nim(value: datetime.date) -> str:
    """Format a date as a Nim table literal."""
    return (
        f'{{"year": {value.year}, "month": {value.month}, "day": {value.day}}}'
    )


@beartype
def _format_datetime_nim(value: datetime.datetime) -> str:
    """Format a datetime as a Nim table literal."""
    return (
        f'{{"year": {value.year}, "month": {value.month}, '
        f'"day": {value.day}, "hour": {value.hour}, '
        f'"minute": {value.minute}, "second": {value.second}}}'
    )


@beartype
def _make_variable_declaration(
    *,
    sequence_mode: bool,
    keyword: str,
    force_sequence: bool,
) -> Callable[[str, str, Value], str]:
    """Create a Nim variable declaration formatter."""

    @beartype
    def _format(name: str, value: str, _data: Value) -> str:
        """Format a declaration, using ``@`` for flat sequences of
        simple scalars.
        """
        use_sequence = (
            isinstance(_data, list)
            and _data
            and (
                force_sequence
                or (
                    sequence_mode
                    and all(
                        isinstance(item, (str, int, float, bool, bytes))
                        for item in _data
                    )
                )
            )
        )
        if use_sequence:
            return f"{keyword} {name} = @{value}"
        if force_sequence:
            return f"{keyword} {name} = {value}"
        return f"{keyword} {name} = %* {value}"

    return _format


@beartype
def _make_variable_assignment(
    *,
    sequence_mode: bool,
) -> Callable[[str, str, Value], str]:
    """Create a Nim variable assignment formatter."""

    @beartype
    def _format(name: str, value: str, _data: Value) -> str:
        """Format an assignment, using ``@`` for flat sequences of
        simple scalars.
        """
        if (
            sequence_mode
            and isinstance(_data, list)
            and _data
            and all(
                isinstance(item, (str, int, float, bool, bytes))
                for item in _data
            )
        ):
            return f"{name} = @{value}"
        return f"{name} = %* {value}"

    return _format


@beartype
class Nim(metaclass=LanguageCls):
    """Nim language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.NIM`` — table literal,
              e.g. ``{"year": 2024, "month": 1, "day": 15}``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.NIM`` — table literal,
              e.g. ``{"year": 2024, "month": 1, "day": 15,
              "hour": 12, "minute": 30, "second": 0}``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".nim"
    pygments_name = "nim"

    class DateFormats(enum.Enum):
        """Date format options for Nim."""

        NIM = DateFormatConfig(
            formatter=_format_date_nim,
            preamble_lines=("import json",),
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso,
            preamble_lines=("import json",),
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Nim."""

        NIM = DatetimeFormatConfig(
            formatter=_format_datetime_nim,
            preamble_lines=("import json",),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=("import json",),
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
        """Sequence type options for Nim."""

        SEQ = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=("import json",),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
            preamble_lines=("import json",),
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
        """Set type options for Nim."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="["),
            close="]",
            empty_set=None,
            preamble_lines=("import json",),
            set_opener_template="",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="#[",
            suffix=" ]#",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        VAR = "var"
        LET = "let"
        CONST = "const"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal)
        BINARY = enum.member(value=format_integer_binary)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = "yes"
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
        date_format: DateFormats = DateFormats.NIM,
        datetime_format: DatetimeFormats = DatetimeFormats.NIM,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.SEQ,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.HASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.VAR,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
    ) -> None:
        """Initialize Nim language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "nil"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=("import json",),
        )
        self.multiline_trailing_comma: bool = trailing_comma.name == "YES"
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_integer: Callable[[int], str] = integer_format
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
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
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="{",
                close="}",
                preamble_lines=("import json",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            )
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        _is_sequence = sequence_format is self.sequence_formats.SEQ
        _is_const = declaration_style is self.declaration_styles.CONST
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _make_variable_declaration(
                sequence_mode=_is_sequence,
                keyword=declaration_style.value,
                force_sequence=_is_const,
            )
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _make_variable_assignment(sequence_mode=_is_sequence)
        )
        _json = ("import json",)
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {
            str: _json,
            int: _json,
            float: _json,
            bool: _json,
            type(None): _json,
            bytes: _json,
            datetime.date: date_format.value.preamble_lines,
            datetime.datetime: datetime_format.value.preamble_lines,
        }
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
