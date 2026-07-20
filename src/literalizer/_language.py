"""Language protocol and internal spec dataclass."""

import dataclasses
import datetime
import enum
import math
import re
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import (
    Any,
    ClassVar,
    Final,
    Protocol,
    assert_never,
    runtime_checkable,
)

import humps
from beartype import beartype

from literalizer._formatters.collection_openers import typed_collection_open
from literalizer._formatters.type_inference import (
    DictType,
    ListType,
    RecordShape,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    InvalidNewVariableNameError,
    ReservedVariableNameError,
    UnrepresentableEmptyDictError,
)


class NewVariableNameSyntax(enum.Enum):
    """Conservative lexical grammars for ``NewVariable`` declarations.

    The grammar describes source names exactly as supplied to a language's
    declaration formatter.  It intentionally does not repair, quote, or
    otherwise transform a caller-provided name.
    """

    ASCII = enum.auto()
    """An ASCII identifier beginning with a letter or underscore."""

    ASCII_KEBAB = enum.auto()
    """An ASCII identifier that may contain hyphens after its start."""

    LOWER_ASCII = enum.auto()
    """An ASCII identifier beginning with a lowercase letter or underscore."""

    LOWER_ASCII_PRIME_SUFFIX = enum.auto()
    """A lower-ASCII identifier with an optional trailing prime suffix."""

    ASCII_LETTER_START = enum.auto()
    """An ASCII identifier that must begin with a letter."""

    def accepts(self, *, name: str) -> bool:
        """Return whether *name* matches this lexical grammar."""
        match self:
            case NewVariableNameSyntax.ASCII:
                pattern = r"[A-Za-z_][A-Za-z0-9_]*"
            case NewVariableNameSyntax.ASCII_KEBAB:
                pattern = r"[A-Za-z_][A-Za-z0-9_-]*"
            case NewVariableNameSyntax.LOWER_ASCII:
                pattern = r"[a-z_][A-Za-z0-9_]*"
            case NewVariableNameSyntax.LOWER_ASCII_PRIME_SUFFIX:
                pattern = r"[a-z_][A-Za-z0-9_]*'*"
            case NewVariableNameSyntax.ASCII_LETTER_START:
                pattern = r"[A-Za-z][A-Za-z0-9_]*"
            case _:  # pragma: no cover - enum exhaustiveness assertion
                assert_never(self)
        return re.fullmatch(pattern=pattern, string=name) is not None


@beartype
def validate_new_variable_name(*, language: "Language", name: str) -> None:
    """Raise when *name* cannot be used for a new variable declaration."""
    language_name = language.__class__.__name__
    if language.reserved_variable_identifiers_case_sensitive:
        is_reserved = name in language.reserved_variable_identifiers
    else:
        folded_name = name.casefold()
        is_reserved = any(
            folded_name == reserved_name.casefold()
            for reserved_name in language.reserved_variable_identifiers
        )
    if is_reserved:
        raise ReservedVariableNameError(
            language_name=language_name,
            variable_name=name,
        )
    language_cls = type(language)
    if not isinstance(language_cls, LanguageCls):  # pragma: no cover
        msg = "NewVariable validation requires a LanguageCls language"
        raise TypeError(msg)
    syntax = language_cls.new_variable_name_syntax
    if not syntax.accepts(name=name):
        raise InvalidNewVariableNameError(
            language_name=language_name,
            variable_name=name,
        )


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
    preamble_lines: tuple[str, ...]
    type_produced: type


@dataclasses.dataclass(frozen=True)
class DatetimeFormatConfig:
    """Configuration for a single datetime format."""

    formatter: Callable[[datetime.datetime], str]
    preamble_lines: tuple[str, ...]
    type_produced: type


@beartype
def date_scalar_preamble(
    *,
    date_format: enum.Enum,
    datetime_format: enum.Enum,
    extra: dict[type, tuple[str, ...]] | None,
) -> dict[type, tuple[str, ...]]:
    """Build the ``scalar_preamble`` dict for date/datetime formats.

    Args:
        date_format: The date format enum member whose ``.value`` has
            a ``preamble_lines`` attribute.
        datetime_format: The datetime format enum member whose ``.value``
            has a ``preamble_lines`` attribute.
        extra: Optional additional type→preamble mappings to include
            unconditionally (e.g. for C++ ``#include <string>`` or the
            ``datetime.time`` import added by languages that emit native
            time literals).

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

    dict_open: Callable[[dict[Scalar, Value]], str]
    close: str
    format_entry: Callable[[str, Value, str], str]
    empty_dict: str | None
    preamble_lines: tuple[str, ...]
    narrowed_open: str | None
    supports_trailing_comma: bool
    narrowed_empty_form: Callable[[Sequence[dict[Scalar, Value]]], str] | None
    """Callback that renders an empty dict beside non-empty map siblings
    (e.g. V's ``map[string]int{}`` when a sibling is ``{"x": 1}``).
    ``None`` keeps the language's default ``empty_dict`` / opener path.
    """


@dataclasses.dataclass(frozen=True)
class OrderedMapFormatConfig:
    """Configuration for ordered-map formatting."""

    ordered_map_open: Callable[[dict[Scalar, Value]], str]
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

    arg_separator: str
    parenthesize_each_arg: bool


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

    ``call_transform`` is not supported for this style (see
    :func:`~literalizer.literalize_call`).
    """

    arg_separator: str


CallStyle = (
    PositionalCallStyle
    | KeywordCallStyle
    | ObjectCallStyle
    | PostfixCallStyle
    | PrefixCallStyle
    | CommandCallStyle
)
"""Tagged union describing how a language passes call arguments."""

type FormatCallArg = Callable[[Value, str], str]
"""Callable that rewrites a formatted direct call argument."""


@runtime_checkable
class LeadingPreamble(Protocol):
    """Callable returning preamble lines that must precede every other
    preamble line (see :attr:`Language.leading_preamble`).

    ``has_variable_declaration`` is keyword-only because it is a
    boolean flag, not a value the callable formats.
    """

    def __call__(
        self, data: Value, /, *, has_variable_declaration: bool
    ) -> tuple[str, ...]:
        """Return the leading preamble lines for *data*."""
        ...  # pylint: disable=unnecessary-ellipsis


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


class BareIntegerWidthStrategies(enum.Enum):
    """Default integer-width strategies: only the no-op ``BARE`` member.

    Most languages render integers as bare numeric literals regardless
    of magnitude, so they share this enum.  Languages whose native
    scalar integer type silently loses precision past a fixed width
    (notably Perl, whose scalars fall back to an NV float past 2**53)
    override this with a wider enum exposing additional strategies
    such as a ``Math::BigInt``-style wrap.
    """

    BARE = enum.auto()


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
    """Whether a generated call stub returns a value or nothing.

    Passed to :attr:`Language.format_call_stub` and
    :attr:`Language.format_call_preamble_stub` to control the return
    type of the no-op target-function stub emitted when a call is
    wrapped in a self-contained file.
    """

    VOID = "void"
    """The call result is discarded, so the stub returns nothing."""

    VALUE = "value"
    """The call result is consumed (passed to a ``call_transform`` or
    bound to a variable), so the stub returns a value.
    """


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


ALL_REF_CASES: frozenset[IdentifierCase] = frozenset(IdentifierCase)
"""Every :class:`IdentifierCase` member.

Use as :attr:`Language.supported_ref_cases` for languages whose
identifier grammar admits every case in :class:`IdentifierCase`,
including ``KEBAB`` (e.g. Lisp-family languages where ``my-var`` is a
single legal symbol).
"""


NON_KEBAB_REF_CASES: frozenset[IdentifierCase] = ALL_REF_CASES - {
    IdentifierCase.KEBAB,
}
"""Every :class:`IdentifierCase` member except ``KEBAB``.

Use as :attr:`Language.supported_ref_cases` for languages whose
identifier grammar rejects ``-`` in identifiers (the common C-family
case, where ``my-var`` would parse as subtraction or fail outright)
while still accepting the four non-kebab cases as legal identifiers.
"""


@beartype
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


class CollectionLayout(enum.Enum):
    """Controls how nested collections are rendered."""

    COMPACT = "compact"
    """Render nested collections on one line."""

    MULTILINE = "multiline"
    """Render nested collections with one element per line."""


@dataclasses.dataclass(frozen=True)
class RenderedRecordLiteral:
    """A record literal as structured pieces, assembled into compact or
    multiline form by the shared record-layout code without re-parsing.

    ``head`` is the literal up to and including its opening delimiter
    (``Record0 {`` for Rust, ``Record0{`` for Go).  ``entries`` is one
    already-formatted field per element (``id: 1``); an entry whose
    value is itself multiline arrives already expanded.  ``closer`` is
    the closing delimiter (``}``).  ``compact_pad`` is inserted just
    inside the delimiters in compact form (a space for Rust's
    ``Name { a }``, empty for Go's ``Name{a}``) and is unused in the
    multiline form.
    """

    head: str
    entries: tuple[str, ...]
    closer: str
    compact_pad: str


@dataclasses.dataclass(frozen=True)
class RenderedTupleLiteral:
    """A heterogeneous-tuple literal as structured pieces, assembled
    into compact or multiline form by the same shared layout code as
    :class:`RenderedRecordLiteral` without re-parsing.

    ``head`` is the literal up to and including its opening delimiter
    (``(`` for Rust, ``std::make_tuple(`` for C++).  ``entries`` is one
    already-formatted element per tuple position (``1``, ``"email"``);
    an entry whose value is itself multiline arrives already expanded.
    ``closer`` is the closing delimiter (``)``).  ``compact_pad`` is
    inserted just inside the delimiters in compact form (empty for
    Rust's ``(a, b)``) and is unused in the multiline form.

    ``multiline_trailing_comma`` is ANDed with the language's
    :attr:`TrailingCommaConfig.multiline_trailing_comma` to decide
    whether the multiline form ends with a trailing comma after the
    last element: ``True`` for Rust (a trailing comma after the last
    tuple element is valid), but ``False`` for C++ because the literal
    is a ``std::make_tuple(...)`` function call where a trailing
    argument comma is a syntax error (even though C++'s braced
    collections, hence its language-wide config, do use trailing
    commas).
    """

    head: str
    entries: tuple[str, ...]
    closer: str
    compact_pad: str
    multiline_trailing_comma: bool


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
    tagged-enum ``Value::Variant(…)``).  ``None`` indicates the
    language does not wrap scalars; in that case ``compute_wrap_ids``
    and ``compute_call_slot_wrap_ids`` must always return an empty set
    of scalar parents.

    ``wrap_non_scalar`` wraps a formatted ref-marker or container value
    when its parent is in ``wrap_ids``.  Used by V's interface strategy,
    which renders ``IVal(...)`` around every formatted child regardless
    of underlying type.  ``None`` indicates the language does not wrap
    non-scalars; languages whose ``compute_wrap_ids`` only marks parents
    with all-scalar children leave this as ``None``.

    ``wrap_empty_container`` wraps an *empty* list/map child of a marked
    container when ``wrap_non_scalar`` is ``None``.  A strategy that wraps
    only scalars still cannot hold a populated container in its value
    type, but an empty one carries no inner values, so Rust's
    ``TAGGED_ENUM`` renders it as a payload-free ``List(vec![])`` /
    ``Map(HashMap::new())`` variant (issue #3028) while keeping the
    scalar-plus-populated-container mix a documented rejection.  ``None``
    for every other behavior, including ``wrap_non_scalar`` strategies
    (which already wrap any non-scalar uniformly).

    ``compute_call_slot_wrap_ids`` is called per positional-argument
    slot with the per-call values gathered at that slot.  It returns
    the ids of top-level scalar call arguments that should be wrapped
    via ``wrap_scalar`` because their Mojo / target-language type
    diverges across sibling calls (the cross-call VARIANT case).
    Languages that do not need cross-call top-level wrapping return
    an empty ``frozenset``.

    ``dict_open_for_wrap_ids`` optionally forces the opening delimiter
    for a dict whose id appears in ``compute_wrap_ids``.  Go's RECORD
    widening uses this to keep every widened map literal at
    ``map[string]any`` even when all of one map's values happen to share
    a narrower scalar type (issue #2911).  Other wrapping strategies
    leave it as ``None`` and retain their normal inferred dict opener.

    ``widens_nested_maps_by_wrapping_scalars`` identifies strategies
    whose scalar wrapper also gives sibling nested maps one shared value
    type.  This is strategy behavior rather than a language-wide fact:
    strict languages expose it only when the corresponding non-default
    heterogeneous strategy is selected.

    ``widens_unrecordizable_nested_sibling_maps`` identifies ``RECORD``
    strategies that fall back to a widened plain map when nested sibling
    maps cannot share one record shape.  It is likewise strategy behavior:
    languages advertise it only while the capable ``RECORD`` strategy is
    selected.

    ``render_record_literal`` renders a record-shaped dict as a
    generated struct literal given its :class:`RecordShape` and a
    mapping of pre-formatted field values, returning a
    :class:`RenderedRecordLiteral` (structured pieces the shared
    record-layout code assembles into compact or multiline form).  It
    returns ``None`` for a record-eligible dict the strategy does not
    render as a struct after all -- a nested sibling map widened to a
    plain map (issue #2910) -- so the shared formatter falls through to
    normal map rendering.  The hook is ``None`` for
    strategies that do not opt into the ``RECORD`` style.

    ``compute_record_shapes`` walks the data once and returns a
    mapping from ``id(dict)`` to :class:`RecordShape` for every dict
    the strategy will render as a record literal.  Used by
    :func:`~literalizer._checks.check_data` to carve record-eligible
    dicts out of the heterogeneous-values checks.  It is ``None`` for
    non-RECORD strategies, paired with
    ``render_record_literal``: a behavior either sets both (RECORD)
    or neither.

    ``render_tuple_literal`` renders a fixed-length heterogeneous
    scalar array as a native tuple given the raw list and its
    pre-formatted elements, returning a :class:`RenderedTupleLiteral`
    (structured pieces the same shared layout code assembles into
    compact or multiline form).  It is ``None`` for strategies
    that do not opt into the ``TUPLE`` style.

    ``compute_tuple_list_ids`` walks the data once and returns the set
    of ``id(list)`` for every list the strategy will render as a tuple
    (a heterogeneous scalar array that is a dict value / record field
    value / document root, all elements scalar, spanning at least two
    scalar buckets).  Used by
    :func:`~literalizer._checks.check_data` to carve those lists out of
    the heterogeneous-scalar / mixed-list / mixed-dict-value checks.
    It is ``None`` for non-TUPLE strategies, paired with
    ``render_tuple_literal``: a behavior either sets both (TUPLE) or
    neither.  The ``TUPLE`` strategy additionally sets the ``RECORD``
    hooks so a record field whose value is a heterogeneous scalar
    array becomes a tuple-typed field (the two strategies compose).

    Languages that do not wrap expose
    :data:`NO_HETEROGENEOUS_BEHAVIOR`.
    """

    skip_scalar_checks: bool
    compute_wrap_ids: Callable[[Value], frozenset[int]]
    wrap_scalar: Callable[[Scalar, str], str] | None
    wrap_non_scalar: Callable[[Value, str], str] | None
    wrap_empty_container: Callable[[Value], str] | None
    compute_call_slot_wrap_ids: Callable[[Sequence[Value]], frozenset[int]]
    dict_open_for_wrap_ids: str | None
    widens_nested_maps_by_wrapping_scalars: bool
    widens_unrecordizable_nested_sibling_maps: bool
    render_record_literal: (
        Callable[
            [dict[Scalar, Value], Mapping[str, str]],
            RenderedRecordLiteral | None,
        ]
        | None
    )
    compute_record_shapes: Callable[[Value], Mapping[int, RecordShape]] | None
    render_tuple_literal: (
        Callable[
            [list[Value], Sequence[str]],
            RenderedTupleLiteral,
        ]
        | None
    )
    compute_tuple_list_ids: Callable[[Value], frozenset[int]] | None


@beartype
def no_compute_wrap_ids(_data: Value, /) -> frozenset[int]:
    """Return an empty wrap-id set — used by non-wrapping languages."""
    return frozenset()


@beartype
def _no_compute_call_slot_wrap_ids(
    _slot_values: Sequence[Value],
    /,
) -> frozenset[int]:
    """Return an empty wrap-id set for languages without cross-call
    top-level scalar wrapping.
    """
    return frozenset()


no_compute_call_slot_wrap_ids: Callable[[Sequence[Value]], frozenset[int]] = (
    _no_compute_call_slot_wrap_ids
)
"""Shared callable for languages without cross-call top-level scalar
wrapping (every non-Mojo VARIANT-style behavior).
"""


NO_HETEROGENEOUS_BEHAVIOR = HeterogeneousBehavior(
    skip_scalar_checks=False,
    compute_wrap_ids=no_compute_wrap_ids,
    wrap_scalar=None,
    wrap_non_scalar=None,
    wrap_empty_container=None,
    compute_call_slot_wrap_ids=_no_compute_call_slot_wrap_ids,
    dict_open_for_wrap_ids=None,
    widens_nested_maps_by_wrapping_scalars=False,
    widens_unrecordizable_nested_sibling_maps=False,
    render_record_literal=None,
    compute_record_shapes=None,
    render_tuple_literal=None,
    compute_tuple_list_ids=None,
)
"""Shared behavior for languages that do not wrap heterogeneous scalar
values.
"""


NO_CALL_PARAMETER_LIMIT: Final = sys.maxsize
"""Sentinel for ``Language.max_call_parameters`` meaning "no fixed
parameter limit".

Cannot be ``None``: when an attribute's value in a class's
``__dict__`` is ``None``, CPython's ``_proto_hook`` returns
``NotImplemented`` (the PEP 544 "this attribute is not implemented"
signal).  ``NotImplemented`` prevents the ABC subclass cache from
warming, so every subsequent ``isinstance(_, Language)`` falls into
an O(N)-in-protocol-member-count walk in
``_ProtocolMeta.__instancecheck__``.  With our ~110-member protocol
that turned a 1.3 ms ``literalize()`` call into a 305 ms one.  Using
``sys.maxsize`` as the "unlimited" sentinel keeps the cache warm.
"""


@beartype
def _identity_call_arg(_value: Value, formatted: str, /) -> str:
    """Return *formatted* unchanged for languages with no argument wrapper."""
    return formatted


identity_call_arg: FormatCallArg = _identity_call_arg
"""Shared callable for languages that need no call-argument wrapping."""


@beartype
def _no_validate_call_arg(_value: Value, /) -> None:
    """Accept every call argument."""


no_validate_call_arg: Callable[[Value], None] = _no_validate_call_arg
"""Shared callable for languages with no call-argument constraints."""


@beartype
def _identity_call_statement(statement: str, /) -> str:
    """Return *statement* unchanged for languages with bare call
    statements.
    """
    return statement


identity_call_statement: Callable[[str], str] = _identity_call_statement
"""Shared callable for languages whose calls need no statement wrapper."""


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


class RecordVariant(enum.Enum):
    """Focused record behaviors that need integration variants."""

    UNIFY_OPTIONAL_FIELDS = enum.auto()
    NONRECORD_DICT_FIELD = enum.auto()
    KEYWORD_FIELD = enum.auto()
    QUOTED_FIELD = enum.auto()
    FIELD_TYPE_SPLIT = enum.auto()


class NestedMapWideningVariant(enum.Enum):
    """Input shape used to exercise a language's nested-map widening."""

    NONE = enum.auto()
    DEFAULT = enum.auto()
    UNIFORM_KEYS = enum.auto()


class JsonType(enum.Enum):
    """Base class for JSON value-type options.

    JSON representations opt into embedded-null-byte integration variants
    by overriding :attr:`string_literals_escape_null_byte`.
    """

    @property
    def string_literals_escape_null_byte(self) -> bool:
        """Return whether this JSON type faithfully encodes null bytes."""
        return False


@dataclasses.dataclass(frozen=True)
class VariantMetadata:
    r"""Language-owned metadata for constructing integration variants.

    These values describe supported behaviors and compatibility constraints;
    the integration suite remains responsible for choosing input fixtures.

    ``string_literals_escape_null_byte`` is ``True`` only for languages
    whose default string formatter faithfully escapes an embedded null
    byte, including immediately before a digit (the
    ``string_embedded_nul`` golden axis renders such languages).  A
    language that rejects the value, emits a raw null byte, or emits a
    digit-greedy escape (for example Haskell's variable-length ``\x``,
    where ``"\x001"`` denotes U+0001 rather than a null byte followed by
    ``1``) stays ``False`` until its own escaping is corrected.
    """

    pre_indent_comment_scalar_variant: bool
    fixture_module_name_template: str | None
    fixture_module_name_lowercase: bool
    golden_filename_lowercase: bool
    collection_layout_category: str
    record_variants: frozenset[RecordVariant]
    nested_map_widening: NestedMapWideningVariant
    modifier_sequence_format_overrides: dict[str, str]
    string_literals_escape_null_byte: bool


@beartype
def _identity_constructor_target(class_name: str, /) -> str:
    """Return *class_name* as a zero-argument constructor call target."""
    return class_name


identity_constructor_target: Callable[[str], str] = (
    _identity_constructor_target
)
"""Shared callable for languages whose constructors are called as
``ClassName()``.
"""


@beartype
def _new_constructor_target(class_name: str, /) -> str:
    """Return a ``new ClassName`` constructor call target."""
    return f"new {class_name}"


new_constructor_target: Callable[[str], str] = _new_constructor_target
"""Shared callable for languages whose constructors are called as
``new ClassName()``.
"""


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
    IntegerWidthStrategies: type[enum.Enum]
    NumericLiteralSuffixes: type[enum.Enum]
    NumericSeparators: type[enum.Enum]
    NumericStyles: type[enum.Enum]
    StringFormats: type[enum.Enum]
    TrailingCommas: type[enum.Enum]
    StatementTerminatorStyles: type[enum.Enum]
    CallStyles: type[enum.Enum]
    Modifiers: type[enum.Enum]
    HeterogeneousStrategies: type[enum.Enum]
    JsonTypes: type[JsonType]
    BoolFormats: type[enum.Enum]
    identifier_cases: tuple[IdentifierCase, ...]
    supported_ref_cases: frozenset[IdentifierCase]
    modifier_combinations: tuple[ModifierCombination, ...]
    variant_metadata: VariantMetadata
    module_name_case: IdentifierCase
    extension: str
    pygments_name: str | None
    VersionFormats: type[enum.Enum]
    supports_special_floats: bool
    supports_non_ascii_string_literals: bool
    supports_variable_names: bool
    supports_no_variable_wrap_in_file: bool
    supports_dotted_calls: bool
    has_free_function_calls: bool
    reserved_identifiers: frozenset[str]
    reserved_variable_identifiers: frozenset[str]
    reserved_variable_identifiers_case_sensitive: bool
    new_variable_name_syntax: NewVariableNameSyntax = (
        NewVariableNameSyntax.ASCII
    )
    allows_empty_call_parens: bool
    supports_dotted_call_stub: bool
    call_returns_expression: bool
    supports_json_call_result_binding: bool
    """Whether call-result bindings preserve an active JSON value type."""
    supports_zero_parameter_calls: bool
    max_call_parameters: int
    supports_inline_multiline_dict_args: bool
    supports_standalone_comments_in_wrapped_calls: bool
    supports_multi_param_call_wrapper_stub: bool
    supports_dict_literal_as_free_expression: bool
    supports_module_name: bool
    supports_empty_dict_key: bool
    supports_call_style: bool
    supports_default_dict_key_type: bool
    supports_non_string_dict_keys: bool
    supports_default_dict_value_type: bool
    supports_default_sequence_element_type: bool
    supports_default_set_element_type: bool
    supports_default_ordered_map_value_type: bool
    non_default_kwargs: Mapping[str, str]
    """Valid non-default values for configurable string options.

    Keys are constructor field names.  Keeping these values on the language
    class lets metadata consumers exercise those options without maintaining
    a parallel language matrix.
    """
    declaration_style_sequence_format_overrides: Mapping[str, str]
    """Compatible sequence-format names for declaration-style variants."""

    json_type_variant_name_suffix: str | None
    """Stable filename suffix for a non-default JSON type variant."""
    supports_record_struct_name_prefix: bool
    supports_record_shape_names: bool
    dict_supports_heterogeneous_values: bool

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

    __dataclass_fields__: ClassVar[dict[str, dataclasses.Field[Any]]]
    variant_metadata: ClassVar[VariantMetadata]

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

        Every language exposes ``NEVER`` (no annotations, let the
        language infer), ``ALWAYS`` (annotate every variable), and
        ``SAFE``.  ``SAFE`` annotates only when the language's own
        inference would widen the variable to a permissive type (e.g.
        ``unknown[]`` for an empty TypeScript array, ``Object[]`` for an
        empty Java array); for languages without a custom predicate it
        produces the same output as ``NEVER``.
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
    def integer_width_strategies(self) -> type[enum.Enum]:
        """Enum class whose members list the integer-width rendering
        strategies this language supports.

        Most languages support only :attr:`BareIntegerWidthStrategies.BARE`
        (a bare numeric literal).  Languages whose native scalar integer
        type silently loses precision past a fixed mantissa (notably
        Perl past ``2**53``) expose additional opt-in strategies that
        wrap wide values in an arbitrary-precision constructor.
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
    def statement_terminator_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the statement terminator options
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
    def json_types(self) -> type[JsonType]:
        """Enum class whose members list the JSON value-type options
        this language supports.

        Languages without a JSON value-type representation expose an
        empty enum so consumers can enumerate options uniformly without
        reflection.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def bool_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the boolean format options
        this language supports.

        Languages without alternative boolean formats expose an empty
        enum so consumers can enumerate options uniformly without
        reflection.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def version_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the target language versions
        this language class supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def identifier_cases(self) -> tuple[IdentifierCase, ...]:
        """Identifier case conventions idiomatic for this language.

        Ordered by stylistic preference -- the first element is the
        language's default/idiomatic case for generated defaults and
        golden fixtures.  This list is *not* used to validate user
        ``ref_case`` choices; that role belongs to
        :attr:`supported_ref_cases`.  A language may prefer only
        ``SNAKE`` while still syntactically supporting ``CAMEL``,
        ``PASCAL``, and ``UPPER_SNAKE``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def supported_ref_cases(self) -> frozenset[IdentifierCase]:
        """Identifier cases that produce a syntactically legal
        identifier in this language.

        Used solely for correctness validation: passing a
        :class:`IdentifierCase` not in this set to
        :func:`~literalizer.literalize` or
        :func:`~literalizer.literalize_call` via ``ref_case`` is
        rejected with
        :class:`~literalizer.exceptions.UnsupportedIdentifierCaseError`.
        Independent of :attr:`identifier_cases`, which records
        stylistic preference rather than syntactic validity.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    extension: str
    """The file extension for this language, including the leading dot."""

    supports_dotted_calls: bool
    """Whether the language accepts dotted ``target_function`` values
    (e.g. ``"module.fn"``) in
    :func:`~literalizer.literalize_call`.  When ``False``, dotted
    targets are rejected with
    :class:`~literalizer.exceptions.DottedCallTargetNotSupportedError`.
    """

    supports_dotted_call_stub: bool
    """Whether the language can declare a stub for a dotted call wrapper
    name (e.g. ``tracer.emit``).  :func:`~literalizer.literalize_call`
    no longer inspects this (a context-aware ``call_transform`` is
    opaque); it is metadata for callers and the test harness, which use
    it to decide whether a generated dotted-wrapper stub can compile in
    this language.
    """

    has_free_function_calls: bool
    """Whether the language has a free function call syntax (i.e. the
    ability to call a function by a bare name with no dot).  Metadata
    for callers and the test harness, which use it to decide whether a
    generated bare-wrapper stub can compile in this language;
    :func:`~literalizer.literalize_call` does not inspect it.
    """

    supports_multi_param_call_wrapper_stub: bool
    """Whether the language can declare, and positionally invoke, a
    harness wrapper stub that receives the call's result alongside one
    or more additional positional arguments.  Metadata for the test
    harness only; :func:`~literalizer.literalize_call` does not inspect
    it.  ``False`` for languages whose generated multi-parameter stub
    cannot accept the call expression positionally -- e.g. a strongly
    typed stub fed a ``void``-returning call, or an object-style stub
    that rejects a positional multi-argument invocation.
    """

    supports_dict_literal_as_free_expression: bool
    """Whether a dict/map literal can appear as a free-standing
    expression (e.g. spliced as a call argument) rather than only on
    the right-hand side of a typed assignment.  Metadata for the test
    harness only; :func:`~literalizer.literalize_call` does not inspect
    it.  ``False`` for languages whose map-literal syntax needs a typed
    left-hand side to be sized -- e.g. SystemVerilog ``'{...}``
    assignment patterns.
    """

    @property
    def reserved_identifiers(self) -> frozenset[str]:
        """Identifiers that are reserved by the language and therefore
        cannot appear as the innermost segment of ``target_function``.
        :func:`~literalizer.literalize_call` rejects such targets with
        :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def reserved_variable_identifiers(self) -> frozenset[str]:
        """Identifiers that cannot be used for new variable declarations.

        This is separate from :attr:`reserved_identifiers` because a word
        can be a valid property name in a dotted call while still being
        forbidden for a variable declaration (for example, TypeScript's
        ``class`` in JavaScript and TypeScript).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def reserved_variable_identifiers_case_sensitive(self) -> bool:
        """Whether reserved variable identifiers must match case
        exactly.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    supports_variable_names: bool
    """Whether the language supports wrapping output in a named variable
    via the ``variable_form`` argument to
    :func:`~literalizer.literalize`.  When ``False``, passing any
    :class:`~literalizer.NewVariable`,
    :class:`~literalizer.ExistingVariable`,
    or :class:`~literalizer.BothVariableForms` is rejected with
    :class:`~literalizer.exceptions.VariableNameNotSupportedError`.
    """

    supports_no_variable_wrap_in_file: bool
    """Whether the language can represent a bare value (no variable
    binding) at file-statement scope.  When ``False``,
    :func:`~literalizer.literalize` rejects ``wrap_in_file=True`` with
    ``variable_form=None`` with
    :class:`~literalizer.exceptions.WrapInFileWithoutVariableNotSupportedEr
    ror`,
    rather than silently emitting a file whose top-level item is a bare
    expression (a syntax error in strict-typed languages like Rust, C,
    Haskell, Swift, Ada, D, Dart, C#, Elm, Mojo, Nim, Objective-C, Odin,
    SML, V, Zig, etc.).

    Languages with no variable-name syntax at all
    (:attr:`supports_variable_names` is ``False``) must set this to
    ``True``: their ``wrap_in_file`` output has no other shape.
    """

    dict_supports_heterogeneous_values: bool
    """Whether the language's dict format can represent values spanning
    multiple type families (e.g. Python's ``dict``, JavaScript's object
    literal).  When ``False`` (e.g. Rust's ``HashMap``), inputs with
    heterogeneous dict values raise
    :class:`~literalizer.exceptions.MixedDictValuesError`.
    """

    @property
    def language_version(self) -> enum.Enum:
        """The selected version of the target language."""
        ...  # pylint: disable=unnecessary-ellipsis

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
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a :class:`datetime.time` as a string
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
    def format_integer_widened(self) -> Callable[[int], str] | None:
        """Widened-integer formatter for mixed-magnitude int collections,
        or ``None`` when the language has no widening behavior.

        Used when a sequence/set/map mixes integers that do not all fit
        signed 32-bit range (inferred as
        :class:`~literalizer._formatters.type_inference.WideInt`); the
        formatter then casts every element to the wider fixed-width type
        (e.g. ``long`` / ``i64``).  Languages with no such widening (the
        common case) return ``None`` via
        :data:`no_format_integer_widened`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_integer_beyond_i64(self) -> Callable[[int], str] | None:
        """Integer formatter for collections that exceed signed 64-bit
        range, or ``None`` when the language has no such widening.

        Used when a sequence/set/map mixes integers that do not all fit
        signed 64-bit range (inferred as
        :class:`~literalizer._formatters.type_inference.BeyondI64`); the
        formatter then casts every element to the language's further-
        widened type (e.g. ``BigInt``, ``uint64``, ``i128``).  Languages
        with no such widening return ``None`` via
        :data:`no_format_integer_beyond_i64`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a :class:`NewVariable` declaration whose
        right-hand side is a call expression rather than a literal.

        Languages whose literal-binding declaration injects a
        value-type-derived tag (Haskell's ``x :: Val``, F#'s
        ``x: Val = FInt ...``) override this to drop the tag and let the
        compiler infer the call's return type.  Languages with no such
        tag reuse :attr:`format_variable_declaration` unchanged via
        :data:`default_format_call_variable_declaration`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an :class:`ExistingVariable` binding
        whose right-hand side is a call expression rather than a literal.

        The call-expression counterpart of
        :attr:`format_variable_assignment`; see
        :attr:`format_call_variable_declaration`.  Languages with no
        value-type tag reuse :attr:`format_variable_assignment`
        unchanged via :data:`default_format_call_variable_assignment`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def sequence_binding_declarations(
        self, declarations: tuple[str, ...]
    ) -> str:
        """Combine the per-binding ``bare_code`` snippets of a
        multi-binding file into one body.

        Most languages join the snippets with newlines via
        :data:`default_sequence_binding_declarations`.  Languages that
        need ordering (Fortran: every specification statement before
        every executable one) or structural nesting (Nix's chained
        ``let``) override this.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def format_call_binding_body_preamble(self) -> tuple[str, ...]:
        """Module-internal body-preamble lines required only when a
        top-level binding holds an inference-bound call result.

        Most languages need none and return ``()`` via
        :data:`no_call_binding_body_preamble`.  PureScript overrides
        this with ``import Prelude`` (its call stub returns ``Unit``).
        """
        ...  # pylint: disable=unnecessary-ellipsis

    def format_call_binding_file_pragmas(self) -> tuple[str, ...]:
        """File-level compiler-pragma lines required only when a
        top-level binding holds an inference-bound call result.

        Most languages need none and return ``()`` via
        :data:`no_call_binding_file_pragmas`.  Haskell overrides this to
        suppress ``-Wmissing-signatures`` for the binding, whose type
        the renderer cannot annotate.
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
    def integer_width_strategy(self) -> enum.Enum:
        """The integer-width strategy chosen for this language
        instance.
        """
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
    def statement_terminator_style(self) -> enum.Enum:
        """The statement terminator option chosen for this language
        instance.
        """
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
    def leading_preamble(self) -> LeadingPreamble:
        """Callable returning preamble lines that must come *before*
        :attr:`static_preamble` (and every other preamble line).

        Receives the original data value and whether a new variable is
        being declared.  Most languages use :data:`no_leading_preamble`
        (always ``()``); Python uses it to emit ``from __future__ import
        annotations`` only when the rendered code actually contains an
        annotation, since that import must be the first statement.
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
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Data-dependent preamble lines used for call rendering.

        Most languages set this to the same callable as
        :attr:`data_dependent_preamble`.  Languages whose declaration
        preamble does not apply to inline call arguments override it.
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
    def allows_empty_call_parens(self) -> bool:
        """Whether an empty argument list is written as ``()``."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def supports_zero_parameter_calls(self) -> bool:
        """Whether the language can render a function call with no
        parameters.  When ``False``,
        :func:`~literalizer.literalize_call` rejects empty
        ``parameter_names`` with
        :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def max_call_parameters(self) -> int:
        """Maximum parameter count the language's call syntax accepts.

        :data:`NO_CALL_PARAMETER_LIMIT` for languages with no fixed
        limit.  When :func:`~literalizer.literalize_call` is given more
        ``parameter_names`` than this, it raises
        :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def call_returns_expression(self) -> bool:
        """Whether a function call in this language is an expression
        whose value can be consumed by an enclosing expression.  When
        ``False``, :func:`~literalizer.literalize_call` rejects a
        ``call_transform`` (whose output wraps the call as a value)
        with :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    supports_non_string_dict_keys: bool
    """Whether the language can represent a dict whose keys include
    values that are not strings.  When ``False``,
    :func:`~literalizer.literalize` rejects such inputs at the
    formatting boundary with
    :class:`~literalizer.exceptions.UnrepresentableInputError`.

    Most languages allow scalar dict keys natively; pure data formats
    whose surface syntax only admits string keys (JSON-family, TOML)
    set this to ``False``.
    """

    @property
    def supports_inline_multiline_dict_args(self) -> bool:
        """Whether the language can render a call argument as an inline
        dict literal that spans multiple lines.  When ``False``,
        :func:`~literalizer.literalize_call` rejects inputs that would
        produce a multi-key dict argument with
        :class:`~literalizer.exceptions.UnsupportedCallShapeError`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def supports_standalone_comments_in_wrapped_calls(self) -> bool:
        """Whether manually wrapped call output can contain standalone
        comment lines between call statements.
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
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
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
        The fourth argument is the parsed call argument data: one
        entry per rendered call, where each entry is the arguments
        row for that call (a single value for one-parameter calls, a
        list of values for multi-parameter calls).  Languages whose
        stubs need to be typed (e.g. Mojo) infer parameter types from
        this; other languages ignore it.

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
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
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
    def format_constructor_target(self) -> Callable[[str], str]:
        """Return a zero-argument constructor target for *class_name*.

        The returned string is intended to be passed to
        :func:`~literalizer.literalize_call` as ``target_function``.
        Most languages call constructors as ``ClassName()`` and use
        :data:`identity_constructor_target`; languages with constructor
        syntax outside regular function names override this to produce
        targets such as ``new ClassName``, ``NewClassName``,
        ``ClassName.new``, or ``ClassName::new``.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_arg(self) -> FormatCallArg:
        """Rewrite a formatted direct call argument.

        Called as ``format_call_arg(value, formatted)`` after *value*
        has been formatted as a literal or reference.  Languages that
        do not need wrapping set this to :data:`identity_call_arg`;
        languages such as C and Objective-C override this to wrap each
        argument in a canonical parameter type.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Validate a direct call argument after references are removed.

        Languages that accept every supported literal set this to
        :data:`no_validate_call_arg`; languages with additional call
        argument restrictions override it.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_statement(self) -> Callable[[str], str]:
        """Rewrite an assembled call expression into a valid statement.

        Languages that allow bare call statements set this to
        :data:`identity_call_statement`; languages that need a wrapper
        such as ``let _ = ...`` override it.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_ref_identifier(self) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the form
        required by this language's call expression syntax.

        Used when a ``$ref`` appears as a value inside a data structure
        (e.g. an element of a list passed to
        :func:`~literalizer.literalize`).  Languages that cannot support
        bare variable references in that context raise
        :exc:`~literalizer.exceptions.CallArgNotSupportedError` here.

        Called after :func:`~literalizer.literalize_call`'s ``ref_case``
        normalization, so *name* is already in the requested identifier
        case.  The second positional argument is the ``Value`` declared
        elsewhere for that ref (taken from the caller's ``ref_values``
        mapping), or ``None`` when the caller did not supply the value.
        Most languages emit ref identifiers bare and use
        :data:`identity_call_ref_identifier`; languages that wrap the
        identifier in a type-sensitive way (V's ``.clone()`` for
        non-scalars) inspect the value to choose the right form.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_arg_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier used as a direct
        call argument (via :func:`~literalizer.literalize_call`).

        In the call-argument context the referenced variable has already
        been emitted at the same top-level scope, so some languages that
        reject ``$ref`` in the value context (see
        :attr:`format_call_ref_identifier`) can accept it here.

        The default implementation (provided by every language class)
        delegates to :attr:`format_call_ref_identifier`.  Override this
        to allow call-argument ``$ref`` values that would otherwise be
        rejected.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Rewrite a ``{"$ref": "name"}`` call-argument identifier the
        caller authorized as consumable on
        :func:`~literalizer.literalize_call`.

        Used only for refs the caller listed in ``consumable_refs`` and
        that appear in exactly one call argument across the rendered
        calls, so the consuming form cannot strand a later use.

        The default implementation (provided by every language class)
        delegates to :attr:`format_call_arg_ref_identifier`.  Languages
        whose call-argument ``$ref`` semantics consume the variable
        (notably C++ ``std::move``) override this.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def consumable_ref_value_inhibits_consuming_form(
        self,
    ) -> Callable[[Value], bool]:
        """Predicate deciding whether a ref's underlying value type
        makes the language's consume form illegal.

        Returns ``True`` when the consume operator (e.g. Mojo ``^``)
        would be rejected for *value*, in which case the call site
        routes the ref through :attr:`format_call_arg_ref_identifier`
        instead of :attr:`format_call_arg_ref_identifier_consumable`.

        Most languages set this to :data:`never_inhibits_consuming_form`.
        Mojo overrides it: applying ``^`` to a register-trivial scalar
        (``Int``, ``Bool``, ``Float64``) is a hard error under
        ``--Werror``, so those value types inhibit the consume form.
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


@beartype
def _no_call_stub(
    _parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return no stub lines."""
    return ()


no_call_stub: Callable[
    [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
    tuple[str, ...],
] = _no_call_stub
"""Shared callable for languages that need no call stubs."""


@beartype
def _identity_call_target(parts: Sequence[str], /) -> str:
    """Return the parts joined with ``"."``."""
    return ".".join(parts)


identity_call_target: Callable[[Sequence[str]], str] = _identity_call_target
"""Shared callable for languages that need no call-target rewriting."""


@beartype
def _identity_call_ref_identifier(name: str, value: Value | None, /) -> str:
    """Return *name* unchanged.

    Accepts but ignores *value*; only languages whose ref rendering
    depends on the referenced type (e.g. V's ``.clone()`` on non-scalar
    values) inspect it.
    """
    del value
    return name


identity_call_ref_identifier: Callable[[str, Value | None], str] = (
    _identity_call_ref_identifier
)
"""Shared callable for languages that need no ``$ref`` identifier
rewriting.  Languages that decorate ref identifiers (e.g. PHP's
``$name`` or Perl's ``$name``) override
:attr:`Language.format_call_ref_identifier` instead.

The callable receives both the (already case-converted) ref name and the
``Value`` declared elsewhere for that ref (or ``None`` when the caller
did not pass ``ref_values``).  Most languages ignore the value; V uses
it to skip ``.clone()`` for scalars.
"""


@beartype
def _never_inhibits_consuming_form(_value: Value, /) -> bool:
    """Return ``False`` — the language's consuming form accepts every
    value type.
    """
    return False


never_inhibits_consuming_form: Callable[[Value], bool] = (
    _never_inhibits_consuming_form
)
"""Shared callable for languages whose consume form (e.g. C++
``std::move``) is valid for every value type.  Languages whose consume
operator rejects certain value types (notably the Mojo ``^``, which is a
hard error on register-trivial scalars under ``--Werror``) override
:attr:`Language.consumable_ref_value_inhibits_consuming_form` to a
predicate that returns ``True`` for those values.
"""


@beartype
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


@beartype
def _no_data_preamble(_data: Value, /) -> tuple[str, ...]:
    """Return no preamble lines — used by languages that do not need
    data-dependent preamble.
    """
    return ()


no_data_preamble: Callable[[Value], tuple[str, ...]] = _no_data_preamble
"""Shared callable for languages with no data-dependent preamble."""


@beartype
def _no_leading_preamble_callable(
    _data: Value, /, *, has_variable_declaration: bool
) -> tuple[str, ...]:
    """Return no leading preamble lines."""
    del has_variable_declaration
    return ()


@beartype
def _no_leading_preamble(self: "Language") -> LeadingPreamble:
    """Default ``leading_preamble`` -- no preamble lines that must
    precede :attr:`Language.static_preamble`.
    """
    del self
    return _no_leading_preamble_callable


no_leading_preamble: property = property(fget=_no_leading_preamble)
"""Shared ``leading_preamble`` descriptor for languages that emit no
preamble lines required to come before :attr:`Language.static_preamble`.
"""


class _NoPygmentsName(str):
    """Descriptor for languages with no matching Pygments lexer alias."""

    __slots__ = ()

    @beartype
    def __get__(
        self, _instance: object | None, _owner: type[object] | None
    ) -> None:
        """Return ``None`` for both class and instance access."""
        del self, _instance, _owner


# Shared ``pygments_name`` descriptor for languages unsupported by Pygments.
#
# This resolves to ``None`` without storing literal ``None`` in a language
# class ``__dict__``. The interpreter treats that literal value as the PEP 544
# "attribute is not implemented" signal during runtime Protocol checks,
# which prevents ABC cache warming and makes repeated ``isinstance(_,
# Language)`` calls walk every protocol member.
# See https://github.com/python/cpython/issues/102433 for related
# runtime Protocol attribute lookup context.
no_pygments_name = _NoPygmentsName()


@beartype
def _no_validate_spec_for_data(self: "Language", data: Value) -> None:
    """Default ``validate_spec_for_data`` — no spec/data constraints."""
    del self, data


no_validate_spec_for_data: Callable[["Language", Value], None] = (
    _no_validate_spec_for_data
)
"""Shared callable for languages with no spec/data constraints to
check.
"""


@beartype
def _data_has_empty_dict(*, data: Value) -> bool:
    """Return ``True`` if *data* contains an empty mapping anywhere.

    Descends into lists, sets, and dict values.  Dict keys are scalars
    so cannot themselves be empty mappings.
    """
    match data:
        case dict() if len(data) == 0:
            return True
        case dict():
            return any(_data_has_empty_dict(data=v) for v in data.values())
        case list() | set():
            return any(_data_has_empty_dict(data=item) for item in data)
        case _:
            return False


@beartype
def reject_empty_dicts(*, data: Value, language_name: str) -> None:
    """Raise :class:`~literalizer.exceptions.UnrepresentableEmptyDictError`
    if *data* contains an empty mapping at any depth.

    Used by ``validate_spec_for_data`` on languages whose runtime
    representation cannot distinguish an empty mapping from an empty
    sequence (Lua, PHP, R).
    """
    if _data_has_empty_dict(data=data):
        msg = (
            f"{language_name} cannot represent an empty dict "
            "distinctly from an empty list; both serialize to the "
            "same runtime collection so the mapping/sequence "
            "distinction is lost on round-trip."
        )
        raise UnrepresentableEmptyDictError(msg)


@beartype
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
def _no_format_integer_widened(self: "Language") -> None:
    """Default ``format_integer_widened`` -- no mixed-magnitude integer
    widening, so the renderer keeps the normal integer formatter.
    """
    del self


no_format_integer_widened: property = property(fget=_no_format_integer_widened)
"""Shared ``format_integer_widened`` descriptor for languages with no
mixed-magnitude integer widening.  Resolves to ``None`` so the renderer
falls back to the language's normal integer formatter.
"""


@beartype
def _no_format_integer_beyond_i64(self: "Language") -> None:
    """Default ``format_integer_beyond_i64`` -- no beyond-i64 integer
    widening, so the renderer keeps the normal integer formatter.
    """
    del self


no_format_integer_beyond_i64: property = property(
    fget=_no_format_integer_beyond_i64
)
"""Shared ``format_integer_beyond_i64`` descriptor for languages with no
beyond-i64 integer widening.  Resolves to ``None`` so the renderer
falls back to the language's normal integer formatter.
"""


@beartype
def _default_format_call_variable_declaration(
    self: "Language",
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Default ``format_call_variable_declaration`` -- reuse the
    literal-binding declaration formatter unchanged.
    """
    return self.format_variable_declaration


default_format_call_variable_declaration: property = property(
    fget=_default_format_call_variable_declaration
)
"""Shared descriptor for languages whose call-result declaration is
formatted exactly like a literal binding (no value-type tag to drop).
"""


@beartype
def _default_format_call_variable_assignment(
    self: "Language",
) -> Callable[[str, str, Value], str]:
    """Default ``format_call_variable_assignment`` -- reuse the
    literal-binding assignment formatter unchanged.
    """
    return self.format_variable_assignment


default_format_call_variable_assignment: property = property(
    fget=_default_format_call_variable_assignment
)
"""Shared descriptor for languages whose call-result assignment is
formatted exactly like a literal binding (no value-type tag to drop).
"""


@beartype
def _default_sequence_binding_declarations(
    self: "Language", declarations: tuple[str, ...]
) -> str:
    """Default ``sequence_binding_declarations`` -- join the per-binding
    snippets with newlines.
    """
    del self
    return "\n".join(declarations)


default_sequence_binding_declarations: Callable[
    ["Language", tuple[str, ...]], str
] = _default_sequence_binding_declarations
"""Shared callable for languages that concatenate multi-binding
``bare_code`` snippets with plain newlines.
"""


@beartype
def _no_call_binding_body_preamble(self: "Language") -> tuple[str, ...]:
    """Default ``format_call_binding_body_preamble`` -- no extra body
    preamble lines for an inference-bound call result.
    """
    del self
    return ()


no_call_binding_body_preamble: Callable[["Language"], tuple[str, ...]] = (
    _no_call_binding_body_preamble
)
"""Shared callable for languages needing no call-binding body preamble."""


@beartype
def _no_call_binding_file_pragmas(self: "Language") -> tuple[str, ...]:
    """Default ``format_call_binding_file_pragmas`` -- no file-level
    compiler-pragma line for an inference-bound call result.
    """
    del self
    return ()


no_call_binding_file_pragmas: Callable[["Language"], tuple[str, ...]] = (
    _no_call_binding_file_pragmas
)
"""Shared callable for languages needing no call-binding file pragmas."""


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


@beartype
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


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class FileSection:
    """One named region of a multi-section language's rendered output.

    Most languages render a value as a single fragment that a caller can
    drop straight into a program template (the way the C, C++, Haskell
    and Zig round-trip helpers do).  A few cannot: their output spans
    more than one region of a source file that a wrapping template must
    place separately.  COBOL under ``json_type=CJSON`` is the current
    example -- it produces WORKING-STORAGE declarations and PROCEDURE
    DIVISION statements that live in different divisions.

    For such languages :attr:`~literalizer.LiteralizeResult.sections`
    exposes the regions as a tuple of these objects, so a caller can
    compose each one into the right place in its own template without
    parsing any language-internal marker.  Single-section languages
    leave that attribute empty.
    """

    name: str
    """A stable label identifying the region within its language (for
    COBOL ``json_type=CJSON``, ``"WORKING-STORAGE"`` or
    ``"PROCEDURE"``).
    """

    content: str
    """The region's text, with no marker lines and no enclosing program
    boilerplate.
    """


# A language that emits more than one :class:`FileSection` joins the
# regions into the single string its formatter must return by bracketing
# each one with a marker line.  The marker carries a null byte, which
# never occurs in real source, so a content line can never be mistaken
# for a marker and :func:`decode_file_sections` can split single-section
# output back out as "no sections" cheaply.
_FILE_SECTION_OPEN: Final = "\x00literalizer-file-section:"
_FILE_SECTION_CLOSE: Final = "\x00"


@beartype
def encode_file_sections(sections: tuple[FileSection, ...], /) -> str:
    """Join *sections* into one marker-bracketed payload string.

    The inverse of :func:`decode_file_sections`.  A language whose
    formatter must return a single string, yet whose output is really
    several :class:`FileSection` regions, returns the result of this
    function; the wrapping layer (and any
    :attr:`~literalizer.LiteralizeResult.sections` consumer) recovers the
    regions with :func:`decode_file_sections`.
    """
    parts: list[str] = []
    for section in sections:
        parts.append(
            f"{_FILE_SECTION_OPEN}{section.name}{_FILE_SECTION_CLOSE}"
        )
        parts.append(section.content)
    return "\n".join(parts)


@beartype
def _decode_one_section(chunk: str, /) -> FileSection:
    """Build a :class:`FileSection` from one marker-headed *chunk*.

    *chunk* is a region of an :func:`encode_file_sections` payload: a
    marker line (which may retain its leading ``_FILE_SECTION_OPEN``)
    followed by the region's content.
    """
    header, _, content = chunk.partition("\n")
    name = header.removeprefix(_FILE_SECTION_OPEN).removesuffix(
        _FILE_SECTION_CLOSE
    )
    return FileSection(name=name, content=content)


@beartype
def decode_file_sections(payload: str, /) -> tuple[FileSection, ...]:
    """Split an :func:`encode_file_sections` *payload* into its regions.

    Returns an empty tuple when *payload* carries no marker (the
    single-section case for almost every language), so callers can treat
    a non-empty result as "this output is multi-section".
    """
    if _FILE_SECTION_OPEN not in payload:
        return ()
    sectioned = payload[payload.index(_FILE_SECTION_OPEN) :]
    chunks = sectioned.split(sep=f"\n{_FILE_SECTION_OPEN}")
    return tuple(_decode_one_section(chunk) for chunk in chunks)
