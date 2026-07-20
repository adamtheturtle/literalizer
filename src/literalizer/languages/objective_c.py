"""Objective-C language specification."""

import base64
import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_iso_formatter,
    datetime_iso_formatter,
    format_datetime_epoch,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    passthrough_sequence_entry,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    I64_MIN,
    format_integer_hex,
    format_integer_octal_c_style,
    make_overflow_fallback_formatter,
    make_ull_fallback,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    JsonType,
    LanguageCls,
    ModifierCombination,
    NestedMapWideningVariant,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value

# A formatted numeric value can follow ``@`` directly when it is a
# bare unsigned numeric literal (digits, hex/exponent letters, dot,
# optional ``+``/``-`` after ``e``/``E`` for scientific notation, and
# integer-suffix letters).  Anything else — a leading ``-``, an
# identifier like ``INFINITY``/``NAN``, or an embedded comment —
# requires the ``@(...)`` boxed-expression form.
_OBJC_BARE_NUMERIC = re.compile(
    pattern=r"\A[0-9](?:[0-9a-zA-Z._]|[eE][+-])*\Z",
)


@beartype
def _format_objc_entry(original: Value, formatted: str, /) -> str:
    """Wrap a formatted entry for use inside an Objective-C collection.

    Only bare numeric values (``int`` / ``float``, but not ``bool``)
    and epoch datetime values need ``@`` boxing; everything else is
    already a valid Objective-C object expression.  The redundant
    ``@(...)`` parentheses are dropped when the formatted value is a
    bare numeric literal so that clang-tidy's
    ``readability-redundant-parentheses`` check passes.
    """
    is_numeric_datetime = (
        isinstance(
            original,
            datetime.datetime,
        )
        and formatted.lstrip("-").isdigit()
    )
    if isinstance(original, bool) or not (
        isinstance(original, (int, float)) or is_numeric_datetime
    ):
        return formatted
    if _OBJC_BARE_NUMERIC.fullmatch(string=formatted):
        return f"@{formatted}"
    return f"@({formatted})"


@beartype
def _format_objc_declaration(
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format an Objective-C ``id`` declaration, boxing primitive scalars.

    Same reason as :func:`_format_objc_entry`: an ``id`` is a pointer
    type, so bare ``int``/``float`` values must be boxed as ``NSNumber``
    before assignment.
    """
    return f"id {name} = {_format_objc_entry(data, value)};"


@beartype
def _format_objc_assignment(name: str, value: str, data: Value) -> str:
    """Format an Objective-C reassignment, boxing primitive scalars."""
    return f"{name} = {_format_objc_entry(data, value)};"


@beartype
def _format_objc_call_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format an Objective-C ``id`` declaration binding a call result.

    The literal-binding declaration boxes a primitive right-hand side
    as ``NSNumber`` / ``NSString`` because an ``id`` is a pointer type.
    A call expression already evaluates to an object pointer, so the
    ``@(...)`` boxing is dropped and the call result is bound directly.
    """
    return f"id {name} = {value};"


@beartype
def _format_objc_call_assignment(name: str, value: str, _data: Value) -> str:
    """Format an Objective-C reassignment binding a call result.

    The call-expression counterpart of :func:`_format_objc_assignment`;
    no ``@(...)`` boxing since a call already yields an object pointer.
    """
    return f"{name} = {value};"


@beartype
def _format_objc_string(value: str) -> str:
    r"""Format a string as an Objective-C ``NSString`` literal.

    Escapes backslashes, double quotes, newlines, carriage returns, and
    tabs, then wraps the result in ``@"..."``.

    Example: ``hello "world"`` → ``@"hello \"world\""``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f'@"{escaped}"'


@beartype
def _format_objc_bytes(value: bytes) -> str:
    """Format bytes as an Objective-C ``NSString`` hex literal.

    Example: ``b"Hi"`` → ``@"4869"``.
    """
    return f'@"{value.hex()}"'


@beartype
def _format_objc_bytes_base64(value: bytes) -> str:
    """Format bytes as an Objective-C ``NSString`` base64 literal.

    Example: ``b"Hello"`` → ``@"SGVsbG8="``.
    """
    encoded = base64.b64encode(s=value)
    return f'@"{encoded.decode(encoding="ascii")}"'


@beartype
def _objc_global_root(root: str, /) -> str:
    """Return a ``k``-prefixed, title-cased root for an Objective-C
    const global, so the emitted name satisfies clang-tidy's
    ``google-objc-global-variable-declaration`` check.
    """
    return f"k{root.title()}"


@beartype
def _objc_format_call_target(parts: Sequence[str], /) -> str:
    """Rewrite the root of a dotted call target to its k-prefixed form
    so the call site matches the renamed const global emitted by
    :func:`_objc_call_stub`.  Single-name calls resolve to a ``static``
    function (not a const global) and are returned unchanged.
    """
    if len(parts) == 1:
        return parts[0]
    return ".".join((_objc_global_root(parts[0]), *parts[1:]))


# Maximum parameter count of any existing call case; stubs above this
# get a ``// NOLINTNEXTLINE`` for ``bugprone-easily-swappable-parameters``.
_SWAPPABLE_PARAMS_NOLINT_THRESHOLD = 4


@beartype
def _objc_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Objective-C stub declarations for a call name.

    Objective-C is a superset of C, so call stubs reuse C's structure:
    dotted targets become a nested chain of ``struct`` types whose leaf
    field is a function pointer.  Each prototype declares one ``id``
    parameter per call argument; primitive arguments are boxed via
    ``@(...)`` at the call site so every actual argument is an
    Objective-C object.  This avoids K&R unspecified-parameter syntax
    and the ``-Wstrict-prototypes`` / ``-Wdeprecated-non-prototype``
    warnings that clang would otherwise emit.

    The root of a dotted target is rewritten to ``k{Title}`` form (e.g.
    ``throttler`` → ``kThrottler``) so the const global satisfies
    clang-tidy's ``google-objc-global-variable-declaration`` check.

    Single-name calls emit a ``static`` definition so the fixture links
    under the lint workflow's run step — a bare prototype without a body
    would otherwise fail at link time.
    """
    is_value = stub_return is StubReturn.VALUE
    return_keyword = "id" if is_value else "void"
    proto = ", ".join(["id"] * len(params)) if params else "void"
    stub_params = ", ".join(f"id _a{i}" for i in range(len(params)))
    stub_signature = stub_params or "void"
    discards = "".join(f" (void)_a{i};" for i in range(len(params)))
    return_stmt = " return nil;" if is_value else ""
    has_body = discards or is_value
    stub_body = f"{{{discards}{return_stmt} }}" if has_body else "{}"
    # Long uniform-typed parameter lists trip clang-tidy's
    # ``bugprone-easily-swappable-parameters`` check past its
    # name-suffix-dissimilarity silencing heuristic.  The stub is
    # generated, so the warning is not actionable.  Suppress it on
    # stubs whose parameter count exceeds anything the existing call
    # cases use, to avoid touching shorter-stub golden files.
    nolint = (
        ("// NOLINTNEXTLINE(bugprone-easily-swappable-parameters)",)
        if len(params) > _SWAPPABLE_PARAMS_NOLINT_THRESHOLD
        else ()
    )
    if len(parts) == 1:
        return (
            *nolint,
            f"static {return_keyword} {parts[0]}({stub_signature}) "
            f"{stub_body}",
        )
    root = _objc_global_root(parts[0])
    method = parts[-1]
    fields = parts[1:-1]
    stub_fn = "_".join((root, *parts[1:], "stub_"))
    if not fields:
        type_name = f"{root}Type_"
        return (
            *nolint,
            f"static {return_keyword} {stub_fn}({stub_signature}) {stub_body}",
            f"struct {type_name} "
            f"{{ {return_keyword} (*{method})({proto}); }};",
            f"static const struct {type_name} {root} = "
            f"{{ .{method} = {stub_fn} }};",
        )
    lines: list[str] = [
        *nolint,
        f"static {return_keyword} {stub_fn}({stub_signature}) {stub_body}",
    ]
    inner_type = f"{fields[-1]}Type_"
    lines.append(
        f"struct {inner_type} {{ {return_keyword} (*{method})({proto}); }};",
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i]}Type_"
        lines.append(
            f"struct {curr_type} {{ struct {prev_type} {fields[i + 1]}; }};",
        )
        prev_type = curr_type
    root_type = f"{root}Type_"
    lines.append(
        f"struct {root_type} {{ struct {prev_type} {fields[0]}; }};",
    )
    init = f"{{ .{method} = {stub_fn} }}"
    for field in reversed(fields):
        init = f"{{ .{field} = {init} }}"
    lines.append(f"static const struct {root_type} {root} = {init};")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class ObjectiveC(metaclass=LanguageCls):
    """Objective-C language specification."""

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    module_name: str = "Module"

    leading_preamble = no_leading_preamble
    extension = ".m"
    pygments_name = "objective-c"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "auto",
            "break",
            "case",
            "char",
            "const",
            "continue",
            "default",
            "do",
            "double",
            "else",
            "enum",
            "extern",
            "float",
            "for",
            "goto",
            "if",
            "inline",
            "int",
            "long",
            "register",
            "restrict",
            "return",
            "short",
            "signed",
            "sizeof",
            "static",
            "struct",
            "switch",
            "typedef",
            "typeof",
            "union",
            "unsigned",
            "void",
            "volatile",
            "while",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
    call_returns_expression = True
    supports_json_call_result_binding = False
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False
    non_default_kwargs: ClassVar[dict[str, str]] = {}
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        string_literals_escape_null_byte=False,
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for ObjectiveC."""

        OBJC = DateFormatConfig(
            formatter=date_iso_formatter(template='@"{iso}"'),
            preamble_lines=(),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=date_iso_formatter(template='@"{iso}"'),
            type_produced=str,
            preamble_lines=(),
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for ObjectiveC."""

        OBJC = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(template='@"{iso}"'),
            preamble_lines=(),
            type_produced=datetime.datetime,
        )
        ISO = DatetimeFormatConfig(
            formatter=datetime_iso_formatter(template='@"{iso}"'),
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=format_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_objc_bytes)
        BASE64 = enum.member(value=_format_objc_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Objective-C."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="@["),
            close="]",
            empty_sequence="@[]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Objective-C."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="[NSSet setWithArray:@["),
            close="]]",
            empty_set="[NSSet set]",
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
            formatter=_format_objc_declaration,
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
        positive_infinity="INFINITY",
        negative_infinity="-INFINITY",
        nan="NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal_c_style)

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
        """ObjectiveC call style options."""

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

    class JsonTypes(JsonType):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Objective-C."""

        V2 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
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
        """Wrap an Objective-C declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = (
            f"\n{self.indent}(void){variable_name};" if variable_name else ""
        )
        return (
            f"int {self.module_name}(void) {{\n"
            f"@autoreleasepool {{\n{content}{use_line}\n"
            f"}}\n{self.indent}return 0;\n}}"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Objective-C declaration + assignment in a function.

        Reads ``variable_name`` between the declaration and the
        assignment so the initial value is not a dead store flagged by
        clang-tidy's ``clang-analyzer-deadcode.DeadStores`` check.
        """
        mid_use = f"(void){variable_name};\n"
        return self.wrap_in_file(
            content=f"{declaration}\n{mid_use}{assignment}",
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.OBJC
    datetime_format: DatetimeFormats = DatetimeFormats.OBJC
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
    trailing_comma: TrailingCommas = TrailingCommas.YES
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the ``macos-15`` runner image pinned for the
    # ``lint-objectivec`` / ``lint-objectivec-tidy`` jobs in
    # ``.github/workflows/lint.yml``, whose Apple ``clang`` supports this
    # Objective-C 2.0 (``V2``) language generation.
    language_version: VersionFormats = VersionFormats.V2
    indent: str = "    "

    null_literal: ClassVar[str] = "[NSNull null]"
    true_literal: ClassVar[str] = "@YES"
    false_literal: ClassVar[str] = "@NO"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_preamble: ClassVar[Sequence[str]] = (
        "#import <Foundation/Foundation.h>",
    )
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def call_style_config(self) -> PositionalCallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return _format_objc_string

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return _format_objc_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_objc_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return _format_objc_assignment

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call expression.

        The literal-binding declaration boxes a primitive right-hand
        side as ``NSNumber`` / ``NSString`` (an ``id`` is a pointer
        type); a call expression already yields an object pointer, so
        the ``@(...)`` boxing is dropped and the call result is bound
        directly.
        """
        return _format_objc_call_declaration

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call expression.

        The call-expression counterpart of
        :attr:`format_variable_assignment`; the ``@(...)`` boxing is
        dropped since a call already yields an object pointer.
        """
        return _format_objc_call_assignment

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
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return _objc_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target so the root matches the
        ``k``-prefixed const global emitted by :func:`_objc_call_stub`.
        """
        return _objc_format_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

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

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Box each call argument as an ``id`` so call sites match the
        concrete prototype emitted by :func:`_objc_call_stub`.
        """
        return _format_objc_entry

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
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return dict_entry_with_separator(
            separator=": ",
            format_value=_format_objc_entry,
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str="@{"),
            close="}",
            format_entry=self._dict_entry,
            empty_dict="@{}",
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
            narrowed_empty_form=None,
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

        def _format(value: datetime.time) -> str:
            """Format a time as an Objective-C ``NSString`` literal."""
            return f"@{format_time_iso(value=value)}"

        return _format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal.

        Values above ``LLONG_MAX`` get a ``ULL`` suffix so clang does
        not reinterpret the literal as an unsigned type and emit the
        warning the lint workflow treats as an error; values below
        ``LLONG_MIN`` raise ``UnrepresentableIntegerError`` since no
        signed or unsigned 64-bit integer can hold them.
        """
        return make_overflow_fallback_formatter(
            base=self.integer_format,
            fallback=make_ull_fallback(language_name="Objective-C"),
            min_value=I64_MIN,
            max_value=I64_MAX,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="@{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._dict_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Objective-C needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Objective-C needs none)."""
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
