"""Rust language specification."""

import dataclasses
import datetime
import enum
import re
from collections import Counter
from collections.abc import Callable, Hashable, Mapping, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, Final, assert_never

from beartype import beartype

from literalizer._checks import (
    reject_aware_datetimes,
    reject_ragged_nested_sequences,
)
from literalizer._comments import NestingCommentSuffix
from literalizer._formatters.collection_openers import fixed_open
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    sequence_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
    make_overflow_fallback_formatter,
    raise_for_unrepresentable_int,
)
from literalizer._formatters.format_strings import (
    bidi_escape_replacements,
    format_string_backslash,
    has_bidi_formatting_character,
    make_backslash_string_formatter,
)
from literalizer._formatters.tuple_strategy import collect_tuple_list_ids
from literalizer._formatters.type_inference import (
    RecordShape,
    collect_record_shapes,
    drop_unrecordizable_nested_sibling_maps,
    unify_record_shapes,
)
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    collect_sibling_map_wrap_ids,
    iter_wrapped_scalars,
)
from literalizer._json_native_document import (
    register_json_native_document_fast,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
    CallParameterShadowing,
    CallStyle,
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
    LeadingPreamble,
    ModifierCombination,
    NewVariableNameSyntax,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    RecordMapValueTypings,
    RenderedRecordLiteral,
    RenderedTupleLiteral,
    RoundTripCapability,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_compute_call_slot_wrap_ids,
    no_data_preamble,
    no_empty_container_literal_overrides,
    no_format_integer_widened,
    no_type_hint_preamble,
    no_validate_call_arg,
    prepend_body_preamble,
)
from literalizer._types import CallPreambleData, OrderedMap, Scalar, Value
from literalizer.exceptions import (
    IncompatibleFormatsError,
    InvalidRecordNameError,
    UnrepresentableInputError,
)

_RUST_RAW_STRING_OPEN = re.compile(pattern=r'(?<![A-Za-z0-9_])r(#{1,255})"')
_TRAILING_LINE_WHITESPACE = re.compile(pattern=r"[ \t]+(?=\n)")
_format_string_backslash_nul = make_backslash_string_formatter(
    quote_char='"',
    extra_replacements=[
        ("\0", r"\0"),
        *bidi_escape_replacements(template="\\u{{{:04X}}}"),
    ],
)


def _reject_float_collection_keys(data: Value) -> None:
    """Reject floats requiring unavailable Rust
    equality, hashing, and ordering traits.
    """
    match data:
        case dict():
            if any(isinstance(key, float) for key in data):
                msg = "Rust map formats cannot use float keys"
                raise UnrepresentableInputError(msg)
            for value in data.values():
                _reject_float_collection_keys(data=value)
        case set():
            if any(isinstance(value, float) for value in data):
                msg = "Rust set formats cannot use float members"
                raise UnrepresentableInputError(msg)
        case list():
            for value in data:
                _reject_float_collection_keys(data=value)
        case _:
            return


def _indent_code_preserving_raw_strings(text: str, prefix: str) -> str:
    """Indent Rust code lines without changing multiline raw contents."""
    raw_hashes: str | None = None
    result: list[str] = []
    split_lines = text.split(sep="\n")
    for index, line_without_lf in enumerate(iterable=split_lines):
        line = line_without_lf + ("\n" if index < len(split_lines) - 1 else "")
        should_indent = raw_hashes is None and bool(line.strip())
        result.append(prefix + line if should_indent else line)
        position = 0
        while True:
            if raw_hashes is None:
                match = _RUST_RAW_STRING_OPEN.search(
                    string=line,
                    pos=position,
                )
                if match is None:
                    break
                raw_hashes = match[1]
                position = match.end()
            else:
                closer = f'"{raw_hashes}'
                close_position = line.find(closer, position)
                if close_position < 0:
                    break
                position = close_position + len(closer)
                raw_hashes = None
    return "".join(result)


@beartype
def _format_string_raw(value: str) -> str:
    r"""Format a string as a Rust raw string literal.

    Uses the ``r#"…"#`` syntax. If the value contains the closing
    sequence ``"#``, extra ``#`` characters are added to disambiguate.

    Falls back to an escaped string for multiline content, since
    indentation applied by wrapping code would corrupt the value.
    """
    if (
        "\n" in value
        or "\r" in value
        or "\0" in value
        or has_bidi_formatting_character(value=value)
    ):
        return _format_string_backslash_nul(value=value)
    hashes = "#"
    while f'"{hashes}' in value:
        hashes += "#"
    return f'r{hashes}"{value}"{hashes}'


@beartype
def _format_string_multiline(value: str) -> str:
    r"""Format *value* as a collision-free multiline Rust raw string."""
    if (
        "\0" in value
        or "\r" in value
        or has_bidi_formatting_character(value=value)
        or _TRAILING_LINE_WHITESPACE.search(string=value) is not None
    ):
        return _format_string_backslash_nul(value=value)
    for hash_count in range(1, 256):
        hashes = "#" * hash_count
        if f'"{hashes}' not in value:
            return f'r{hashes}"{value}"{hashes}'
    # Rust reserves raw strings with more than 255 hashes. Reaching this
    # requires a value containing every legal raw-string closing delimiter.
    return format_string_backslash(value=value)  # pragma: no cover


class _RustModifiers(enum.Enum):
    """Declaration modifiers supported by Rust.

    Rust has no C++/Java/C#-style storage or qualifier keywords, but a
    ``let`` binding is immutable by default and a mutate-after-bind
    sequence needs ``let mut``.  ``MUT`` requests that mutable binding
    (issue #2537); the member's value is the ``mut`` keyword it renders
    to.  It applies to the default ``LET`` declaration style only.

    Exposed as :attr:`Rust.Modifiers` / :attr:`Rust.modifiers`.
    """

    MUT = "mut"
    """Mutability: the binding may be mutated through its name, so a
    subsequent ``&mut self`` method call on the bound value compiles.
    """


_PASCAL_CASE_IDENTIFIER = re.compile(pattern=r"^[A-Z][A-Za-z0-9_]*$")

# Rust keywords (strict, reserved, weak) that are syntactically valid
# PascalCase identifiers; lowercase keywords cannot collide with a name
# that must start with an uppercase letter.
_RUST_EMITTED_TYPE_NAMES: Final[frozenset[str]] = frozenset(
    {
        # Brought in by the ``use`` lines this back end emits.
        "BTreeMap",
        "BTreeSet",
        "HashMap",
        "HashSet",
        "LazyLock",
        "NaiveDate",
        "NaiveDateTime",
        "NaiveTime",
        # Named by rendered types without an import: the prelude
        # supplies these, and ``serde_json`` supplies ``Value``.
        "Box",
        "Option",
        "String",
        "Value",
        "Vec",
    }
)
"""Type names rendered Rust can reference.

A struct named after one of these either shadows the type the same file
uses or clashes with its ``use`` line, so rustc rejects the output
(issue #4536).
"""


_RUST_PASCAL_KEYWORDS: frozenset[str] = frozenset({"Self"})

# Rust keywords (strict and reserved, editions 2015 through 2024) that
# are legal in raw-identifier form, so a dict key that collides with
# one can still name a struct field as ``r#keyword`` (issue #2880).
# ``crate``/``self``/``super``/``Self`` are excluded because ``rustc``
# rejects them as raw identifiers.  Weak keywords (``union``, ``raw``,
# ...) are valid field names verbatim and need no escaping.
_RUST_RAW_ESCAPABLE_KEYWORDS: frozenset[str] = frozenset(
    {
        "abstract",
        "as",
        "async",
        "await",
        "become",
        "box",
        "break",
        "const",
        "continue",
        "do",
        "dyn",
        "else",
        "enum",
        "extern",
        "false",
        "final",
        "fn",
        "for",
        "gen",
        "if",
        "impl",
        "in",
        "let",
        "loop",
        "macro",
        "match",
        "mod",
        "move",
        "mut",
        "override",
        "priv",
        "pub",
        "ref",
        "return",
        "static",
        "struct",
        "trait",
        "true",
        "try",
        "type",
        "typeof",
        "unsafe",
        "unsized",
        "use",
        "virtual",
        "where",
        "while",
        "yield",
    }
)

# Dict keys that are identifier-shaped text but can never name a Rust
# struct field: the keywords ``rustc`` rejects even in raw-identifier
# form, plus the reserved wildcard identifier ``_`` (``r#_`` is
# likewise rejected).
_RUST_UNUSABLE_FIELD_KEYS: frozenset[str] = frozenset(
    {"crate", "self", "super", "Self", "_"}
)

_RUST_IDENTIFIER = re.compile(pattern=r"^[A-Za-z_][A-Za-z0-9_]*$")

_I32_MIN = -(2**31)
_I32_MAX = 2**31 - 1
_I64_MIN = -(2**63)
_I64_MAX = 2**63 - 1
_I128_MIN = -(2**127)
_I128_MAX = 2**127 - 1
_SERDE_JSON_MACRO = "serde_json::json!"

# A location in parsed input: list indexes are integers and mapping keys are
# strings.  ``()`` identifies the document root.
type EmptyContainerPath = tuple[str | int, ...]


@beartype
def _rust_integer_type(value: int) -> str:
    """Return the narrowest Rust integer type for *value*."""
    if _I32_MIN <= value <= _I32_MAX:
        return "i32"
    if _I64_MIN <= value <= _I64_MAX:
        return "i64"
    return "i128"


@beartype
def _apply_rust_integer_suffix(value: int, base: Callable[[int], str]) -> str:
    """Format with a Rust type suffix when *value* overflows i32."""
    formatted = base(value)
    if _I32_MIN <= value <= _I32_MAX:
        return formatted
    return f"{formatted}{_rust_integer_type(value=value)}"


@beartype
def _make_rust_integer_suffix_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a formatter to append a Rust type suffix when the value
    overflows i32.

    A Rust integer literal with no suffix defaults to ``i32``.
    Values that don't fit in ``i32`` must carry a type suffix or a
    type-annotated context, otherwise ``rustc`` rejects them with
    ``literal out of range for i32``.  The suffix chosen matches the
    narrowest type that holds *value*.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_rust_integer_suffix(value=value, base=base)

    return _format


@beartype
def _make_rust_i128_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a formatter to always append the ``i128`` type suffix.

    Used for homogeneous collections whose least upper bound is
    ``i128`` (mixed signed-64-bit / beyond-i64 magnitudes) so every
    element agrees with the container type rustc infers.
    """

    def _format(value: int) -> str:
        """Format *value* as ``<base>i128``."""
        return f"{base(value)}i128"

    return _format


@beartype
def _format_constructor_target(class_name: str, /) -> str:
    """Return a Rust ``ClassName::new`` constructor call target."""
    return f"{class_name}::new"


_constructor_target: Callable[[str], str] = _format_constructor_target


_RUST_INTEGER_WIDTHS = ("i32", "i64", "i128")


@beartype
def _unify_rust_types(types: Sequence[str]) -> str:
    """Return a single Rust type that covers *types*.

    All-integer type lists widen to the largest integer; otherwise,
    returns the single type present.  A declaration style that needs an
    annotation can still reach a collection whose element types differ
    in shape rather than in width -- a list beside a map -- which no
    single Rust type covers, so that is refused (issue #3939).

    Callers must pass a non-empty sequence.
    """
    unique = list(dict.fromkeys(types))
    match unique:
        case [only]:
            return only
        case _ if all(name in _RUST_INTEGER_WIDTHS for name in unique):
            return max(unique, key=_RUST_INTEGER_WIDTHS.index)
        case _:
            msg = (
                "Rust cannot annotate a collection whose element types "
                f"differ: {', '.join(sorted(unique))}."
            )
            raise UnrepresentableInputError(msg)


@beartype
def _rust_scalar_type(
    *,
    data: Scalar,
    date_type: str,
    datetime_type: str,
) -> str:
    """Return the Rust type annotation for a scalar value."""
    match data:
        case bool():
            result = "bool"
        case int():
            result = _rust_integer_type(value=data)
        case float():
            result = "f64"
        case str() | bytes():
            result = "&str"
        case datetime.date():
            result = (
                datetime_type
                if isinstance(data, datetime.datetime)
                else date_type
            )
        case datetime.time():
            result = "&str"
        case None:
            result = "Option<()>"
        case _ as unreachable:
            assert_never(unreachable)
    return result


@beartype
def _rust_homogeneous_element_type(
    *,
    elements: Sequence[Value],
    infer: Callable[[Value], str],
    default_type: str,
    sequence_encodes_length: bool,
) -> str:
    """Return the element type for a homogeneous Rust collection.

    An empty nested collection infers the language's default element
    type, which is a placeholder rather than a statement about the
    data, so a non-empty sibling decides for it (issue #3939).

    An empty *sequence* is only a placeholder where the sequence
    annotation leaves length out.  ``[T; 0]`` is a different type from
    ``[T; 2]`` and no sibling can speak for it, so under a
    length-bearing format the empty sequence keeps its own type and
    unification reports the mismatch.
    """
    if not elements:
        return default_type
    informative = [
        element
        for element in elements
        if element
        or not isinstance(element, (list, dict, set))
        or (sequence_encodes_length and isinstance(element, list))
    ]
    types = [infer(element) for element in informative or elements]
    return _unify_rust_types(types=types)


@beartype
def _rust_sequence_encodes_length(
    *,
    sequence_format_type_annotation: Callable[[str, int], str],
) -> bool:
    """Return whether a sequence annotation spells its length.

    ``ARRAY`` renders ``[T; N]`` and ``VEC`` renders ``Vec<T>``, so the
    formatter itself answers this rather than a declared flag.
    """
    return sequence_format_type_annotation(
        "T", 0
    ) != sequence_format_type_annotation("T", 1)


@beartype
def _rust_type_annotation(
    *,
    data: Value,
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
    set_format_type_annotation: Callable[[str], str],
    dict_format_type_annotation: Callable[[str, str], str],
    default_sequence_element_type: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
) -> str:
    """Derive a Rust type annotation string from a ``Value``.

    ``dict_format_type_annotation`` emits ``HashMap<K, V>`` or
    ``BTreeMap<K, V>`` for ``LAZY_STATIC``; for ``CONST`` / ``STATIC``
    it is a callable that raises :exc:`IncompatibleFormatsError`,
    since Rust has no const-expression dict format.
    """

    def recurse(element: Value) -> str:
        """Delegate to module-level implementation."""
        return _rust_type_annotation(
            data=element,
            date_type=date_type,
            datetime_type=datetime_type,
            sequence_format_type_annotation=sequence_format_type_annotation,
            sequence_supports_heterogeneity=sequence_supports_heterogeneity,
            set_format_type_annotation=set_format_type_annotation,
            dict_format_type_annotation=dict_format_type_annotation,
            default_sequence_element_type=default_sequence_element_type,
            default_set_element_type=default_set_element_type,
            default_dict_key_type=default_dict_key_type,
            default_dict_value_type=default_dict_value_type,
        )

    # A heterogeneous format annotates each element in place, so its
    # arity already carries the length and the probe below must not run
    # -- ``format_type_annotation`` raises for those formats.
    sequence_encodes_length = (
        sequence_supports_heterogeneity
        or _rust_sequence_encodes_length(
            sequence_format_type_annotation=sequence_format_type_annotation,
        )
    )

    match data:
        case set():
            element_type = _rust_homogeneous_element_type(
                elements=list(data),
                infer=recurse,
                default_type=default_set_element_type,
                sequence_encodes_length=sequence_encodes_length,
            )
            return set_format_type_annotation(element_type)
        case list():
            if sequence_supports_heterogeneity:
                element_types = [recurse(element=e) for e in data]
                inner = ", ".join(element_types)
                if len(element_types) == 1:
                    inner += ","
                return f"({inner})"
            element_type = _rust_homogeneous_element_type(
                elements=data,
                infer=recurse,
                default_type=default_sequence_element_type,
                sequence_encodes_length=sequence_encodes_length,
            )
            return sequence_format_type_annotation(element_type, len(data))
        case dict():
            keys: list[Value] = list(data)
            key_type = _rust_homogeneous_element_type(
                elements=keys,
                infer=recurse,
                default_type=default_dict_key_type,
                sequence_encodes_length=sequence_encodes_length,
            )
            value_type = _rust_homogeneous_element_type(
                elements=list(data.values()),
                infer=recurse,
                default_type=default_dict_value_type,
                sequence_encodes_length=sequence_encodes_length,
            )
            return dict_format_type_annotation(key_type, value_type)
        case _:
            return _rust_scalar_type(
                data=data,
                date_type=date_type,
                datetime_type=datetime_type,
            )


@beartype
def _format_typed_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    keyword: str,
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
    default_sequence_element_type: str,
    default_set_element_type: str,
) -> str:
    """Format a ``const`` or ``static`` declaration with a type
    annotation.
    """

    def _reject_dict(_key_type: str, _value_type: str) -> str:
        """Reject dict data for ``CONST`` / ``STATIC``.

        Rust's ``HashMap::from`` and ``BTreeMap::from`` are runtime
        calls, so neither produces a constant-expression initializer.
        """
        msg = (
            f"Rust {keyword.upper()} requires a constant-expression "
            f"initializer, but the dict format produces a runtime "
            f"::from([…]) call which is not a constant expression."
        )
        raise IncompatibleFormatsError(msg)

    def _reject_set(_element_type: str) -> str:
        """Reject set data for ``CONST`` / ``STATIC``.

        Rust's ``HashSet::from`` and ``BTreeSet::from`` are runtime
        calls, so neither produces a constant-expression initializer.
        """
        msg = (
            f"Rust {keyword.upper()} requires a constant-expression "
            f"initializer, but the set format produces a runtime "
            f"::from([…]) call which is not a constant expression."
        )
        raise IncompatibleFormatsError(msg)

    type_annotation = _rust_type_annotation(
        data=data,
        date_type=date_type,
        datetime_type=datetime_type,
        sequence_format_type_annotation=(sequence_format_type_annotation),
        sequence_supports_heterogeneity=(sequence_supports_heterogeneity),
        set_format_type_annotation=_reject_set,
        dict_format_type_annotation=_reject_dict,
        default_sequence_element_type=default_sequence_element_type,
        default_set_element_type=default_set_element_type,
        default_dict_key_type="",
        default_dict_value_type="",
    )
    return f"{keyword} {name}: {type_annotation} = {value};"


@beartype
def _format_lazy_static_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
    set_format_type_annotation: Callable[[str], str],
    dict_format_type_annotation: Callable[[str, str], str],
    default_sequence_element_type: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
) -> str:
    """Format a ``LazyLock``-wrapped ``static`` declaration."""
    type_annotation = _rust_type_annotation(
        data=data,
        date_type=date_type,
        datetime_type=datetime_type,
        sequence_format_type_annotation=sequence_format_type_annotation,
        sequence_supports_heterogeneity=sequence_supports_heterogeneity,
        set_format_type_annotation=set_format_type_annotation,
        dict_format_type_annotation=dict_format_type_annotation,
        default_sequence_element_type=default_sequence_element_type,
        default_set_element_type=default_set_element_type,
        default_dict_key_type=default_dict_key_type,
        default_dict_value_type=default_dict_value_type,
    )
    return (
        f"static {name}: LazyLock<{type_annotation}> = "
        f"LazyLock::new(|| {value});"
    )


@beartype
def _lazy_static_placeholder_formatter(
    _name: str,
    _value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Unreachable placeholder for ``LAZY_STATIC``'s config formatter.

    ``LAZY_STATIC`` needs the inferred Rust type to render
    ``LazyLock<T>``, which the template-based config formatter cannot
    provide.  :meth:`DeclarationStyles.build_formatter` routes
    ``LAZY_STATIC`` to :func:`_format_lazy_static_declaration`
    instead; this function exists only so the enum value is distinct
    from ``STATIC`` (``ruff`` ``PIE796``).
    """
    msg = (
        "Rust LAZY_STATIC requires the type-aware formatter built by "
        "build_formatter; the DeclarationStyleConfig formatter is a "
        "placeholder and must not be called directly."
    )
    raise NotImplementedError(msg)


@beartype
def _format_let_declaration(
    name: str,
    value: str,
    _data: Value,
    modifiers: frozenset[enum.Enum],
) -> str:
    """Format a Rust ``let`` binding for the ``LET`` declaration style.

    ``LET`` is immutable by default.  When the caller requests
    :attr:`Rust.Modifiers.MUT` via ``NewVariable(modifiers=…)`` the
    rendered binding gains a ``mut`` keyword after ``let`` so the bound
    value can be mutated through the name (issue #2537).  Modifier
    members of other languages' enums are silently ignored.
    """
    keyword = "let mut" if _RustModifiers.MUT in modifiers else "let"
    return f"{keyword} {name} = {value};"


@beartype
def _rust_json_value_expression(value: str, /) -> str:
    """Wrap *value* in ``serde_json::json!`` unless it is already a
    JSON macro expression.
    """
    if value.startswith(f"{_SERDE_JSON_MACRO}("):
        return value
    return f"{_SERDE_JSON_MACRO}({value})"


@beartype
def _format_rust_json_call_arg(_raw_value: Value, formatted: str) -> str:
    """Format a direct Rust call argument as ``serde_json::Value``."""
    return _rust_json_value_expression(formatted)


@beartype
def _rust_json_non_scalar_child(  # pragma: no cover
    _raw_value: Value,
    formatted: str,
) -> str:
    """Identity wrapper signaling JSON can hold non-scalar children."""
    return formatted


@beartype
def _format_rust_json_assignment(name: str, value: str, _data: Value) -> str:
    """Assign a rendered literal to a Rust JSON value binding."""
    return f"{name} = {_rust_json_value_expression(value)};"


@beartype
def _format_date_rust(value: datetime.date) -> str:
    """Format a date as a Rust ``NaiveDate::from_ymd_opt(...)`` call."""
    return (
        f"NaiveDate::from_ymd_opt({value.year}, {value.month}, {value.day})"
        ".unwrap()"
    )


@beartype
def _format_datetime_rust(value: datetime.datetime) -> str:
    """Format a datetime as a Rust ``NaiveDateTime::new(...)`` call."""
    date = _format_date_rust(value=value)
    if value.microsecond:
        time_call = (
            f"NaiveTime::from_hms_micro_opt("
            f"{value.hour}, {value.minute}, {value.second}, "
            f"{value.microsecond}).unwrap()"
        )
    else:
        time_call = (
            f"NaiveTime::from_hms_opt("
            f"{value.hour}, {value.minute}, {value.second}).unwrap()"
        )
    return f"NaiveDateTime::new({date}, {time_call})"


@dataclasses.dataclass(frozen=True)
class _VariantSignature:
    """Name and optional inner-type string for one tagged-enum variant.

    ``inner_type`` is ``None`` for unit variants (e.g. ``Null``); for
    payload-carrying variants it's the Rust type rendered between the
    parentheses, e.g. ``"i32"`` for ``I32(i32)``.
    """

    name: str
    inner_type: str | None


@beartype
def _heterogeneous_variant_for_scalar(  # noqa: C901  # pylint: disable=too-complex
    *,
    value: Scalar,
    date_type: str,
    datetime_type: str,
) -> _VariantSignature:
    """Return the tagged-enum variant signature for *value*.

    Integer values use narrowest-width variants
    (``I32``/``I64``/``I128``) to match Rust's default integer-type
    inference.
    """
    match value:
        case bool():
            signature = _VariantSignature(name="Bool", inner_type="bool")
        case int():
            int_type = _rust_integer_type(value=value)
            signature = _VariantSignature(
                name=int_type.upper(),
                inner_type=int_type,
            )
        case float():
            signature = _VariantSignature(name="F64", inner_type="f64")
        case str():
            signature = _VariantSignature(
                name="Str",
                inner_type="&'static str",
            )
        case bytes():
            signature = _VariantSignature(
                name="Bytes",
                inner_type="&'static str",
            )
        case datetime.datetime() if datetime_type in {"i32", "i64", "i128"}:
            signature = _VariantSignature(
                name=datetime_type.upper(),
                inner_type=datetime_type,
            )
        case datetime.datetime():
            signature = _VariantSignature(
                name="DateTime",
                inner_type=datetime_type,
            )
        case datetime.date():
            signature = _VariantSignature(name="Date", inner_type=date_type)
        case datetime.time():
            signature = _VariantSignature(
                name="Time",
                inner_type="&'static str",
            )
        case None:
            signature = _VariantSignature(name="Null", inner_type=None)
        case _ as unreachable:
            assert_never(unreachable)
    return signature


@dataclasses.dataclass(frozen=True)
class _StrategyParams:
    """Bundle of Rust spec knobs handed to a heterogeneous-strategy
    builder.

    Bundling these into one object keeps the builder signatures stable
    as new RECORD-only knobs (e.g. shape-unification) are added.
    """

    enum_name: str
    date_type: str
    datetime_type: str
    record_prefix: str
    record_shape_names: Mapping[frozenset[str], str]
    unify_optional_fields: bool
    map_value_typing: RecordMapValueTypings
    empty_container_type_hints: Mapping[EmptyContainerPath, str]
    sequence_format_type_annotation: Callable[[str, int], str]
    sequence_supports_heterogeneity: bool


@dataclasses.dataclass(frozen=True)
class _HeterogeneousStrategyConfig:
    """Configuration for one Rust heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Rust instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the tagged-enum declaration lines).  Both
    receive a :class:`_StrategyParams` carrying the Rust instance's
    configurable enum name, scalar type names and RECORD-strategy
    knobs.
    """

    build_behavior: Callable[[_StrategyParams], HeterogeneousBehavior]
    build_preamble: Callable[
        [_StrategyParams],
        Callable[[Value], tuple[str, ...]],
    ]


@beartype
def _build_error_behavior(
    _params: _StrategyParams,
    /,
) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


@beartype
def _build_error_preamble(
    _params: _StrategyParams,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


@beartype
def _rust_value_scalar_wrapper(
    params: _StrategyParams,
    /,
) -> Callable[[Scalar, str], str]:
    """Return a callable wrapping a scalar in the value enum.

    Shared by the ``TAGGED_ENUM`` behavior and the ``RECORD`` behavior's
    sibling-map widening (issue #2910): both render a scalar leaf as
    ``{enum_name}::{Variant}(formatted)`` (or the payload-free
    ``{enum_name}::{Variant}`` for a unit variant such as ``Null``).
    """

    def _wrap(raw_value: Scalar, formatted: str) -> str:
        """Wrap a scalar in ``{enum_name}::{Variant}(formatted)``."""
        signature = _heterogeneous_variant_for_scalar(
            value=raw_value,
            date_type=params.date_type,
            datetime_type=params.datetime_type,
        )
        if signature.inner_type is None:
            return f"{params.enum_name}::{signature.name}"
        return f"{params.enum_name}::{signature.name}({formatted})"

    return _wrap


@beartype
def _rust_is_empty_container(*, value: Value) -> bool:
    """Return whether *value* is an empty list or empty map."""
    return isinstance(value, (list, dict)) and len(value) == 0


@beartype
def _rust_is_scalar(*, value: object) -> bool:
    """Return whether *value* is a scalar rather than a ref/container."""
    return value is None or isinstance(
        value,
        (str, int, float, datetime.date, datetime.time, bytes),
    )


@beartype
def _rust_mark_container_subtree(*, item: Value, ids: set[int]) -> None:
    """Mark each list/map whose children must become enum values."""
    if not isinstance(item, (list, dict)):
        return
    ids.add(id(item))
    children = item.values() if isinstance(item, dict) else item
    for child in children:
        _rust_mark_container_subtree(item=child, ids=ids)


@beartype
def _rust_visit_container_wrap_ids(*, item: Value, ids: set[int]) -> None:
    """Find scalar-plus-container lists and mark nested contents."""
    if not isinstance(item, (list, dict)):
        return
    children: list[Value] = list(
        item.values() if isinstance(item, dict) else item
    )
    for child in children:
        _rust_visit_container_wrap_ids(item=child, ids=ids)
    if not isinstance(item, list):
        return
    has_scalar = any(_rust_is_scalar(value=child) for child in children)
    has_container = any(isinstance(child, (list, dict)) for child in children)
    has_set = any(isinstance(child, set) for child in children)
    if has_scalar and has_container and not has_set:
        _rust_mark_container_subtree(item=item, ids=ids)


@beartype
def _rust_container_wrap_ids(data: Value, /) -> frozenset[int]:
    """Return ids needed to wrap scalar-plus-container lists."""
    ids: set[int] = set()
    _rust_visit_container_wrap_ids(item=data, ids=ids)
    return frozenset(ids)


@beartype
def _tagged_enum_wrap_ids(data: Value, /) -> frozenset[int]:
    """Return every container id the ``TAGGED_ENUM`` strategy wraps.

    Unions the shared heterogeneous-scalar and sibling-map collectors
    with the Rust-specific scalar-plus-container collector so the
    behavior and preamble agree on which children are wrapped.
    """
    return (
        collect_heterogeneous_container_ids(data=data)
        | collect_sibling_map_wrap_ids(data=data)
        | _rust_container_wrap_ids(data)
    )


@beartype
def _rust_wrapped_container_kinds(
    *,
    data: Value,
    wrap_ids: frozenset[int],
) -> tuple[bool, bool, bool, bool]:
    """Return wrapped and populated list/map-kind flags.

    Mirrors :func:`iter_wrapped_scalars`: a list/map whose immediate
    container id appears in *wrap_ids* renders as a ``List`` /
    ``Map`` variant of the value enum, so the enum declaration must
    carry that variant.
    """
    has_list = False
    has_map = False
    has_populated_list = False
    has_populated_map = False

    def _visit(item: Value) -> None:
        """Record which empty-container kinds *item* wraps."""
        nonlocal has_list, has_map, has_populated_list, has_populated_map
        match item:
            case dict():
                children: list[Value] = list(item.values())
            case list():
                children = list(item)
            case _:
                return
        parent_wrapped = id(item) in wrap_ids
        for child in children:
            if parent_wrapped and isinstance(child, (list, dict)):
                match child:
                    case list():
                        has_list = True
                        has_populated_list = has_populated_list or bool(child)
                    case _:
                        has_map = True
                        has_populated_map = has_populated_map or bool(child)
            _visit(item=child)

    _visit(item=data)
    return (has_list, has_map, has_populated_list, has_populated_map)


@beartype
def _rust_container_wrapper(
    params: _StrategyParams,
    /,
) -> Callable[[Value, str], str]:
    """Return a callable wrapping a container in the value enum.

    For an empty collection, the formatted literal carries its own
    element type (e.g.
    ``Vec::<String>::new()``), which the enum variant's type would
    reject, so a bare ``vec![]`` / ``HashMap::new()`` is emitted instead
    and inferred against the variant's ``Vec<Value>`` /
    ``HashMap<&'static str, Value>``.
    """

    def _wrap(raw_value: Value, formatted_value: str) -> str:
        """Wrap a container as ``{enum_name}::{List,Map}(...)``."""
        match raw_value:
            case list():
                payload = formatted_value
                if not raw_value:
                    payload = "vec![]"
                return f"{params.enum_name}::List({payload})"
            case _:
                payload = formatted_value
                if not raw_value:
                    payload = "HashMap::new()"
                return f"{params.enum_name}::Map({payload})"

    return _wrap


@beartype
def _rust_values_by_path(*, data: Value) -> dict[EmptyContainerPath, Value]:
    """Return *data* and its descendants indexed by input path."""
    by_path: dict[EmptyContainerPath, Value] = {}

    def _visit(value: Value, path: EmptyContainerPath) -> None:
        """Index *value* and its descendants by their input paths."""
        by_path[path] = value
        if isinstance(value, list):
            for index, child in enumerate(iterable=value):
                _visit(value=child, path=(*path, index))
        elif isinstance(value, dict):
            for key, child in value.items():
                if isinstance(key, str):
                    _visit(value=child, path=(*path, key))

    _visit(value=data, path=())
    return by_path


@beartype
def _rust_empty_container_literal_overrides(
    *,
    data: Value,
    hints: Mapping[EmptyContainerPath, str],
) -> Mapping[int, str]:
    """Resolve configured empty-container paths to typed Rust literals."""
    by_path = _rust_values_by_path(data=data)
    overrides: dict[int, str] = {}
    for path, type_name in hints.items():
        value = by_path.get(path)
        if value is None:
            continue
        if not type_name:
            msg = (
                f"empty-container type hint at {path!r} must be a "
                "non-empty string"
            )
            raise ValueError(msg)
        if not _rust_is_empty_container(value=value):
            msg = (
                f"empty-container type hint at {path!r} does not target "
                "an empty list or map"
            )
            raise ValueError(msg)
        overrides[id(value)] = f"<{type_name}>::new()"
    return overrides


@beartype
def _rust_empty_container_literal_override_hook(
    params: _StrategyParams,
    /,
) -> Callable[[Value], Mapping[int, str]]:
    """Return an empty-container override hook with this strategy
    configuration.
    """

    def _overrides(data: Value, /) -> Mapping[int, str]:
        """Resolve typed empty-container literals in *data*."""
        return _rust_empty_container_literal_overrides(
            data=data,
            hints=params.empty_container_type_hints,
        )

    return _overrides


@beartype
def _rust_empty_container_hint_types(
    *, data: Value, hints: Mapping[EmptyContainerPath, str]
) -> tuple[set[str], set[str]]:
    """Return the configured ``(list_types, map_types)`` for *data*."""
    by_path = _rust_values_by_path(data=data)
    list_types: set[str] = set()
    map_types: set[str] = set()
    for path, type_name in hints.items():
        value = by_path.get(path)
        if isinstance(value, list):
            list_types.add(type_name)
        elif isinstance(value, dict):
            map_types.add(type_name)
    return (list_types, map_types)


@beartype
def _build_tagged_enum_behavior(
    params: _StrategyParams,
    /,
) -> HeterogeneousBehavior:
    """TAGGED_ENUM strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose children should wrap."""
        return _tagged_enum_wrap_ids(data)

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_rust_value_scalar_wrapper(params),
        wrap_non_scalar=None,
        wrap_empty_container=_rust_container_wrapper(params),
        empty_container_literal_overrides=no_empty_container_literal_overrides,
        compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
        dict_open_for_wrap_ids=None,
        widens_nested_maps_by_wrapping_scalars=True,
        widens_unrecordizable_nested_sibling_maps=False,
        render_record_literal=None,
        compute_record_shapes=None,
        render_tuple_literal=None,
        compute_tuple_list_ids=None,
        alias_record_ids=None,
    )


@beartype
def _rust_value_enum_lines(
    *,
    scalars: Sequence[Scalar],
    enum_name: str,
    date_type: str,
    datetime_type: str,
    include_list_variant: bool,
    include_map_variant: bool,
    list_inner_type: str | None,
    map_inner_type: str | None,
) -> list[str]:
    """Return the value-enum declaration lines for *scalars*.

    One variant per distinct scalar family present, in first-seen order,
    followed by a ``List(Vec<{enum}>)`` and/or
    ``Map(HashMap<&'static str, {enum}>)`` variant when a list/map is
    wrapped alongside the scalars. Returns an empty
    list when no variant is needed.  Shared by the ``TAGGED_ENUM``
    preamble and the ``RECORD`` preamble's sibling-map widening (issue
    #2910), which wraps scalar leaves in the same enum and never wraps
    empty containers (so it passes ``include_*_variant=False``).
    """
    variants: list[_VariantSignature] = []
    seen: set[str] = set()
    for scalar in scalars:
        signature = _heterogeneous_variant_for_scalar(
            value=scalar,
            date_type=date_type,
            datetime_type=datetime_type,
        )
        if signature.name in seen:
            continue
        seen.add(signature.name)
        variants.append(signature)
    if include_list_variant:
        variants.append(
            _VariantSignature(
                name="List", inner_type=list_inner_type or f"Vec<{enum_name}>"
            )
        )
    if include_map_variant:
        variants.append(
            _VariantSignature(
                name="Map",
                inner_type=(
                    map_inner_type or f"HashMap<&'static str, {enum_name}>"
                ),
            )
        )
    if not variants:
        return []
    lines: list[str] = [f"enum {enum_name} {{"]
    for variant in variants:
        body = (
            variant.name
            if variant.inner_type is None
            else f"{variant.name}({variant.inner_type})"
        )
        lines.append(f"    {body},")
    lines.append("}")
    return lines


@beartype
def _build_tagged_enum_preamble(
    params: _StrategyParams,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """TAGGED_ENUM strategy: emit a minimal ``enum`` declaration."""

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the tagged-enum declaration for *data*."""
        values: tuple[Value, ...] = (
            data.argument_values
            if isinstance(data, CallPreambleData)
            else (data,)
        )
        if isinstance(data, CallPreambleData):
            # Argument slots are artificial lists used only to infer
            # cross-call scalar/map widening. A scalar and a container in
            # the same parameter slot are never siblings in one rendered
            # Rust collection, so apply scalar-plus-container wrapping only
            # inside the real argument values.
            slot_wrap_ids = frozenset(
                wrap_id
                for slot in data.argument_slots
                for wrap_id in (
                    collect_heterogeneous_container_ids(data=slot)
                    | collect_sibling_map_wrap_ids(data=slot)
                )
            )
            value_wrap_ids = frozenset(
                wrap_id
                for value in values
                for wrap_id in _tagged_enum_wrap_ids(value)
            )
            wrap_ids = slot_wrap_ids | value_wrap_ids
        else:
            wrap_ids = _tagged_enum_wrap_ids(data)
        if not wrap_ids:
            return ()
        scalars = tuple(
            scalar
            for value in values
            for scalar in iter_wrapped_scalars(
                data=value,
                wrap_ids=wrap_ids,
            )
        )
        has_list = False
        has_map = False
        has_populated_list = False
        has_populated_map = False
        for value in values:
            (
                value_has_list,
                value_has_map,
                value_has_populated_list,
                value_has_populated_map,
            ) = _rust_wrapped_container_kinds(data=value, wrap_ids=wrap_ids)
            has_list = has_list or value_has_list
            has_map = has_map or value_has_map
            has_populated_list = has_populated_list or value_has_populated_list
            has_populated_map = has_populated_map or value_has_populated_map
        hinted_types = [
            _rust_empty_container_hint_types(
                data=value,
                hints=params.empty_container_type_hints,
            )
            for value in values
        ]
        list_hint_types: set[str] = set()
        map_hint_types: set[str] = set()
        for list_types, map_types in hinted_types:
            list_hint_types.update(list_types)
            map_hint_types.update(map_types)
        if has_populated_list:
            list_hint_types.clear()
        if has_populated_map:
            map_hint_types.clear()
        if len(list_hint_types) > 1:
            msg = (
                "TAGGED_ENUM can use only one concrete empty-list type per "
                "literal; supply the same type for each hinted empty list."
            )
            raise ValueError(msg)
        if len(map_hint_types) > 1:
            msg = (
                "TAGGED_ENUM can use only one concrete empty-map type per "
                "literal; supply the same type for each hinted empty map."
            )
            raise ValueError(msg)
        return tuple(
            _rust_value_enum_lines(
                scalars=scalars,
                enum_name=params.enum_name,
                date_type=params.date_type,
                datetime_type=params.datetime_type,
                include_list_variant=has_list,
                include_map_variant=has_map,
                list_inner_type=next(iter(list_hint_types), None),
                map_inner_type=next(iter(map_hint_types), None),
            )
        )

    return _preamble


@beartype
def _rust_derecordized_map_ids(
    *,
    data: Value,
    unify_optional_fields: bool,
) -> frozenset[int]:
    """Return the ids of every dict widened to a plain map (issue #2910).

    Recomputes the record-shape mapping the same way
    ``compute_record_shapes`` does (collect, optionally unify, then drop
    the nested sibling-map families that cannot share one record shape)
    and returns the ids that the drop removed: exactly the maps whose
    scalar leaves are wrapped in the value enum and whose declared field
    type is the widened ``HashMap``.
    """
    raw_shapes_by_id = collect_record_shapes(data=data)
    unified_shapes_by_id = (
        unify_record_shapes(data=data, shapes_by_id=raw_shapes_by_id)
        if unify_optional_fields
        else raw_shapes_by_id
    )
    widened_shapes_by_id = drop_unrecordizable_nested_sibling_maps(
        data=data,
        shapes_by_id=unified_shapes_by_id,
    )
    return frozenset(set(unified_shapes_by_id) - set(widened_shapes_by_id))


@beartype
def _rust_is_derecordized_map(*, value: dict[Scalar, Value]) -> bool:
    """Return whether *value* is a record-eligible dict that was widened
    to a plain map (issue #2910).

    A record-eligible dict (non-empty, string-keyed, not an ordered map)
    absent from the shape mapping was dropped by
    :func:`~literalizer._formatters.type_inference.drop_unrecordizable_nested_sibling_maps`,
    so it renders as a widened ``HashMap`` rather than a struct; an empty,
    non-string-keyed, or ordered-map dict is a genuine non-record field
    the ``RECORD`` strategy rejects instead.
    """
    return (
        not isinstance(value, OrderedMap)
        and bool(value)
        and all(isinstance(key, str) for key in value)
    )


@beartype
def _raise_for_derecordized_map_container_values(
    *, data: Value, widened_ids: frozenset[int]
) -> None:
    """Reject widened maps whose scalar enum cannot hold a value."""
    match data:
        case dict():
            if id(data) in widened_ids and any(
                isinstance(value, (dict, list, set)) for value in data.values()
            ):
                msg = (
                    "Rust cannot widen divergent record maps whose values "
                    "contain containers"
                )
                raise UnrepresentableInputError(msg)
            for value in data.values():
                _raise_for_derecordized_map_container_values(
                    data=value, widened_ids=widened_ids
                )
        case list() | set():
            for value in data:
                _raise_for_derecordized_map_container_values(
                    data=value, widened_ids=widened_ids
                )
        case _:
            return


@dataclasses.dataclass
class _RustWidenedMapNarrowing:
    """Per-pass cache of the widened fallback maps' narrow value type.

    ``value_type`` holds the single concrete Rust type shared by every
    scalar inside the maps the ``RECORD`` strategy widened out of the
    record-shape mapping, or ``None`` when those scalars mix Rust types
    and the value enum is required (issue #3608).  Refreshed by the
    strategy's ``compute_wrap_ids`` hook, which the shared data checks
    run before any rendering; the scalar wrapper reads the cached
    decision within the same pass.
    """

    value_type: str | None


@beartype
def _rust_narrow_derecordized_map_value_type(
    *,
    data: Value,
    wrap_ids: frozenset[int],
    date_type: str,
    datetime_type: str,
    map_value_typing: RecordMapValueTypings,
) -> str | None:
    """Return the single Rust type every widened-map scalar shares.

    Returns ``None`` when the widened maps genuinely mix scalar types
    (the value enum is then required), when there is nothing to widen,
    when any widened scalar is ``None`` (the payload-free ``Null``
    variant has no inner type a plain ``HashMap`` value could take), or
    when *map_value_typing* asks for the value enum whatever the data
    holds.
    """
    if map_value_typing is RecordMapValueTypings.WIDE:
        return None
    scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
    if not scalars:
        return None
    inner_types = {
        _heterogeneous_variant_for_scalar(
            value=scalar,
            date_type=date_type,
            datetime_type=datetime_type,
        ).inner_type
        for scalar in scalars
    }
    if len(inner_types) != 1:
        return None
    (inner_type,) = inner_types
    return inner_type


@beartype
def _rust_record_wrap_ids_hook(
    *,
    params: _StrategyParams,
    narrowing: _RustWidenedMapNarrowing,
) -> Callable[[Value], frozenset[int]]:
    """Return the ``RECORD`` strategy's ``compute_wrap_ids`` hook.

    The hook returns the widened-map ids whose scalars wrap in the
    value enum (issue #2910) and refreshes *narrowing*, the per-pass
    narrow-type cache the scalar wrapper reads (issue #3608).
    """

    def _compute_wrap_ids(data: Value) -> frozenset[int]:
        """Return the widened-map ids, refreshing the narrow-type
        cache.
        """
        wrap_ids = _rust_derecordized_map_ids(
            data=data,
            unify_optional_fields=params.unify_optional_fields,
        )
        narrowing.value_type = _rust_narrow_derecordized_map_value_type(
            data=data,
            wrap_ids=wrap_ids,
            date_type=params.date_type,
            datetime_type=params.datetime_type,
            map_value_typing=params.map_value_typing,
        )
        return wrap_ids

    return _compute_wrap_ids


@beartype
def _rust_narrowing_scalar_wrapper(
    *,
    params: _StrategyParams,
    narrowing: _RustWidenedMapNarrowing,
) -> Callable[[Scalar, str], str]:
    """Return the ``RECORD`` strategy's widened-map scalar wrapper.

    When every widened scalar shares one concrete Rust type the plain
    ``HashMap`` already holds the bare literal, so no enum construction
    is needed (issue #3608); otherwise the scalar wraps in the value
    enum exactly as under ``TAGGED_ENUM``.
    """
    base_wrap_scalar = _rust_value_scalar_wrapper(params)

    def _wrap_scalar(raw_value: Scalar, formatted: str) -> str:
        """Construct the value-enum variant for a widened map."""
        if narrowing.value_type is not None:
            return formatted
        return base_wrap_scalar(raw_value, formatted)

    return _wrap_scalar


@beartype
def _rust_record_field_type(
    *,
    value: Value,
    date_type: str,
    datetime_type: str,
    derecordized_map_value_type: str,
    record_names: "dict[RecordShape, str]",
    shapes_by_id: "Mapping[int, RecordShape]",
    tuple_list_ids: frozenset[int],
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
) -> str:
    """Return the Rust struct field type for *value*.

    Scalar fields reuse :func:`_heterogeneous_variant_for_scalar`'s
    ``inner_type``.  A list field whose ``id`` is in *tuple_list_ids*
    is a tuple-eligible heterogeneous scalar array and is typed as a
    fixed-size tuple ``(T0, T1, ...)`` with one type per element
    (composing the ``TUPLE`` and ``RECORD`` strategies); any other list
    field uses ``Vec<T>`` over the inferred inner type.  Nested record
    fields use the corresponding generated struct name, looked up via
    *shapes_by_id* so unification-rewritten shapes match.  A
    record-eligible dict absent from *shapes_by_id* was widened to a
    plain map (issue #2910): its sibling maps could not share one record
    shape, so it renders as the widened ``HashMap<&'static str,
    {derecordized_map_value_type}>``.  That value type names the value
    enum whose variants wrap the widened scalar leaves, or -- when
    every widened scalar shares one concrete Rust type -- that bare
    type (issue #3608).
    """
    # An empty-list field has no element type to infer, so it falls
    # back to ``Vec<String>`` (the ``record_sequence`` fixture exercises
    # this).  A set-valued field, and a dict-valued field whose dict is
    # not record-eligible (empty, non-string-keyed, or an ordered map),
    # have no struct field type that matches the set or map literal
    # rendered for the value, so the ``case set()`` and the non-record
    # ``case dict()`` paths reject the input instead of emitting a
    # struct that fails to compile.
    match value:
        case [] if not sequence_supports_heterogeneity:
            return sequence_format_type_annotation("String", 0)
        case list() if (
            id(value) in tuple_list_ids or sequence_supports_heterogeneity
        ):
            element_types = [
                _rust_record_field_type(
                    value=item,
                    date_type=date_type,
                    datetime_type=datetime_type,
                    derecordized_map_value_type=derecordized_map_value_type,
                    record_names=record_names,
                    shapes_by_id=shapes_by_id,
                    tuple_list_ids=tuple_list_ids,
                    sequence_format_type_annotation=(
                        sequence_format_type_annotation
                    ),
                    sequence_supports_heterogeneity=(
                        sequence_supports_heterogeneity
                    ),
                )
                for item in value
            ]
            trailing_comma = "," if len(element_types) == 1 else ""
            return f"({', '.join(element_types)}{trailing_comma})"
        case list():
            inner_types = [
                _rust_record_field_type(
                    value=item,
                    date_type=date_type,
                    datetime_type=datetime_type,
                    derecordized_map_value_type=derecordized_map_value_type,
                    record_names=record_names,
                    shapes_by_id=shapes_by_id,
                    tuple_list_ids=tuple_list_ids,
                    sequence_format_type_annotation=(
                        sequence_format_type_annotation
                    ),
                    sequence_supports_heterogeneity=(
                        sequence_supports_heterogeneity
                    ),
                )
                for item in value
            ]
            return sequence_format_type_annotation(
                _unify_rust_types(types=inner_types), len(value)
            )
        case dict():
            shape = shapes_by_id.get(id(value))
            if shape is not None and shape in record_names:
                return record_names[shape]
            if _rust_is_derecordized_map(value=value):
                return f"HashMap<&'static str, {derecordized_map_value_type}>"
            msg = (
                "Rust cannot represent a non-record dict (empty, "
                "non-string-keyed, or an ordered map) as a field "
                "under the RECORD heterogeneous strategy"
            )
            raise UnrepresentableInputError(msg)
        case set():
            msg = (
                "Rust cannot represent a set-valued field under the "
                "RECORD heterogeneous strategy"
            )
            raise UnrepresentableInputError(msg)
        case _:
            signature = _heterogeneous_variant_for_scalar(
                value=value,
                date_type=date_type,
                datetime_type=datetime_type,
            )
            return (
                "Option<()>"
                if signature.inner_type is None
                else signature.inner_type
            )


@beartype
def _rust_record_field_identifier(key: str, /) -> str:
    """Return the Rust struct field name for dict *key*.

    A key that collides with a Rust keyword is escaped as a raw
    identifier (``r#type``) so the struct declaration and its literals
    compile (issue #2880).  Keys that no escape can rescue are rejected
    by :func:`_validate_rust_record_field_key` before rendering, so
    they never reach this helper.
    """
    if key in _RUST_RAW_ESCAPABLE_KEYWORDS:
        return f"r#{key}"
    return key


@beartype
def _validate_rust_record_field_key(*, key: str) -> None:
    """Raise for a dict key that cannot name a Rust struct field.

    ``crate``/``self``/``super``/``Self`` are keywords ``rustc``
    rejects even in raw-identifier form, ``_`` is the reserved
    wildcard identifier, and a key that is not identifier-shaped text
    (e.g. it contains ``-`` or a space) is beyond what raw-identifier
    escaping can express.
    """
    if key in _RUST_UNUSABLE_FIELD_KEYS or not _RUST_IDENTIFIER.match(
        string=key
    ):
        msg = (
            f"Rust cannot represent the dict key {key!r} as a struct "
            f"field name under the RECORD heterogeneous strategy: it "
            f"is not usable as a Rust identifier and raw-identifier "
            f"escaping (r#...) cannot express it"
        )
        raise UnrepresentableInputError(msg)


@dataclasses.dataclass(frozen=True, kw_only=True)
class _FieldVariantRecordShape(RecordShape):
    """A record shape split off from same-key-set dicts whose field
    types conflict.

    Two dicts with equal key tuples share one :class:`RecordShape`,
    but when a field's value type differs between them (e.g. the
    nested record under a key has different fields) they cannot share
    one generated struct: the declaration would take the field types
    of the first dict, and the literal for the other dict would not
    compile (issue #2881).  :func:`_refine_record_shapes` gives each
    conflicting group its own instance of this subclass; ``variant``
    tells the groups apart, numbered in document order of each
    group's first dict.  The subclass never compares equal to a plain
    :class:`RecordShape`, so every shape-keyed lookup treats each
    group as a distinct record shape.
    """

    variant: int


# Signature slot for a key a dict lacks (possible only for a
# unification-added optional key).  Dicts that differ solely in which
# optional keys they carry stay in one group (see
# :func:`_present_signatures_agree`), so this slot value only tells
# dicts apart once some key's present values already conflict.
_ABSENT_FIELD: str = "<absent field>"


@beartype
def _unify_signatures(*, signatures: Sequence[Hashable]) -> Hashable:
    """Mirror :func:`_unify_rust_types` at the signature level.

    A repeated signature collapses; all-integer signatures widen to
    the largest width, matching the ``Vec`` element type
    :func:`_rust_record_field_type` declares.  Any other mix keeps the
    distinct tuple; that fallback is only reached for element mixes
    :func:`~literalizer._checks.check_data` rejects right after shape
    computation, so it never influences emitted code and only has to
    be deterministic.
    """
    unique = list(dict.fromkeys(signatures))
    integer_signatures = [
        signature
        for signature in unique
        if isinstance(signature, str) and signature in {"i32", "i64", "i128"}
    ]
    match unique:
        case [only]:
            return only
        case _ if len(integer_signatures) == len(unique):
            return _unify_rust_types(types=integer_signatures)
        case _:
            return tuple(unique)


@beartype
def _record_field_type_signature(  # pylint: disable=redefined-variable-type
    *,
    value: Value,
    group_of: Mapping[int, Hashable],
    tuple_list_ids: frozenset[int],
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
) -> Hashable:
    """Return a structural stand-in for the Rust type
    :func:`_rust_record_field_type` would declare for *value*.

    Mirrors that function branch for branch, except that a nested
    record dict is represented by its current refinement group token
    (struct names are not assigned during refinement) and values that
    :func:`_rust_record_field_type` rejects (sets, non-record dicts)
    map to fixed tokens: such values are rejected later either way, so
    the signature only has to avoid splitting on them.  Two field
    values with different signatures would be declared with different
    Rust types, so their parent dicts cannot share one generated
    struct.
    """

    def recurse(*, item: Value) -> Hashable:
        """Return the signature of one nested element of *value*."""
        return _record_field_type_signature(
            value=item,
            group_of=group_of,
            tuple_list_ids=tuple_list_ids,
            date_type=date_type,
            datetime_type=datetime_type,
            sequence_format_type_annotation=sequence_format_type_annotation,
            sequence_supports_heterogeneity=(sequence_supports_heterogeneity),
        )

    result: Hashable
    match value:
        case [] if not sequence_supports_heterogeneity:
            result = sequence_format_type_annotation("String", 0)
        case list() if (
            id(value) in tuple_list_ids or sequence_supports_heterogeneity
        ):
            result = ("tuple", tuple(recurse(item=item) for item in value))
        case list():
            element_signatures = [recurse(item=item) for item in value]
            result = (
                sequence_format_type_annotation("T", len(value)),
                _unify_signatures(signatures=element_signatures),
            )
        case dict() if id(value) in group_of:
            result = group_of[id(value)]
        case dict():
            result = "<non-record dict>"
        case set():
            result = "<set>"
        case _:
            signature = _heterogeneous_variant_for_scalar(
                value=value,
                date_type=date_type,
                datetime_type=datetime_type,
            )
            if signature.inner_type is None:
                result = "Option<()>"
            else:
                result = signature.inner_type
    return result


@beartype
def _record_dicts_in_document_order(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
) -> list[dict[Scalar, Value]]:
    """Return every record-shaped dict in *data*, in document order.

    A dict aliased into the tree more than once (e.g. via a YAML
    anchor) appears once.
    """
    ordered: list[dict[Scalar, Value]] = []
    seen: set[int] = set()

    def walk(node: Value) -> None:
        """Append record dicts under *node* in document order."""
        match node:
            case dict():
                if id(node) in shapes_by_id and id(node) not in seen:
                    seen.add(id(node))
                    ordered.append(node)
                for child in node.values():
                    walk(node=child)
            case list():
                for item in node:
                    walk(node=item)
            case _:
                return

    walk(node=data)
    return ordered


@beartype
def _instance_signature(
    *,
    instance: dict[Scalar, Value],
    shape: RecordShape,
    group_of: Mapping[int, Hashable],
    tuple_list_ids: frozenset[int],
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
) -> tuple[Hashable, ...]:
    """Return the per-key field-type signatures of *instance*, in
    shape-key order, with :data:`_ABSENT_FIELD` for a key it lacks.
    """
    return tuple(
        _record_field_type_signature(
            value=instance[key],
            group_of=group_of,
            tuple_list_ids=tuple_list_ids,
            date_type=date_type,
            datetime_type=datetime_type,
            sequence_format_type_annotation=sequence_format_type_annotation,
            sequence_supports_heterogeneity=(sequence_supports_heterogeneity),
        )
        if key in instance
        else _ABSENT_FIELD
        for key in shape.keys
    )


@beartype
def _present_signatures_agree(
    *,
    member_signatures: Sequence[tuple[Hashable, ...]],
) -> bool:
    """Return ``True`` when, for every key slot, the present
    (non-absent) signatures across *member_signatures* are all equal,
    i.e. the group's dicts can share one struct declaration.
    """
    key_count = len(member_signatures[0])
    for slot in range(key_count):
        present = {
            signatures[slot]
            for signatures in member_signatures
            if signatures[slot] != _ABSENT_FIELD
        }
        if len(present) > 1:
            return False
    return True


@beartype
def _regroup_by_field_signatures(
    *,
    instances: Sequence[dict[Scalar, Value]],
    shapes_by_id: Mapping[int, RecordShape],
    group_of: Mapping[int, Hashable],
    tuple_list_ids: frozenset[int],
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
) -> dict[int, Hashable]:
    """Run one refinement round: split each group of *group_of* whose
    members' field signatures conflict, keeping agreeing groups whole.
    """
    members_by_group: dict[Hashable, list[dict[Scalar, Value]]] = {}
    for instance in instances:
        members_by_group.setdefault(group_of[id(instance)], []).append(
            instance
        )
    new_group_of: dict[int, Hashable] = {}
    for token, members in members_by_group.items():
        member_signatures = [
            _instance_signature(
                instance=member,
                shape=shapes_by_id[id(member)],
                group_of=group_of,
                tuple_list_ids=tuple_list_ids,
                date_type=date_type,
                datetime_type=datetime_type,
                sequence_format_type_annotation=(
                    sequence_format_type_annotation
                ),
                sequence_supports_heterogeneity=(
                    sequence_supports_heterogeneity
                ),
            )
            for member in members
        ]
        if _present_signatures_agree(member_signatures=member_signatures):
            for member in members:
                new_group_of[id(member)] = token
        else:
            for member, signatures in zip(
                members, member_signatures, strict=True
            ):
                new_group_of[id(member)] = (token, signatures)
    return new_group_of


@beartype
def _partition(
    *,
    instances: Sequence[dict[Scalar, Value]],
    group_of: Mapping[int, Hashable],
) -> frozenset[tuple[int, ...]]:
    """Return the grouping of *instances* induced by *group_of* in a
    form comparable across refinement rounds (group tokens change
    representation between rounds even when the grouping does not).
    """
    ids_by_group: dict[Hashable, list[int]] = {}
    for instance in instances:
        ids_by_group.setdefault(group_of[id(instance)], []).append(
            id(instance)
        )
    return frozenset(tuple(ids) for ids in ids_by_group.values())


@beartype
def _materialize_refined_shapes(
    *,
    instances: Sequence[dict[Scalar, Value]],
    shapes_by_id: Mapping[int, RecordShape],
    group_of: Mapping[int, Hashable],
) -> dict[int, RecordShape]:
    """Map each dict to its refined shape.

    A shape whose dicts all landed in one group keeps its original
    :class:`RecordShape` object, so unaffected inputs render exactly
    as before; a split shape's groups become
    :class:`_FieldVariantRecordShape` instances numbered in document
    order of each group's first dict.
    """
    tokens_by_shape: dict[RecordShape, set[Hashable]] = {}
    for instance in instances:
        tokens_by_shape.setdefault(shapes_by_id[id(instance)], set()).add(
            group_of[id(instance)]
        )
    shape_for_token: dict[Hashable, RecordShape] = {}
    variant_counter: Counter[RecordShape] = Counter()
    refined: dict[int, RecordShape] = {}
    for instance in instances:
        token = group_of[id(instance)]
        base = shapes_by_id[id(instance)]
        if token not in shape_for_token:
            if len(tokens_by_shape[base]) == 1:
                shape_for_token[token] = base
            else:
                shape_for_token[token] = _FieldVariantRecordShape(
                    keys=base.keys,
                    optional_keys=base.optional_keys,
                    variant=variant_counter[base],
                )
                variant_counter[base] += 1
        refined[id(instance)] = shape_for_token[token]
    return refined


@beartype
def _refine_record_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    tuple_list_ids: frozenset[int],
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
) -> dict[int, RecordShape]:
    """Split record shapes whose dicts disagree on a field's Rust type.

    *shapes_by_id* keys shapes by key tuple (plus optional-field
    unification), so two dicts with the same keys share a shape even
    when a field's value type differs between them; declaring the
    field with the type from the first dict then makes the literal
    for the other dict fail to compile (issue #2881).  This pass
    splits each shape's dicts into groups by per-field type signature
    so each group gets its own generated struct.  Sibling lists
    spanning split groups then fail
    :func:`~literalizer._checks.check_data`'s mixed-record-shape gate
    (the honest heterogeneous-siblings outcome) instead of silently
    emitting mismatched field types, while groups that never share a
    list each render as a genuinely distinct struct that compiles.

    Signatures reference nested records by group, so the grouping is
    computed to a fixed point: splitting a nested shape can in turn
    split the shape of the dicts embedding it.  Dicts that differ only
    in which unification-added optional keys they carry stay in one
    group (see :func:`_present_signatures_agree`).
    """
    instances = _record_dicts_in_document_order(
        data=data,
        shapes_by_id=shapes_by_id,
    )
    group_of: dict[int, Hashable] = {
        id(instance): shapes_by_id[id(instance)] for instance in instances
    }
    while True:
        regrouped = _regroup_by_field_signatures(
            instances=instances,
            shapes_by_id=shapes_by_id,
            group_of=group_of,
            tuple_list_ids=tuple_list_ids,
            date_type=date_type,
            datetime_type=datetime_type,
            sequence_format_type_annotation=sequence_format_type_annotation,
            sequence_supports_heterogeneity=(sequence_supports_heterogeneity),
        )
        old_partition = _partition(instances=instances, group_of=group_of)
        new_partition = _partition(instances=instances, group_of=regrouped)
        if new_partition == old_partition:
            break
        group_of = regrouped
    return _materialize_refined_shapes(
        instances=instances,
        shapes_by_id=shapes_by_id,
        group_of=group_of,
    )


@beartype
def _assign_record_struct_names(
    *,
    ordered_shapes: Sequence[RecordShape],
    record_prefix: str,
    record_shape_names: Mapping[frozenset[str], str],
) -> dict[RecordShape, str]:
    """Assign a struct name to each shape, in document order.

    A shape whose key set is mapped in *record_shape_names* takes the
    custom name; the auto ``{prefix}{index}`` counter advances only
    for the unmapped shapes.  When more than one distinct shape
    carries a custom-named key set (same keys but conflicting field
    types or key order -- see :func:`_refine_record_shapes`), the
    custom name cannot identify one struct, so the input is rejected
    rather than emitting duplicate ``struct`` declarations under that
    name.
    """
    key_set_counts = Counter(frozenset(shape.keys) for shape in ordered_shapes)
    names: dict[RecordShape, str] = {}
    prefix_index = 0
    for shape in ordered_shapes:
        key_set = frozenset(shape.keys)
        custom = record_shape_names.get(key_set)
        if custom is None:
            names[shape] = f"{record_prefix}{prefix_index}"
            prefix_index += 1
        elif key_set_counts[key_set] > 1:
            sorted_keys = ", ".join(sorted(key_set))
            msg = (
                f"record_shape_names maps the key set {{{sorted_keys}}} "
                f"to {custom!r}, but the data contains multiple distinct "
                f"record shapes with that key set (their field types or "
                f"key order differ), so one custom name cannot identify "
                f"one generated struct"
            )
            raise UnrepresentableInputError(msg)
        else:
            names[shape] = custom
    return names


@beartype
def _record_behavior_impl(
    params: _StrategyParams,
    /,
    *,
    enable_tuples: bool,
) -> HeterogeneousBehavior:
    """RECORD strategy: render record-shaped dicts as struct literals."""
    # ``name_cache`` and ``id_to_shape`` are rebuilt on every
    # ``compute_record_shapes`` call so concurrent ``literalize``
    # invocations on the same cached Rust spec (e.g. variant golden
    # tests reuse one instance) cannot leak shape -> name assignments
    # from a previous call.
    name_cache: dict[RecordShape, str] = {}
    id_to_shape: dict[int, RecordShape] = {}

    def _compute_shapes(data: Value) -> Mapping[int, RecordShape]:
        """Walk *data* and return ``id(dict)`` -> :class:`RecordShape`.

        With ``unify_optional_fields`` on, multiple ids collapse to a
        shared unified shape (see :func:`unify_record_shapes`); shapes
        whose dicts disagree on a field's Rust type are then split so
        each field-type group gets its own struct (see
        :func:`_refine_record_shapes`).  Re-populates the shared
        caches in document order so the preamble's struct names match
        the rendered literals.
        """
        raw_shapes_by_id = collect_record_shapes(data=data)
        unified_shapes_by_id = (
            unify_record_shapes(data=data, shapes_by_id=raw_shapes_by_id)
            if params.unify_optional_fields
            else raw_shapes_by_id
        )
        widened_shapes_by_id = drop_unrecordizable_nested_sibling_maps(
            data=data,
            shapes_by_id=unified_shapes_by_id,
        )
        shapes_by_id = _refine_record_shapes(
            data=data,
            shapes_by_id=widened_shapes_by_id,
            tuple_list_ids=(
                collect_tuple_list_ids(data=data)
                if enable_tuples
                else frozenset()
            ),
            date_type=params.date_type,
            datetime_type=params.datetime_type,
            sequence_format_type_annotation=(
                params.sequence_format_type_annotation
            ),
            sequence_supports_heterogeneity=(
                params.sequence_supports_heterogeneity
            ),
        )
        name_cache.clear()
        id_to_shape.clear()
        id_to_shape.update(shapes_by_id)
        ordered = _ordered_record_shapes(
            data=data,
            shapes_by_id=shapes_by_id,
        )
        for shape in ordered:
            for key in shape.keys:
                _validate_rust_record_field_key(key=key)
        name_cache.update(
            _assign_record_struct_names(
                ordered_shapes=ordered,
                record_prefix=params.record_prefix,
                record_shape_names=params.record_shape_names,
            )
        )
        return shapes_by_id

    def _render_literal(
        value: "dict[Scalar, Value]",
        fields: Mapping[str, str],
    ) -> RenderedRecordLiteral | None:
        """Render a record-shape dict as a Rust struct literal.

        Looks up *value*'s (possibly unified) shape from the
        ``compute_record_shapes`` mapping populated during
        ``check_data``.  A record-eligible dict absent from that mapping
        was widened to a plain map (issue #2910) -- its sibling maps
        could not share one record shape -- so ``None`` is returned and
        the shared formatter renders it as the widened ``HashMap``
        instead.
        Iterates the unified shape's keys: keys missing from this
        instance render as ``None``; keys marked optional render as
        ``Some(value)``; required keys render bare.  Returns the
        structured pieces (``Name {``, one entry per field, ``}``,
        single-space compact padding) the shared record-layout code
        assembles into compact or multiline form.
        """
        if id(value) not in id_to_shape:
            return None
        shape = id_to_shape[id(value)]
        parts: list[str] = []
        for key in shape.keys:
            field_name = _rust_record_field_identifier(key)
            if key in fields:
                formatted = fields[key]
                if key in shape.optional_keys:
                    parts.append(f"{field_name}: Some({formatted})")
                else:
                    parts.append(f"{field_name}: {formatted}")
            else:
                parts.append(f"{field_name}: None")
        return RenderedRecordLiteral(
            head=f"{name_cache[shape]} {{",
            entries=tuple(parts),
            closer="}",
            compact_pad=" ",
        )

    narrowing = _RustWidenedMapNarrowing(value_type=None)

    return HeterogeneousBehavior(
        skip_scalar_checks=False,
        compute_wrap_ids=_rust_record_wrap_ids_hook(
            params=params,
            narrowing=narrowing,
        ),
        wrap_scalar=_rust_narrowing_scalar_wrapper(
            params=params,
            narrowing=narrowing,
        ),
        wrap_non_scalar=None,
        wrap_empty_container=None,
        empty_container_literal_overrides=no_empty_container_literal_overrides,
        compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
        dict_open_for_wrap_ids=None,
        widens_nested_maps_by_wrapping_scalars=False,
        widens_unrecordizable_nested_sibling_maps=True,
        render_record_literal=_render_literal,
        compute_record_shapes=_compute_shapes,
        render_tuple_literal=None,
        compute_tuple_list_ids=None,
        alias_record_ids=None,
    )


@beartype
def _build_record_behavior(
    params: _StrategyParams,
    /,
) -> HeterogeneousBehavior:
    """RECORD strategy: render record-shaped dicts as struct literals."""
    return _record_behavior_impl(params, enable_tuples=False)


@beartype
def _render_rust_tuple(
    value: list[Value],
    elements: Sequence[str],
) -> RenderedTupleLiteral:
    """Render a heterogeneous scalar array as a Rust tuple literal.

    ``collect_tuple_list_ids`` only marks arrays spanning at least two
    distinct scalar buckets, so a Rust tuple here always has at least
    two elements and never needs the 1-tuple ``(e0,)`` trailing comma.
    The shared record-layout assembler joins *elements* into the
    compact ``(a, b)`` or one-per-line multiline form; *value* is
    unused because every element is already formatted.
    """
    del value
    return RenderedTupleLiteral(
        head="(",
        entries=tuple(elements),
        closer=")",
        compact_pad="",
        # ``(a,\n    b,\n)`` is valid Rust, so keep the language-wide
        # trailing-comma policy (``True``) for the multiline form.
        multiline_trailing_comma=True,
    )


@beartype
def _rust_tuple_list_ids(data: Value, /) -> frozenset[int]:
    """Adapt :func:`collect_tuple_list_ids` to the positional
    ``compute_tuple_list_ids`` hook signature.
    """
    return collect_tuple_list_ids(data=data)


@beartype
def _build_tuple_behavior(
    params: _StrategyParams,
    /,
) -> HeterogeneousBehavior:
    """TUPLE strategy: render heterogeneous scalar arrays as fixed-size
    tuples.

    Composes the ``RECORD`` behavior (so a record field whose value is
    such an array becomes a tuple-typed struct field) and adds the
    tuple render hook plus the list-id collector that
    :func:`~literalizer._checks.check_data` uses to carve those arrays
    out of the heterogeneous-scalar checks.
    """
    record_behavior = _record_behavior_impl(params, enable_tuples=True)
    return dataclasses.replace(
        record_behavior,
        render_tuple_literal=_render_rust_tuple,
        compute_tuple_list_ids=_rust_tuple_list_ids,
    )


@beartype
def _ordered_record_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
) -> list[RecordShape]:
    """Return record shapes in document order, one entry per distinct
    shape.
    """
    ordered: list[RecordShape] = []
    seen: set[RecordShape] = set()
    _accumulate_ordered_shapes(
        data=data,
        shapes_by_id=shapes_by_id,
        ordered=ordered,
        seen=seen,
    )
    return ordered


@beartype
def _accumulate_ordered_shapes(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    ordered: list[RecordShape],
    seen: set[RecordShape],
) -> None:
    """Walk *data* and append each newly-seen record shape to
    *ordered*.
    """
    match data:
        case dict():
            if id(data) in shapes_by_id:
                shape = shapes_by_id[id(data)]
                if shape not in seen:
                    seen.add(shape)
                    ordered.append(shape)
            for value in data.values():
                _accumulate_ordered_shapes(
                    data=value,
                    shapes_by_id=shapes_by_id,
                    ordered=ordered,
                    seen=seen,
                )
        case list():
            for item in data:
                _accumulate_ordered_shapes(
                    data=item,
                    shapes_by_id=shapes_by_id,
                    ordered=ordered,
                    seen=seen,
                )
        case _:
            return


@beartype
def _record_preamble_impl(
    params: _StrategyParams,
    /,
    *,
    enable_tuples: bool,
) -> Callable[[Value], tuple[str, ...]]:
    """Emit ``struct`` declarations for each record shape in the data.

    When *enable_tuples* is ``True`` (the ``TUPLE`` strategy, which
    composes ``RECORD``) a record field whose value is a tuple-eligible
    heterogeneous scalar array is typed as a fixed-size tuple rather
    than ``Vec<T>``; tuples themselves need no declaration so the
    struct blocks are the entire preamble either way.
    """

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build struct declarations for every record shape in *data*."""
        raw_shapes_by_id = collect_record_shapes(data=data)
        if not raw_shapes_by_id:
            return ()
        tuple_list_ids = (
            collect_tuple_list_ids(data=data)
            if enable_tuples
            else frozenset[int]()
        )
        unified_shapes_by_id: Mapping[int, RecordShape] = (
            unify_record_shapes(data=data, shapes_by_id=raw_shapes_by_id)
            if params.unify_optional_fields
            else raw_shapes_by_id
        )
        widened_shapes_by_id = drop_unrecordizable_nested_sibling_maps(
            data=data,
            shapes_by_id=unified_shapes_by_id,
        )
        shapes_by_id: Mapping[int, RecordShape] = _refine_record_shapes(
            data=data,
            shapes_by_id=widened_shapes_by_id,
            tuple_list_ids=tuple_list_ids,
            date_type=params.date_type,
            datetime_type=params.datetime_type,
            sequence_format_type_annotation=(
                params.sequence_format_type_annotation
            ),
            sequence_supports_heterogeneity=(
                params.sequence_supports_heterogeneity
            ),
        )
        ordered_shapes: list[RecordShape] = []
        seen: set[RecordShape] = set()
        field_values: dict[RecordShape, dict[str, Value]] = {}
        _gather_record_field_values(
            data=data,
            shapes_by_id=shapes_by_id,
            ordered_shapes=ordered_shapes,
            seen=seen,
            field_values=field_values,
        )
        record_names = _assign_record_struct_names(
            ordered_shapes=ordered_shapes,
            record_prefix=params.record_prefix,
            record_shape_names=params.record_shape_names,
        )
        emit_order: list[RecordShape] = []
        emit_seen: set[RecordShape] = set()
        _accumulate_emit_order(
            data=data,
            shapes_by_id=shapes_by_id,
            emit_ordered=emit_order,
            emit_seen=emit_seen,
        )
        # A widened nested sibling map (issue #2910) renders as a
        # ``HashMap`` whose scalar leaves wrap in the value enum -- or,
        # when every widened scalar shares one concrete Rust type, as a
        # plain ``HashMap`` of that bare type with no enum at all
        # (issue #3608).
        wrap_ids = _rust_derecordized_map_ids(
            data=data,
            unify_optional_fields=params.unify_optional_fields,
        )
        narrow_value_type = _rust_narrow_derecordized_map_value_type(
            data=data,
            wrap_ids=wrap_ids,
            date_type=params.date_type,
            datetime_type=params.datetime_type,
            map_value_typing=params.map_value_typing,
        )
        struct_blocks: list[str] = []
        for shape in emit_order:
            block: list[str] = [f"struct {record_names[shape]} {{"]
            for key in shape.keys:
                example = field_values[shape].get(key)
                field_type = _rust_record_field_type(
                    value=example,
                    date_type=params.date_type,
                    datetime_type=params.datetime_type,
                    derecordized_map_value_type=(
                        narrow_value_type
                        if narrow_value_type is not None
                        else params.enum_name
                    ),
                    record_names=record_names,
                    shapes_by_id=shapes_by_id,
                    tuple_list_ids=tuple_list_ids,
                    sequence_format_type_annotation=(
                        params.sequence_format_type_annotation
                    ),
                    sequence_supports_heterogeneity=(
                        params.sequence_supports_heterogeneity
                    ),
                )
                if key in shape.optional_keys:
                    field_type = f"Option<{field_type}>"
                field_name = _rust_record_field_identifier(key)
                block.append(f"    {field_name}: {field_type},")
            block.append("}")
            struct_blocks.append("\n".join(block))
        enum_lines = (
            ()
            if narrow_value_type is not None
            else _rust_value_enum_lines(
                scalars=iter_wrapped_scalars(data=data, wrap_ids=wrap_ids),
                enum_name=params.enum_name,
                date_type=params.date_type,
                datetime_type=params.datetime_type,
                include_list_variant=False,
                include_map_variant=False,
                list_inner_type=None,
                map_inner_type=None,
            )
        )
        enum_block = ("\n".join(enum_lines),) if enum_lines else ()
        return enum_block + tuple(struct_blocks)

    return _preamble


@beartype
def _build_record_preamble(
    params: _StrategyParams,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """RECORD strategy: emit ``struct`` declarations for each shape."""
    return _record_preamble_impl(params, enable_tuples=False)


@beartype
def _build_tuple_preamble(
    params: _StrategyParams,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """TUPLE strategy: emit ``struct`` declarations (tuples themselves
    need no preamble), typing tuple-eligible record fields as fixed-size
    tuples.
    """
    return _record_preamble_impl(params, enable_tuples=True)


@beartype
def _accumulate_emit_order(
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    emit_ordered: list[RecordShape],
    emit_seen: set[RecordShape],
) -> None:
    """Walk *data* post-order to emit each shape after its
    dependencies.
    """
    match data:
        case dict():
            for value in data.values():
                _accumulate_emit_order(
                    data=value,
                    shapes_by_id=shapes_by_id,
                    emit_ordered=emit_ordered,
                    emit_seen=emit_seen,
                )
            shape = shapes_by_id.get(id(data))
            if shape is not None and shape not in emit_seen:
                emit_seen.add(shape)
                emit_ordered.append(shape)
        case list():
            for item in data:
                _accumulate_emit_order(
                    data=item,
                    shapes_by_id=shapes_by_id,
                    emit_ordered=emit_ordered,
                    emit_seen=emit_seen,
                )
        case _:
            return


@beartype
def _gather_record_field_values(  # noqa: C901  # pylint: disable=too-complex
    *,
    data: Value,
    shapes_by_id: Mapping[int, RecordShape],
    ordered_shapes: list["RecordShape"],
    seen: set["RecordShape"],
    field_values: dict["RecordShape", dict[str, Value]],
) -> None:
    """Walk *data* recording the first observed value for each
    (shape, key) pair, in document order.
    """
    match data:
        case dict() if id(data) in shapes_by_id:
            shape = shapes_by_id[id(data)]
            if shape not in seen:
                seen.add(shape)
                ordered_shapes.append(shape)
                field_values[shape] = {}
            # Iterate ``shape.keys`` (guaranteed strings) rather than
            # ``data.items()`` so ``stored`` keeps its ``dict[str, ...]``
            # type without per-key type narrowing.  First occurrence
            # wins, so later same-shape siblings don't overwrite the
            # example values used for type inference.
            stored = field_values[shape]
            for key in shape.keys:
                if key in stored:
                    continue
                if key not in data:
                    continue
                stored[key] = data[key]
            for value in data.values():
                _gather_record_field_values(
                    data=value,
                    shapes_by_id=shapes_by_id,
                    ordered_shapes=ordered_shapes,
                    seen=seen,
                    field_values=field_values,
                )
        case dict():
            # Non-record dicts (empty, non-string-keyed, or an ordered
            # map) sitting next to record dicts have no precise Rust
            # component type under the RECORD strategy (#2317).  Keep
            # walking its values so a record dict nested deeper inside
            # one is still found, even though
            # :func:`_rust_record_field_type` later rejects such a dict
            # when it is itself a record field.
            for value in data.values():
                _gather_record_field_values(
                    data=value,
                    shapes_by_id=shapes_by_id,
                    ordered_shapes=ordered_shapes,
                    seen=seen,
                    field_values=field_values,
                )
        case list():
            for item in data:
                _gather_record_field_values(
                    data=item,
                    shapes_by_id=shapes_by_id,
                    ordered_shapes=ordered_shapes,
                    seen=seen,
                    field_values=field_values,
                )
        case _:
            return


@beartype
def _rust_type_var(*, index: int) -> str:
    """Return a unique uppercase identifier for a type parameter.

    Indices ``0``..``25`` map to ``A``..``Z``; higher indices append a
    numeric suffix (``A1``..``Z1``, ``A2``..``Z2``, ...) so that
    27-or-more parameter stubs do not overflow the alphabet into
    non-letter ASCII like ``[``.
    """
    letter = chr(ord("A") + index % 26)
    group = index // 26
    if group == 0:
        return letter
    return f"{letter}{group}"


@beartype
def _rust_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Rust stub declarations for a call name."""
    # Use generic type parameters so any argument type is accepted.
    type_vars = [_rust_type_var(index=i) for i in range(len(params))]
    generic_decl = ", ".join(type_vars)
    generic_clause = f"<{generic_decl}>" if generic_decl else ""
    if len(parts) == 1:
        param_list = ", ".join(
            f"_{p}: {t}" for p, t in zip(params, type_vars, strict=True)
        )
        return (f"fn {parts[0]}{generic_clause}({param_list}) {{}}",)
    root = parts[0]
    method = parts[-1]
    param_list = ", ".join(
        f"_{p}: {t}" for p, t in zip(params, type_vars, strict=True)
    )
    method_param_list = f"&self, {param_list}" if param_list else "&self"
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root.title()}Type_"
        return (
            f"struct {type_name};",
            (
                f"impl {type_name} {{"
                f" fn {method}{generic_clause}"
                f"({method_param_list}) {{}} }}"
            ),
            f"let {root} = {type_name};",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1].title()}Type_"
    lines.append(f"struct {inner_type};")
    lines.append(
        f"impl {inner_type} {{"
        f" fn {method}{generic_clause}"
        f"({method_param_list}) {{}} }}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i].title()}Type_"
        lines.append(f"struct {curr_type} {{ {fields[i + 1]}: {prev_type} }}")
        prev_type = curr_type
    root_type = f"{root.title()}Type_"
    lines.append(f"struct {root_type} {{ {fields[0]}: {prev_type} }}")
    construction = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"{fields[i].title()}Type_"
        construction = f"{curr_type} {{ {fields[i + 1]}: {construction} }}"
    construction = f"{root_type} {{ {fields[0]}: {construction} }}"
    lines.append(f"let {root} = {construction};")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Rust(metaclass=LanguageCls):
    """Rust language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.RUST`` —
              ``NaiveDate::from_ymd_opt(...)`` call,
              e.g. ``NaiveDate::from_ymd_opt(2024, 1, 15).unwrap()``.
              Requires the ``chrono`` crate.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.RUST`` —
              ``NaiveDateTime::new(...)`` call, e.g.
              ``NaiveDateTime::new(NaiveDate::from_ymd_opt(2024, 1, 15)
              .unwrap(), NaiveTime::from_hms_opt(12, 30, 0).unwrap())``.
              Requires the ``chrono`` crate.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        sequence_format: Which Rust sequence type to use.

            * ``sequence_formats.VEC`` — ``vec![]`` macro,
              e.g. ``vec![1, 2, 3]``.  Because ``Vec`` is
              homogeneous, heterogeneous-scalar inputs raise.
            * ``sequence_formats.ARRAY`` — fixed-size array literal,
              e.g. ``[1, 2, 3]``.  Because Rust arrays are
              homogeneous, heterogeneous-scalar inputs raise.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.

        default_sequence_element_type: Type name used for empty
            ``Vec`` literals, e.g. ``Vec::<String>::new()``.
            Defaults to ``"String"``.

        json_type: When set to ``json_types.SERDE_JSON_VALUE``, render
            values through ``serde_json::json!`` instead of Rust's narrow
            collection types.

        record_map_value_typing: Value type for a ``RECORD`` strategy
            field whose dict has no record shape of its own and so
            renders as a plain ``HashMap``.

            * ``record_map_value_typings.NARROW`` — the concrete type
              every widened scalar in this input shares, e.g.
              ``HashMap<&'static str, &'static str>``, falling back to
              the generated value ``enum`` when they span more than one
              type.  This is the default.
            * ``record_map_value_typings.WIDE`` — always the generated
              value ``enum``, e.g. ``HashMap<&'static str, Value>``,
              with each leaf wrapped in its variant.  Two inputs
              sharing one record shape then declare the field
              identically, so one input's literals compile against the
              other's ``struct``.
    """

    reserved_module_identifiers: ClassVar[frozenset[str]] = frozenset()
    immutable_variable_modifiers: ClassVar[frozenset[enum.Enum]] = frozenset()
    wrap_in_file_tolerates_pre_indent = True
    module_name_shares_variable_scope = False
    reserved_variable_identifier_pattern = None
    reserved_call_parameter_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_call_parameter_identifier_pattern = None
    accepts_type_name_call_target = True
    declares_type_name_call_target = True
    dotted_call_root_shares_entrypoint_namespace = True
    reserved_bare_call_target_identifiers: ClassVar[frozenset[str]] = (
        frozenset()
    )
    reserved_call_target_head_identifiers: ClassVar[frozenset[str]] = (
        frozenset()
    )
    call_parameter_shadowing = CallParameterShadowing.ALLOWED
    reserved_call_target_keywords_case_sensitive = True
    module_name_must_start_uppercase = False
    new_variable_name_syntax = NewVariableNameSyntax.ASCII
    max_variable_identifier_length = None
    call_target_name_syntax = None
    supports_multiline_dict_layout = True
    pools_map_integer_width = True

    format_integer_widened = no_format_integer_widened
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(_constructor_target)
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    extension = ".rs"
    pygments_name = "rust"
    stringifies_nested_collections = False
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    wraps_data_dependent_preamble_in_body = False
    dict_supports_heterogeneous_values = False
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    contextual_call_target_identifiers: ClassVar[frozenset[str]] = frozenset(
        {"self"}
    )
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "Self",
            # ``_`` is a pattern that discards its value rather than a
            # binding, so the generated file cannot read it back
            # (issue #4510).
            "_",
            "abstract",
            "as",
            "async",
            "await",
            "become",
            "box",
            "break",
            "const",
            "continue",
            "crate",
            "do",
            "dyn",
            "else",
            "enum",
            "extern",
            "false",
            "final",
            "fn",
            "for",
            "if",
            "impl",
            "in",
            "let",
            "loop",
            "macro",
            "main",
            "match",
            "mod",
            "move",
            "mut",
            "override",
            "priv",
            "pub",
            "ref",
            "return",
            "self",
            "static",
            "struct",
            "super",
            "trait",
            "true",
            "try",
            "type",
            "typeof",
            "union",
            "unsafe",
            "unsized",
            "use",
            "virtual",
            "where",
            "while",
            "yield",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    dotted_call_stub_requires_unique_parts = True
    dotted_call_stub_normalizes_part_case = True
    call_returns_expression = True
    supports_json_call_result_binding = False
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = False
    supports_empty_dict_key = False
    supports_call_style = True
    supports_default_dict_key_type = True
    supports_default_dict_value_type = True
    supports_default_sequence_element_type = True
    supports_default_set_element_type = True
    supports_default_ordered_map_value_type = False
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    supports_multiline_string_literals = True
    supports_empty_sibling_sequence_type_hints = True
    supports_typed_dict_open = False
    language_id: ClassVar[str] = "rust"
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        round_trip_capabilities=frozenset(
            {
                RoundTripCapability.I64_BOUNDARIES,
                RoundTripCapability.INTERPOLATION_STRINGS,
                RoundTripCapability.EMBEDDED_NUL,
            }
        ),
        modifier_sequence_format_overrides={},
        string_literals_escape_null_byte=True,
        supports_ref_elements_in_tuple_strategy=False,
    )
    supports_record_struct_name_prefix = True
    supports_record_shape_names = True
    record_shape_names_emit_declarations = True
    supports_non_string_dict_keys = True
    checks_raw_control_dict_keys_separately = False

    class DateFormats(enum.Enum):
        """Date format options for Rust."""

        RUST = DateFormatConfig(
            formatter=_format_date_rust,
            preamble_lines=("use chrono::NaiveDate;",),
            type_produced=datetime.date,
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso, type_produced=str, preamble_lines=()
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Rust."""

        RUST = DatetimeFormatConfig(
            formatter=_format_datetime_rust,
            preamble_lines=(
                "use chrono::NaiveDate;",
                "use chrono::NaiveDateTime;",
                "use chrono::NaiveTime;",
            ),
            type_produced=datetime.datetime,
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
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

        HEX = enum.member(value=format_bytes_hex)
        BASE64 = enum.member(value=format_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Rust."""

        VEC = enum.member(
            value=sequence_format_factory(
                open_template="vec![",
                close="]",
                supports_heterogeneity=False,
                single_element_trailing_comma=False,
                single_element_template=None,
                supports_trailing_comma=True,
                empty_template="Vec::<{type}>::new()",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        ARRAY = enum.member(
            value=sequence_format_factory(
                open_template="[",
                close="]",
                supports_heterogeneity=False,
                single_element_trailing_comma=False,
                single_element_template=None,
                supports_trailing_comma=True,
                empty_template="[] as [{type}; 0]",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )
        TUPLE = enum.member(
            value=sequence_format_factory(
                open_template="(",
                close=")",
                supports_heterogeneity=True,
                # ``(x)`` is a parenthesized expression; a one-element
                # tuple needs the trailing comma (issue #3940).
                single_element_trailing_comma=True,
                single_element_template=None,
                supports_trailing_comma=True,
                empty_template=None,
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback_template=None,
            )
        )

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

        def format_type_annotation(
            self,
            element_type: str,
            length: int,
        ) -> str:
            """Return the Rust type annotation for this format."""
            cls = type(self)
            if self is cls.TUPLE:
                msg = "Use per-element types for tuples"
                raise IncompatibleFormatsError(msg)
            if self is cls.VEC:
                return f"Vec<{element_type}>"
            return f"[{element_type}; {length}]"

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self(default_type="String").supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Rust."""

        HASH_SET = enum.member(
            value=set_format_factory(
                open_template="HashSet::from([",
                close="])",
                empty_template="HashSet::<{type}>::new()",
                preamble_lines=("use std::collections::HashSet;",),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )
        BTREE_SET = enum.member(
            value=set_format_factory(
                open_template="BTreeSet::from([",
                close="])",
                empty_template="BTreeSet::<{type}>::new()",
                preamble_lines=("use std::collections::BTreeSet;",),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

        def format_type_annotation(self, element_type: str) -> str:
            """Return the Rust type annotation for this set format."""
            cls = type(self)
            if self is cls.HASH_SET:
                return f"HashSet<{element_type}>"
            return f"BTreeSet<{element_type}>"

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="/*",
            suffix=NestingCommentSuffix(object=" */"),
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=_format_let_declaration,
            supports_redefinition=False,
        )
        LET_MUT = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let mut {name} = {value};"
            ),
            supports_redefinition=True,
        )
        CONST = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="const {name} = {value};"
            ),
            supports_redefinition=False,
        )
        STATIC = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="static {name} = {value};"
            ),
            supports_redefinition=False,
        )
        LAZY_STATIC = DeclarationStyleConfig(
            formatter=_lazy_static_placeholder_formatter,
            supports_redefinition=False,
        )

        def build_json_formatter(
            self,
            *,
            json_type: str,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return a formatter for ``serde_json::Value`` output."""
            cls = type(self)
            if self is cls.LAZY_STATIC:

                def _lazy_formatter(
                    name: str,
                    value: str,
                    _data: Value,
                    _modifiers: frozenset[enum.Enum],
                ) -> str:
                    """Format a lazy static JSON-backed declaration."""
                    expr = _rust_json_value_expression(value)
                    return (
                        f"static {name}: LazyLock<{json_type}> = "
                        f"LazyLock::new(|| {expr});"
                    )

                return _lazy_formatter

            keyword = {
                cls.LET: "let",
                cls.LET_MUT: "let mut",
            }[self]

            def _local_formatter(
                name: str,
                value: str,
                _data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Format a local JSON-backed declaration."""
                expr = _rust_json_value_expression(value)
                effective_keyword = (
                    "let mut" if _RustModifiers.MUT in modifiers else keyword
                )
                return f"{effective_keyword} {name}: {json_type} = {expr};"

            return _local_formatter

        def build_formatter(
            self,
            *,
            date_type: str,
            datetime_type: str,
            sequence_format_type_annotation: Callable[[str, int], str],
            sequence_supports_heterogeneity: bool,
            set_format_type_annotation: Callable[[str], str],
            dict_format_type_annotation: Callable[[str, str], str],
            default_sequence_element_type: str,
            default_set_element_type: str,
            default_dict_key_type: str,
            default_dict_value_type: str,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return a formatter for this declaration style.

            For ``LET`` and ``LET_MUT`` the formatter is used
            directly.  For ``CONST`` and ``STATIC`` a
            type-annotated formatter is built from the language
            configuration.  ``LAZY_STATIC`` additionally wraps the
            inferred type in ``LazyLock<…>`` and the value in a
            ``LazyLock::new(|| …)`` call, enabling module-level
            declarations of runtime-initialized collections like
            ``HashMap`` and ``Vec``.
            """
            cls = type(self)
            if self is cls.LAZY_STATIC:

                def _lazy_formatter(
                    name: str,
                    value: str,
                    data: Value,
                    modifiers: frozenset[enum.Enum],
                ) -> str:
                    """Adapt :func:`_format_lazy_static_declaration` to the
                    positional formatter interface.
                    """
                    return _format_lazy_static_declaration(
                        name=name,
                        value=value,
                        data=data,
                        _modifiers=modifiers,
                        date_type=date_type,
                        datetime_type=datetime_type,
                        sequence_format_type_annotation=(
                            sequence_format_type_annotation
                        ),
                        sequence_supports_heterogeneity=(
                            sequence_supports_heterogeneity
                        ),
                        set_format_type_annotation=set_format_type_annotation,
                        dict_format_type_annotation=(
                            dict_format_type_annotation
                        ),
                        default_sequence_element_type=(
                            default_sequence_element_type
                        ),
                        default_set_element_type=default_set_element_type,
                        default_dict_key_type=default_dict_key_type,
                        default_dict_value_type=default_dict_value_type,
                    )

                return _lazy_formatter
            if self not in {cls.CONST, cls.STATIC}:
                config: DeclarationStyleConfig = self.value
                return config.formatter
            keyword = self.name.lower()

            def _formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt :func:`_format_typed_declaration` to the
                positional formatter interface.
                """
                return _format_typed_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    keyword=keyword,
                    date_type=date_type,
                    datetime_type=datetime_type,
                    sequence_format_type_annotation=(
                        sequence_format_type_annotation
                    ),
                    sequence_supports_heterogeneity=(
                        sequence_supports_heterogeneity
                    ),
                    default_sequence_element_type=(
                        default_sequence_element_type
                    ),
                    default_set_element_type=default_set_element_type,
                )

            return _formatter

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        HASH_MAP = enum.member(
            value=dict_format_factory(
                open_template="HashMap::from([",
                close="])",
                format_entry=tuple_dict_entry(
                    format_value=passthrough_sequence_entry
                ),
                empty_template="HashMap::<{key_type}, {type}>::from([])",
                preamble_lines=("use std::collections::HashMap;",),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        )
        BTREE_MAP = enum.member(
            value=dict_format_factory(
                open_template="BTreeMap::from([",
                close="])",
                format_entry=tuple_dict_entry(
                    format_value=passthrough_sequence_entry
                ),
                empty_template="BTreeMap::<{key_type}, {type}>::from([])",
                preamble_lines=("use std::collections::BTreeMap;",),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        )

        def __call__(
            self,
            default_type: str,
            *,
            default_key_type: str = "&str",
        ) -> DictFormatConfig:
            """Create a dict format config for the given type."""
            return self.value(
                default_type,
                default_key_type=default_key_type,
            )

        def format_type_annotation(
            self,
            key_type: str,
            value_type: str,
        ) -> str:
            """Return the Rust type annotation for this dict format."""
            cls = type(self)
            if self is cls.HASH_MAP:
                return f"HashMap<{key_type}, {value_type}>"
            return f"BTreeMap<{key_type}, {value_type}>"

    class EmptyDictKey(enum.Enum):
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="f64::INFINITY",
        negative_infinity="f64::NEG_INFINITY",
        nan="f64::NAN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

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
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
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

        DOUBLE = enum.member(value=_format_string_backslash_nul)
        RAW = enum.member(value=_format_string_raw)
        MULTILINE = enum.member(value=_format_string_multiline)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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

    class JsonTypes(JsonType):
        """JSON value type options for Rust."""

        SERDE_JSON_VALUE = "serde_json::Value"
        """Serde's dynamic JSON value type."""

    json_types = JsonTypes
    declaration_styles = DeclarationStyles
    dict_entry_styles = DictEntryStyles
    dict_formats = DictFormats
    empty_dict_keys = EmptyDictKey
    float_formats = FloatFormats
    integer_formats = IntegerFormats
    integer_width_strategies = BareIntegerWidthStrategies
    record_map_value_typings = RecordMapValueTypings
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
        """Rust call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
        )

    call_styles = CallStyles

    Modifiers = _RustModifiers

    modifiers = _RustModifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for representing dicts or lists whose scalar values
        span more than one Rust type.
        """

        ERROR = _HeterogeneousStrategyConfig(
            build_behavior=_build_error_behavior,
            build_preamble=_build_error_preamble,
        )
        """Raise
        :exc:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
        (or :exc:`~literalizer.exceptions.HeterogeneousSiblingListsError`)
        when scalar values of mixed types appear in a container that
        cannot represent them.  This is the default, matching Rust's
        strict-typing convention.
        """

        TAGGED_ENUM = _HeterogeneousStrategyConfig(
            build_behavior=_build_tagged_enum_behavior,
            build_preamble=_build_tagged_enum_preamble,
        )
        """Auto-generate a tagged ``enum`` in the preamble containing
        only the variants actually present in the data, and wrap each
        heterogeneous scalar value with ``{EnumName}::{Variant}(value)``.

        Integer variants use narrowest-width names (``I32``, ``I64``,
        ``I128``) matching Rust's default integer-type inference.  The
        enum name is configurable via
        :attr:`Rust.heterogeneous_value_enum_name`.
        """

        RECORD = _HeterogeneousStrategyConfig(
            build_behavior=_build_record_behavior,
            build_preamble=_build_record_preamble,
        )
        """Render record-shaped dicts (non-empty, string-keyed) as
        generated ``struct`` literals.

        Each distinct ordered-key tuple becomes a struct declared in
        the preamble (``struct Record0 { field: Type, ... }``) and
        each matching dict in the data renders as a struct literal
        (``Record0 { field: value, ... }``) rather than a
        ``HashMap::from([...])`` call.  Useful for inputs whose dict
        values span multiple Rust scalar types but always share the
        same field set.  The prefix is configurable via
        :attr:`Rust.record_struct_name_prefix`.

        A key that collides with a Rust keyword (e.g. ``type``,
        ``match``) renders as a raw identifier (``r#type``) in both
        the struct declaration and its literals.  A key with no
        compiling struct field name (``crate``, ``self``, ``super``,
        ``Self``, ``_``, or a key that is not identifier-shaped text)
        raises
        :class:`~literalizer.exceptions.UnrepresentableInputError`.
        """

        TUPLE = _HeterogeneousStrategyConfig(
            build_behavior=_build_tuple_behavior,
            build_preamble=_build_tuple_preamble,
        )
        """Render a fixed-length heterogeneous **scalar** array (a dict
        value, record field value, or the document root, all elements
        scalar and spanning at least two scalar buckets) as a native
        Rust tuple ``(e0, e1, ...)`` typed ``(T0, T1, ...)`` instead of
        rejecting it.

        Composes with ``RECORD``: a record field whose value is such an
        array becomes a tuple-typed struct field (e.g.
        ``struct Record0 { call: &'static str, args: (i32, &'static str,
        &'static str, i32) }``).  Heterogeneous arrays nested inside
        another list, or containing a non-scalar element, are out of
        scope and still raise.  Rust tuples have no length limit.
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Rust."""

        EDITION_2021 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    @cached_property
    def leading_preamble(self) -> LeadingPreamble:
        """Raise the macro recursion limit before every other file
        item.
        """
        enabled = self._json_type_active

        def _recursion_limit(
            _data: Value, /, *, has_variable_declaration: bool
        ) -> tuple[str, ...]:
            """Return the crate attribute for JSON macro output."""
            del has_variable_declaration
            if enabled:
                return (
                    "// Permit serde_json::json! to expand wide values.",
                    '#![recursion_limit = "4096"]',
                )
            return ()

        return _recursion_limit

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Rust let binding in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = _indent_code_preserving_raw_strings(
            text=content,
            prefix=self.indent,
        )
        use_line = (
            f"\n{self.indent}let _ = {variable_name};" if variable_name else ""
        )
        return f"fn main() {{\n{indented}{use_line}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Rust declaration + assignment in a main function."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.RUST
    datetime_format: DatetimeFormats = DatetimeFormats.RUST
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.VEC
    set_format: SetFormats = SetFormats.HASH_SET
    default_sequence_element_type: str = "String"
    default_set_element_type: str = "String"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "String"
    json_type: JsonTypes | None = None
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.LET
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.HASH_MAP
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
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    heterogeneous_value_enum_name: str = "Value"
    record_struct_name_prefix: str = "Record"
    record_shape_names: Mapping[frozenset[str], str] = dataclasses.field(
        default_factory=lambda: MappingProxyType(mapping={}),
        hash=False,
    )
    empty_container_type_hints: Mapping[EmptyContainerPath, str] = (
        dataclasses.field(
            default_factory=lambda: MappingProxyType(mapping={}),
            hash=False,
        )
    )
    """Concrete Rust types for empty lists or maps at input paths.

    This opt-in escape hatch is useful with ``TAGGED_ENUM`` when schema
    knowledge is available but an empty container has no elements from which
    Rust can infer a type.  Paths use mapping keys and list indexes; for
    example, ``{(1,): "HashMap<String, String>"}`` targets the second item
    of ``[1, {}]``.  The supplied type is emitted as ``<TYPE>::new()``.
    """
    record_unify_optional_fields: bool = False
    record_map_value_typing: RecordMapValueTypings = (
        RecordMapValueTypings.NARROW
    )
    # Keep in sync with the ``--edition`` flag in
    # ``.github/workflows/lint.yml``.
    language_version: VersionFormats = VersionFormats.EDITION_2021
    indent: str = "    "

    _default_null_literal: ClassVar[str] = "None::<()>"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ";"
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether Rust should render via ``serde_json::Value``."""
        return self.json_type is not None

    @cached_property
    def null_literal(self) -> str:
        """Null literal for the active Rust representation."""
        if self._json_type_active:
            return "null"
        return self._default_null_literal

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file.

        ``LAZY_STATIC`` adds ``use std::sync::LazyLock;``; other
        declaration styles produce no static preamble.
        """
        cls = type(self.declaration_style)
        if self.declaration_style is cls.LAZY_STATIC:
            return ("use std::sync::LazyLock;",)
        return ()

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument."""
        if self._json_type_active:
            return _format_rust_json_call_arg
        return identity_call_arg

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
        if self._json_type_active:
            return _format_rust_json_assignment
        return variable_formatter(template="{name} = {value};")

    @cached_property
    def _heterogeneous_variant_date_type(self) -> str:
        """Rust type used for :class:`datetime.date` variant payloads."""
        return (
            "&'static str"
            if self.date_format.value.type_produced is str
            else "NaiveDate"
        )

    @cached_property
    def _heterogeneous_variant_datetime_type(self) -> str:
        """Rust type used for :class:`datetime.datetime` variant
        payloads.
        """
        produced = self.datetime_format.value.type_produced
        if produced is str:
            return "&'static str"
        if produced is int:
            return "i64"
        return "NaiveDateTime"

    @cached_property
    def _strategy_params(self) -> _StrategyParams:
        """Bundle of arguments handed to the active strategy's
        builders.
        """
        return _StrategyParams(
            enum_name=self.heterogeneous_value_enum_name,
            date_type=self._heterogeneous_variant_date_type,
            datetime_type=self._heterogeneous_variant_datetime_type,
            record_prefix=self.record_struct_name_prefix,
            record_shape_names=self.record_shape_names,
            unify_optional_fields=self.record_unify_optional_fields,
            map_value_typing=self.record_map_value_typing,
            empty_container_type_hints=self.empty_container_type_hints,
            sequence_format_type_annotation=(
                self.sequence_format.format_type_annotation
            ),
            sequence_supports_heterogeneity=(
                self.sequence_format.supports_heterogeneity
            ),
        )

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
                skip_scalar_checks=True,
                wrap_non_scalar=_rust_json_non_scalar_child,
            )
        return dataclasses.replace(
            self.heterogeneous_strategy.value.build_behavior(
                self._strategy_params,
            ),
            empty_container_literal_overrides=(
                _rust_empty_container_literal_override_hook(
                    self._strategy_params
                )
            ),
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.TAGGED_ENUM`` emits a minimal
        ``enum`` declaration listing only the variants actually used in
        heterogeneous positions in the data.  For
        ``HeterogeneousStrategies.RECORD`` emits one ``struct``
        declaration per record shape present in the data.  Other
        strategies produce no preamble.
        """
        if self._json_type_active:
            return no_data_preamble
        return self.heterogeneous_strategy.value.build_preamble(
            self._strategy_params,
        )

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
        return _rust_call_stub

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

    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    def __post_init__(self) -> None:
        """Validate that incompatible formats are not combined."""
        _decl_cls = type(self.declaration_style)
        _seq_cls = type(self.sequence_format)
        if self._json_type_active and self.declaration_style in {
            _decl_cls.CONST,
            _decl_cls.STATIC,
        }:
            msg = (
                "Rust json_type uses serde_json::json!(…), which is not "
                "a constant-expression initializer. Use LET, LET_MUT, or "
                "LAZY_STATIC instead."
            )
            raise IncompatibleFormatsError(msg)
        if (
            self.declaration_style in {_decl_cls.CONST, _decl_cls.STATIC}
            and self.sequence_format is _seq_cls.VEC
        ):
            msg = (
                f"Rust {self.declaration_style.name} requires a "
                f"constant-expression initializer, but the "
                f"VEC sequence format produces vec![…] which "
                f"is not a constant expression. "
                f"Use ARRAY or TUPLE instead."
            )
            raise IncompatibleFormatsError(msg)
        self._validate_record_naming()

    def _validate_json_value_keys(self, data: Value, /) -> None:
        """Reject non-string object keys for ``serde_json::Value``."""
        match data:
            case dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "Rust json_type can only represent dict keys "
                            f"as JSON object strings, not {type(key).__name__}"
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value_keys(value)
            case list():
                for item in data:
                    self._validate_json_value_keys(item)
            case set():
                for item in data:
                    self._validate_json_value_keys(item)
            case _:
                return

    def _validate_record_naming(self) -> None:
        """Validate ``record_struct_name_prefix`` and
        ``record_shape_names`` for PascalCase identifier shape,
        reserved-keyword collisions, collisions with
        ``heterogeneous_value_enum_name``, and duplicate target names.
        """
        prefix = self.record_struct_name_prefix
        auto_name_pattern = re.compile(
            pattern=rf"^{re.escape(pattern=prefix)}\d+$",
        )
        seen_names: set[str] = set()
        for keys, name in self.record_shape_names.items():
            if not _PASCAL_CASE_IDENTIFIER.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which is not a PascalCase Rust "
                    f"identifier."
                )
                raise InvalidRecordNameError(msg)
            if name in _RUST_PASCAL_KEYWORDS:
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which is a Rust reserved keyword."
                )
                raise InvalidRecordNameError(msg)
            if name in _RUST_EMITTED_TYPE_NAMES:
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which names a type the generated "
                    f"code itself uses."
                )
                raise InvalidRecordNameError(msg)
            if name == self.heterogeneous_value_enum_name:
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which collides with "
                    f"heterogeneous_value_enum_name."
                )
                raise InvalidRecordNameError(msg)
            if auto_name_pattern.match(string=name):
                msg = (
                    f"record_shape_names entry for keys {sorted(keys)!r} "
                    f"maps to {name!r}, which collides with the "
                    f"auto-generated {prefix!r}-prefixed struct names."
                )
                raise InvalidRecordNameError(msg)
            if name in seen_names:
                msg = (
                    f"record_shape_names maps multiple key-sets to "
                    f"{name!r}; struct names must be unique."
                )
                raise InvalidRecordNameError(msg)
            seen_names.add(name)

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        if self._json_type_active:
            return self._validate_json_value_keys
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate Rust-specific data/format combinations."""
        _reject_float_collection_keys(data=data)
        # The element types of a tuple stand apart, so siblings inside
        # a list written as one need no common type (issue #4663).
        renders_list_as_tuple = (
            self.sequence_format is type(self.sequence_format).TUPLE
        )
        if self.sequence_format in {
            type(self.sequence_format).ARRAY,
            type(self.sequence_format).TUPLE,
        }:
            reject_ragged_nested_sequences(
                data=data,
                language_name="Rust",
                record_fields_are_independent=(
                    self.heterogeneous_strategy
                    is type(self.heterogeneous_strategy).RECORD
                ),
                list_elements_are_independent=renders_list_as_tuple,
            )
        if self._json_type_active:
            self._validate_json_value_keys(data)
        if (
            self.heterogeneous_strategy
            is type(self.heterogeneous_strategy).RECORD
        ):
            widened_ids = _rust_derecordized_map_ids(
                data=data,
                unify_optional_fields=self.record_unify_optional_fields,
            )
            _raise_for_derecordized_map_container_values(
                data=data, widened_ids=widened_ids
            )
        if (
            not self._json_type_active
            and self.datetime_format.value.type_produced is datetime.datetime
        ):
            reject_aware_datetimes(
                data=data, language_name="Rust", allow_utc_offset=False
            )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return SequenceFormatConfig(
                sequence_open=fixed_open(open_str=f"{_SERDE_JSON_MACRO}(["),
                close="])",
                supports_heterogeneity=True,
                single_element_trailing_comma=False,
                single_element_template=None,
                supports_trailing_comma=True,
                empty_sequence=f"{_SERDE_JSON_MACRO}([])",
                preamble_lines=(),
                format_entry=passthrough_sequence_entry,
                typed_opener_fallback=None,
                uses_typed_literal_for_scalars=False,
                requires_uniform_record_shapes=False,
                declared_type=(
                    self.json_type.value
                    if self.json_type is not None
                    else None
                ),
                narrowed_empty_form=None,
            )
        return self.sequence_format(
            default_type=self.default_sequence_element_type,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return SetFormatConfig(
                set_open=fixed_open(open_str=f"{_SERDE_JSON_MACRO}(["),
                close="])",
                empty_set=f"{_SERDE_JSON_MACRO}([])",
                preamble_lines=(),
                set_opener_template="",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        return self.set_format(default_type=self.default_set_element_type)

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return DictFormatConfig(
                dict_open=fixed_open(open_str=f"{_SERDE_JSON_MACRO}({{"),
                close="})",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_dict=f"{_SERDE_JSON_MACRO}({{}})",
                preamble_lines=(),
                narrowed_open=None,
                supports_trailing_comma=True,
                narrowed_empty_form=None,
            )
        return dataclasses.replace(
            self.dict_format(
                default_type=self.default_dict_value_type,
                default_key_type=self.default_dict_key_type,
            ),
            narrowed_empty_form=self._narrowed_empty_dict_form,
        )

    @cached_property
    def _narrowed_empty_dict_form(
        self,
    ) -> Callable[[Sequence[dict[Scalar, Value]]], str]:
        """Render an empty map that borrows a non-empty sibling's type.

        ``[{}, {"x": 1}]`` renders the empty map as
        ``<HashMap<&str, i32>>::from([])`` so it shares the concrete
        key/value types Rust infers for the non-empty sibling
        ``HashMap::from([("x", 1)])``; without the annotation the empty
        map defaults to ``HashMap<String, String>`` and the list fails
        to type-check (issue #3013).
        """

        def recurse(element: Value) -> str:
            """Resolve a sibling element to its Rust type annotation."""
            return _rust_type_annotation(
                data=element,
                date_type=self._declaration_date_type,
                datetime_type=self._declaration_datetime_type,
                sequence_format_type_annotation=(
                    self.sequence_format.format_type_annotation
                ),
                sequence_supports_heterogeneity=(
                    self.sequence_format.supports_heterogeneity
                ),
                set_format_type_annotation=(
                    self.set_format.format_type_annotation
                ),
                dict_format_type_annotation=(
                    self.dict_format.format_type_annotation
                ),
                default_sequence_element_type=(
                    self.default_sequence_element_type
                ),
                default_set_element_type=self.default_set_element_type,
                default_dict_key_type=self.default_dict_key_type,
                default_dict_value_type=self.default_dict_value_type,
            )

        def _form(siblings: Sequence[dict[Scalar, Value]]) -> str:
            """Type the empty map from its first non-empty sibling."""
            sibling = siblings[0]
            # As in ``_rust_type_annotation``, a heterogeneous format
            # annotates each element in place and its
            # ``format_type_annotation`` raises, so it must not be
            # probed.
            encodes_length = (
                self.sequence_format.supports_heterogeneity
                or _rust_sequence_encodes_length(
                    sequence_format_type_annotation=(
                        self.sequence_format.format_type_annotation
                    ),
                )
            )
            key_type = _rust_homogeneous_element_type(
                elements=list(sibling),
                infer=recurse,
                default_type=self.default_dict_key_type,
                sequence_encodes_length=encodes_length,
            )
            value_type = _rust_homogeneous_element_type(
                elements=list(sibling.values()),
                infer=recurse,
                default_type=self.default_dict_value_type,
                sequence_encodes_length=encodes_length,
            )
            annotation = self.dict_format.format_type_annotation(
                key_type=key_type,
                value_type=value_type,
            )
            return f"<{annotation}>::from([])"

        return _form

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
        if self._json_type_active:
            return format_date_iso
        return self.date_format

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if (
            self._json_type_active
            and self.datetime_format.value.type_produced is not int
        ):
            return format_datetime_iso
        return self.datetime_format

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return format_time_iso

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self.string_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal.

        Rust's widest built-in integer types are ``i128``/``u128``;
        values outside the signed ``i128`` range have no native literal
        form, so raise :class:`UnrepresentableIntegerError` rather than
        emit a literal ``rustc`` will reject.
        """
        return make_overflow_fallback_formatter(
            base=_make_rust_integer_suffix_formatter(
                base=self.integer_format.get_formatter(
                    numeric_separator=self.numeric_separator,
                ),
            ),
            min_value=_I128_MIN,
            max_value=_I128_MAX,
            fallback=raise_for_unrepresentable_int(language_name="Rust"),
        )

    @cached_property
    def format_integer_beyond_i64(self) -> Callable[[int], str]:
        """Always-``i128``-suffixed formatter for collections that
        exceed signed 64-bit range.
        """
        return make_overflow_fallback_formatter(
            base=_make_rust_i128_formatter(
                base=self.integer_format.get_formatter(
                    numeric_separator=self.numeric_separator,
                ),
            ),
            min_value=_I128_MIN,
            max_value=_I128_MAX,
            fallback=raise_for_unrepresentable_int(language_name="Rust"),
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(
                    open_str=f"{_SERDE_JSON_MACRO}({{"
                ),
                close="})",
                preamble_lines=(),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="HashMap::from(["),
            close="])",
            preamble_lines=("use std::collections::HashMap;",),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        if self._json_type_active:
            return dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            )
        return tuple_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def _declaration_date_type(self) -> str:
        """Rust type used to annotate :class:`datetime.date` values."""
        return (
            "&str"
            if self.date_format.value.type_produced is str
            else "NaiveDate"
        )

    @cached_property
    def _declaration_datetime_type(self) -> str:
        """Rust type used to annotate :class:`datetime.datetime`
        values.
        """
        produced = self.datetime_format.value.type_produced
        if produced is int:
            return "i64"
        if produced is str:
            return "&str"
        return "NaiveDateTime"

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        if self._json_type_active:
            assert self.json_type is not None  # noqa: S101
            return self.declaration_style.build_json_formatter(
                json_type=self.json_type.value,
            )
        return self.declaration_style.build_formatter(
            date_type=self._declaration_date_type,
            datetime_type=self._declaration_datetime_type,
            sequence_format_type_annotation=(
                self.sequence_format.format_type_annotation
            ),
            sequence_supports_heterogeneity=(
                self.sequence_format.supports_heterogeneity
            ),
            set_format_type_annotation=(
                self.set_format.format_type_annotation
            ),
            dict_format_type_annotation=(
                self.dict_format.format_type_annotation
            ),
            default_sequence_element_type=self.default_sequence_element_type,
            default_set_element_type=self.default_set_element_type,
            default_dict_key_type=self.default_dict_key_type,
            default_dict_value_type=self.default_dict_value_type,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        if self._json_type_active:
            return {}
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            extra=None,
        )

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value


register_json_native_document_fast(language_cls=Rust)
