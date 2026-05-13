"""Fortran language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property, partial
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
from literalizer._formatters.format_strings import format_string_concat_control
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
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
    identity_call_ref_identifier,
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
def _format_fortran_datetime_epoch(value: datetime.datetime, /) -> str:
    """Format a datetime as an int64 Fortran epoch literal."""
    return f"{format_datetime_epoch(value=value)}_int64"


@beartype
def _apply_fortran_entry(
    *,
    original: Value,
    formatted: str,
    int_name: str,
    real_name: str,
    str_name: str,
) -> str:
    """Wrap a formatted entry in its constructor call."""
    match original:
        case bool():
            return formatted
        case datetime.datetime() if (
            formatted.removesuffix("_int64").lstrip("-").isdigit()
        ):
            return f"{int_name}({formatted})"
        case int():
            return f"{int_name}({formatted})"
        case float():
            return f"{real_name}({formatted})"
        case str() | bytes() | datetime.date():
            return f"{str_name}({formatted})"
        case _:
            return formatted


@beartype
def _build_format_fortran_entry(
    *,
    int_name: str,
    real_name: str,
    str_name: str,
) -> Callable[[Value, str], str]:
    """Build a formatter that wraps values in the appropriate
    constructor.
    """

    def _format_fortran_entry(original: Value, formatted: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_fortran_entry(
            original=original,
            formatted=formatted,
            int_name=int_name,
            real_name=real_name,
            str_name=str_name,
        )

    return _format_fortran_entry


@beartype
def _fortran_comment_pos(line: str) -> int | None:
    """Return the index of the ``!`` comment character in *line* that
    lies outside any string literal, or ``None`` if there is no comment.
    """
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        match c:
            case "'" if not in_double_quote:
                if (
                    in_single_quote
                    and i + 1 < len(line)
                    and line[i + 1] == "'"
                ):
                    i += 2
                    continue
                in_single_quote = not in_single_quote
            case '"' if not in_single_quote:
                in_double_quote = not in_double_quote
            case "!" if not in_single_quote and not in_double_quote:
                return i
            case _:
                pass
        i += 1
    return None


@beartype
def _add_continuation(value: str) -> str:
    """Add Fortran ``&`` line-continuation to non-comment, non-last
    lines.

    In Fortran free-form source a logical line may span multiple physical
    lines.  The ``&`` continuation character must be the last
    non-whitespace, non-comment character on the physical line.  Pure
    comment lines (blank or starting with ``!``) are transparent to the
    continuation mechanism and receive no ``&``.
    """
    lines = value.splitlines()
    if len(lines) <= 1:
        return value
    result: list[str] = []
    for i, line in enumerate(iterable=lines):
        is_last = i == len(lines) - 1
        stripped = line.strip()
        is_pure_comment = not stripped or stripped.startswith("!")
        if is_last or is_pure_comment:
            result.append(line)
        else:
            pos = _fortran_comment_pos(line=line)
            if pos is not None:
                result.append(line[:pos].rstrip() + " &  " + line[pos:])
            else:
                result.append(line + " &")
    return "\n".join(result)


@beartype
def _apply_fortran_variable_declaration(
    name: str,
    value: str,
    data: Value,
    format_entry: Callable[[Value, str], str],
) -> str:
    """Format a variable declaration and initialisation."""
    fval = format_entry(data, value)
    continued = _add_continuation(value=fval)
    return f"type(fval_t) :: {name}\n{name} = {continued}"


@beartype
def _build_format_variable_declaration(
    *,
    format_entry: Callable[[Value, str], str],
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Build a variable declaration formatter."""

    def _format_variable_declaration(
        name: str,
        value: str,
        data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_fortran_variable_declaration(
            name=name, value=value, data=data, format_entry=format_entry
        )

    return _format_variable_declaration


@beartype
def _apply_fortran_variable_assignment(
    name: str,
    value: str,
    data: Value,
    format_entry: Callable[[Value, str], str],
) -> str:
    """Format an assignment to an existing variable."""
    fval = format_entry(data, value)
    continued = _add_continuation(value=fval)
    return f"{name} = {continued}"


@beartype
def _build_format_variable_assignment(
    *,
    format_entry: Callable[[Value, str], str],
) -> Callable[[str, str, Value], str]:
    """Build a variable assignment formatter."""

    def _format_variable_assignment(name: str, value: str, data: Value) -> str:
        """Delegate to module-level implementation."""
        return _apply_fortran_variable_assignment(
            name=name, value=value, data=data, format_entry=format_entry
        )

    return _format_variable_assignment


@beartype
def _fortran_call_target(parts: Sequence[str], /) -> str:
    """Return the last component of a dotted call target as the Fortran
    procedure name.

    ``app.client.fetch`` produces ``fetch`` so the generated call and
    stub use a simple identifier that Fortran can declare as an internal
    procedure without object/module prefix notation.
    """
    return parts[-1]


@beartype
def _fortran_call_statement(call: str, /) -> str:
    """Prepend ``call `` to a Fortran subroutine-call statement.

    All top-level call statements in the generated output invoke void
    subroutines (or subroutines wrapping a value-returning function),
    which require the ``call`` keyword in Fortran.
    """
    return f"call {call}"


@beartype
def _fortran_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return a Fortran internal-procedure stub for a call expression.

    VOID stubs emit a ``subroutine``; VALUE stubs emit a ``function``
    that returns ``type(fval_t)`` via ``fnull()``.  Both use ``implicit
    none`` and declare each parameter as ``type(fval_t), intent(in)``.
    The host program's ``use fval_m`` provides ``fval_t`` and ``fnull``
    via host association, so no additional ``use`` statement is needed.

    Leading underscores are stripped from parameter names so that a
    placeholder like ``_arg`` becomes the valid Fortran identifier
    ``arg``.
    """
    method = parts[-1]
    clean_params = [p.lstrip("_") or p for p in params]

    if stub_return is StubReturn.VOID:
        param_str = f"({', '.join(clean_params)})" if clean_params else "()"
        lines: list[str] = [f"subroutine {method}{param_str}"]
        lines.append(f"{indent}implicit none")
        if clean_params:
            joined = ", ".join(clean_params)
            lines.append(f"{indent}type(fval_t), intent(in) :: {joined}")
        lines.append(f"end subroutine {method}")
        return ("\n".join(lines),)

    param_str = f"({', '.join(clean_params)})" if clean_params else "()"
    lines = [f"function {method}{param_str} result(r)"]
    lines.append(f"{indent}implicit none")
    if clean_params:
        joined = ", ".join(clean_params)
        lines.append(f"{indent}type(fval_t), intent(in) :: {joined}")
    lines.append(f"{indent}type(fval_t) :: r")
    lines.append(f"{indent}r = fnull()")
    lines.append(f"end function {method}")
    return ("\n".join(lines),)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Fortran(metaclass=LanguageCls):
    """Fortran language specification."""

    module_name: str = "Module"

    extension = ".f90"
    pygments_name = "fortran"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    call_returns_expression = True
    supports_zero_parameter_calls = True
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_module_name = True
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = False
    supports_default_dict_value_type = False
    supports_default_sequence_element_type = False
    supports_default_set_element_type = False
    supports_default_ordered_map_value_type = False

    class DateFormats(enum.Enum):
        """Date format options for Fortran."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Fortran."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=_format_fortran_datetime_epoch,
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
        """Sequence type options for Fortran."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="flist([fval_t :: "),
            close="])",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
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
        """Set type options for Fortran."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="fset([fval_t :: "),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        EXCLAMATION = CommentConfig(
            prefix="!",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = DeclarationStyleConfig(
            formatter=_build_format_variable_declaration(
                format_entry=_build_format_fortran_entry(
                    int_name="fint",
                    real_name="freal",
                    str_name="fstr",
                ),
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
        positive_infinity="ieee_value(0.0, ieee_positive_inf)",
        negative_infinity="ieee_value(0.0, ieee_negative_inf)",
        nan="ieee_value(0.0, ieee_quiet_nan)",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.auto()

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
        """Fortran call style options."""

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
        """Version options for Fortran."""

        V2003 = enum.auto()

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

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Fortran variable declaration or call block in a program.

        When *variable_name* is non-empty (variable declaration mode),
        *body_preamble* is prepended before *content* in the program
        body.  When *variable_name* is empty (call mode), *body_preamble*
        holds internal-procedure stubs that go in the ``contains`` section
        after the executable statements in *content*.
        """
        if variable_name:
            content = prepend_body_preamble(
                content=content,
                body_preamble=body_preamble,
            )
            indented = textwrap.indent(text=content, prefix=self.indent)
            return (
                f"program {self.module_name}\n"
                f"{self.indent}use fval_m\n"
                f"{self.indent}implicit none\n"
                f"{indented}\n"
                f"end program {self.module_name}"
            )
        indented = textwrap.indent(text=content, prefix=self.indent)
        stubs_str = "\n".join(body_preamble)
        indented_stubs = textwrap.indent(text=stubs_str, prefix=self.indent)
        return (
            f"program {self.module_name}\n"
            f"{self.indent}use fval_m\n"
            f"{self.indent}implicit none\n"
            f"{indented}\n"
            f"contains\n"
            f"{indented_stubs}\n"
            f"end program {self.module_name}"
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Fortran declaration + assignment in separate
        subroutines.
        """
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        decl_indented = textwrap.indent(text=declaration, prefix=self.indent)
        assign_indented = textwrap.indent(text=assignment, prefix=self.indent)
        return (
            f"subroutine {self.module_name}_declaration()\n"
            f"{self.indent}use fval_m\n"
            f"{self.indent}implicit none\n"
            f"{decl_indented}\n"
            f"end subroutine {self.module_name}_declaration\n"
            "\n"
            f"subroutine {self.module_name}_assignment()\n"
            f"{self.indent}use fval_m\n"
            f"{self.indent}implicit none\n"
            f"{self.indent}type(fval_t) :: {variable_name}\n"
            f"{assign_indented}\n"
            f"end subroutine {self.module_name}_assignment\n"
            "\n"
            "program main\n"
            f"{self.indent}call {self.module_name}_declaration()\n"
            f"{self.indent}call {self.module_name}_assignment()\n"
            "end program main"
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.EXCLAMATION
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
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.V2003
    indent: str = "    "
    null_name: str = "fnull"
    bool_name: str = "fbool"
    int_name: str = "fint"
    real_name: str = "freal"
    str_name: str = "fstr"
    list_name: str = "flist"
    map_name: str = "fmap"
    set_name: str = "fset"
    entry_name: str = "fentry"

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    special_float_preamble: ClassVar[tuple[str, ...]] = (
        "  use, intrinsic :: ieee_arithmetic",
    )
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as an int64 Fortran literal."""
        return make_overflow_fallback_formatter(
            base=lambda value: f"{value}_int64",
            fallback=raise_for_unrepresentable_int(language_name="Fortran"),
        )

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
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression."""
        return partial(_fortran_call_stub, indent=self.indent)

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
        return _fortran_call_target

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap a call argument in the appropriate ``fval_t``
        constructor.
        """
        return self._format_entry

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Prepend the Fortran ``call`` keyword to each call statement."""
        return _fortran_call_statement

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

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Fortran call stubs and variable declarations alongside
        calls.

        Fortran requires all specification statements (type
        declarations) to precede executable statements (assignments and
        calls).  Each declaration *bare_code* from :func:`literalize`
        is a two-part string: a ``type(fval_t) :: name`` declaration on
        the first line and an assignment on the remaining lines.  This
        method splits them so that all type-declaration lines appear
        before any assignment or call lines, producing a valid program.

        Call stubs are placed in the ``contains`` section via
        :meth:`wrap_in_file`.
        """
        type_decls: list[str] = []
        exec_stmts: list[str] = []
        for bare_code in declarations:
            lines = bare_code.splitlines()
            type_decls.append(lines[0])
            exec_stmts.extend(lines[1:])
        body_parts: list[str] = [*type_decls, *exec_stmts, calls]
        content = "\n".join(body_parts)
        return self.wrap_in_file(
            content=content,
            variable_name="",
            body_preamble=body_preamble,
        )

    @cached_property
    def _format_entry(self) -> Callable[[Value, str], str]:
        """Shared entry formatter for Fortran values."""
        return _build_format_fortran_entry(
            int_name=self.int_name,
            real_name=self.real_name,
            str_name=self.str_name,
        )

    @cached_property
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.null_name}()"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"{self.bool_name}(.true.)"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"{self.bool_name}(.false.)"

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        fmt = self.sequence_format.value
        return SequenceFormatConfig(
            sequence_open=fixed_open(
                open_str=f"{self.list_name}([fval_t :: ",
            ),
            close="])",
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
            set_open=fixed_open(
                open_str=f"{self.set_name}([fval_t :: ",
            ),
            close="])",
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
            dict_open=fixed_open(
                open_str=f"{self.map_name}([fval_t :: ",
            ),
            close="])",
            format_entry=dict_entry_with_template(
                template=f"{self.entry_name}({{key}}, {{value}})",
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
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return format_string_concat_control(
            quote_char="'",
            quote_escape="''",
            control_char_template="achar({})",
            concat_operator=" // ",
            escape_backslash=False,
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

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
            ordered_map_open=fixed_open(
                open_str=f"{self.map_name}([fval_t :: ",
            ),
            close="])",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_template(
            template=f"{self.entry_name}({{key}}, {{value}})",
            format_value=self._format_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return _build_format_variable_declaration(
            format_entry=self._format_entry,
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return _build_format_variable_assignment(
            format_entry=self._format_entry,
        )

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file."""
        return ("module fval_m",)

    @cached_property
    def static_body_preamble(self) -> Sequence[str]:
        """Static body-preamble lines emitted once per file."""
        return (
            "  use, intrinsic :: iso_fortran_env, only: int64",
            "  implicit none",
            "  type :: fval_t",
            "    integer :: t = 0",
            "  end type fval_t",
            "contains",
            f"  function {self.null_name}() result(v)"
            "; type(fval_t) :: v; end function",
            f"  function {self.bool_name}(b) result(v)"
            "; logical, intent(in) :: b"
            "; type(fval_t) :: v; end function",
            f"  function {self.int_name}(n) result(v)"
            "; integer(kind=int64), intent(in) :: n"
            "; type(fval_t) :: v; end function",
            f"  function {self.real_name}(x) result(v)"
            "; real, intent(in) :: x"
            "; type(fval_t) :: v; end function",
            f"  function {self.str_name}(s) result(v)"
            "; character(len=*), intent(in) :: s"
            "; type(fval_t) :: v; end function",
            f"  function {self.list_name}(a) result(v)"
            "; type(fval_t), intent(in) :: a(:)"
            "; type(fval_t) :: v; end function",
            f"  function {self.map_name}(a) result(v)"
            "; type(fval_t), intent(in) :: a(:)"
            "; type(fval_t) :: v; end function",
            f"  function {self.set_name}(a) result(v)"
            "; type(fval_t), intent(in) :: a(:)"
            "; type(fval_t) :: v; end function",
            f"  function {self.entry_name}(k, u) result(v)"
            "; character(len=*), intent(in) :: k"
            "; type(fval_t), intent(in) :: u"
            "; type(fval_t) :: v; end function",
            "end module fval_m",
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Fortran needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Fortran needs none)."""
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
