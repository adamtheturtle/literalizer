"""Language protocol and internal spec dataclass."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable, Sequence
from typing import Protocol, assert_never, runtime_checkable

import humps
from beartype import beartype

from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import DictType, ListType
from literalizer._types import Value


@dataclasses.dataclass(frozen=True)
class SequenceFormatConfig:
    """Configuration for a single sequence format."""

    sequence_open: Callable[[list[Value]], str]
    close: str
    supports_heterogeneity: bool
    single_element_trailing_comma: bool
    supports_trailing_comma: bool
    empty_sequence: str | None
    preamble_lines: tuple[str, ...]
    format_entry: Callable[[Value, str], str]
    typed_opener_fallback: str | None
    uses_typed_literal_for_scalars: bool
    requires_uniform_record_shapes: bool
    declared_type: str | None
    narrowed_empty_form: Callable[[Sequence[list[Value]]], str] | None


@dataclasses.dataclass(frozen=True)
class DateFormatConfig:
    """Configuration for a single date format."""

    formatter: Callable[[datetime.date], str]
    preamble_lines: tuple[str, ...] = ()
    type_produced: type = datetime.date


@dataclasses.dataclass(frozen=True)
class DatetimeFormatConfig:
    """Configuration for a single datetime format."""

    formatter: Callable[[datetime.datetime], str]
    preamble_lines: tuple[str, ...] = ()
    type_produced: type = datetime.datetime


@beartype
def date_scalar_preamble(
    *,
    date_format: enum.Enum,
    datetime_format: enum.Enum,
    extra: dict[type, tuple[str, ...]] | None = None,
) -> dict[type, tuple[str, ...]]:
    """Build the ``scalar_preamble`` dict for date/datetime formats.

    Args:
        date_format: The date format enum member whose ``.value`` has
            a ``preamble_lines`` attribute.
        datetime_format: The datetime format enum member whose ``.value``
            has a ``preamble_lines`` attribute.
        extra: Optional additional type→preamble mappings to include
            unconditionally (e.g. for C++ ``#include <string>``).

    Returns:
        A dict mapping Python types to their required preamble lines,
        omitting entries whose preamble is empty.
    """
    return {
        **(extra or {}),
        **{
            t: p
            for t, p in (
                (datetime.date, date_format.value.preamble_lines),
                (datetime.datetime, datetime_format.value.preamble_lines),
            )
            if p
        },
    }


@dataclasses.dataclass(frozen=True)
class SetFormatConfig:
    """Configuration for a single set format."""

    set_open: Callable[[list[Value]], str]
    close: str
    empty_set: str | None
    preamble_lines: tuple[str, ...]
    set_opener_template: str
    supports_heterogeneity: bool
    supports_trailing_comma: bool

    def with_typed_opener(
        self,
        *,
        type_to_opener: Callable[[type | ListType | DictType], str | None],
        fallback: str,
    ) -> "SetFormatConfig":
        """Return a copy with ``set_open`` replaced by a typed opener.

        The *type_to_opener* callable is used to infer the opener from the
        element type.  When inference fails, *fallback* is used instead.
        """
        return dataclasses.replace(
            self,
            set_open=typed_collection_open(
                type_to_opener=type_to_opener,
                fallback=fallback,
            ),
        )


@dataclasses.dataclass(frozen=True)
class CommentConfig:
    """Configuration for language comment syntax."""

    prefix: str
    suffix: str


@dataclasses.dataclass(frozen=True)
class DictFormatConfig:
    """Configuration for dict formatting."""

    dict_open: Callable[[dict[str, Value]], str]
    close: str
    format_entry: Callable[[str, Value, str], str]
    empty_dict: str | None
    preamble_lines: tuple[str, ...]
    narrowed_open: str | None
    supports_trailing_comma: bool


@dataclasses.dataclass(frozen=True)
class OrderedMapFormatConfig:
    """Configuration for ordered-map formatting."""

    ordered_map_open: Callable[[dict[str, Value]], str]
    close: str
    preamble_lines: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class TrailingCommaConfig:
    """Configuration for trailing-comma behavior.

    When ``multiline_trailing_comma`` is ``True``, trailing commas are added
    to multiline collections where the chosen format supports them.
    Some sequence formats (e.g. Java's ``List.of()``) do not support trailing
    commas; in those cases the trailing comma is omitted regardless of this
    setting.
    """

    multiline_trailing_comma: bool


@dataclasses.dataclass(frozen=True)
class DeclarationStyleConfig:
    """Configuration for a single declaration style."""

    formatter: Callable[[str, str, Value, frozenset[enum.Enum]], str]
    supports_redefinition: bool


@dataclasses.dataclass(frozen=True)
class PositionalCallStyle:
    """Positional arguments only: ``func(value1, value2)``."""


@dataclasses.dataclass(frozen=True)
class KeywordCallStyle:
    """Named arguments: ``func(name=value)``.

    *separator* is the string placed between the parameter name and its
    value (e.g. ``"="`` for Python, ``": "`` for Ruby).
    """

    separator: str


@dataclasses.dataclass(frozen=True)
class ObjectCallStyle:
    """Arguments wrapped in an object literal: ``func({ name: value })``.

    *separator* is the string placed between the parameter name and its
    value inside the object literal (e.g. ``": "`` for JavaScript).
    """

    separator: str


@dataclasses.dataclass(frozen=True)
class PostfixCallStyle:
    """Postfix (stack) calls: ``value1 value2 func``.

    Used by stack-based languages like Forth where arguments are
    pushed onto the stack before the word is invoked.  *arg_separator*
    is the string placed between arguments.
    """

    arg_separator: str


@dataclasses.dataclass(frozen=True)
class PrefixCallStyle:
    """S-expression-style calls: ``(func value1 value2)``.

    Used by Lisp-family languages (Racket, Scheme, Common Lisp,
    Clojure) where the function and its arguments are wrapped
    together in one pair of parentheses.  *arg_separator* is the
    string between arguments (typically a single space).

    Arguments are emitted as
    ``{keyword_prefix}{name}{arg_separator}{value}`` pairs (e.g.
    Racket's ``#:user_id "u"``).
    """

    arg_separator: str
    keyword_prefix: str


@dataclasses.dataclass(frozen=True)
class CommandCallStyle:
    """Shell-command-style calls: ``func value1 value2``.

    Used by shell languages (Bash, POSIX sh) and Tcl where the function
    name is followed by space-separated positional arguments with no
    surrounding parentheses.  *arg_separator* is the string between
    the target and each argument (typically a single space).

    When a ``call_transform`` like ``lambda c: f"emit({c})"`` is
    supplied, the wrapper word is extracted and the inner call is
    formatted using *wrapped_call_template*, a ``str.format``-style
    template with ``{wrapper}`` and ``{inner}`` placeholders (e.g.
    the default ``'{wrapper} "$({inner})"'`` produces
    ``emit "$(target arg1 arg2)"`` for Bash; Tcl uses
    ``'{wrapper} [{inner}]'`` instead).
    """

    arg_separator: str
    wrapped_call_template: str = '{wrapper} "$({inner})"'


CallStyle = (
    PositionalCallStyle
    | KeywordCallStyle
    | ObjectCallStyle
    | PostfixCallStyle
    | PrefixCallStyle
    | CommandCallStyle
)
"""Tagged union describing how a language passes call arguments."""


class CallSupport(enum.Enum):
    """Sentinel describing why a language does not have a
    :class:`CallStyle` configured.
    """

    NOT_IN_LANGUAGE = "not_in_language"
    """The target language has no function call syntax (e.g. pure
    data/markup formats like YAML, TOML, JSON5, Norg).
    """

    NOT_IMPLEMENTED_BY_TOOL = "not_implemented_by_tool"
    """The target language has function call syntax but literalizer
    has not yet implemented call rendering for it.
    """


class Support(enum.Enum):
    """Three-way enum describing the level of support for a language
    capability.

    Modeled on :class:`CallSupport` but for capabilities where there is
    no accompanying configuration object.
    """

    NOT_IN_LANGUAGE = "not_in_language"
    """The target language has no syntax for this feature."""

    NOT_IMPLEMENTED_BY_TOOL = "not_implemented_by_tool"
    """The target language has syntax for this feature but literalizer
    has not yet implemented it.
    """

    SUPPORTED = "supported"
    """The target language supports this feature and literalizer has
    implemented it.
    """


class FloatSpecialsMixin:
    """Mixin for ``FloatFormats`` enums that provides ``__call__``.

    Subclasses pass ``positive_infinity``, ``negative_infinity``, and
    ``nan`` as keyword arguments to the class definition.  The mixin
    stores them and provides a ``__call__`` that handles the
    ``isinf``/``isnan`` dispatch, delegating finite values to the enum
    member's formatter.
    """

    _positive_infinity: str
    _negative_infinity: str
    _nan: str
    _formatter: Callable[[float], str]

    def __init_subclass__(
        cls,
        *,
        positive_infinity: str,
        negative_infinity: str,
        nan: str,
    ) -> None:
        """Store float-special strings as class attributes."""
        super().__init_subclass__()
        cls._positive_infinity = positive_infinity
        cls._negative_infinity = negative_infinity
        cls._nan = nan

    def __init__(self, formatter: Callable[[float], str], /) -> None:
        """Capture the per-member formatter from the enum value."""
        self._formatter = formatter

    def __call__(self, value: float, /) -> str:
        """Format a float, handling inf and nan."""
        if math.isinf(value):
            if value < 0:
                return self._negative_infinity
            return self._positive_infinity
        if math.isnan(value):
            return self._nan
        return self._formatter(value)


class StubReturn(enum.Enum):
    """Whether a call stub should return a value or void."""

    VOID = "void"
    VALUE = "value"


class IdentifierCase(enum.Enum):
    """A naming convention for a single identifier.

    Passed to :func:`~literalizer.literalize_call` via ``ref_case`` to
    convert ``{"$ref": "name"}`` markers to the target language's
    idiomatic case at render time.  Each :class:`Language` exposes the
    subset it understands via its nested ``IdentifierCases`` enum.
    """

    SNAKE = "snake"
    """``snake_case`` — e.g. ``user_obj``."""

    CAMEL = "camel"
    """``camelCase`` — e.g. ``userObj``."""

    PASCAL = "pascal"
    """``PascalCase`` — e.g. ``UserObj``."""

    UPPER_SNAKE = "upper_snake"
    """``UPPER_SNAKE_CASE`` — e.g. ``USER_OBJ``."""

    KEBAB = "kebab"
    """``kebab-case`` — e.g. ``user-obj``."""

    def convert(self, *, name: str) -> str:
        """Return *name* converted to this case.

        Normalizes any input convention to ``snake_case`` first so the
        conversion is deterministic even when the source identifier
        does not follow the recommended ``snake_case`` authoring
        convention.  Acronyms are lost in normalization
        (``HTTPRequest`` becomes ``http_request`` and then
        ``HttpRequest``), so passing ``snake_case`` input when
        exact-round-trip matters is recommended.
        """
        return _convert_identifier_case(case=self, name=name)


def _convert_identifier_case(*, case: IdentifierCase, name: str) -> str:
    """Convert *name* to *case* with snake_case normalization.

    Extracted from :meth:`IdentifierCase.convert` as a free function
    so the ``match`` exhaustiveness check narrows on the plain
    :class:`IdentifierCase` parameter rather than on ``self``, which
    some type checkers (notably pyrefly) treat as the broader
    ``Self@IdentifierCase`` and reject as non-exhaustive.
    """
    snake = humps.decamelize(
        str_or_iter=humps.dekebabize(str_or_iter=name),
    ).lower()
    match case:
        case IdentifierCase.SNAKE:
            return snake
        case IdentifierCase.CAMEL:
            return humps.camelize(str_or_iter=snake)
        case IdentifierCase.PASCAL:
            return humps.pascalize(str_or_iter=snake)
        case IdentifierCase.UPPER_SNAKE:
            return snake.upper()
        case IdentifierCase.KEBAB:
            return humps.kebabize(str_or_iter=snake)
        case _ as unreachable:
            assert_never(unreachable)


@dataclasses.dataclass(frozen=True)
class HeterogeneousBehavior:
    """Per-language hook describing how heterogeneous scalar
    collections are rendered.

    ``skip_scalar_checks`` tells :func:`~literalizer._checks.check_data`
    to skip the four scalar-heterogeneity checks when the language has
    opted into a wrapping strategy that handles mixed scalars at
    render time.

    ``compute_wrap_ids`` pre-walks the data once and returns the ids
    of containers whose scalar children must be wrapped.

    ``wrap_scalar`` wraps a formatted scalar value (e.g. Rust's
    tagged-enum ``Value::Variant(…)``).  For non-scalar inputs the
    implementation is expected to return *formatted* unchanged.

    Languages that do not wrap expose
    :data:`NO_HETEROGENEOUS_BEHAVIOR`.
    """

    skip_scalar_checks: bool
    compute_wrap_ids: Callable[[Value], frozenset[int]]
    wrap_scalar: Callable[[Value, str], str]


def _no_compute_wrap_ids(_data: Value, /) -> frozenset[int]:
    """Return an empty wrap-id set — used by non-wrapping languages."""
    return frozenset()


def _no_wrap_scalar(_raw: Value, formatted: str, /) -> str:
    """Return *formatted* unchanged — used by non-wrapping languages."""
    return formatted


NO_HETEROGENEOUS_BEHAVIOR = HeterogeneousBehavior(
    skip_scalar_checks=False,
    compute_wrap_ids=_no_compute_wrap_ids,
    wrap_scalar=_no_wrap_scalar,
)
"""Shared behavior for languages that do not wrap heterogeneous scalar
values.
"""


@dataclasses.dataclass(frozen=True)
class ModifierCombination:
    """A named combination of declaration modifiers for a language.

    Languages that support declaration modifiers (e.g. Java ``public
    static final``, C# ``public static readonly``, C++ ``static const``)
    expose their canonical multi-modifier combinations via
    :attr:`LanguageCls.modifier_combinations`.
    """

    name: str
    """Identifier for this combination, used in generated code."""

    modifiers: frozenset[enum.Enum]
    """The set of modifier enum members that make up this combination."""


class LanguageCls(type):
    """Meta-class that declares the nested format Enum class attributes.

    Language classes use ``metaclass=LanguageCls`` so that downstream
    code can write ``dict[str, LanguageCls]`` and access
    ``cls.DateFormats``, ``cls.SequenceFormats``, etc. without ``cast``
    or ``type: ignore``.
    """

    DateFormats: type[enum.Enum]
    DatetimeFormats: type[enum.Enum]
    BytesFormats: type[enum.Enum]
    SequenceFormats: type[enum.Enum]
    SetFormats: type[enum.Enum]
    CommentFormats: type[enum.Enum]
    VariableTypeHints: type[enum.Enum]
    DeclarationStyles: type[enum.Enum]
    DictEntryStyles: type[enum.Enum]
    DictFormats: type[enum.Enum]
    EmptyDictKey: type[enum.Enum]
    FloatFormats: type[enum.Enum]
    IntegerFormats: type[enum.Enum]
    NumericLiteralSuffixes: type[enum.Enum]
    NumericSeparators: type[enum.Enum]
    NumericStyles: type[enum.Enum]
    StringFormats: type[enum.Enum]
    TrailingCommas: type[enum.Enum]
    LineEndings: type[enum.Enum]
    CallStyles: type[enum.Enum]
    Modifiers: type[enum.Enum]
    HeterogeneousStrategies: type[enum.Enum]
    identifier_cases: tuple[IdentifierCase, ...]
    modifier_combinations: tuple[ModifierCombination, ...] = ()
    module_name_case: IdentifierCase
    extension: str
    pygments_name: str | None
    variable_name_support: Support
    dotted_call_support: Support

    def __call__(cls, *args: object, **kwargs: object) -> "Language":
        """Construct a language instance, typed as :class:`Language`."""
        instance: Language = super().__call__(*args, **kwargs)
        return instance


@runtime_checkable
class Language(Protocol):
    """Protocol describing how a language formats scalar literals and
    sequences.

    Predefined instances for common languages are available as module-level
    constants in :mod:`literalizer.languages` (e.g.
    :data:`~literalizer.languages.PYTHON`,
    :data:`~literalizer.languages.JAVASCRIPT`). To support additional
    languages or override defaults, write a class that provides all the
    required attributes.
    """

    # Each language class defines PascalCase nested Enum classes
    # (``DateFormats``, ``SequenceFormats``, …) and snake_case class
    # attributes that alias them (``date_formats = DateFormats``, …).
    # The aliases look redundant but are required: nested classes are
    # class-level (ClassVar) attributes, while Protocol properties are
    # instance-level.  No single declaration style (``@property``,
    # ``ClassVar``, or plain annotation) satisfies mypy, pyright, *and*
    # pyrefly simultaneously for PascalCase names that shadow nested
    # classes.  The snake_case aliases sidestep the issue entirely.

    @property
    def bytes_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the bytes formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the sequence formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the set formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def date_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the date formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def datetime_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the datetime formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the comment formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_type_hints_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the variable type hint options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def declaration_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the declaration style options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_entry_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the dict entry style options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the dict/map format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def float_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the float format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def integer_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the integer format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_literal_suffixes(self) -> type[enum.Enum]:
        """Enum class whose members list the numeric literal suffix
        options this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_separators(self) -> type[enum.Enum]:
        """Enum class whose members list the numeric separator options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the numeric literal style
        options this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def string_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the string format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_commas(self) -> type[enum.Enum]:
        """Enum class whose members list the trailing comma options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def line_endings(self) -> type[enum.Enum]:
        """Enum class whose members list the line ending options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def call_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the call style options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def modifiers(self) -> type[enum.Enum]:
        """Enum class whose members list the declaration modifiers
        this language supports.

        Languages without modifier vocabulary expose an empty enum.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def heterogeneous_strategies(self) -> type[enum.Enum]:
        """Enum class whose members list the heterogeneous-scalar
        strategies this language supports.

        Languages that only know how to raise on heterogeneous scalar
        collections expose a single-member enum whose only option is
        ``ERROR``.  Languages with richer strategies (e.g. Rust's
        ``TAGGED_ENUM``) expose additional members.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def identifier_cases(self) -> tuple[IdentifierCase, ...]:
        """Identifier case conventions this language supports for
        ``$ref`` conversion.

        Ordered by idiomatic preference — the first element is the
        language's default case.  Passing a :class:`IdentifierCase`
        to :func:`~literalizer.literalize_call` via ``ref_case`` is
        rejected with
        :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`
        unless it is in this tuple.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    extension: str
    """The file extension for this language, including the leading dot."""

    @property
    def pygments_name(self) -> str | None:
        """The Pygments lexer short name for syntax highlighting.

        ``None`` if Pygments does not support this language.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def null_literal(self) -> str:
        """The literal representing null/None."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def true_literal(self) -> str:
        """The literal representing true/True."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def false_literal(self) -> str:
        """The literal representing false/False."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Receives the list of items about to be formatted, so the delimiter
        can depend on the element types when needed.  For a fixed delimiter
        use :func:`~literalizer.fixed_open`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior.

        Trailing commas are only added to collection formats that support
        them.  See :class:`TrailingCommaConfig` for details.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a :class:`bytes` value as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a :class:`datetime.date` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a :class:`datetime.datetime` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a sequence entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Callable that formats a set entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def indent(self) -> str:
        """The indentation step for elements inside delimiters in
        multi-line structures (e.g. ``"    "`` for 4-space indent).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def indent_closing_delimiter(self) -> bool:
        """Whether to indent the closing delimiter of multi-line
        structures by one ``indent`` step.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def element_separator(self) -> str:
        """The separator placed between elements in inline sequences."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def skip_null_dict_values(self) -> bool:
        """Whether to omit dict entries whose value is ``None``."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def supports_collection_comments(self) -> bool:
        """Whether the language supports comments inside collection
        initializers.

        When ``False``, YAML comments on collection elements are emitted
        as standalone comment lines immediately before the collection
        (or before the variable declaration when a variable name is
        supplied) rather than being placed inside the ``{...}`` block.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def supports_scalar_before_comments(self) -> bool:
        r"""Whether the language supports a line comment between the
        assignment operator and the value on the next line.

        For example, in JavaScript ``const x = // note\n42;`` is valid
        because the parser continues the incomplete expression past the
        line comment.  In Python ``x = # note\n42`` is a syntax error
        because the ``#`` comment terminates the statement.

        When ``False``, YAML comments that appear before a scalar value
        are emitted as standalone comment lines immediately before the
        variable declaration rather than between the ``=`` and the
        value.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def supports_scalar_inline_comments(self) -> bool:
        """Whether the language supports a trailing line comment on a
        scalar value without breaking surrounding syntax.

        For example, in JavaScript ``const x = 42  // note`` is valid
        because no closing token follows on the same line.  In C
        ``((_CVal){.i = 42  // note});`` is a syntax error because the
        ``//`` comment consumes the closing ``});``.

        When ``False``, YAML inline comments on scalar values are
        emitted as standalone comment lines immediately before the
        variable declaration rather than being appended after the
        value.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_name_support(self) -> Support:
        """Whether the language supports variable declarations.

        :attr:`~Support.NOT_IN_LANGUAGE` means the language has no
        variable declaration syntax (e.g. YAML, JSON5).
        :attr:`~Support.NOT_IMPLEMENTED_BY_TOOL` means the language has
        variable syntax but literalizer has not yet implemented it.
        :attr:`~Support.SUPPORTED` means variable declarations are
        fully supported.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dotted_call_support(self) -> Support:
        """Whether the language supports dotted function call targets
        (e.g. ``foo.bar.baz(args)``).

        :attr:`~Support.NOT_IN_LANGUAGE` means the language has no
        dotted call syntax.
        :attr:`~Support.NOT_IMPLEMENTED_BY_TOOL` means the language
        supports it but literalizer has not yet implemented it.
        :attr:`~Support.SUPPORTED` means dotted call targets are
        fully supported.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration.

        Called as
        ``format_variable_declaration(name, value, data, modifiers)`` where
        *name* is the variable name, *value* is the already-formatted literal
        value, *data* is the original parsed data structure, and *modifiers*
        is the set of modifier enum values requested by the caller.  Each
        language exposes its modifier vocabulary as its nested
        :attr:`Modifiers` enum; values that are not members of that
        enum are silently ignored.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable.

        Called as ``format_variable_assignment(name, value, data)`` where
        *name* is the variable name, *value* is the already-formatted literal
        value, and *data* is the original parsed data structure.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_type_hints(self) -> enum.Enum:
        """The variable type hint option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_format(self) -> enum.Enum:
        """The sequence format chosen for this language instance.

        ``sequence_format_config`` exposes the format-specific
        configuration (e.g. ``supports_heterogeneity``).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_format(self) -> enum.Enum:
        """The set format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_format(self) -> enum.Enum:
        """The comment format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def date_format(self) -> enum.Enum:
        """The date format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def datetime_format(self) -> enum.Enum:
        """The datetime format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def declaration_style(self) -> enum.Enum:
        """The declaration style chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_entry_style(self) -> enum.Enum:
        """The dict entry style chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_format(self) -> enum.Enum:
        """The dict/map format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def float_format(self) -> enum.Enum:
        """The float format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def integer_format(self) -> enum.Enum:
        """The integer format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_literal_suffix(self) -> enum.Enum:
        """The numeric literal suffix chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_separator(self) -> enum.Enum:
        """The numeric separator option chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_style(self) -> enum.Enum:
        """The numeric literal style chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def string_format(self) -> enum.Enum:
        """The string format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_comma(self) -> enum.Enum:
        """The trailing comma option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def line_ending(self) -> enum.Enum:
        """The line ending option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def heterogeneous_strategy(self) -> enum.Enum:
        """The heterogeneous-scalar strategy chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def static_preamble(self) -> Sequence[str]:
        """Lines (imports, package declarations, etc.) that are always
        emitted before the generated code, regardless of what types
        appear in the data.  Use an empty sequence when none are needed.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Maps Python scalar types to the preamble lines required when
        that type appears in the data.  For example, a language that
        needs ``import datetime`` when dates are present would include
        ``{datetime.date: ("import datetime",)}``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def static_body_preamble(self) -> Sequence[str]:
        """Lines that are always prepended to the generated code,
        regardless of what types appear in the data.  Appears after the
        header preamble but before the code body.  Use an empty sequence
        when none are needed.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Maps Python scalar types to body-preamble lines that are
        prepended to the generated code.

        Most languages leave this empty.  Haskell uses it for typeclass
        instance definitions.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Computes body-preamble lines based on which types are present
        in the data.  Most languages build this from
        :attr:`scalar_body_preamble`; Haskell overrides it to compose
        the ``data Val`` declaration and imports dynamically.

        The second argument is the original data value, allowing
        implementations to inspect actual values when needed (e.g. to
        determine whether datetime microsecond-precision imports are
        required).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Callable that receives the original data value and returns
        extra preamble lines that depend on data content rather than
        just which scalar types are present.

        Most languages use :func:`no_data_preamble` (returns ``()``);
        C++ uses this to conditionally emit its ``Any`` helper struct
        only when the data contains heterogeneous collections.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Describes how this language handles heterogeneous scalar
        collections.

        Languages that don't wrap heterogeneous values expose
        :data:`NO_HETEROGENEOUS_BEHAVIOR`.  Languages that wrap them
        (e.g. Rust's ``HeterogeneousStrategies.TAGGED_ENUM``) return a
        :class:`HeterogeneousBehavior` whose ``wrap_scalar`` and
        ``compute_wrap_ids`` implement the wrapping.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Callable that receives the set of collection types that have
        empty instances in the data and returns preamble lines needed
        for type-hint annotations.

        Most languages return ``()`` unconditionally; Python uses this
        to emit ``from typing import Any`` only when the specific empty
        collection types present actually require it.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def special_float_preamble(self) -> tuple[str, ...]:
        """Preamble lines added only when special float values (inf,
        -inf, nan) appear in the data.  Most languages set this to
        ``()``.  Languages whose special-float literals require imports
        (e.g. Go needs ``import "math"``) populate this field so the
        import is only emitted when actually needed.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def call_style_config(self) -> CallStyle | CallSupport:
        """Describes how this language passes arguments in function
        calls.

        Returns a :class:`CallStyle` variant for supported languages,
        or a :class:`CallSupport` sentinel for languages with an empty
        :attr:`CallStyles` enum (distinguishing whether the language
        has no call syntax at all, or literalizer has not yet
        implemented call rendering for it).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def statement_terminator(self) -> str:
        """String appended to each call expression to form a complete
        statement.

        Most C-family languages use ``";"``.  Python, Ruby, and other
        languages where a bare expression is a valid statement use
        ``""``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declaration lines for a name used in a call
        expression.

        *parts* is a sequence of name parts -- a single element for
        simple function calls (e.g. ``("process",)``), multiple for
        method calls (e.g. ``("throttler", "check")``).  The second
        argument is the list of parameter names (e.g.
        ``["user_id", "ts"]``) so that keyword-style languages can
        generate stubs with matching named parameters.
        *stub_return* controls the return type of the generated stub:
        :attr:`StubReturn.VALUE` when the call expression's return
        value is consumed (e.g. passed as an argument to a transform
        wrapper), :attr:`StubReturn.VOID` otherwise.

        Stub lines are placed **inside** the language wrapper (e.g.
        inside ``func main()`` for Go, inside ``class Check`` for
        Java).  Languages that need stubs at file/package scope should
        use :attr:`format_call_preamble_stub` instead.

        Returns an empty tuple when no stub is needed (e.g. for
        built-in functions, or in languages whose lint checks only
        verify syntax).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Like :attr:`format_call_stub` but the lines are placed
        **before** the language wrapper — at file, package, or module
        scope.

        Most languages return an empty tuple here and put all stubs in
        :attr:`format_call_stub`.  Languages like Go that cannot
        declare types inside function bodies use this instead.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a sequence of call target parts into the form
        required by this language's call expression syntax.

        Most languages accept dotted member-access as-is and use
        :data:`identity_call_target`.  PHP overrides this to produce
        ``$app->client->fetch``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the form
        required by this language's call expression syntax.

        Called after :func:`~literalizer.literalize_call`'s ``ref_case``
        normalization, so *name* is already in the requested identifier
        case.  Most languages emit ref identifiers bare and use
        :data:`identity_call_ref_identifier`.  Languages where variable
        references carry a sigil (e.g. PHP ``$name``, Perl ``$name``)
        override this to prepend the sigil.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a code snippet in a complete, valid file."""
        ...  # pylint: disable=unnecessary-ellipsis

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a declaration and assignment in a complete, valid file."""
        ...  # pylint: disable=unnecessary-ellipsis

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a sequence of top-level *declarations* (each one a
        full ``literalize`` ``bare_code`` for a ``$ref`` target)
        alongside a block of bare call expressions in a complete,
        valid file.

        Most languages can splice the declarations directly in front
        of the calls and route through :meth:`wrap_in_file` in call
        mode; they assign :data:`default_wrap_calls_with_declarations`
        as a no-op wrapper.  Languages whose call-mode wrapping moves
        bare expressions into a different scope than top-level
        bindings (e.g. Haskell's ``main = do`` block, where bindings
        belong at module scope) override this method.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid code for *data*.

        Languages whose output depends on format/data combinations that
        cannot produce valid code (e.g. Rust ``CONST`` + a dict value)
        override this method to raise
        :class:`~literalizer.exceptions.IncompatibleFormatsError` at
        literalize time.  Languages with no such constraints assign
        :func:`no_validate_spec_for_data` as a no-op.
        """
        ...  # pylint: disable=unnecessary-ellipsis


def _no_call_stub(
    _parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return no stub lines."""
    return ()


no_call_stub: Callable[
    [Sequence[str], Sequence[str], StubReturn], tuple[str, ...]
] = _no_call_stub
"""Shared callable for languages that need no call stubs."""


def _identity_call_target(parts: Sequence[str], /) -> str:
    """Return the parts joined with ``"."``."""
    return ".".join(parts)


identity_call_target: Callable[[Sequence[str]], str] = _identity_call_target
"""Shared callable for languages that need no call-target rewriting."""


def _identity_call_ref_identifier(name: str, /) -> str:
    """Return *name* unchanged."""
    return name


identity_call_ref_identifier: Callable[[str], str] = (
    _identity_call_ref_identifier
)
"""Shared callable for languages that need no ``$ref`` identifier
rewriting.  Languages that decorate ref identifiers (e.g. PHP's
``$name`` or Perl's ``$name``) override
:attr:`Language.format_call_ref_identifier` instead.
"""


def _no_type_hint_preamble(
    _empty_collection_types: frozenset[type],
    /,
) -> tuple[str, ...]:
    """Return no preamble lines — used by languages that do not emit
    type hints for empty collections.
    """
    return ()


no_type_hint_preamble: Callable[[frozenset[type]], tuple[str, ...]] = (
    _no_type_hint_preamble
)
"""Shared callable for languages that need no type-hint preamble."""


def _no_data_preamble(_data: Value, /) -> tuple[str, ...]:
    """Return no preamble lines — used by languages that do not need
    data-dependent preamble.
    """
    return ()


no_data_preamble: Callable[[Value], tuple[str, ...]] = _no_data_preamble
"""Shared callable for languages with no data-dependent preamble."""


def _no_validate_spec_for_data(self: "Language", data: Value) -> None:
    """Default ``validate_spec_for_data`` — no spec/data constraints."""
    del self, data


no_validate_spec_for_data: Callable[["Language", Value], None] = (
    _no_validate_spec_for_data
)
"""Shared callable for languages with no spec/data constraints to
check.
"""


def _default_wrap_calls_with_declarations(
    self: "Language",
    declarations: tuple[str, ...],
    calls: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Default ``wrap_calls_with_declarations`` — concatenate the
    *declarations* and *calls* and route through :meth:`wrap_in_file`
    in call mode.
    """
    content = "\n".join((*declarations, calls)) if declarations else calls
    return self.wrap_in_file(
        content=content,
        variable_name="",
        body_preamble=body_preamble,
    )


default_wrap_calls_with_declarations: Callable[
    ["Language", tuple[str, ...], str, tuple[str, ...]], str
] = _default_wrap_calls_with_declarations
"""Shared callable for languages whose call-mode :meth:`wrap_in_file`
already accepts the declarations spliced in front of the call
expressions.
"""


@beartype
def value_contains(data: Value, predicate: Callable[[Value], bool]) -> bool:
    """Return ``True`` if any element of *data* satisfies *predicate*.

    Walks the data tree and invokes *predicate* on every node (scalars
    and collections alike).  Used by languages to detect whether a
    payload will trigger a format combination that cannot produce valid
    output (e.g. Rust ``CONST`` + a dict value).
    """
    if predicate(data):
        return True
    match data:
        case dict():
            return any(
                value_contains(data=v, predicate=predicate)
                for v in data.values()
            )
        case list() | set():
            return any(
                value_contains(data=v, predicate=predicate) for v in data
            )
        case _:
            return False


@beartype
def prepend_body_preamble(
    content: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Prepend *body_preamble* lines to *content*."""
    if not body_preamble:
        return content
    return "\n".join(body_preamble) + "\n" + content


@beartype
def wrap_in_file_noop(
    content: str,
    variable_name: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Default ``wrap_in_file`` that only adds body preamble."""
    del variable_name  # unused
    return prepend_body_preamble(content=content, body_preamble=body_preamble)


@beartype
def wrap_combined_in_file_noop(
    declaration: str,
    assignment: str,
    variable_name: str,
    body_preamble: tuple[str, ...],
) -> str:
    """Default ``wrap_combined_in_file``: join with newline, prepend
    preamble.
    """
    return wrap_in_file_noop(
        content=declaration + "\n" + assignment,
        variable_name=variable_name,
        body_preamble=body_preamble,
    )


def body_preamble_from_scalars(
    *,
    scalar_body_preamble: dict[type, tuple[str, ...]],
    format_lines: Callable[[list[str]], tuple[str, ...]],
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a ``compute_body_preamble`` from a scalar-body-preamble
    dict.

    Args:
        scalar_body_preamble: Mapping from type to preamble lines.
        format_lines: Post-processing for the deduplicated lines
            (e.g. adding language-specific prefixes).
    """

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return unique body-preamble lines for *types*."""
        del data  # unused by the generic implementation
        seen: set[str] = set()
        result: list[str] = []
        for scalar_type, lines in scalar_body_preamble.items():
            if scalar_type in types:
                for line in lines:
                    if line not in seen:
                        seen.add(line)
                        result.append(line)
        return format_lines(result)

    return _compute
