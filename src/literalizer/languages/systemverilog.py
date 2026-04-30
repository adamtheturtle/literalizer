"""SystemVerilog language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    CallStyle,
    CallSupport,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value

_INT32_MIN = -(2**31)
_INT32_MAX = 2**31 - 1


@beartype
def _format_integer_hex_sv(value: int) -> str:
    """Format an integer as a SystemVerilog hexadecimal literal."""
    bits = 64
    if value < 0:
        return f"-{bits}'h{abs(value):x}"
    return f"{bits}'h{value:x}"


@beartype
def _format_integer_decimal_sv(value: int) -> str:
    """Format an integer as a SystemVerilog decimal literal.

    Values outside 32-bit signed range get an explicit 64-bit signed
    width prefix; smaller values are emitted as bare decimals.
    """
    if _INT32_MIN <= value <= _INT32_MAX:
        return str(object=value)
    bits = 64
    if value < 0:
        return f"-{bits}'sd{abs(value)}"
    return f"{bits}'sd{value}"


@beartype
def _escape_nested(text: str) -> str:
    """Escape a nested collection literal for embedding as a string."""
    return text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")


@beartype
def _format_sv_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in a named ``_VVal`` struct literal."""
    match original:
        case str() | bytes() | datetime.date():
            return f"_VVal'{{tag: _VVAL_STR, i: 0, r: 0.0, s: {formatted}}}"
        case bool():
            return formatted
        case int():
            return f'_VVal\'{{tag: _VVAL_INT, i: {formatted}, r: 0.0, s: ""}}'
        case float():
            return f'_VVal\'{{tag: _VVAL_REAL, i: 0, r: {formatted}, s: ""}}'
        case list() | dict() | set():
            escaped = _escape_nested(text=formatted)
            return f'_VVal\'{{tag: _VVAL_STR, i: 0, r: 0.0, s: "{escaped}"}}'
        case _:
            return formatted


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a SystemVerilog variable declaration."""
    match data:
        case list() | set():
            return f"static _VVal {name}[] = {value};"
        case dict():
            return f"static _VKV {name}[] = {value};"
        case _:
            wrapped = _format_sv_entry(original=data, formatted=value)
            return f"static _VVal {name} = {wrapped};"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format a SystemVerilog variable assignment."""
    if isinstance(data, (list, set, dict)):
        return f"{name} = {value};"
    wrapped = _format_sv_entry(original=data, formatted=value)
    return f"{name} = {wrapped};"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class SystemVerilog(metaclass=LanguageCls):
    """SystemVerilog language specification."""

    module_name: str = "Module"

    extension = ".sv"
    pygments_name = "systemverilog"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for SystemVerilog."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for SystemVerilog."""

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
        """Sequence type options for SystemVerilog."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="'{"),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
            empty_sequence="'{}",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for SystemVerilog."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="'{"),
            close="}",
            empty_set="'{}",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
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

        TYPED = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
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
        positive_infinity="$bitstoreal(64'h7FF0000000000000)",
        negative_infinity="$bitstoreal(64'hFFF0000000000000)",
        nan="$bitstoreal(64'h7FF8000000000000)",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=_format_integer_decimal_sv)
        HEX = enum.member(value=_format_integer_hex_sv)

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

        DOUBLE = enum.auto()

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

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
        """SystemVerilog call style options."""

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
        """Version options for SystemVerilog."""

        IEEE_1800_2017 = "IEEE 1800-2017"

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a SystemVerilog declaration in a module."""
        del variable_name
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        return (
            f"module {self.module_name};\n"
            f"initial begin\n{content}\nend\nendmodule"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap SystemVerilog declaration + assignment in a module."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.TYPED
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    line_ending: LineEndings = LineEndings.SEMICOLON
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.IEEE_1800_2017
    indent: str = "    "

    null_literal: ClassVar[str] = (
        '_VVal\'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""}'
    )
    true_literal: ClassVar[str] = (
        '_VVal\'{tag: _VVAL_INT, i: 1, r: 0.0, s: ""}'
    )
    false_literal: ClassVar[str] = (
        '_VVal\'{tag: _VVAL_INT, i: 0, r: 0.0, s: ""}'
    )
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = (
        "typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;",
        "typedef struct {",
        "    _VTag tag;",
        "    longint i;",
        "    real r;",
        "    string s;",
        "} _VVal;",
        "typedef struct {",
        "    string k;",
        "    _VVal v;",
        "} _VKV;",
    )
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()
    call_style_config: ClassVar[CallStyle | CallSupport] = (
        CallSupport.NOT_IMPLEMENTED_BY_TOOL
    )

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return _format_sv_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_sv_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return _format_variable_assignment

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
        return no_call_stub

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

    scalar_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}
    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def _vkv_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter producing ``_VKV`` struct
        literals.
        """
        return dict_entry_with_template(
            template="_VKV'{{k: {key}, v: {value}}}",
            format_value=_format_sv_entry,
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str="'{"),
            close="}",
            format_entry=self._vkv_entry,
            empty_dict="'{}",
            preamble_lines=(),
            narrowed_open=None,
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
        return make_overflow_fallback_formatter(
            base=self.integer_format,
            fallback=raise_for_unrepresentable_int(
                language_name="SystemVerilog",
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
            ordered_map_open=fixed_open(open_str="'{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._vkv_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
