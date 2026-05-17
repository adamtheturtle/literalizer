"""Carbon language specification.

Carbon is the experimental successor-to-C++ language from the
``carbon-language`` project.  It is statically typed with explicit
type annotations on declarations (``var x: i32 = 1;`` / ``let x: i32 =
1;``), uses ``//`` whole-line comments, semicolon-terminated
statements, and struct value literals of the form ``{.field = value}``
-- structurally the closest existing analog is :class:`~literalizer.
languages.Zig`.

Because Carbon is strongly typed and has no ``null``, arbitrary
heterogeneous JSON/YAML data is represented through a single
``choice CVal`` tagged union (the Carbon equivalent of the Zig
``ZVal`` union): every scalar, sequence, set, and map entry is
wrapped in the matching ``CVal`` alternative so collections remain
homogeneously typed.

Generated fixtures are compiled in CI by the ``lint-carbon`` job
against a pinned ``carbon`` nightly (see
``.github/workflows/lint.yml``).
"""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
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
    I64_MAX,
    I64_MIN,
    format_integer_binary,
    format_integer_hex,
    format_integer_underscore,
)
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
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
from literalizer.exceptions import UnrepresentableIntegerError


@beartype
def _format_date_carbon(value: datetime.date) -> str:
    """Format a date as epoch seconds (midnight UTC)."""
    dt = datetime.datetime(
        year=value.year,
        month=value.month,
        day=value.day,
        tzinfo=datetime.UTC,
    )
    return str(object=int(dt.timestamp()))


@beartype
def _format_datetime_carbon(value: datetime.datetime) -> str:
    """Format a datetime as epoch seconds (UTC)."""
    if value.tzinfo is None:
        value = value.replace(tzinfo=datetime.UTC)
    return str(object=int(value.timestamp()))


@dataclasses.dataclass(frozen=True)
class _CarbonDeclarationStyleConfig:
    """Configuration for a Carbon declaration style.

    Unlike :class:`DeclarationStyleConfig`, this carries no
    ``formatter`` slot: Carbon builds its declaration formatter
    per-instance in :attr:`Carbon.format_variable_declaration`.
    """

    keyword: str
    supports_redefinition: bool


@beartype
def _format_carbon_entry(
    *,
    original: Value,
    formatted: str,
    date_type: type,
    datetime_type: type,
) -> str:
    """Wrap a formatted entry in the appropriate ``CVal`` alternative.

    The ``str`` vs ``int`` choice for dates/datetimes is driven by the
    parsed :class:`Value` together with the chosen date/datetime
    format's ``type_produced``, rather than by sniffing *formatted*.
    """
    match original:
        case bool():
            return formatted
        case int():
            if original < I64_MIN:
                msg = (
                    f"Carbon cannot represent negative integer "
                    f"{original} below the signed 64-bit range using "
                    "the CVal union's unsigned alternative."
                )
                raise UnrepresentableIntegerError(msg)
            tag = "UInt" if original > I64_MAX else "Int"
        case float():
            tag = "Float"
        case str() | bytes():
            tag = "Str"
        case datetime.datetime():
            tag = "Str" if datetime_type is str else "Int"
        case datetime.time():
            tag = "Str"
        case datetime.date():
            tag = "Str" if date_type is str else "Int"
        case _:
            return formatted
    return f"CVal.{tag}({formatted})"


@beartype
def _make_carbon_call_preamble_stub() -> Callable[
    [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
    tuple[str, ...],
]:
    """Build the file-scope Carbon call-stub formatter.

    Carbon disallows nested function declarations, so call stubs are
    emitted at file scope.  Stubs return nothing so a bare
    ``stub(...);`` statement is valid whether or not a
    ``call_transform`` consumed the value.  Every parameter is typed
    ``CVal`` so the union literals emitted at the call site
    (``CVal.Int(1)``) match the parameter shape.  Dotted targets are
    realized as a nested ``class`` chain rooted at a file-level
    constant, so an expression like ``app.client.fetch(...)`` resolves
    to a real method call on a real value.
    """

    @beartype
    def _carbon_call_preamble_stub(
        parts: Sequence[str],
        params: Sequence[str],
        _stub_return: StubReturn,
        _args: Sequence[Value],
        /,
    ) -> tuple[str, ...]:
        """Return file-scope Carbon stub declarations for a call name."""
        method = parts[-1]
        if len(parts) == 1:
            param_list = ", ".join(f"{p}: CVal" for p in params)
            return (f"fn {method}({param_list}) {{}}",)
        chain = parts[:-1]
        holder = chain[-1]
        holder_type = f"{holder.title()}Type_"
        # A Carbon method takes its receiver as a ``[self: Self]``
        # deduced parameter before the ordinary parameter list.
        method_params = ", ".join(f"{p}: CVal" for p in params)
        lines: list[str] = [
            f"class {holder_type} {{ "
            f"fn {method}[self: Self]({method_params}) {{}} }}",
        ]
        prev_type = holder_type
        for i in range(len(chain) - 2, 0, -1):
            curr_type = f"{chain[i].title()}Type_"
            lines.append(
                f"class {curr_type} {{ var {chain[i + 1]}: {prev_type}; }}",
            )
            prev_type = curr_type
        root = chain[0]
        intermediates = chain[1:]
        if intermediates:
            root_type = f"{root.title()}Type_"
            lines.append(
                f"class {root_type} {{ var {intermediates[0]}: "
                f"{prev_type}; }}",
            )
        else:
            root_type = prev_type
        lines.append(f"var {root}: {root_type};")
        return tuple(lines)

    return _carbon_call_preamble_stub


@beartype
def _format_carbon_call_assignment(
    name: str,
    value: str,
    _data: Value,
) -> str:
    """Format a Carbon reassignment binding a call result.

    The call-expression counterpart of
    :attr:`Carbon.format_call_variable_declaration`; the variable
    already exists, so the call result is assigned directly with none
    of the ``CVal`` union wrapping a literal-binding assignment applies
    (a call result is not a ``CVal`` union literal).
    """
    return f"{name} = {value};"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Carbon(metaclass=LanguageCls):
    """Carbon language specification."""

    format_integer_widened = no_format_integer_widened
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".carbon"
    pygments_name = None
    supports_special_floats = False
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset(
        {
            "abstract",
            "addr",
            "alias",
            "and",
            "api",
            "as",
            "auto",
            "base",
            "break",
            "case",
            "choice",
            "class",
            "constraint",
            "continue",
            "default",
            "else",
            "extend",
            "final",
            "fn",
            "for",
            "forall",
            "friend",
            "if",
            "impl",
            "import",
            "in",
            "interface",
            "let",
            "library",
            "match",
            "namespace",
            "not",
            "observe",
            "or",
            "override",
            "package",
            "partial",
            "private",
            "protected",
            "require",
            "return",
            "returned",
            "self",
            "then",
            "type",
            "var",
            "virtual",
            "where",
            "while",
        },
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_module_name = False
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
        """Date format options for Carbon."""

        CARBON = DateFormatConfig(
            formatter=_format_date_carbon,
            type_produced=int,
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Carbon."""

        CARBON = DatetimeFormatConfig(
            formatter=_format_datetime_carbon,
            type_produced=int,
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
        """Sequence type options for Carbon."""

        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="CVal.Arr(("),
            close="))",
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
        """Set type options for Carbon."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="CVal.Set(("),
            close="))",
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

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = _CarbonDeclarationStyleConfig(
            keyword="let",
            supports_redefinition=False,
        )
        VAR = _CarbonDeclarationStyleConfig(
            keyword="var",
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
        positive_infinity="",
        negative_infinity="",
        nan="",
    ):
        """Float format options.

        Carbon has no portable infinity/NaN literal, so
        :attr:`supports_special_floats` is ``False`` and the
        :class:`FloatSpecialsMixin` special strings are never emitted.
        """

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options.

        Carbon has no octal literal syntax, so only decimal, hex, and
        binary are offered.
        """

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
        """Carbon call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options.

        ``ERROR`` keeps the default ``CVal`` union model: a
        record-shaped dict that mixes scalars with a container is
        rendered as a homogeneous-typed ``CVal.Map((...))``.
        """

        ERROR = enum.auto()

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for Carbon."""

        V0 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.CAMEL,
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
        """Wrap a Carbon declaration in a ``Run`` function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix=self.indent)
        if not variable_name:
            return f"fn Run() {{\n{indented}\n}}"
        use = f"{self.indent}let _: CVal = {variable_name};"
        return f"fn Run() {{\n{indented}\n{use}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Carbon declaration + assignment in a ``Run`` function."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.CARBON
    datetime_format: DatetimeFormats = DatetimeFormats.CARBON
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.LET
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
    language_version: VersionFormats = VersionFormats.V0
    indent: str = "  "

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def _format_entry(self) -> Callable[[Value, str], str]:
        """Shared entry formatter closing over date/datetime
        ``type_produced``.
        """
        date_type = self.date_format.value.type_produced
        datetime_type = self.datetime_format.value.type_produced

        @beartype
        def _formatter(original: Value, formatted: str) -> str:
            """Adapt :func:`_format_carbon_entry` to the positional
            entry-formatter interface.
            """
            return _format_carbon_entry(
                original=original,
                formatted=formatted,
                date_type=date_type,
                datetime_type=datetime_type,
            )

        return _formatter

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return self._format_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return self._format_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        format_entry = self._format_entry

        @beartype
        def _format_assign(name: str, value: str, data: Value) -> str:
            """Format a Carbon assignment to an existing ``CVal``
            variable.
            """
            wrapped = format_entry(data, value)
            return f"{name} = {wrapped};"

        return _format_assign

    @cached_property
    def null_literal(self) -> str:
        """The literal representing null (the ``CVal.Nil``
        alternative).
        """
        return "CVal.Nil"

    @cached_property
    def true_literal(self) -> str:
        """The literal representing true."""
        return "CVal.Bool(true)"

    @cached_property
    def false_literal(self) -> str:
        """The literal representing false."""
        return "CVal.Bool(false)"

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """File-scope preamble: the ``CVal`` tagged-union declaration.

        ``Core.String`` is the prelude string type and the array
        alternatives carry a homogeneous ``CVal`` element type so a
        sequence/set/map can hold mixed JSON values.
        """
        return (
            "choice CVal {",
            "  Nil,",
            "  Bool(bool),",
            "  Int(i64),",
            "  UInt(u64),",
            "  Float(f64),",
            "  Str(Core.String),",
            "  Arr(Core.Array(CVal)),",
            "  Map(Core.Array({.key: Core.String, .val: CVal})),",
            "  Set(Core.Array(CVal)),",
            "}",
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines (Carbon needs none)."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        The ``CVal`` union model represents every mixed collection
        natively, so no special heterogeneous behavior is required.
        """
        return NO_HETEROGENEOUS_BEHAVIOR

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
        """Return stub declarations for a call expression.

        Carbon disallows nested function declarations, so every stub is
        emitted at file scope via :attr:`format_call_preamble_stub`
        instead.
        """
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return _make_carbon_call_preamble_stub()

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each call argument in the ``CVal`` union so call sites
        match the parameter shape emitted by
        :func:`_carbon_call_preamble_stub`.
        """
        return self._format_entry

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
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Format a ``$ref`` the caller authorized as consumable."""
        return self.format_call_arg_ref_identifier

    @cached_property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        inhibits the consume form.
        """
        return never_inhibits_consuming_form

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
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        Every dict is rendered as the ``CVal.Map`` alternative whose
        entries are ``{.key = ..., .val = ...}`` struct literals.
        """
        return DictFormatConfig(
            dict_open=fixed_open(open_str="CVal.Map(("),
            close="))",
            format_entry=dict_entry_with_template(
                template="{{.key = {key}, .val = {value}}}",
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
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""

        def _format(value: str) -> str:
            """Format a string as a Carbon quoted literal."""
            return format_string_backslash_control(
                value=value,
                control_char_fmt="\\x{:02X}",
            )

        return _format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting.

        An ordered map is rendered with the same ``CVal.Map``
        alternative as a plain dict.
        """
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="CVal.Map(("),
            close="))",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_template(
            template="{{.key = {key}, .val = {value}}}",
            format_value=self._format_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Closes over the chosen date/datetime ``type_produced`` so the
        ``CVal`` alternative selection is driven by the parsed
        :class:`Value` rather than the rendered text.
        """
        keyword = self.declaration_style.value.keyword
        format_entry = self._format_entry

        @beartype
        def _format_decl(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a Carbon declaration with an explicit ``: CVal``
            type.
            """
            wrapped = format_entry(data, value)
            return f"{keyword} {name}: CVal = {wrapped};"

        return _format_decl

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call result.

        A ``CVal`` literal binding declares an explicit ``: CVal``
        type.  A call's return type is opaque to the renderer, so the
        call result is bound with an inferred ``: auto`` declaration
        (``let my_data: auto = make_widget(...);`` /
        ``var my_data: auto = make_widget(...);``): no caller-supplied
        return-type hint is needed and the value-wrapping is dropped.
        """
        keyword = self.declaration_style.value.keyword

        @beartype
        def _format_call_decl(
            name: str,
            value: str,
            _data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format an inferred Carbon declaration binding a call."""
            return f"{keyword} {name}: auto = {value};"

        return _format_call_decl

    @cached_property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment binding a call result.

        The call-expression counterpart of
        :attr:`format_call_variable_declaration`; the ``CVal`` wrapping
        a literal-binding assignment applies is dropped since a call
        result is not a ``CVal`` union literal.
        """
        return _format_carbon_call_assignment

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Carbon needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Carbon needs none)."""
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
