"""Go language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_type_to_opener,
    typed_collection_open,
    typed_dict_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import set_format_factory
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    make_int64_cast_formatter,
    make_overflow_fallback_formatter,
    make_unsigned_overflow_fallback,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value


@beartype
def _format_go_uint64_positive(value: int) -> str:
    """Format a positive value outside signed 64-bit range as a Go
    ``uint64`` typed conversion.

    A Go integer constant without an explicit type can hold arbitrary
    size, but its default promotion to ``int`` overflows.  Wrapping in
    ``uint64(...)`` forces a typed conversion and accepts values up to
    ``math.MaxUint64``.
    """
    return f"uint64({value})"


@beartype
def _go_call_preamble_stub(
    parts: Sequence[str], _params: Sequence[str], _stub_return: StubReturn, /
) -> tuple[str, ...]:
    """Return Go stub declarations for a call name."""
    if len(parts) == 1:
        return (f"func {parts[0]}(args ...any) any {{ return nil }}",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root}Type_"
        return (
            f"type {type_name} struct{{}}",
            f"func ({type_name}) {method}(args ...any) any {{ return nil }}",
            f"var {root} {type_name}",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1]}Type_"
    lines.append(f"type {inner_type} struct{{}}")
    lines.append(
        f"func ({inner_type}) {method}(args ...any) any {{ return nil }}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i]}Type_"
        field = fields[i + 1]
        lines.append(f"type {curr_type} struct{{ {field} {prev_type} }}")
        prev_type = curr_type
    root_type = f"{root}Type_"
    lines.append(f"type {root_type} struct{{ {fields[0]} {prev_type} }}")
    lines.append(f"var {root} {root_type}")
    return tuple(lines)


@beartype
def _go_month_name(month: int) -> str:
    """Return the Go ``time.Month`` constant for a 1-based month
    number.
    """
    return (
        "time.January",
        "time.February",
        "time.March",
        "time.April",
        "time.May",
        "time.June",
        "time.July",
        "time.August",
        "time.September",
        "time.October",
        "time.November",
        "time.December",
    )[month - 1]


@beartype
def _format_date_go(value: datetime.date) -> str:
    """Format a date as a Go ``time.Date(...)`` call."""
    month = _go_month_name(month=value.month)
    return (
        f"time.Date({value.year}, {month}, {value.day}, 0, 0, 0, 0, time.UTC)"
    )


@beartype
def _format_datetime_go(value: datetime.datetime) -> str:
    """Format a datetime as a Go ``time.Date(...)`` call."""
    month = _go_month_name(month=value.month)
    nanoseconds = value.microsecond * 1000
    return (
        f"time.Date({value.year}, {month}, {value.day}, "
        f"{value.hour}, {value.minute}, {value.second}, "
        f"{nanoseconds}, time.UTC)"
    )


@beartype
def _format_go_set_entry(_original: Value, item: str) -> str:
    """Format a Go set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple": struct{}{}``.
    """
    return f"{item}: struct{{}}{{}}"


@beartype
def _apply_go_nil_safe_declaration(
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> str:
    """Format a Go variable declaration, guarding top-level
    ``nil``.
    """
    if data is None:
        return f"var {name} any = {value}"
    return base_formatter(name, value, data, modifiers)


@beartype
def _nil_safe_declaration(
    base_formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Wrap *base_formatter* so top-level ``nil`` gets a typed form.

    Go cannot infer a type from ``nil`` alone, so
    ``my_data := nil`` and ``var my_data = nil`` both fail to compile.
    Emit ``var {name} any = nil`` when the value is ``None``.
    """

    def _format(
        name: str,
        value: str,
        data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_go_nil_safe_declaration(
            name=name,
            value=value,
            data=data,
            modifiers=modifiers,
            base_formatter=base_formatter,
        )

    return _format


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Go(metaclass=LanguageCls):
    """Go language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 0, 0, 0, 0,
              time.UTC)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.GO`` — ``time.Date`` call,
              e.g. ``time.Date(2024, time.January, 15, 12, 30, 0, 0,
              time.UTC)``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".go"
    pygments_name = "go"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = True
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_commented_dict_call_args = True
    supports_module_name = False
    supports_call_refs_in_dict_literals = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Go."""

        GO = DateFormatConfig(
            formatter=_format_date_go,
            preamble_lines=('import "time"',),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Go."""

        GO = DatetimeFormatConfig(
            formatter=_format_datetime_go,
            preamble_lines=('import "time"',),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
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
        """Sequence type options for Go."""

        SLICE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="[]any{"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Go."""

        SET = enum.member(
            value=set_format_factory(
                open_template="map[{type}]struct{{}}{{",
                close="}}",
                empty_template=None,
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
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

        SHORT = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} := {value}"
            ),
            supports_redefinition=True,
        )
        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
            ),
            supports_redefinition=True,
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
        positive_infinity="math.Inf(1)",
        negative_infinity="math.Inf(-1)",
        nan="math.NaN()",
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

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()
        AUTO = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()
        UNDERSCORE = enum.auto()

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)

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

        SEMICOLON = ";"
        NONE = ""

        @property
        def statement_terminator(self) -> str:
            """Terminator appended to complete call statements."""
            return self.value

        def wrap_declaration_formatter(
            self,
            formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str],
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Wrap a declaration formatter with this line ending."""
            if not self.value:
                return formatter

            def with_semicolon(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Format with a trailing semicolon."""
                return formatter(name, value, data, modifiers) + self.value

            return with_semicolon

        def wrap_assignment_formatter(
            self,
            formatter: Callable[[str, str, Value], str],
        ) -> Callable[[str, str, Value], str]:
            """Wrap an assignment formatter with this line ending."""
            if not self.value:
                return formatter

            def with_semicolon(
                name: str,
                value: str,
                data: Value,
            ) -> str:
                """Format with a trailing semicolon."""
                return formatter(name, value, data) + self.value

            return with_semicolon

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Go call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options — this language only
        supports raising.
        """

        ERROR = NO_HETEROGENEOUS_BEHAVIOR

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for Go."""

        V1_18 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Go declaration in ``func main()``."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = f"\n_ = {variable_name}" if variable_name else ""
        return f"\nfunc main() {{\n{content}{use_line}\n}}"

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Go declaration + assignment in ``func main()``."""
        return Go.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.GO
    datetime_format: DatetimeFormats = DatetimeFormats.GO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.SLICE
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "any"
    default_sequence_element_type: str = "any"
    default_dict_key_type: str = "string"
    default_dict_value_type: str = "any"
    default_ordered_map_value_type: str = "any"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.SHORT
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
    line_ending: LineEndings = LineEndings.NONE
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.V1_18
    indent: str = "\t"

    null_literal: ClassVar[str] = "nil"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    static_preamble: ClassVar[Sequence[str]] = ("package main",)
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ('import "math"',)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_go_set_entry

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return _go_call_preamble_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def _init_element_to_type(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Element-to-type resolver for the configured Go types."""
        _type_names: dict[type, str] = {
            datetime.date: "time.Time",
            datetime.datetime: "time.Time",
            str: "string",
        }
        suffix_is_auto = self.numeric_literal_suffix.name == "AUTO"
        go_int_type = "int64" if suffix_is_auto else "int"
        _type_names[int] = go_int_type
        date_type = _type_names.get(self.date_format.value.type_produced)
        datetime_type = _type_names.get(
            self.datetime_format.value.type_produced,
        )
        return make_element_to_type(
            str_type="string",
            bool_type="bool",
            int_type=go_int_type,
            float_type="float64",
            mixed_numeric_type="float64",
            bytes_type="string",
            date_type=date_type,
            datetime_type=datetime_type,
            list_template="[]{inner}",
            dict_type_template=f"map[{self.default_dict_key_type}]{{inner}}",
            fallback_value_type="any",
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        base_set_config: SetFormatConfig = self.set_format(
            default_type=self.default_set_element_type,
        )
        return base_set_config.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=self._init_element_to_type,
                opener_template="map[{type_name}]struct{{}}{{",
            ),
            fallback=base_set_config.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return typed_collection_open(
            type_to_opener=make_type_to_opener(
                element_to_type=self._init_element_to_type,
                opener_template="[]{type_name}{{",
            ),
            fallback=f"[]{self.default_sequence_element_type}{{",
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=typed_dict_open(
                type_to_opener=make_type_to_opener(
                    element_to_type=self._init_element_to_type,
                    opener_template=f"map[{self.default_dict_key_type}]{{type_name}}{{{{",
                ),
                fallback=f"map[{self.default_dict_key_type}]{self.default_dict_value_type}{{",
            ),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open="{",
            supports_trailing_comma=True,
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
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        base_int_formatter = self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )
        suffix_is_auto = self.numeric_literal_suffix.name == "AUTO"
        base: Callable[[int], str] = (
            make_int64_cast_formatter(base=base_int_formatter)
            if suffix_is_auto
            else base_int_formatter
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_go_uint64_positive,
                language_name="Go",
            ),
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"[][2]{self.default_ordered_map_value_type}{{"
            ),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return braced_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def statement_terminator(self) -> str:
        """String appended to each call expression."""
        return self.line_ending.statement_terminator

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.line_ending.wrap_declaration_formatter(
            formatter=_nil_safe_declaration(
                base_formatter=self.declaration_style.value.formatter,
            ),
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return self.line_ending.wrap_assignment_formatter(
            formatter=variable_formatter(template="{name} = {value}"),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
        )

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Go needs none)."""
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
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value
