"""COBOL language specification (GnuCOBOL free-format)."""

import dataclasses
import datetime
import enum
import re
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
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    strip_key_quotes,
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
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    CallStyle,
    CommandCallStyle,
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
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_wrap_calls_with_declarations,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Value
from literalizer.exceptions import CallArgNotSupportedError

_COBOL_EMPTY_LITERAL = "05 FILLER PIC X(1) VALUE SPACES."


def _cobol_narrowed_empty_form(_siblings: Sequence[list[Value]]) -> str:
    """Keep COBOL's structured empty literal beside typed siblings.

    Inheriting a sibling's COMP-5 group opener for the empty slot
    would produce a malformed COBOL record; the language's
    ``PIC X(1) VALUE SPACES`` placeholder is the structurally valid
    empty form here.
    """
    return _COBOL_EMPTY_LITERAL


@beartype
def _format_string_cobol(value: str) -> str:
    """Format a COBOL alphanumeric string literal.

    Control characters (newlines, tabs, carriage returns) are replaced
    with spaces because COBOL string literals cannot span multiple lines
    and have no escape sequences.  Double quotes are escaped by doubling
    them, then the whole string is wrapped in double quotes.

    Example: ``say "hi" loud`` becomes ``"say ""hi"" loud"``.
    """
    cleaned = value
    for char, replacement in {"\n": " ", "\r": " ", "\t": " "}.items():
        cleaned = cleaned.replace(char, replacement)
    escaped = cleaned.replace('"', '""')
    return f'"{escaped}"'


@beartype
def _is_data_entry(s: str) -> bool:
    """Return True if *s* looks like a COBOL DATA DIVISION entry.

    A DATA DIVISION entry starts with two decimal digits followed by a
    space (e.g. ``05 FILLER ...``).
    """
    return bool(re.match(pattern=r"^\d{2} ", string=s))


@beartype
def _pic_from_value(value: str) -> str:
    """Return a COBOL PIC (or storage) clause for a formatted literal.

    Inspects the pre-formatted value string to choose the narrowest
    appropriate clause.
    """
    if value == "SPACES":
        return "PIC X(1)"
    if value in {'"TRUE"', '"FALSE"'}:
        return "PIC X(5)"
    if value.startswith('"') and value.endswith('"'):
        inner = value[1:-1].replace('""', '"')
        return f"PIC X({max(1, len(inner))})"
    if re.match(pattern=r"^-?\d+$", string=value):
        return "PIC S9(18) COMP-5"
    # Float or other numeric
    return "COMP-2"


@beartype
def _to_cobol_entry(value: str, name: str, level: int) -> str:
    """Wrap a scalar literal in a COBOL DATA DIVISION entry.

    Example: ``"42"`` → ``"05 FILLER PIC S9(18) COMP-5 VALUE 42."``
    """
    picture_clause = _pic_from_value(value=value)
    return f"{level:02d} {name} {picture_clause} VALUE {value}."


@beartype
def _bump_levels(content: str) -> str:
    """Increment every COBOL level number in *content* by 5.

    Only lines whose first non-space token is a two-digit level number
    are modified.
    """

    def _bump(m: re.Match[str]) -> str:
        """Return the matched level-number prefix with its level
        incremented by 5.
        """
        new_level = min(int(m.group(2)) + 5, 49)
        return f"{m.group(1)}{new_level:02d}{m.group(3)}"

    return re.sub(
        pattern=r"^(\s*)(\d{2})(\s)",
        repl=_bump,
        string=content,
        flags=re.MULTILINE,
    )


@beartype
def _format_cobol_sequence_entry(_original: Value, item: str) -> str:
    """Format a sequence item as a COBOL DATA DIVISION entry.

    Scalar values become ``05 FILLER PIC … VALUE …`` items.
    Nested collections are wrapped in a ``05 FILLER.`` group with
    inner level numbers bumped by 5.
    """
    if "\n" in item:
        bumped = _bump_levels(content=item)
        return f"05 FILLER.\n{bumped}"
    if _is_data_entry(s=item.strip()):
        return item.strip()
    return _to_cobol_entry(value=item, name="FILLER", level=5)


@beartype
def _key_to_cobol_name(key_str: str) -> str:
    """Convert a formatted COBOL string literal to a valid COBOL data name.

    Strips outer quotes, converts doubled double-quotes back to single,
    converts the result to upper case, replaces non-alphanumeric characters
    with hyphens, and adds the ``F-`` prefix to avoid clashes with COBOL
    reserved words.  The result is truncated to 28 characters (leaving
    room for the prefix).
    """
    name = strip_key_quotes(key=key_str).replace('""', '"')
    name = name.upper()
    name = re.sub(pattern=r"[^A-Z0-9]", repl="-", string=name)
    name = re.sub(pattern=r"-+", repl="-", string=name).strip("-")
    name = name[:28].strip("-") or "FILLER"
    return f"F-{name}"


@beartype
def _format_cobol_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format a COBOL DATA DIVISION entry for a dict key-value pair.

    The key string is converted to a valid COBOL data name.  Scalar
    values produce elementary items; nested collections produce group
    items with bumped level numbers.
    """
    name = _key_to_cobol_name(key_str=key)
    if "\n" in formatted_value:
        bumped = _bump_levels(content=formatted_value)
        return f"05 {name}.\n{bumped}"
    if _is_data_entry(s=formatted_value.strip()):
        bumped = _bump_levels(content=formatted_value.strip())
        return f"05 {name}.\n{bumped}"
    picture_clause = _pic_from_value(value=formatted_value)
    return f"05 {name} {picture_clause} VALUE {formatted_value}."


@beartype
def _to_cobol_name(python_name: str) -> str:
    """Convert a Python-style identifier to a COBOL data name.

    Converts the name to upper case and replaces underscores with hyphens.
    """
    return python_name.upper().replace("_", "-")


@beartype
def _cobol_call_target(parts: Sequence[str], /) -> str:
    """Return the COBOL CALL literal and USING keyword for a call target.

    Only the innermost name is used: ``app.client.fetch`` produces
    ``"FETCH" USING`` so that the call site emits
    ``CALL "FETCH" USING BY CONTENT ...``.
    """
    return f'"{_to_cobol_name(python_name=parts[-1])}" USING'


@beartype
def _cobol_format_call_arg(_value: Value, formatted: str, /) -> str:
    """Prepend ``BY CONTENT`` to a COBOL CALL argument."""
    return f"BY CONTENT {formatted}"


@beartype
def _cobol_call_statement(call: str, /) -> str:
    """Wrap a COBOL call expression as a complete CALL statement."""
    return f"CALL {call}."


@beartype
def _cobol_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return a nested COBOL program stub for a call target.

    The stub is a minimal nested program that accepts any arguments
    and stops immediately, acting as a valid placeholder for the
    called subprogram.
    """
    name = _to_cobol_name(python_name=parts[-1])
    stub = "\n".join(
        [
            "IDENTIFICATION DIVISION.",
            f"PROGRAM-ID. {name}.",
            "PROCEDURE DIVISION.",
            f"{indent}STOP RUN.",
            f"END PROGRAM {name}.",
        ]
    )
    return (stub,)


@beartype
def _format_variable_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a COBOL 01-level variable declaration.

    Scalars become an elementary 01-level item; collections become a
    group 01-level item containing 05-level sub-items.
    """
    cobol_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(s=scalar):
        return f"01 {cobol_name}.\n{stripped}"
    picture_clause = _pic_from_value(value=scalar)
    return f"01 {cobol_name} {picture_clause} VALUE {scalar}."


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a COBOL PROCEDURE DIVISION assignment statement.

    Scalars use a ``MOVE … TO …`` statement; complex group items use
    ``INITIALIZE`` (which resets alphanumeric sub-items to SPACES and
    numeric sub-items to ZEROS).
    """
    cobol_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(s=scalar):
        return f"INITIALIZE {cobol_name}."
    return f"MOVE {scalar} TO {cobol_name}."


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Cobol(metaclass=LanguageCls):
    """GnuCOBOL free-format language specification.

    Data is represented as COBOL WORKING-STORAGE SECTION level items:
    scalars become elementary data items with VALUE clauses, and
    sequences / dicts become group items with 05-level sub-items.
    """

    extension = ".cob"
    pygments_name = "cobol"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    call_returns_expression = False
    supports_inline_multiline_dict_args = False
    supports_module_name = False

    class DateFormats(enum.Enum):
        """Date format options for Cobol."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Cobol."""

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
        """Sequence type options for COBOL."""

        SEQUENCE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str=""),
            close="",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=_COBOL_EMPTY_LITERAL,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for COBOL."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str=""),
            close="",
            empty_set=_COBOL_EMPTY_LITERAL,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        STAR_ANGLE = CommentConfig(
            prefix="*>",
            suffix="",
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
        positive_infinity="9.99E99",
        negative_infinity="-9.99E99",
        nan="0.0",
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

        SEMICOLON = enum.auto()

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Cobol call style options."""

        POSITIONAL = CommandCallStyle(arg_separator=" ")

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
        """Version options for COBOL."""

        V2002 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.UPPER_SNAKE,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    _PROGRAM_PREFIX: ClassVar[str] = (
        "IDENTIFICATION DIVISION.\n"
        "PROGRAM-ID. CHECK.\n"
        "DATA DIVISION.\n"
        "WORKING-STORAGE SECTION.\n"
    )
    _PROGRAM_SUFFIX: ClassVar[str] = "PROCEDURE DIVISION.\n    STOP RUN."

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a COBOL variable declaration or call block in a program.

        In variable-declaration mode (*variable_name* is non-empty),
        *content* goes in the DATA DIVISION and *body_preamble* is
        prepended before it.  In call mode (*variable_name* is empty),
        *content* holds PROCEDURE DIVISION statements and *body_preamble*
        holds nested-program stubs that follow ``STOP RUN.``.
        """
        if variable_name:
            content = prepend_body_preamble(
                content=content,
                body_preamble=body_preamble,
            )
            return (
                Cobol._PROGRAM_PREFIX + f"{content}\n" + Cobol._PROGRAM_SUFFIX
            )
        indented = textwrap.indent(text=content, prefix=self.indent)
        if body_preamble:
            stubs = "\n".join(body_preamble)
            return (
                Cobol._PROGRAM_PREFIX
                + "PROCEDURE DIVISION.\n"
                + f"{indented}\n"
                + f"{self.indent}STOP RUN.\n"
                + f"{stubs}\n"
                + "END PROGRAM CHECK."
            )
        return (  # pragma: no cover
            Cobol._PROGRAM_PREFIX
            + "PROCEDURE DIVISION.\n"
            + f"{indented}\n"
            + f"{self.indent}STOP RUN."
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap COBOL declaration and assignment in a complete program."""
        del variable_name
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        return (
            Cobol._PROGRAM_PREFIX
            + f"{declaration}\n"
            + "PROCEDURE DIVISION.\n"
            + f"    {assignment}\n"
            + "    STOP RUN."
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.SEQUENCE
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.STAR_ANGLE
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
    language_version: VersionFormats = VersionFormats.V2002
    indent: str = "    "

    null_literal: ClassVar[str] = "SPACES"
    true_literal: ClassVar[str] = '"TRUE"'
    false_literal: ClassVar[str] = '"FALSE"'
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = "\n"
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return _format_string_cobol

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=str,
            fallback=raise_for_unrepresentable_int(language_name="Cobol"),
        )

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return _format_cobol_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return _format_cobol_sequence_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return _format_variable_assignment

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry."""
        return _format_cobol_dict_entry

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
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return nested-program stub declarations for a call
        expression.
        """
        return partial(_cobol_call_stub, indent=self.indent)

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Return the quoted COBOL program name and USING keyword."""
        return _cobol_call_target

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Prepend ``BY CONTENT`` to each COBOL CALL argument."""
        return _cobol_format_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Wrap a call expression as a complete COBOL CALL statement."""
        return _cobol_call_statement

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Raise for any ``{"$ref": "name"}`` identifier.

        COBOL DATA DIVISION VALUE clauses only accept literals, not
        identifier references, so refs are not supported.
        """

        def _raise_for_cobol_ref(name: str, /) -> str:
            """Raise ``CallArgNotSupportedError`` unconditionally."""
            raise CallArgNotSupportedError(
                language_name="COBOL",
                reason=(
                    "COBOL DATA DIVISION VALUE clauses only accept "
                    f"literals, not identifier references (got {name!r})"
                ),
            )

        return _raise_for_cobol_ref

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
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            narrowed_empty_form=_cobol_narrowed_empty_form,
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
            dict_open=fixed_open(open_str=""),
            close="",
            format_entry=_format_cobol_dict_entry,
            empty_dict=_COBOL_EMPTY_LITERAL,
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
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=""),
            close="",
            preamble_lines=(),
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (COBOL needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (COBOL needs none)."""
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
