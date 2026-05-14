"""Visual Basic (.NET) language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    make_element_to_type,
    make_type_to_opener,
    typed_collection_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_vb,
)
from literalizer._formatters.format_entries import (
    braced_dict_entry,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    ordered_map_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    make_long_suffix_formatter,
    make_overflow_fallback_formatter,
    make_unsigned_overflow_fallback,
)
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
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
    KeywordCallStyle,
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
    identity_call_arg,
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
def _format_vb_ulong_positive(value: int) -> str:
    """Format a positive value above signed 64-bit range as a VB.NET
    ``UL`` unsigned 64-bit literal.

    The default VB.NET integer type is signed 64-bit; values above
    that range need the ``UL`` suffix to select the unsigned 64-bit
    type, which covers up to 2^64 - 1.
    """
    return f"{value}UL"


@beartype
def _flush_vb_current(
    *,
    parts: list[str],
    current: str,
) -> str:
    """Flush accumulated literal characters into parts."""
    if current:
        parts.append(f'"{current}"')
    return ""


@beartype
def _vb_string_parts(value: str) -> list[str]:
    """Generate VB.NET string parts for control character handling."""
    control_char_threshold = 32
    parts: list[str] = []
    current = ""
    i = 0
    char_replacements = {"\n": "Chr(10)", "\r": "Chr(13)", "\t": "vbTab"}
    while i < len(value):
        c = value[i]
        if c == '"':
            current += '""'
            i += 1
        elif c == "\r" and i + 1 < len(value) and value[i + 1] == "\n":
            current = _flush_vb_current(parts=parts, current=current)
            parts.append("vbCrLf")
            i += 2
        elif c in char_replacements:
            current = _flush_vb_current(parts=parts, current=current)
            parts.append(char_replacements[c])
            i += 1
        elif ord(c) < control_char_threshold:
            current = _flush_vb_current(parts=parts, current=current)
            parts.append(f"Chr({ord(c)})")
            i += 1
        else:
            current += c
            i += 1
    _flush_vb_current(parts=parts, current=current)
    return parts


@beartype
def _format_string_vb(value: str) -> str:
    r"""Format a string using VB.NET string escaping rules.

    VB.NET strings use ``""`` to escape embedded double quotes and do not
    support backslash escapes.  Control characters such as newlines and
    tabs are expressed via ``vbCrLf``, ``vbTab``, or ``Chr(N)`` string
    concatenation.
    """
    parts = _vb_string_parts(value=value)
    if not parts:
        return '""'
    if len(parts) == 1:
        return parts[0]
    return " & ".join(parts)


def _vb_unique_class_name(*, segment: str, position: int) -> str:
    """Build a stub class name unique to a segment's path position.

    VB.NET is case-insensitive, so two segments that differ only in
    case (or repeat exactly) — e.g. ``app.app.method`` — would
    otherwise produce duplicate ``Class`` declarations.  Suffixing
    with the segment's position in the dotted target keeps every
    generated name distinct.
    """
    return f"{segment.title()}Type_{position}_"


def _vb_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return Visual Basic stub declarations for a call name.

    For a single-name target the stub is a module-level ``Function``
    whose parameter list matches the given names; for a dotted target
    a chain of nested stub classes is emitted so ``a.b.c.d(...)``
    dispatches to a real method whose body returns ``Nothing``.

    Each declaration block is returned as one tuple entry containing
    embedded newlines so that the call-test harness's whole-line
    duplicate filter does not strip repeated structural keywords like
    ``End Class`` or ``End Function`` that legitimately appear in
    every block.
    """
    param_list = ", ".join(f"{p} As Object" for p in params)
    method_block = (
        f"Public Function {{method}}({param_list}) As Object\n"
        f"{indent}Return Nothing\n"
        "End Function"
    )
    if len(parts) == 1:
        return (
            f"Function {parts[0]}({param_list}) As Object\n"
            f"{indent}Return Nothing\n"
            "End Function",
        )
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    method_body = textwrap.indent(
        text=method_block.format(method=method),
        prefix=indent,
    )
    if not fields:
        type_name = _vb_unique_class_name(segment=root, position=0)
        return (
            f"Class {type_name}\n{method_body}\nEnd Class",
            f"Dim {root} As New {type_name}()",
        )
    blocks: list[str] = []
    inner_type = _vb_unique_class_name(
        segment=fields[-1],
        position=len(fields),
    )
    blocks.append(f"Class {inner_type}\n{method_body}\nEnd Class")
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = _vb_unique_class_name(segment=fields[i], position=i + 1)
        blocks.append(
            f"Class {curr_type}\n"
            f"    Public {fields[i + 1]} As New {prev_type}()\n"
            "End Class"
        )
        prev_type = curr_type
    root_type = _vb_unique_class_name(segment=root, position=0)
    blocks.append(
        f"Class {root_type}\n"
        f"    Public {fields[0]} As New {prev_type}()\n"
        "End Class"
    )
    blocks.append(f"Dim {root} As New {root_type}()")
    return tuple(blocks)


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a VB.NET variable declaration."""
    return f"Dim {name} = {value}"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class VisualBasic(metaclass=LanguageCls):
    """Visual Basic (.NET) language specification.

    VB.NET collection initializers (``New T() { ... }``,
    ``New HashSet(Of T) From { ... }``, etc.) do not support comments
    inside the ``{ ... }`` block.  YAML comments associated with
    collection elements are therefore emitted as standalone comment lines
    *before* the collection — or before the variable declaration when a
    variable name is supplied.
    """

    extension = ".vb"
    pygments_name = "vb.net"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    supports_call_variable_binding = True
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
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
    supports_default_dict_key_type = True
    supports_default_dict_value_type = True
    supports_default_sequence_element_type = True
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    supports_non_string_dict_keys = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for VisualBasic."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for VisualBasic."""

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
        """Sequence type options for Visual Basic."""

        ARRAY = enum.auto()

    class SetFormats(enum.Enum):
        """Set type options for Visual Basic."""

        HASH_SET = enum.member(
            value=set_format_factory(
                open_template="New HashSet(Of {type}) From {{",
                close="}}",
                empty_template="New HashSet(Of {type})()",
                preamble_lines=(),
                set_opener_template=("New HashSet(Of {type_name}) From {{"),
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

    class CommentFormats(enum.Enum):
        """Comment style options."""

        APOSTROPHE = CommentConfig(
            prefix="'",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        DIM = DeclarationStyleConfig(
            formatter=_format_variable_declaration,
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template=(
                    "New Dictionary(Of {key_type}, {type}) From {{"
                ),
                close="}",
                format_entry=braced_dict_entry(
                    format_value=passthrough_sequence_entry,
                ),
                empty_template=None,
                preamble_lines=("Imports System.Collections.Generic",),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        )

        def __call__(
            self,
            default_type: str,
            *,
            default_key_type: str = "String",
        ) -> DictFormatConfig:
            """Create a dict format config for the given type."""
            return self.value(
                default_type,
                default_key_type=default_key_type,
            )

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Double.PositiveInfinity",
        negative_infinity="Double.NegativeInfinity",
        nan="Double.NaN",
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
        """VisualBasic call style options."""

        POSITIONAL = PositionalCallStyle()
        NAMED = KeywordCallStyle(separator=":=")

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
        """Version options for Visual Basic."""

        DOTNET_6 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
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
        """Wrap a VB.NET Dim declaration inside a Module.

        When *body_preamble* carries call-stub declarations (``Class``
        and ``Function`` blocks plus their ``Dim ... As New ...``
        instances) the stubs sit at module scope and *content* is
        placed inside ``Sub _calls()``: VB rejects bare expression
        statements at module level, but shared subs taking no
        arguments are invoked by the fixture linter so the calls
        still execute.
        """
        del variable_name
        has_stubs = any(
            line.startswith(("Function ", "Class ")) for line in body_preamble
        )
        if has_stubs:
            preamble_block = "\n".join(body_preamble)
            preamble_indented = textwrap.indent(
                text=preamble_block,
                prefix=self.indent,
            )
            content_indented = textwrap.indent(
                text=content, prefix=self.indent * 2
            )
            return (
                "Module Check\n"
                f"{preamble_indented}\n"
                f"{self.indent}Sub _calls()\n"
                f"{content_indented}\n"
                f"{self.indent}End Sub\n"
                "End Module"
            )
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix=self.indent)
        return f"Module Check\n{indented}\nEnd Module"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap VB.NET declaration + assignment in separate Subs."""
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        decl_indented = textwrap.indent(
            text=declaration, prefix=self.indent * 2
        )
        assign_indented = textwrap.indent(
            text=assignment, prefix=self.indent * 2
        )
        return (
            "Module Check\n"
            f"{self.indent}Sub _declaration()\n"
            f"{decl_indented}\n"
            f"{self.indent}End Sub\n"
            f"{self.indent}Sub _assignment()\n"
            f"{self.indent * 2}Dim {variable_name} As Object\n"
            f"{assign_indented}\n"
            f"{self.indent}End Sub\n"
            "End Module"
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.ARRAY
    set_format: SetFormats = SetFormats.HASH_SET
    default_set_element_type: str = "Object"
    default_sequence_element_type: str = "Object"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "Object"
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.APOSTROPHE
    declaration_style: DeclarationStyles = DeclarationStyles.DIM
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
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the `LanguageVersion` passed to the VB lint host
    # in `.github/scripts/lint-vb/Program.cs`.
    language_version: VersionFormats = VersionFormats.DOTNET_6
    indent: str = "    "

    null_literal: ClassVar[str] = "Nothing"
    true_literal: ClassVar[str] = "True"
    false_literal: ClassVar[str] = "False"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = False
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return _format_string_vb

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=str,
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_vb_ulong_positive,
                language_name="VB.NET",
            ),
        )

    @cached_property
    def format_integer_widened(self) -> Callable[[int], str]:
        """Always-``L``-suffixed integer formatter for widened
        collections (mixed-magnitude int sets/lists).
        """
        return make_overflow_fallback_formatter(
            base=make_long_suffix_formatter(base=str),
            fallback=make_unsigned_overflow_fallback(
                format_positive=_format_vb_ulong_positive,
                language_name="VB.NET",
            ),
        )

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
        return variable_formatter(template="{name} = {value}")

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
        return partial(_vb_call_stub, indent=self.indent)

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config

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
    def _element_to_type(
        self,
    ) -> Callable[[type | ListType | DictType], str | None]:
        """Shared element-to-type mapping used by collection openers."""
        datetime_type = (
            "Integer"
            if self.datetime_format.value.type_produced is int
            else "String"
        )
        return make_element_to_type(
            str_type="String",
            bool_type="Boolean",
            int_type="Integer",
            wide_int_type="Long",
            float_type="Double",
            mixed_numeric_type="Double",
            bytes_type="String",
            date_type="String",
            datetime_type=datetime_type,
            time_type="TimeOnly",
            list_template="{inner}()",
            dict_type_template=None,
            fallback_value_type=None,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        vb_type_to_opener = make_type_to_opener(
            element_to_type=self._element_to_type,
            opener_template="New {type_name}() {{",
        )
        return SequenceFormatConfig(
            sequence_open=typed_collection_open(
                type_to_opener=vb_type_to_opener,
                fallback="New Object() {",
            ),
            close="}",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=f"New {self.default_sequence_element_type}() {{}}",
            preamble_lines=("Imports System.Collections.Generic",),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        base = self.set_format(default_type=self.default_set_element_type)
        return base.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=self._element_to_type,
                opener_template="New HashSet(Of {type_name}) From {{",
            ),
            fallback=base.set_open([]),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return self.dict_format(
            default_type=self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
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
        return format_time_vb

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return ordered_map_format_factory(
            open_template=("New Dictionary(Of {key_type}, {type}) From {{"),
            close="}",
            preamble_lines=(),
        )(
            self.default_dict_value_type,
            default_key_type=self.default_dict_key_type,
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return braced_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble."""
        return {datetime.time: ("Imports System",)}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (VisualBasic needs none)."""
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
