"""Ada language specification."""

import dataclasses
import datetime
import enum
import math
import textwrap
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
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    identity_call_ref_identifier,
    identity_call_statement,
    never_inhibits_consuming_form,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value

_ADA_EMPTY_LITERAL = "AList'[]"

_ADA_FLOAT_SPECIAL_DECLS = {
    "pos_inf": "Pos_Inf : constant Long_Float := 1.0 / Zero;",
    "neg_inf": "Neg_Inf : constant Long_Float := -1.0 / Zero;",
    "nan": "NaN : constant Long_Float := Zero / Zero;",
}


def _ada_special_float_kinds(*, data: Value) -> frozenset[str]:
    """Return which IEEE-special float kinds appear anywhere in *data*.

    Walks lists, dicts, and sets so a nested ``float('inf')`` is still
    detected.  The returned set uses the tags ``pos_inf``, ``neg_inf``,
    and ``nan`` so :meth:`Ada.compute_body_preamble` only emits the
    constants it actually needs.
    """
    kinds: set[str] = set()
    stack: list[Value] = [data]
    while stack:
        item = stack.pop()
        match item:
            case bool():
                continue
            case float() if math.isnan(item):
                kinds.add("nan")
            case float() if math.isinf(item):
                kinds.add("pos_inf" if item > 0 else "neg_inf")
            case list() | set():
                stack.extend(item)
            case dict():
                stack.extend(item.values())
            case _:
                continue
    return frozenset(kinds)


def _ada_narrowed_empty_form(_siblings: Sequence[list[Value]]) -> str:
    """Ada's structured empty literal beside typed siblings.

    ``A_Stub.A_Val`` carries the Ada 2022 ``Aggregate`` aspect, so an
    empty container aggregate is written as ``AList'[]`` — the bracket
    form distinguishes container aggregates from array aggregates.
    """
    return _ADA_EMPTY_LITERAL


@beartype
def _format_ada_entry(original: Value, formatted: str) -> str:
    """Wrap a formatted entry in the appropriate Ada ``A_Val`` constructor."""
    match original:
        case bool():
            return formatted
        case datetime.datetime() if formatted.lstrip("-").isdigit():
            return f"AInt ({formatted})"
        case int():
            return f"AInt ({formatted})"
        case float():
            return f"AFloat ({formatted})"
        case str() | bytes() | datetime.date():
            return f"AStr ({formatted})"
        case _:
            return formatted


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format an Ada object declaration.

    Example: ``"x"`` and ``"AList'[AInt (1)]"`` →
    ``"x : A_Val := AList'[AInt (1)];"``
    """
    wrapped = _format_ada_entry(original=data, formatted=value)
    return f"{name} : A_Val := {wrapped};"


@beartype
def _format_variable_assignment(name: str, value: str, data: Value) -> str:
    """Format an Ada assignment statement to an existing variable.

    Example: ``"x"`` and ``"AList'[AInt (1)]"`` →
    ``"x := AList'[AInt (1)];"``
    """
    wrapped = _format_ada_entry(original=data, formatted=value)
    return f"{name} := {wrapped};"


@beartype
def _ada_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Ada stub declarations for a call expression.

    Stubs go in the declarative section of the enclosing procedure.
    Only the innermost name is used: ``app.client.fetch`` produces the
    same stub as ``fetch``, so that the call site can use a simple
    ``Fetch(...)`` rather than Ada prefix notation (which requires
    package-scope declarations).
    """
    method_ada = parts[-1].title()
    param_list = "; ".join(f"{p.strip('_').title()} : A_Val" for p in params)

    if stub_return is StubReturn.VOID:
        if param_list:
            stub = (
                f"procedure {method_ada} ({param_list})"
                f" is begin null; end {method_ada};"
            )
        else:
            stub = f"procedure {method_ada} is begin null; end {method_ada};"
    elif param_list:
        stub = f"function {method_ada} ({param_list}) return A_Val is (ANull);"
    else:
        stub = f"function {method_ada} return A_Val is (ANull);"
    return (stub,)


@beartype
def _ada_call_target(parts: Sequence[str], /) -> str:
    """Return the title-cased method name for an Ada call expression.

    Ada primitive operations (needed for prefix notation) must be in a
    package spec, not a procedure body.  Using the plain method name
    avoids prefix notation and produces a stub that GNAT can compile.
    """
    return parts[-1].title()


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Ada(metaclass=LanguageCls):
    """Ada language specification."""

    module_name: str = "Check"

    extension = ".adb"
    pygments_name = "ada"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    allows_empty_call_parens = False
    supports_dotted_call_stub = False
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
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
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Ada."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Ada."""

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
        """Sequence type options for Ada."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="AList'["),
            close="]",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=_ADA_EMPTY_LITERAL,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Ada."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="ASet'["),
            close="]",
            empty_set="ASet'[]",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_DASH = CommentConfig(
            prefix="--",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        DECLARE = DeclarationStyleConfig(
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
        positive_infinity="Pos_Inf",
        negative_infinity="Neg_Inf",
        nan="NaN",
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
        """Ada call style options."""

        KEYWORD = KeywordCallStyle(separator=" => ")

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
        """Version options for Ada."""

        ADA_2022 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.PASCAL
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

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Ada call stubs and variable declarations alongside calls.

        Stubs and variable declarations go in the declarative section;
        call expressions go in the executable section.
        """
        return self.wrap_in_file(
            content=calls,
            variable_name="",
            body_preamble=(*body_preamble, *declarations),
        )

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap an Ada object declaration or call block inside a procedure.

        When *variable_name* is non-empty (variable declaration mode),
        *body_preamble* and *content* go in the declarative section and
        the executable section contains only ``null;``.  When
        *variable_name* is empty (call mode), *body_preamble* (stubs)
        goes in the declarative section and *content* (calls) goes in
        the executable section.
        """
        if variable_name:
            content = prepend_body_preamble(
                content=content,
                body_preamble=body_preamble,
            )
            indented = textwrap.indent(text=content, prefix=self.indent)
            return (
                "with A_Stub; use A_Stub;\n"
                f"procedure {self.module_name} is\n{indented}\n"
                f"begin\n{self.indent}null;\nend {self.module_name};"
            )
        calls_indented = textwrap.indent(text=content, prefix=self.indent)
        decl_section = textwrap.indent(
            text="\n".join(body_preamble), prefix=self.indent
        )
        return "\n".join(
            part
            for part in [
                "with A_Stub; use A_Stub;",
                f"procedure {self.module_name} is",
                decl_section,
                "begin",
                calls_indented,
                f"end {self.module_name};",
            ]
            if part
        )

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Ada declaration + assignment in a single procedure.

        Earlier revisions wrapped each form in its own nested
        ``Check_Declaration`` / ``Check_Assignment`` procedure, but the
        assignment then referenced ``my_data`` from a sibling scope and
        only compiled because the lint job did syntax-only checking.
        Putting both in one procedure keeps the variable in scope so
        the fixture compiles and runs end-to-end.
        """
        del variable_name
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        decl_indented = textwrap.indent(text=declaration, prefix=self.indent)
        assign_indented = textwrap.indent(text=assignment, prefix=self.indent)
        return (
            "with A_Stub; use A_Stub;\n"
            f"procedure {self.module_name} is\n"
            f"{decl_indented}\n"
            "begin\n"
            f"{assign_indented}\n"
            f"end {self.module_name};"
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_DASH
    declaration_style: DeclarationStyles = DeclarationStyles.DECLARE
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
    call_style: CallStyles = CallStyles.KEYWORD
    language_version: VersionFormats = VersionFormats.ADA_2022
    indent: str = "    "

    null_literal: ClassVar[str] = "ANull"
    true_literal: ClassVar[str] = "ABool (True)"
    false_literal: ClassVar[str] = "ABool (False)"
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
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=str,
            fallback=raise_for_unrepresentable_int(language_name="Ada"),
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return _format_ada_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_ada_entry

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
        return _ada_call_stub

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
        return _ada_call_target

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap a call argument in the appropriate A_Val constructor."""
        return _format_ada_entry

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
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            narrowed_empty_form=_ada_narrowed_empty_form,
        )

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
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(open_str="AMap'["),
            close="]",
            format_entry=dict_entry_with_template(
                template="AEntry ({key}, {value})",
                format_value=_format_ada_entry,
            ),
            empty_dict="AMap'[]",
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
        """Callable that formats a string value as a quoted literal.

        Ada distinguishes ``String`` from ``Character``, so a literal
        consisting solely of ``Character'Val(N)`` would not satisfy the
        ``AStr (S : String)`` constructor.  Prepend an empty string in
        that case so the ``&`` operator widens the result to ``String``.
        """
        inner = format_string_concat_control(
            quote_char='"',
            quote_escape='""',
            control_char_template="Character'Val({})",
            concat_operator=" & ",
            escape_backslash=False,
        )

        def _format(value: str) -> str:
            """Widen a bare ``Character'Val(N)`` result to ``String``."""
            formatted = inner(value)
            if formatted.startswith("Character'Val"):
                return f'"" & {formatted}'
            return formatted

        return _format

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
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="AMap'["),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_template(
            template="AEntry ({key}, {value})",
            format_value=_format_ada_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Ada needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Ada needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Emit local IEEE-special constants when needed.

        Ada has no portable inline literal for ``+Inf``, ``-Inf`` or
        ``NaN``: GNAT statically rejects ``1.0 / 0.0`` with
        ``static expression fails Constraint_Check``.  When the data
        contains one of these IEEE specials, declare matching local
        constants in the enclosing procedure's declarative part using
        a volatile zero denominator so GNAT cannot constant-fold the
        division, and suppress ``Division_Check`` so the IEEE result
        propagates instead of raising ``Constraint_Error`` at runtime.
        """

        def _compute(
            types: frozenset[type],
            data: Value,
            /,
        ) -> tuple[str, ...]:
            """Build the IEEE-special constant declarations for *data*."""
            del types
            kinds = _ada_special_float_kinds(data=data)
            if not kinds:
                return ()
            return (
                "pragma Suppress (Division_Check);",
                "Zero : Long_Float := 0.0;",
                "pragma Volatile (Zero);",
                *(_ADA_FLOAT_SPECIAL_DECLS[kind] for kind in sorted(kinds)),
            )

        return _compute
