"""Occam-pi language specification."""

import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_hex,
    passthrough_sequence_entry,
    variable_formatter,
)
from literalizer._formatters.format_strings import format_string_backslash
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
    from collections.abc import Callable, Sequence


@beartype
def _format_occam_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in the appropriate occam-pi ``LIT``
    constructor.
    """
    match original:
        case bool():
            return formatted
        case int():
            return f"MOBILE LIT(lit.int; {formatted})"
        case float():
            return f"MOBILE LIT(lit.float; {formatted}(REAL32))"
        case str() | bytes() | datetime.date():
            return f"MOBILE LIT(lit.str; MOBILE []BYTE {formatted})"
        case _:
            return formatted


@beartype
class Occam(metaclass=LanguageCls):
    """Occam-pi language specification."""

    extension = ".occ"
    # Pygments has no occam lexer.
    pygments_name = "text"
    supports_default_set_type = False

    class DateFormats(enum.Enum):
        """Date format options for Occam."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Occam."""

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
        """Sequence type options for Occam."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(
                open_str="MOBILE LIT(lit.list; MOBILE []MOBILE LIT [",
            ),
            close="])",
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
        """Set type options for Occam."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(
                open_str="MOBILE LIT(lit.set; MOBILE []MOBILE LIT [",
            ),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_DASH = CommentConfig(
            prefix="--",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        VAL = "val"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = "allow"

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
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_DASH,
        declaration_style: DeclarationStyles = DeclarationStyles.VAL,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Occam language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "MOBILE LIT(lit.null)"
        self.true_literal = "MOBILE LIT(lit.bool; TRUE)"
        self.false_literal = "MOBILE LIT(lit.bool; FALSE)"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(
                open_str="MOBILE LIT(lit.map; MOBILE []MOBILE LIT [",
            ),
            close="])",
            format_entry=dict_entry_with_template(
                template="MOBILE LIT(lit.pair; MOBILE []BYTE {key}; {value})",
                format_value=_format_occam_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
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
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[Value, str], str] = (
            _format_occam_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            _format_occam_entry
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
                open_str="MOBILE LIT(lit.map; MOBILE []MOBILE LIT [",
                close="])",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_template(
                template="MOBILE LIT(lit.pair; MOBILE []BYTE {key}; {value})",
                format_value=_format_occam_entry,
            )
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(
                template="VAL MOBILE LIT {name} IS {value}:",
            )
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} := {value}")
        )
        self.static_preamble: Sequence[str] = (
            "MOBILE DATA TYPE LIT IS\n"
            "  CASE\n"
            "    lit.null\n"
            "    lit.bool ; BOOL\n"
            "    lit.int ; INT\n"
            "    lit.float ; REAL32\n"
            "    lit.str ; MOBILE []BYTE\n"
            "    lit.list ; MOBILE []MOBILE LIT\n"
            "    lit.map ; MOBILE []MOBILE LIT\n"
            "    lit.pair ; MOBILE []BYTE ; MOBILE LIT\n"
            "    lit.set ; MOBILE []MOBILE LIT\n"
            ":",
        )
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
