"""YAML language specification."""

import datetime
import enum
import functools
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    date_iso_formatter,
    datetime_iso_formatter,
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash_control,
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
)

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from literalizer._types import Value


@beartype
class Yaml(metaclass=LanguageCls):
    """YAML language specification.

    Produces YAML flow-style values — flow mappings for dicts, and
    flow sequences for sequences and sets — so that the output is
    valid inline YAML that can be embedded in any YAML document.

    Dates and datetimes are rendered as unquoted YAML native date /
    datetime literals, which YAML parsers interpret as typed values.
    """

    extension = ".yaml"
    pygments_name = "yaml"

    class DateFormats(enum.Enum):
        """Date format options for Yaml."""

        YAML = DateFormatConfig(
            formatter=date_iso_formatter(template="{iso}"),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Yaml."""

        YAML = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(template="{iso}"),
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
        """Sequence type options for YAML."""

        SEQUENCE = SequenceFormatConfig(
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

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for YAML."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = "assign"

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
        date_format: DateFormats = DateFormats.YAML,
        datetime_format: DatetimeFormats = DatetimeFormats.YAML,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.SEQUENCE,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.HASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize YAML language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self._null_literal = "null"
        self._true_literal = "true"
        self._false_literal = "false"
        fmt = sequence_format.value
        self._sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self._set_format_config: SetFormatConfig = set_format.value
        self._sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self._dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self._trailing_comma_config: TrailingCommaConfig = TrailingCommaConfig(
            multiline_trailing_comma=False,
        )
        self._format_bytes: Callable[[bytes], str] = bytes_format
        self._format_date: Callable[[datetime.date], str] = date_format
        self._format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self._format_string: Callable[[str], str] = functools.partial(
            format_string_backslash_control,
            control_char_fmt="\\x{:02x}",
        )
        self._format_integer: Callable[[int], str] = str
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
                open_str="{",
                close="}",
                preamble_lines=(),
            )
        )
        self._format_ordered_map_entry: Callable[[str, Value, str], str] = (
            dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            )
        )
        self._indent = indent
        self._indent_closing_delimiter = False
        self._element_separator = ", "
        self._skip_null_dict_values = False
        self._supports_collection_comments = True
        self._format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name}: {value}")
        )
        self._format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name}: {value}")
        )
        self._static_preamble: Sequence[str] = ()
        self._static_body_preamble: Sequence[str] = ()
        self._scalar_preamble: dict[type, tuple[str, ...]] = {}
        self._scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self._compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self._scalar_body_preamble,
        )

        self._type_hint_collection_preamble_lines: tuple[str, ...] = ()
