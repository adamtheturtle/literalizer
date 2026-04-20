"""C# language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, cast

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    TypeOpeners,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    ordered_map_format_factory,
    sequence_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MIN,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_verbatim_csharp,
)
from literalizer._language import (
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    KeywordCallStyle,
    LanguageCls,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value


@dataclasses.dataclass(frozen=True)
class _CSharpDictSpec:
    """Per-format dict config pieces resolved at init time."""

    opener_template: str


def _csharp_call_stub(
    name: str,
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return C# stub declarations for a call name."""
    parts = name.split(sep=".")
    if len(parts) == 1:
        return (f"dynamic {parts[0]}(dynamic a) => null;",)
    root = parts[0]
    return (f"dynamic {root} = new System.Dynamic.ExpandoObject();",)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
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
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

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
        dict_opener_template="new Dictionary<{key_type}, {type_name}> {{",
        set_opener_template="new HashSet<{type_name}> {{",
        dict_type_template="Dictionary<{key_type}, {inner}>",
        fallback_value_type="object",
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
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for C#."""

        TUPLE = enum.member(
            value=sequence_format_factory(
                open_template="(",
                close=")",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=False,
                empty_template="ValueTuple.Create()",
                preamble_lines=("using System;",),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        ARRAY = enum.member(
            value=sequence_format_factory(
                open_template="new {type}[] {{",
                close="}",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                supports_trailing_comma=True,
                empty_template="Array.Empty<{type}>()",
                preamble_lines=("using System.Collections.Generic;",),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=("new {type}[] {{"),
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

    class SetFormats(enum.Enum):
        """Set type options for C#."""

        HASH_SET = enum.member(
            value=set_format_factory(
                open_template="new HashSet<{type}> {{",
                close="}}",
                empty_template="new HashSet<{type}>()",
                preamble_lines=("using System.Collections.Generic;",),
                set_opener_template="",
                supports_heterogeneity=True,
            )
        )
        SORTED_SET = enum.member(
            value=set_format_factory(
                open_template="new SortedSet<{type}> {{",
                close="}}",
                empty_template="new SortedSet<{type}>()",
                preamble_lines=("using System.Collections.Generic;",),
                set_opener_template="new SortedSet<{type_name}> {{",
                supports_heterogeneity=True,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

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

        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value};"),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DICTIONARY = _CSharpDictSpec(
            opener_template="new Dictionary<{key_type}, {type_name}> {{",
        )
        SORTED_DICTIONARY = _CSharpDictSpec(
            opener_template="new SortedDictionary<{key_type}, {type_name}> {{",
        )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="double.PositiveInfinity",
        negative_infinity="double.NegativeInfinity",
        nan="double.NaN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

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

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        VERBATIM = enum.member(value=format_string_verbatim_csharp)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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

        AUTO = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """CSharp call style options."""

        POSITIONAL = PositionalCallStyle()
        NAMED = KeywordCallStyle(separator=": ")

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file (no-op)."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.CSHARP
    datetime_format: DatetimeFormats = DatetimeFormats.CSHARP
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.TUPLE
    set_format: SetFormats = SetFormats.HASH_SET
    default_set_element_type: str = "object"
    default_sequence_element_type: str = "object"
    default_dict_key_type: str = "string"
    default_dict_value_type: str = "object"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAR
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DICTIONARY
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.NO
    line_ending: LineEndings = LineEndings.SEMICOLON
    call_style: CallStyles = CallStyles.POSITIONAL
    indent: str = "    "

    null_literal: ClassVar[str] = "(object?)null"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value};")

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry."""
        return dict_entry_with_template(
            template="[{key}] = {value}",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _csharp_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def _date_tp(self) -> type:
        """Python type produced by the chosen date format."""
        return self.date_format.value.type_produced

    @cached_property
    def _dt_tp(self) -> type:
        """Python type produced by the chosen datetime format."""
        return self.datetime_format.value.type_produced

    @cached_property
    def _base_set_format_config(self) -> SetFormatConfig:
        """Base set format config before typed-opener application."""
        return self.set_format(
            default_type=self.default_set_element_type,
        )

    @cached_property
    def _openers(self) -> TypeOpeners:
        """Typed openers built from the opener config."""
        cfg = self._opener_config
        return cfg.build(
            date_type=cfg.type_name(py_type=self._date_tp),
            datetime_type=cfg.type_name(py_type=self._dt_tp),
            set_opener_template=(
                self._base_set_format_config.set_opener_template or None
            ),
            narrow_dict_values=False,
            dict_key_type=self.default_dict_key_type,
        )

    @cached_property
    def _resolved_dict_opener(self) -> str:
        """Opener template with the key type resolved."""
        return self.dict_format.value.opener_template.replace(
            "{key_type}",
            self.default_dict_key_type,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format(
            default_type=self.default_sequence_element_type,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format (with typed opener)."""
        base = self._base_set_format_config
        return base.with_typed_opener(
            type_to_opener=self._openers.set,
            fallback=base.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        fmt = self.sequence_format_config
        if fmt.typed_opener_fallback is not None:
            return typed_collection_open(
                type_to_opener=self._openers.seq,
                fallback=fmt.typed_opener_fallback,
            )
        return fmt.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        cfg = self._opener_config
        resolved = self._resolved_dict_opener
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=cfg.element_to_type(
                        list_template=None,
                        date_type=cfg.type_name(py_type=self._date_tp),
                        datetime_type=cfg.type_name(py_type=self._dt_tp),
                        enable_dict_type=False,
                        dict_key_type=self.default_dict_key_type,
                    ),
                    opener_template=resolved,
                ),
                fallback=resolved.format(
                    type_name=self.default_dict_value_type,
                ),
            ),
            close="}",
            format_entry=dict_entry_with_template(
                template="[{key}] = {value}",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=("using System.Collections.Generic;",),
            narrowed_open=None,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self.bytes_format

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        return self.datetime_format

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self.string_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal.

        Positive values above ``long.MaxValue`` are accepted as bare
        literals because C# infers ``ulong`` for literals without a
        type suffix up to ``ulong.MaxValue``.  Values below
        ``long.MinValue`` have no clean literal form (unary minus
        cannot apply to ``ulong``), so they raise
        ``UnrepresentableIntegerError``.
        """
        base = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=raise_for_unrepresentable_int(language_name="C#"),
            min_value=I64_MIN,
            max_value=2**64 - 1,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return ordered_map_format_factory(
            open_template="new Dictionary<{key_type}, {type}> {{",
            close="}",
            preamble_lines=("using System.Collections.Generic;",),
        )(
            self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (C# needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

    @cached_property
    def call_style_config(self) -> CallStyle | None:
        """Configuration for the chosen call style."""
        return cast("CallStyle", self.call_style.value)
