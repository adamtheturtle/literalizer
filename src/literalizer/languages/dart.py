"""Dart language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import (
    TypedOpenerConfig,
    TypeOpeners,
    fixed_dict_open,
    fixed_sequence_open,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    date_iso_formatter,
    datetime_iso_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import set_format_factory
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import format_integer_hex
from literalizer._formatters.format_strings import (
    format_string_backslash_dollar,
    format_string_backslash_dollar_single,
)
from literalizer._language import (
    CallStyleConfig,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value


@beartype
def _dart_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    data: Value,
    *,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
    sequence_is_tuple: bool,
) -> str:
    """Derive a Dart type annotation from *data*."""
    recurse = functools.partial(
        _dart_type_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
        sequence_is_tuple=sequence_is_tuple,
    )
    match data:
        case bool():
            return "bool"
        case int():
            return "int"
        case float():
            return "double"
        case str():
            return "String"
        case bytes():
            return "String"
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case None:
            return "Null"
        case dict():
            if not data:
                return (
                    f"Map<{default_dict_key_type}, {default_dict_value_type}>"
                )
            val_types = [recurse(data=v) for v in data.values()]
            unique = list(dict.fromkeys(val_types))
            val_type = unique[0] if len(unique) == 1 else "dynamic"
            return f"Map<{default_dict_key_type}, {val_type}>"
        case set():
            if not data:
                return f"Set<{default_set_element_type}>"
            elem_types = sorted({recurse(data=e) for e in data})
            elem_type = elem_types[0] if len(elem_types) == 1 else "dynamic"
            return f"Set<{elem_type}>"
        case list():
            if not data:
                if sequence_is_tuple:
                    return "()"
                return "List<dynamic>"
            if sequence_is_tuple:
                elem_types = [recurse(data=e) for e in data]
                return f"({', '.join(elem_types)},)"
            elem_types = [recurse(data=e) for e in data]
            unique = list(dict.fromkeys(elem_types))
            elem_type = unique[0] if len(unique) == 1 else "dynamic"
            return f"List<{elem_type}>"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _format_dart_typed_declaration(
    name: str,
    value: str,
    data: Value,
    *,
    keyword: str,
    date_hint: str,
    datetime_hint: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
    sequence_is_tuple: bool,
) -> str:
    """Format a Dart variable declaration with an explicit type."""
    hint = _dart_type_hint(
        data=data,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
        sequence_is_tuple=sequence_is_tuple,
    )
    return f"{keyword}{hint} {name} = {value};"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Dart(metaclass=LanguageCls):
    """Dart language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.DART`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15")``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.DART`` — ``DateTime.parse(...)`` call,
              e.g. ``DateTime.parse("2024-01-15T12:30:00")``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".dart"
    pygments_name = "dart"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    _opener_config = TypedOpenerConfig(
        str_type="String",
        bool_type="bool",
        int_type="int",
        float_type="double",
        mixed_numeric_type="double",
        bytes_type="String",
        date_type="DateTime",
        datetime_type="DateTime",
        list_template="List<{inner}>",
        sequence_opener_template="<{type_name}>[",
        dict_opener_template="<{key_type}, {type_name}>{{",
        set_opener_template="<{type_name}>{{",
        dict_type_template="Map<{key_type}, {inner}>",
        fallback_value_type="dynamic",
    )

    class DateFormats(enum.Enum):
        """Date formatting options for Dart."""

        DART = DateFormatConfig(
            formatter=date_iso_formatter(
                template='DateTime.parse("{iso}")',
            ),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Dart."""

        DART = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(
                template='DateTime.parse("{iso}")',
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
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Dart."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback="[",
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            supports_trailing_comma=True,
            empty_sequence="()",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Dart."""

        SET = enum.member(
            value=set_format_factory(
                open_template="{{",
                close="}}",
                empty_template="<{type}>{{}}",
                preamble_lines=(),
                set_opener_template="",
                coerce_mixed_to_str=False,
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

        FINAL = DeclarationStyleConfig(
            formatter=variable_formatter(template="final {name} = {value};"),
            supports_redefinition=False,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_formatter(template="var {name} = {value};"),
            supports_redefinition=False,
        )
        CONST = DeclarationStyleConfig(
            formatter=variable_formatter(template="const {name} = {value};"),
            supports_redefinition=False,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="double.infinity",
        negative_infinity="double.negativeInfinity",
        nan="double.nan",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash_dollar)
        SINGLE = enum.member(value=format_string_backslash_dollar_single)

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
        ALWAYS = enum.auto()

        def formatter(
            self,
            *,
            auto_formatter: Callable[[str, str, Value], str],
            keyword: str,
            date_hint: str,
            datetime_hint: str,
            default_set_element_type: str,
            default_dict_key_type: str,
            default_dict_value_type: str,
            sequence_is_tuple: bool,
        ) -> Callable[[str, str, Value], str]:
            """Return the variable declaration formatter."""
            if self is type(self).AUTO:
                return auto_formatter
            return functools.partial(
                _format_dart_typed_declaration,
                keyword=keyword,
                date_hint=date_hint,
                datetime_hint=datetime_hint,
                default_set_element_type=default_set_element_type,
                default_dict_key_type=default_dict_key_type,
                default_dict_value_type=default_dict_value_type,
                sequence_is_tuple=sequence_is_tuple,
            )

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
        """Dart call style options."""

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

    date_format: DateFormats = DateFormats.DART
    datetime_format: DatetimeFormats = DatetimeFormats.DART
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "dynamic"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "dynamic"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.FINAL
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.SEMICOLON
    indent: str = "    "

    null_literal: ClassVar[str] = "null"
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
    call_style_config: ClassVar[CallStyleConfig | None] = None

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
        return dict_entry_with_separator(
            separator=": ", format_value=passthrough_sequence_entry
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
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[str], str]:
        """Transform a dotted call target."""
        return identity_call_target

    @cached_property
    def _date_tp(self) -> type:
        """Python type produced by the chosen date format."""
        return self.date_format.value.type_produced

    @cached_property
    def _dt_tp(self) -> type:
        """Python type produced by the chosen datetime format."""
        return self.datetime_format.value.type_produced

    @cached_property
    def _openers(self) -> TypeOpeners:
        """Typed openers built from the opener config."""
        cfg = self._opener_config
        return cfg.build(
            date_type=cfg.type_name(py_type=self._date_tp),
            datetime_type=cfg.type_name(py_type=self._dt_tp),
            set_opener_template=None,
            narrow_dict_values=True,
            dict_key_type=self.default_dict_key_type,
        )

    @cached_property
    def _dart_keyword(self) -> str:
        """Keyword prefix derived from the declaration style."""
        kw = self.declaration_style.name.lower()
        return "" if kw == "var" else f"{kw} "

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format(
            default_type=self.default_set_element_type,
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        fmt = self.sequence_format.value
        if fmt.typed_opener_fallback is not None:
            return typed_collection_open(
                type_to_opener=self._openers.seq,
                fallback=fmt.typed_opener_fallback,
            )
        return fmt.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=self._openers.dict,
                fallback=(
                    f"<{self.default_dict_key_type}, "
                    f"{self.default_dict_value_type}>{{"
                ),
            ),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
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
        """Callable that formats an int value as a literal."""
        return self.integer_format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_dict_open(open_str="{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration."""
        return self.variable_type_hints.formatter(
            auto_formatter=self.declaration_style.value.formatter,
            keyword=self._dart_keyword,
            date_hint=(
                "String"
                if self.date_format.value.type_produced is str
                else "DateTime"
            ),
            datetime_hint=(
                "String"
                if self.datetime_format.value.type_produced is str
                else "DateTime"
            ),
            default_set_element_type=self.default_set_element_type,
            default_dict_key_type=self.default_dict_key_type,
            default_dict_value_type=self.default_dict_value_type,
            sequence_is_tuple=(self.sequence_format.name == "TUPLE"),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Dart needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Dart needs none)."""
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
