"""Mojo language specification."""

import dataclasses
import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    make_element_to_type,
    make_type_to_opener,
    typed_set_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    sequence_format_factory,
    set_format_factory,
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
def _format_mojo_ordered_map_entry(key: str, _val: Value, value: str) -> str:
    """Format one Mojo ordered-map entry as a ``Tuple(key, value)``."""
    return f"Tuple({key}, {value})"


@beartype
class Mojo(metaclass=LanguageCls):
    """Mojo language specification.

    Mojo does not support heterogeneous collections — every element in a
    list or set must share a single type.  When a collection contains
    scalar values of mixed types (e.g. ``[1, 2.5, 3]``), **all values
    are coerced to their string representations** so that the resulting
    literal is valid Mojo (e.g. ``["1", "2.5", "3"]``).

    For sets, this coercion can cause the output to have fewer elements
    than the input when distinct values of different types coerce to the
    same string (e.g. ``{1, "1"}`` both become ``"1"``).
    """

    extension = ".mojo"
    pygments_name = "mojo"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_type = True

    class DateFormats(enum.Enum):
        """Date format options for Mojo."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Mojo."""

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
        """Sequence type options for Mojo."""

        LIST = enum.member(
            value=sequence_format_factory(
                open_template="[",
                close="]",
                supports_heterogeneity=False,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template="List[{type}]()",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self(default_type="String").supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Mojo."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set[{type}](",
                close=")",
                empty_template="Set[{type}]()",
                preamble_lines=("from std.collections import Set",),
                set_opener_template="Set[{type_name}](",
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

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

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template="{{",
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="Dict[{type}, {type}]()",
                preamble_lines=(),
                narrowed_open=None,
            )
        )

        def __call__(self, default_type: str) -> DictFormatConfig:
            """Create a dict format config for the given type."""
            return self.value(default_type)

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

        YES = "yes"

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
        default_set_element_type: str = "String",
        default_sequence_element_type: str = "String",
        default_dict_type: str = "String",
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.HASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize Mojo language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "None"
        self.true_literal = "True"
        self.false_literal = "False"
        fmt = sequence_format(default_type=default_sequence_element_type)
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format

        self.set_format_config: SetFormatConfig = set_format(
            default_type=default_set_element_type,
        )
        self.set_format_config = dataclasses.replace(
            self.set_format_config,
            set_open=typed_set_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=make_element_to_type(
                        str_type="String",
                        bool_type="Bool",
                        int_type="Int",
                        float_type="Float64",
                        mixed_numeric_type="String",
                        bytes_type=None,
                        date_type=None,
                        datetime_type=None,
                        list_template="List[{inner}]",
                        dict_type_template=None,
                        fallback_value_type=None,
                    ),
                    opener_template="Set[{type_name}](",
                ),
                fallback=self.set_format_config.set_open([]),
            ),
        )
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = dict_format(
            default_type=default_dict_type,
        )
        self.trailing_comma_config: TrailingCommaConfig = TrailingCommaConfig(
            multiline_trailing_comma=True,
        )
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_integer: Callable[[int], str] = str
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
                open_str="[",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            _format_mojo_ordered_map_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(template="var {name} = {value}")
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
