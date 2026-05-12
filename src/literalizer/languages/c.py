"""C language specification."""

import collections.abc
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
    format_datetime_epoch,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    variable_declaration_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    I64_MAX,
    format_integer_hex,
    make_long_suffix_formatter,
    make_overflow_fallback_formatter,
    make_ull_fallback,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
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
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    never_inhibits_consuming_form,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value


@beartype
def _apply_format_c_entry(  # noqa: PLR0911
    *,
    original: Value,
    formatted: str,
    int_field: str,
    uint_field: str,
    float_field: str,
    string_field: str,
) -> str:
    """Wrap a formatted entry in the appropriate union literal."""
    match original:
        case datetime.datetime() if formatted.lstrip("-").isdigit():
            return f"((CVal){{.{int_field} = {formatted}}})"
        case str() | bytes() | datetime.date():
            return f"((CVal){{.{string_field} = {formatted}}})"
        case bool():
            return formatted
        case int():
            # Values above ``LLONG_MAX`` cannot be assigned to the signed
            # ``long long`` field without an implementation-defined
            # narrowing conversion; route them to the unsigned field.
            if original > I64_MAX:
                return f"((CVal){{.{uint_field} = {formatted}}})"
            return f"((CVal){{.{int_field} = {formatted}}})"
        case float():
            return f"((CVal){{.{float_field} = {formatted}}})"
        case _:
            return formatted


@beartype
def _make_format_c_entry(
    *,
    int_field: str,
    uint_field: str,
    float_field: str,
    string_field: str,
) -> collections.abc.Callable[[Value, str], str]:
    """Return a formatter that wraps values in the appropriate
    ``CVal`` union literal using the given field names.
    """

    def _format_c_entry(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_format_c_entry(
            original=original,
            formatted=formatted,
            int_field=int_field,
            uint_field=uint_field,
            float_field=float_field,
            string_field=string_field,
        )

    return _format_c_entry


def _c_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return C stub declarations for a call name.

    C has no member functions and no type-generic function templates,
    so dotted targets are modeled as a nested chain of ``struct`` types
    whose leaf field is a function pointer.  Each prototype declares
    one ``CVal`` parameter per call argument so call sites pass values
    through the union-typed wrapper defined in the static preamble; this
    avoids the K&R unspecified-parameter syntax (and the
    ``-Wdeprecated-non-prototype`` clang warning it triggers) while
    still letting the same stub accept any mix of argument types.

    Single-name calls emit a ``static`` definition so the fixture links
    under the lint workflow's run step — a bare prototype without a body
    would otherwise fail at link time.
    """
    is_value = stub_return is StubReturn.VALUE
    return_keyword = "CVal" if is_value else "void"
    proto = ", ".join(["CVal"] * len(params)) if params else "void"
    stub_params = ", ".join(f"CVal _a{i}" for i in range(len(params)))
    stub_signature = stub_params or "void"
    discards = "".join(f" (void)_a{i};" for i in range(len(params)))
    return_stmt = " return (CVal){0};" if is_value else ""
    has_body = discards or is_value
    stub_body = f"{{{discards}{return_stmt} }}" if has_body else "{}"
    match parts:
        case [single]:
            return (
                f"static {return_keyword} {single}({stub_signature}) "
                f"{stub_body}",
            )
        case [root, method]:
            stub_fn = f"{root}_{method}_stub_"
            type_name = f"{root}Type_"
            return (
                f"static {return_keyword} {stub_fn}({stub_signature}) "
                f"{stub_body}",
                f"struct {type_name} "
                f"{{ {return_keyword} (*{method})({proto}); }};",
                f"static const struct {type_name} {root} = "
                f"{{ .{method} = {stub_fn} }};",
            )
        case _:
            pass
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    stub_fn = "_".join((*parts, "stub_"))
    lines: list[str] = [
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
class C(metaclass=LanguageCls):
    """C language specification."""

    module_name: str = "Module"

    extension = ".c"
    pygments_name = "c"
    supports_special_floats = True
    supports_variable_names = True
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_commented_dict_call_args = True
    supports_module_name = True

    class DateFormats(enum.Enum):
        """Date format options for C."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for C."""

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
        """Sequence type options for C."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(
                open_str="((CVal){.a = (CVal[]){",
            ),
            close="}})",
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
        """Set type options for C."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="((CVal){.a = (CVal[]){"),
            close="}})",
            empty_set=None,
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
            formatter=variable_declaration_formatter(
                template="CVal {name} = {value};",
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

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()
        AUTO = enum.auto()

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
        """C call style options."""

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
        """Version options for C."""

        C99 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.SNAKE
    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
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
        """Wrap a C declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        use_line = (
            f"\n{self.indent}(void){variable_name};" if variable_name else ""
        )
        return (
            f"int {self.module_name}(void) {{\n{content}{use_line}\n"
            f"{self.indent}return 0;\n}}"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap C declaration + assignment in a function.

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
    # Keep in sync with the ``-std=`` flag passed to clang and clang-tidy
    # in ``.github/workflows/lint.yml``.
    language_version: VersionFormats = VersionFormats.C99
    indent: str = "    "
    bool_field: str = "b"
    int_field: str = "i"
    uint_field: str = "u"
    float_field: str = "f"
    string_field: str = "s"
    array_field: str = "a"
    map_field: str = "m"
    key_field: str = "k"
    value_field: str = "v"

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("#include <math.h>",)
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def call_style_config(self) -> PositionalCallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

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
        return _c_call_stub

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
        """Wrap each call argument in the ``CVal`` union so call sites
        match the concrete prototype emitted by :func:`_c_call_stub`.
        """
        return self._format_entry

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def _format_entry(self) -> Callable[[Value, str], str]:
        """Shared entry formatter that wraps values in ``CVal``
        literals.
        """
        return _make_format_c_entry(
            int_field=self.int_field,
            uint_field=self.uint_field,
            float_field=self.float_field,
            string_field=self.string_field,
        )

    @cached_property
    def _seq_open_str(self) -> str:
        """Opening string for a C sequence literal."""
        return f"((CVal){{.{self.array_field} = (CVal[]){{"

    @cached_property
    def _map_open_str(self) -> str:
        """Opening string for a C map literal."""
        return f"((CVal){{.{self.map_field} = (CKV[]){{"

    @cached_property
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"((CVal){{.{self.string_field} = NULL}})"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"((CVal){{.{self.bool_field} = true}})"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"((CVal){{.{self.bool_field} = false}})"

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        fmt = self.sequence_format.value
        return SequenceFormatConfig(
            sequence_open=fixed_open(open_str=self._seq_open_str),
            close="}})",
            supports_heterogeneity=fmt.supports_heterogeneity,
            single_element_trailing_comma=(fmt.single_element_trailing_comma),
            supports_trailing_comma=fmt.supports_trailing_comma,
            empty_sequence=fmt.empty_sequence,
            preamble_lines=fmt.preamble_lines,
            format_entry=fmt.format_entry,
            typed_opener_fallback=fmt.typed_opener_fallback,
            uses_typed_literal_for_scalars=(
                fmt.uses_typed_literal_for_scalars
            ),
            requires_uniform_record_shapes=(
                fmt.requires_uniform_record_shapes
            ),
            declared_type=fmt.declared_type,
            narrowed_empty_form=None,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return SetFormatConfig(
            set_open=fixed_open(open_str=self._seq_open_str),
            close="}})",
            empty_set=self.set_format.value.empty_set,
            preamble_lines=self.set_format.value.preamble_lines,
            set_opener_template=self.set_format.value.set_opener_template,
            supports_heterogeneity=self.set_format.value.supports_heterogeneity,
            supports_trailing_comma=True,
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str=self._map_open_str),
            close="}})",
            format_entry=braced_dict_entry(
                format_value=self._format_entry,
            ),
            empty_dict=None,
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
        suffix_is_auto = self.numeric_literal_suffix.name == "AUTO"
        base: Callable[[int], str] = (
            make_long_suffix_formatter(base=self.integer_format)
            if suffix_is_auto
            else self.integer_format
        )
        return make_overflow_fallback_formatter(
            base=base,
            fallback=make_ull_fallback(language_name="C"),
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats one sequence entry."""
        return self._format_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats one set entry."""
        return self._format_entry

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=self._map_open_str),
            close="}})",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return braced_dict_entry(format_value=self._format_entry)

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        format_entry = self._format_entry

        @beartype
        def _format_decl(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a C variable declaration."""
            wrapped = format_entry(data, value)
            return f"CVal {name} = {wrapped};"

        return _format_decl

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        format_entry = self._format_entry

        @beartype
        def _format_assign(name: str, value: str, data: Value) -> str:
            """Format a C variable assignment."""
            wrapped = format_entry(data, value)
            return f"{name} = {wrapped};"

        return _format_assign

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file."""
        return (
            "#include <stdbool.h>",
            "#include <stddef.h>",
            "typedef struct CVal CVal;",
            "typedef struct CKV CKV;",
            "struct CVal {",
            "    union {",
            f"        _Bool {self.bool_field};",
            f"        long long {self.int_field};",
            f"        unsigned long long {self.uint_field};",
            f"        double {self.float_field};",
            f"        const char *{self.string_field};",
            f"        const CVal *{self.array_field};",
            f"        const CKV *{self.map_field};",
            "    };",
            "};",
            (
                f"struct CKV {{ const char *{self.key_field}; "
                f"CVal {self.value_field}; }};"
            ),
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (C needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (C needs none)."""
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
