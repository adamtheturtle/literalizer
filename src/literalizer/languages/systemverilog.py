"""SystemVerilog language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
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
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
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
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value
from literalizer.exceptions import CallArgNotSupportedError

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
        case bool():
            return formatted
        case datetime.datetime() if formatted.lstrip("-").isdigit():
            payload = f'_VVAL_INT, i: {formatted}, r: 0.0, s: ""'
        case int():
            payload = f'_VVAL_INT, i: {formatted}, r: 0.0, s: ""'
        case float():
            payload = f'_VVAL_REAL, i: 0, r: {formatted}, s: ""'
        case str() | bytes() | datetime.date():
            payload = f"_VVAL_STR, i: 0, r: 0.0, s: {formatted}"
        case list() | dict() | set():
            escaped = _escape_nested(text=formatted)
            payload = f'_VVAL_STR, i: 0, r: 0.0, s: "{escaped}"'
        case _:
            return formatted
    return f"_VVal'{{tag: {payload}}}"


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


_SV_NULL = '_VVal\'{tag: _VVAL_STR, i: 0, r: 0.0, s: ""}'


@beartype
def _sv_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    indent: str,
) -> tuple[str, ...]:
    """Return SystemVerilog stub declarations for a call expression.

    VOID stubs emit a ``task``; VALUE stubs emit a ``function`` that
    returns ``_VVal`` via the null literal.  Dotted names generate
    nested class declarations with a module-level instance variable.
    """
    param_str = ", ".join(f"input _VVal {p}" for p in params)

    if len(parts) == 1:
        name = parts[0]
        if stub_return is StubReturn.VOID:
            return (f"task {name}({param_str}); endtask",)
        return (
            f"function _VVal {name}({param_str});\n"
            f"{indent}{name} = {_SV_NULL};\n"
            f"endfunction",
        )

    method = parts[-1]
    root = parts[0]
    fields = list(parts[1:-1])

    if stub_return is StubReturn.VOID:
        method_decl = f"{indent}task {method}({param_str}); endtask"
    else:
        method_decl = (
            f"{indent}function _VVal {method}({param_str});\n"
            f"{indent}{indent}{method} = {_SV_NULL};\n"
            f"{indent}endfunction"
        )

    if not fields:
        type_name = f"{root.title()}Type_"
        return (
            f"class {type_name};\n{method_decl}\nendclass",
            f"{type_name} {root} = new();",
        )

    lines: list[str] = []
    inner_type = f"{fields[-1].title()}Type_"
    lines.append(f"class {inner_type};\n{method_decl}\nendclass")
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i].title()}Type_"
        lines.append(
            f"class {curr_type};\n"
            f"{indent}{prev_type} {fields[i + 1]} = new();\n"
            f"endclass"
        )
        prev_type = curr_type
    root_type = f"{root.title()}Type_"
    lines.append(
        f"class {root_type};\n"
        f"{indent}{prev_type} {fields[0]} = new();\n"
        f"endclass"
    )
    lines.append(f"{root_type} {root} = new();")
    return tuple(lines)


@beartype
def _format_systemverilog_call_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a SystemVerilog declaration binding a call result.

    A literal binding wraps the right-hand side in a named ``_VVal``
    (or ``_VKV``) struct literal derived from the parsed value's runtime
    type.  That is wrong for a call, whose return type is opaque to the
    renderer and is never a ``_VVal`` struct-literal projection.

    SystemVerilog declarations are typed and have no inference, so the
    binding still needs an explicit declared type.  No caller-supplied
    return-type hint is required: every generated SystemVerilog call
    stub that yields a value returns the universal tagged ``_VVal``
    struct (a ``StubReturn.VALUE`` stub is ``function _VVal name(...)``),
    so the call result's static type is always ``_VVal`` -- exactly the
    type a SystemVerilog scalar literal binding already declares.  The
    only call-vs-literal difference is dropping the value-wrapping
    struct literal, so the call result is bound directly with a plain
    ``static _VVal`` declaration regardless of the source data type.
    """
    return f"static _VVal {name} = {value};"


@beartype
def _format_systemverilog_call_assignment(
    name: str,
    value: str,
    _data: Value,
) -> str:
    """Format a SystemVerilog reassignment binding a call result.

    The call-expression counterpart of
    :func:`_format_systemverilog_call_declaration`; the variable is
    already declared ``_VVal``, so the call result is assigned directly
    with no ``_VVal`` struct-literal wrapping.
    """
    return f"{name} = {value};"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class SystemVerilog(metaclass=LanguageCls):
    """SystemVerilog language specification."""

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    module_name: str = "Module"

    leading_preamble = no_leading_preamble
    extension = ".sv"
    pygments_name = "systemverilog"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    allows_empty_call_parens = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = False
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

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

        NEVER = enum.auto()
        SAFE = enum.auto()

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    integer_width_strategies = BareIntegerWidthStrategies
    numeric_literal_suffixes = NumericLiteralSuffixes
    numeric_separators = NumericSeparators
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """SystemVerilog call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

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

        IEEE_1800_2017 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    validate_spec_for_data = no_validate_spec_for_data

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a SystemVerilog declaration in a module.

        In call mode (``variable_name`` is empty), *body_preamble* holds
        task/function stubs that go at module scope outside
        ``initial begin``.  In declaration mode, *body_preamble* is
        prepended inside ``initial begin`` as usual.
        """
        if variable_name:
            content = prepend_body_preamble(
                content=content,
                body_preamble=body_preamble,
            )
            stubs_block = ""
        else:
            stubs_block = "".join(f"{s}\n" for s in body_preamble)
        return (
            f"module {self.module_name};\n"
            f"{stubs_block}"
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

    def wrap_call_variable_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a call-result variable binding in a SystemVerilog module.

        In :meth:`wrap_in_file`'s ``variable_name`` branch,
        *body_preamble* is prepended inside ``initial begin`` (where,
        for a literal binding, it is data-dependent preamble).  For a
        call binding
        those lines are instead the module-scope ``task``/``function``/
        ``class`` stubs emitted by :func:`_sv_call_stub`, and a
        ``function`` declared inside ``initial begin`` is illegal.  Place
        the stubs at module scope (matching the call-without-binding
        branch of :meth:`wrap_in_file`) while keeping the
        ``static _VVal my_data = make_widget(...);`` binding inside
        ``initial begin``.
        """
        del variable_name
        stubs_block = "".join(f"{s}\n" for s in body_preamble)
        return (
            f"module {self.module_name};\n"
            f"{stubs_block}"
            f"initial begin\n{content}\nend\nendmodule"
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.TYPED
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.DEFAULT
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    integer_width_strategy: BareIntegerWidthStrategies = (
        BareIntegerWidthStrategies.BARE
    )
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    # The `Check SystemVerilog syntax` step in
    # `.github/workflows/lint.yml` passes `verilator --language 1800-2017`,
    # matching this default (`IEEE_1800_2017` is the IEEE 1800-2017
    # SystemVerilog standard). Keep the two in sync.
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
        (
            "typedef enum int {_VVAL_INT, _VVAL_REAL, _VVAL_STR} _VTag;\n"
            "typedef struct {\n"
            "    _VTag tag;\n"
            "    longint i;\n"
            "    real r;\n"
            "    string s;\n"
            "} _VVal;\n"
            "typedef struct {\n"
            "    string k;\n"
            "    _VVal v;\n"
            "} _VKV;"
        ),
    )
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

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
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for call rendering."""
        return self.data_dependent_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        indent = self.indent
        return functools.partial(_sv_call_stub, indent=indent)

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each call argument in the ``_VVal`` struct literal."""
        return _format_sv_entry

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax, rejecting scalar refs.

        SystemVerilog's variable declarations key the type off the
        marker mapping shape (``_VKV name[]``), so a top-level ref
        pointing to a scalar produces a typed declaration that does
        not match the referenced ``_VVal`` variable.  Refuse those
        cases so the renderer fails fast instead of emitting code that
        the SystemVerilog compiler rejects with "types are not
        assignment compatible".
        """

        def _sv_format_ref_identifier(
            name: str, value: Value | None, /
        ) -> str:
            """Reject scalar refs; emit any other ref unchanged."""
            if value is not None and not isinstance(value, (list, dict, set)):
                raise CallArgNotSupportedError(
                    language_name="SystemVerilog",
                    reason=(
                        f"SystemVerilog cannot reference a scalar value "
                        f"behind a ``$ref`` (got {name!r}); the variable "
                        f"declaration shape is keyed off the ref marker "
                        f"and does not match the scalar's ``_VVal`` type."
                    ),
                )
            return name

        return _sv_format_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Emit a call-argument ``$ref`` as the bare identifier.

        Call arguments have their type fixed by the function signature,
        so the scalar/dict shape mismatch that affects
        :attr:`format_call_ref_identifier` (top-level ``$ref`` in
        :func:`literalize`) does not arise here.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.

        Delegates to :data:`never_inhibits_consuming_form`.  Languages
        whose consume operator rejects certain value types (notably
        the Mojo ``^`` on register-trivial scalars) override this.
        """
        return never_inhibits_consuming_form

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
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

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
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        A literal binding wraps the right-hand side in a named ``_VVal``
        struct literal derived from the parsed value's runtime type; a
        call's return type is opaque to the renderer and is always the
        universal ``_VVal`` struct (the type every generated
        value-returning call stub returns), so the call result is bound
        directly with a plain ``static _VVal`` declaration and no
        struct-literal wrapping.
        """
        return _format_systemverilog_call_declaration

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_variable_assignment`; the ``_VVal`` struct-literal
        wrapping is dropped since the call already yields a ``_VVal``.
        """
        return _format_systemverilog_call_assignment

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )
