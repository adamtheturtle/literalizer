"""JavaScript language specification."""

import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    format_string_backslash_single,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _format_date_js(value: datetime.date) -> str:
    """Format a date as a JavaScript ``new Date(...)`` call.

    Example: ``new Date("2024-01-15")``.
    """
    return f'new Date("{value.isoformat()}")'


@beartype
def _format_datetime_js(value: datetime.datetime) -> str:
    """Format a datetime as a JavaScript ``new Date(...)`` call.

    Example: ``new Date("2024-01-15T12:30:00")``.
    """
    return f'new Date("{value.isoformat()}")'


@beartype
def _format_integer_hex(value: int) -> str:
    """Format an integer as a JavaScript hexadecimal literal."""
    if value < 0:
        return f"-0x{abs(value):x}"
    return f"0x{value:x}"


@beartype
def _format_integer_underscore(value: int) -> str:
    """Format an integer with underscore separators."""
    s = str(object=abs(value))
    # Insert underscores every 3 digits from the right.
    group_size = 3
    groups: list[str] = []
    while len(s) > group_size:
        groups.append(s[-group_size:])
        s = s[:-group_size]
    groups.append(s)
    formatted = "_".join(reversed(groups))
    if value < 0:
        return f"-{formatted}"
    return formatted


@beartype
def _format_map_entry(key: str, value: str) -> str:
    """Format a JavaScript ``Map`` entry as ``[key, value]``."""
    return f"[{key}, {value}]"


@beartype
class JavaScript(metaclass=LanguageCls):
    """JavaScript language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15")``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.JS`` — ``new Date(...)`` call,
              e.g. ``new Date("2024-01-15T12:30:00")``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".js"
    pygments_name = "javascript"

    class DateFormats(enum.Enum):
        """Date formatting options for JavaScript."""

        JS = DateFormatConfig(formatter=_format_date_js)
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for JavaScript."""

        JS = DatetimeFormatConfig(formatter=_format_datetime_js)
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
        """Sequence type options for JavaScript."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
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
        """Set type options for JavaScript."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="new Set(["),
            close="])",
            empty_set="new Set()",
            preamble_lines=(),
            set_opener_template="",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=" */",
        )

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"
        NONE = "none"

        def wrap_formatter(
            self,
            formatter: Callable[[str, str, Value], str],
        ) -> Callable[[str, str, Value], str]:
            """Wrap a formatter to match this line ending style."""
            if self.value != "none":
                return formatter

            def without_semicolon(name: str, value: str, data: Value) -> str:
                """Format without a trailing semicolon."""
                return formatter(name, value, data).removesuffix(";")

            return without_semicolon

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        CONST = DeclarationStyleConfig(
            formatter=variable_formatter(template="const {name} = {value};"),
        )
        LET = DeclarationStyleConfig(
            formatter=variable_formatter(template="let {name} = {value};"),
        )

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        OBJECT = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(separator=": "),
            empty_dict=None,
            preamble_lines=(),
        )
        MAP = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="new Map(["),
            close="])",
            format_entry=_format_map_entry,
            empty_dict="new Map()",
            preamble_lines=(),
        )

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"
        UNDERSCORE = "underscore"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": _format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": _format_integer_hex,
                "UNDERSCORE": _format_integer_hex,
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

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        SINGLE = enum.member(value=format_string_backslash_single)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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
    numeric_separators = NumericSeparators
    integer_formats = IntegerFormats
    string_formats = StringFormats
    trailing_commas = TrailingCommas
    line_endings = LineEndings

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.JS,
        datetime_format: DatetimeFormats = DatetimeFormats.JS,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.ARRAY,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.CONST,
        dict_format: DictFormats = DictFormats.OBJECT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
    ) -> None:
        """Initialize JavaScript language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = dict_format.value
        self.multiline_trailing_comma: bool = trailing_comma.name == "YES"
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = string_format
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
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
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            dict_entry_with_separator(separator=": ")
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        _base_decl: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            line_ending.wrap_formatter(formatter=_base_decl)
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            line_ending.wrap_formatter(
                formatter=variable_formatter(template="{name} = {value};"),
            )
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
