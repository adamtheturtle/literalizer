"""C# language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    TypedOpenerConfig,
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    dict_entry_with_template,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
    format_string_backslash,
    make_type_to_opener,
    passthrough_sequence_entry,
    passthrough_set_entry,
    typed_dict_open,
    typed_sequence_open,
    typed_set_open,
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


@dataclasses.dataclass(frozen=True)
class _CSharpDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str
    fallback: str


@beartype
class CSharp(metaclass=LanguageCls):
    """C# language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.CSHARP`` — ``new DateOnly(...)`` call,
              e.g. ``new DateOnly(2024, 1, 15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.CSHARP`` — ``new DateTime(...)`` call,
              e.g. ``new DateTime(2024, 1, 15, 12, 30, 0)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".cs"
    pygments_name = "csharp"

    _opener_config = TypedOpenerConfig(
        str_type="string",
        bool_type="bool",
        int_type="int",
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="string",
        date_type="DateOnly",
        datetime_type="DateTime",
        list_template="{inner}[]",
        sequence_opener_template="new {type_name}[] {{",
        dict_opener_template="new Dictionary<string, {type_name}> {{",
        set_opener_template="new HashSet<{type_name}> {{",
    )

    class DateFormats(enum.Enum):
        """Date format options for C#."""

        CSHARP = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="new DateOnly({year}, {month}, {day})",
            ),
            preamble_lines=("using System;",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C#."""

        CSHARP = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template="new DateTime({year}, {month}, {day}, "
                "{hour}, {minute}, {second})",
            ),
            preamble_lines=("using System;",),
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
        """Sequence type options for C#."""

        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="ValueTuple.Create()",
            preamble_lines=("using System;",),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            supports_trailing_comma=False,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="new object[] {"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="Array.Empty<object>()",
            preamble_lines=("using System.Collections.Generic;",),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="new object[] {",
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for C#."""

        HASH_SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="new HashSet<object> {"),
            close="}",
            empty_set="new HashSet<object>()",
            preamble_lines=("using System.Collections.Generic;",),
            set_opener_template="",
        )
        SORTED_SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="new SortedSet<object> {"),
            close="}",
            empty_set="new SortedSet<object>()",
            preamble_lines=("using System.Collections.Generic;",),
            set_opener_template="new SortedSet<{type_name}> {{",
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

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        VAR = "var"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DICTIONARY = _CSharpDictSpec(
            opener_template="new Dictionary<string, {type_name}> {{",
            fallback="new Dictionary<string, object> {",
        )
        SORTED_DICTIONARY = _CSharpDictSpec(
            opener_template="new SortedDictionary<string, {type_name}> {{",
            fallback="new SortedDictionary<string, object> {",
        )

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
        date_format: DateFormats = DateFormats.CSHARP,
        datetime_format: DatetimeFormats = DatetimeFormats.CSHARP,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.TUPLE,
        set_format: SetFormats = SetFormats.HASH_SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.VAR,
        dict_format: DictFormats = DictFormats.DICTIONARY,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
    ) -> None:
        """Initialize CSharp language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "(object?)null"
        self.true_literal = "true"
        self.false_literal = "false"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        csharp_dict_entry = dict_entry_with_template(
            template="[{key}] = {value}",
            format_value=passthrough_sequence_entry,
        )

        date_tp = date_format.value.type_produced
        dt_tp = datetime_format.value.type_produced
        cfg = self._opener_config
        openers = cfg.build(
            date_type=cfg.type_name(py_type=date_tp),
            datetime_type=cfg.type_name(py_type=dt_tp),
            set_opener_template=set_format.value.set_opener_template or None,
        )
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=typed_set_open(
                type_to_opener=openers.set,
                fallback=set_format.value.set_open([]),
            ),
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            typed_sequence_open(
                type_to_opener=openers.seq,
                fallback=fmt.typed_opener_fallback,
            )
            if fmt.typed_opener_fallback is not None
            else fmt.sequence_open
        )
        dict_spec: _CSharpDictSpec = dict_format.value
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=cfg.element_to_type(
                        date_type=cfg.type_name(py_type=date_tp),
                        datetime_type=cfg.type_name(py_type=dt_tp),
                    ),
                    opener_template=dict_spec.opener_template,
                ),
                fallback=dict_spec.fallback,
            ),
            close="}",
            format_entry=csharp_dict_entry,
            empty_dict=None,
            preamble_lines=("using System.Collections.Generic;",),
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
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
                open_str="new Dictionary<string, object> {",
                close="}",
                preamble_lines=("using System.Collections.Generic;",),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            csharp_dict_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            variable_formatter(template="var {name} = {value};")
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value};")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
            )
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
