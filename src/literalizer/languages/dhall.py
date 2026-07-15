"""Dhall language specification."""

import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar, assert_never

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_narrowed_empty_form,
)
from literalizer._formatters.format_dates import (
    datetime_epoch_formatter,
    format_date_iso,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import (
    escape_control_chars,
)
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    collect_sibling_map_wrap_ids,
    iter_wrapped_scalars,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
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
    default_sequence_binding_declarations,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_compute_call_slot_wrap_ids,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_pygments_name,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    wrap_in_file_noop,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    CallArgNotSupportedError,
    InvalidDictKeyError,
    WrapCombinedInFileNotSupportedError,
)

_IDENTIFIER_RE = re.compile(pattern=r"^[A-Za-z_][A-Za-z0-9_/\-]*$")

_DHALL_UNESCAPE_RE = re.compile(pattern=r"\\([$\"\\nrt]|u\{([0-9A-Fa-f]+)\})")

# Dhall backtick labels allow printable ASCII excluding backtick:
# %x20-5F / %x61-7E (space through underscore, a-z plus {|}~).
_BACKTICK_LABEL_RE = re.compile(pattern=r"^[\x20-\x5f\x61-\x7e]+$")


@beartype
def _unescape_dhall_string(value: str) -> str:
    """Reverse Dhall double-quoted string escapes to produce raw
    content.
    """
    _simple_escapes = {
        "$": "$",
        '"': '"',
        "\\": "\\",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }

    def _replace(match: re.Match[str]) -> str:
        """Replace a single escape sequence with its raw character."""
        hex_digits: str | None = match.group(2)
        if hex_digits is not None:
            return chr(int(hex_digits, base=16))
        return _simple_escapes[match.group(1)]

    return _DHALL_UNESCAPE_RE.sub(repl=_replace, string=value)


_dhall_narrowed_empty_form = make_narrowed_empty_form(
    element_to_type=make_element_to_type(
        str_type="Text",
        bool_type="Bool",
        int_type="Integer",
        float_type="Double",
        mixed_numeric_type="Text",
        bytes_type="Text",
        date_type="Text",
        datetime_type="Text",
        time_type="Text",
        list_template="(List {inner})",
        enable_list_type=True,
        dict_type_template=None,
        fallback_value_type="Text",
    ),
    template="[] : List {type}",
    fallback_type="Text",
)


@beartype
def _format_dhall_integer(value: int) -> str:
    """Format an integer for Dhall.

    Dhall distinguishes ``Natural`` (non-negative, no prefix) from
    ``Integer`` (signed, requires ``+`` or ``-`` prefix).  To keep
    lists type-homogeneous we always emit the ``Integer`` form.
    """
    if value >= 0:
        return f"+{value}"
    return f"{value}"


@beartype
def _format_dhall_string(value: str) -> str:
    r"""Format a string for Dhall using backslash escaping.

    Escapes backslashes, double quotes, dollar signs (Dhall uses
    ``${...}`` for interpolation), newlines, tabs, and C0 control
    characters, then wraps the result in double quotes.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("$", "\\$")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    escaped = escape_control_chars(value=escaped, fmt="\\u{{{:04X}}}")
    return f'"{escaped}"'


@beartype
def _format_dhall_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format a Dhall record entry as ``key = value``.

    If the key is a valid Dhall simple label (letter or underscore
    followed by letters, digits, hyphens, underscores, or slashes),
    the quotes are stripped for idiomatic bare output.  Otherwise the
    key is wrapped in backticks, which Dhall uses for non-identifier
    labels.
    """
    inner = key[1:-1]
    if _IDENTIFIER_RE.match(string=inner):
        return f"{inner} = {formatted_value}"
    raw = _unescape_dhall_string(value=inner)
    if not raw or not _BACKTICK_LABEL_RE.match(string=raw):
        msg = (
            f"Dhall does not support the dict key {key}. "
            "Backtick-quoted labels must be non-empty and contain only "
            "printable ASCII (no backticks or control characters)."
        )
        raise InvalidDictKeyError(msg)
    return f"`{raw}` = {formatted_value}"


_DHALL_DVAL_TYPE = (
    "let DVal = "
    "< DBool : Bool | DDouble : Double | DInteger : Integer | DText : Text >"
)


@beartype
def _dhall_call_preamble_stub(
    _parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return the ``DVal`` union-type definition for Dhall call stubs."""
    return (_DHALL_DVAL_TYPE,)


@beartype
def _dhall_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    r"""Return Dhall let-binding stub declarations for a call target.

    Single-part targets produce curried functions such as
    ``let name = \(_ : DVal) -> \(_ : DVal) -> body``.
    Dotted targets nest record literals: ``app.client.fetch`` becomes
    ``let app = { client = { fetch = \(_ : DVal) -> body } }``.
    The *stub_return* controls the body: ``VOID`` stubs return ``{=}``;
    ``VALUE`` stubs return ``DVal.DBool True`` so the result type
    matches callers that consume the return value (e.g. a transform
    wrapper like ``emit``).
    """
    body = "{=}" if stub_return is StubReturn.VOID else "DVal.DBool True"
    fn_expr = body
    for _param in reversed(params):
        fn_expr = f"\\(_ : DVal) -> {fn_expr}"
    if len(parts) == 1:
        return (f"let {parts[0]} = {fn_expr}",)
    root = parts[0]
    nested: str = fn_expr
    for field in reversed(parts[1:]):
        nested = f"{{ {field} = {nested} }}"
    return (f"let {root} = {nested}",)


@beartype
def _dhall_format_call_arg(original: Value, formatted: str, /) -> str:
    """Wrap a formatted scalar in the appropriate ``DVal`` constructor.

    Booleans, integers, floats, and strings each get their own
    ``DVal.DXxx`` tag so the stub (which accepts ``DVal``) type-checks
    against heterogeneous call arguments.
    """
    match original:
        case bool():
            return f"DVal.DBool {formatted}"
        case int():
            return f"DVal.DInteger {formatted}"
        case float():
            return f"DVal.DDouble {formatted}"
        case str() | bytes() | datetime.datetime() | datetime.date() | None:
            return f"DVal.DText {formatted}"
        case _:
            raise CallArgNotSupportedError(
                language_name="Dhall",
                reason="Dhall call stubs only support scalar arguments",
            )


@beartype
def _dhall_format_call_target(parts: Sequence[str], /) -> str:
    """Join call target parts with dots and append a trailing space.

    Dhall requires whitespace between a function expression and its
    argument.  Dhall's positional style parenthesizes each argument, so
    a trailing space on the target string yields valid curried
    application such as ``target (arg1) (arg2)``.
    """
    return ".".join(parts) + " "


# Matches a Dhall double-quoted string literal including escape sequences,
# so string contents are stripped before scanning for structural patterns.
_DHALL_STRING_RE = re.compile(pattern=r'"(?:[^"\\]|\\.)*"')


@beartype
def _dhall_validate_call_stmt(call_expr: str) -> None:
    """Raise :exc:`~literalizer.exceptions.CallArgNotSupportedError` for
    call expressions that cannot be represented as valid Dhall.

    This rejects function-application wrappers with a word character
    directly followed by ``(`` -- for example a call-transform wrapper
    like ``emit(...)`` written without the whitespace that Dhall
    requires before a function argument.

    String literals are stripped first so quoted content is never
    mistaken for this pattern.
    """
    sanitized = _DHALL_STRING_RE.sub(repl="", string=call_expr)
    prev_is_word = False
    for c in sanitized:
        next_prev_is_word = False
        match c:
            case "(":
                if prev_is_word:
                    raise CallArgNotSupportedError(
                        language_name="Dhall",
                        reason=(
                            "call_transform produces a function application "
                            "without the whitespace Dhall requires before '(' "
                            f"(in: {call_expr!r})"
                        ),
                    )
            case _:
                next_prev_is_word = c.isalnum() or c == "_"
        prev_is_word = next_prev_is_word


@beartype
def _dhall_format_call_variable_declaration(
    name: str,
    value: str,
    _data: Value,
    _modifiers: frozenset[enum.Enum],
    /,
) -> str:
    """Format a Dhall call-result declaration after validating the
    call.
    """
    _dhall_validate_call_stmt(call_expr=value)
    return f"let {name} = {value} in {name}"


@beartype
def _dhall_format_call_variable_assignment(
    name: str,
    value: str,
    _data: Value,
    /,
) -> str:
    """Format a Dhall call-result assignment after validating the call."""
    _dhall_validate_call_stmt(call_expr=value)
    return f"let {name} = {value} in {name}"


@beartype
def _dhall_reject_ref_identifier(name: str, _value: Value | None, /) -> str:
    """Raise :exc:`~literalizer.exceptions.CallArgNotSupportedError` for
    any ``$ref`` argument.

    Dhall's stub parameter type is ``DVal``, but a ref variable holds a
    concrete type (e.g. ``List Integer``) that Dhall's type-checker
    cannot unify with ``DVal``.
    """
    raise CallArgNotSupportedError(
        language_name="Dhall",
        reason=(
            f"ref variable {name!r} has a concrete type that cannot be "
            "unified with the DVal stub parameter type"
        ),
    )


@dataclasses.dataclass(frozen=True)
class _VariantSignature:
    """Name and optional inner-type string for one Dhall union variant.

    ``inner_type`` is ``None`` for unit variants (e.g. ``Null``); for
    payload-carrying variants it's the Dhall type rendered after the
    ``:``, e.g. ``"Text"`` for ``Str : Text``.
    """

    name: str
    inner_type: str | None


_DHALL_TYPE_FOR_PYTHON_TYPE: dict[type, str] = {
    str: "Text",
    int: "Integer",
    float: "Double",
    bool: "Bool",
}


@beartype
def _dhall_variant_for_scalar(  # pylint: disable=too-complex
    *,
    value: Scalar,
    datetime_inner_type: str,
) -> _VariantSignature:
    """Return the Dhall union-type variant signature for *value*.

    Dhall has no per-width integer types, so all integers map to a
    single ``Int : Integer`` variant.  ``date`` and ``bytes`` are
    always rendered as ``Text`` by Dhall's built-in formatters;
    ``datetime`` may render as ``Text`` (ISO) or ``Integer`` (epoch),
    so its inner type is supplied by the caller.
    """
    match value:
        case bool():
            signature = _VariantSignature(name="Bool", inner_type="Bool")
        case int():
            signature = _VariantSignature(name="Int", inner_type="Integer")
        case float():
            signature = _VariantSignature(name="Double", inner_type="Double")
        case str():
            signature = _VariantSignature(name="Str", inner_type="Text")
        case bytes():
            signature = _VariantSignature(name="Bytes", inner_type="Text")
        case datetime.datetime():
            signature = _VariantSignature(
                name="DateTime", inner_type=datetime_inner_type
            )
        case datetime.date():
            signature = _VariantSignature(name="Date", inner_type="Text")
        case datetime.time():
            signature = _VariantSignature(name="Time", inner_type="Text")
        case None:
            signature = _VariantSignature(name="Null", inner_type=None)
        case _ as unreachable:
            assert_never(unreachable)
    return signature


@dataclasses.dataclass(frozen=True)
class _HeterogeneousStrategyConfig:
    """Configuration for one Dhall heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Dhall instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the ``let Value = < … > in`` declaration).
    Both receive the Dhall instance's configurable union name so the
    resulting functions can close over it.
    """

    build_behavior: Callable[[str, str], HeterogeneousBehavior]
    build_preamble: Callable[[str, str], Callable[[Value], tuple[str, ...]]]


@beartype
def _build_error_behavior(
    _union_name: str,
    _datetime_inner_type: str,
    /,
) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


@beartype
def _build_error_preamble(
    _union_name: str,
    _datetime_inner_type: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


@beartype
def _build_union_type_behavior(
    union_name: str,
    datetime_inner_type: str,
    /,
) -> HeterogeneousBehavior:
    """UNION_TYPE strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should wrap."""
        return collect_heterogeneous_container_ids(
            data=data
        ) | collect_sibling_map_wrap_ids(data=data)

    def _wrap(raw_value: Scalar, formatted: str) -> str:
        """Wrap a scalar as ``{union_name}.{Variant} payload``."""
        signature = _dhall_variant_for_scalar(
            value=raw_value,
            datetime_inner_type=datetime_inner_type,
        )
        if signature.inner_type is None:
            return f"{union_name}.{signature.name}"
        return f"{union_name}.{signature.name} {formatted}"

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
        wrap_non_scalar=None,
        compute_call_slot_wrap_ids=no_compute_call_slot_wrap_ids,
        dict_open_for_wrap_ids=None,
    )


@beartype
def _build_union_type_preamble(
    union_name: str,
    datetime_inner_type: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """UNION_TYPE strategy: emit a minimal ``let`` binding declaring
    the union type used to wrap heterogeneous scalars.
    """

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the union-type declaration for *data*."""
        wrap_ids = collect_heterogeneous_container_ids(
            data=data
        ) | collect_sibling_map_wrap_ids(data=data)
        if not wrap_ids:
            return ()
        scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
        variants: list[_VariantSignature] = []
        seen: set[str] = set()
        for scalar in scalars:
            signature = _dhall_variant_for_scalar(
                value=scalar,
                datetime_inner_type=datetime_inner_type,
            )
            if signature.name in seen:
                continue
            seen.add(signature.name)
            variants.append(signature)
        parts = [
            variant.name
            if variant.inner_type is None
            else f"{variant.name} : {variant.inner_type}"
            for variant in variants
        ]
        body = " | ".join(parts)
        return (f"let {union_name} = < {body} > in",)

    return _preamble


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Dhall(metaclass=LanguageCls):
    """Dhall language specification.

    Produces Dhall values — records for mappings, and lists for
    sequences and sets — following `Dhall <https://dhall-lang.org/>`_
    syntax.

    Dhall is a programmable configuration language that is not
    Turing-complete.  It supports records (``{ key = value }``), lists
    (``[1, 2, 3]``), ``Text``, ``Natural``, ``Double``, and ``Bool``
    types.

    Dhall has no ``null`` type; ``null`` values are rendered as the
    empty string ``""``.

    Dates and datetimes are rendered as quoted ISO 8601 strings because
    Dhall has no native date type.

    Dict keys that cannot be represented as Dhall backtick-quoted labels
    raise :class:`~literalizer.exceptions.InvalidDictKeyError`.  This
    includes empty keys and keys containing control characters or
    backticks, since Dhall labels only allow printable ASCII.
    """

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_declaration: ClassVar[property] = property(
        fget=lambda _self: _dhall_format_call_variable_declaration,
    )
    format_call_variable_assignment: ClassVar[property] = property(
        fget=lambda _self: _dhall_format_call_variable_assignment,
    )
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".dhall"
    pygments_name: ClassVar[str | None] = no_pygments_name
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = False
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = False
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
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
        """Date format options for Dhall."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Dhall."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=datetime_epoch_formatter(
                format_integer=_format_dhall_integer,
            ),
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
        """Sequence type options for Dhall."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="[] : List {}",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=True,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Dhall."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="["),
            close="]",
            empty_set="[] : List {}",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        LINE = CommentConfig(
            prefix="--",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value} in {name}",
            ),
            supports_redefinition=False,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options.

        Dhall backtick-quoted labels must be non-empty and contain only
        printable ASCII, so unsupported dict keys always raise
        :class:`~literalizer.exceptions.InvalidDictKeyError`.
        """

        ERROR = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Infinity",
        negative_infinity="-Infinity",
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

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

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
    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Dhall call style options."""

        POSITIONAL = PositionalCallStyle(
            arg_separator=" ",
            parenthesize_each_arg=True,
        )

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for representing dicts or lists whose scalar values
        span more than one Dhall type.
        """

        ERROR = _HeterogeneousStrategyConfig(
            build_behavior=_build_error_behavior,
            build_preamble=_build_error_preamble,
        )
        """Raise
        :exc:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
        (or
        :exc:`~literalizer.exceptions.HeterogeneousSiblingListsError`)
        when scalar values of mixed types appear in a container that
        cannot represent them.  This is the default, matching Dhall's
        strict-typing convention.
        """

        UNION_TYPE = _HeterogeneousStrategyConfig(
            build_behavior=_build_union_type_behavior,
            build_preamble=_build_union_type_preamble,
        )
        """Auto-generate a Dhall union type in the preamble containing
        only the variants actually present in the data, and wrap each
        heterogeneous scalar value as ``{UnionName}.{Variant} payload``.

        The union name is configurable via
        :attr:`Dhall.heterogeneous_value_union_name` (default
        ``"Value"``).
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class JsonTypes(enum.Enum):
        """Empty: this language has no JSON value-type variants."""

    json_types = JsonTypes

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class VersionFormats(enum.Enum):
        """Version options for Dhall."""

        V17 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
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

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid Dhall file.

        When *variable_name* is empty the call is from a call context
        (either :meth:`wrap_calls_with_declarations` or
        :func:`~literalizer.literalize_call` with ``wrap_in_file=True``);
        both need a closing ``in {=}`` to complete the ``let``-chain
        into a valid Dhall expression.  When *variable_name* is set the
        call is from a regular :func:`~literalizer.literalize` path
        whose content already ends with the ``in <varname>`` clause
        produced by the variable form.
        """
        wrapped = wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )
        if not variable_name:
            wrapped += "\nin {=}"
        return wrapped

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Unsupported: literalize() rejects BothVariableForms
        upstream.
        """
        del declaration, assignment, variable_name, body_preamble
        raise WrapCombinedInFileNotSupportedError

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.LINE
    declaration_style: DeclarationStyles = DeclarationStyles.LET
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
    heterogeneous_value_union_name: str = "Value"
    # Keep in sync with the pinned ``dhall`` binary in the ``Install
    # Dhall`` step of ``.github/workflows/lint.yml``.  Note the Dhall
    # *language* standard version is distinct from the ``dhall-haskell``
    # binary version: the pinned binary ``dhall-haskell`` 1.42.2
    # implements Dhall language standard 23.1.0, which is ``>=`` this
    # ``V17`` (Dhall standard 17.0.0) default, so the fixture gate runs
    # under a binary that accepts the declared language version.
    language_version: VersionFormats = VersionFormats.V17
    indent: str = "  "
    call_style: CallStyles = CallStyles.POSITIONAL

    null_literal: ClassVar[str] = '""'
    true_literal: ClassVar[str] = "True"
    false_literal: ClassVar[str] = "False"
    indent_closing_delimiter: ClassVar[bool] = False
    skip_null_dict_values: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return _format_dhall_string

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return _format_dhall_integer

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry."""
        return _format_dhall_dict_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="let {name} = {value} in {name}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.UNION_TYPE`` emits a ``let``
        binding declaring a union type containing only the variants
        actually used in heterogeneous positions in the data.  Other
        strategies produce no preamble.
        """
        return self.heterogeneous_strategy.value.build_preamble(
            self.heterogeneous_value_union_name,
            _DHALL_TYPE_FOR_PYTHON_TYPE[
                self.datetime_format.value.type_produced
            ],
        )

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        return self.heterogeneous_strategy.value.build_behavior(
            self.heterogeneous_value_union_name,
            _DHALL_TYPE_FOR_PYTHON_TYPE[
                self.datetime_format.value.type_produced
            ],
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
        return _dhall_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return the ``DVal`` union-type preamble for a call
        expression.
        """
        return _dhall_call_preamble_stub

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each scalar call argument in the ``DVal`` union tag."""
        return _dhall_format_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Validate and wrap a call expression as a ``let _ =`` binding.

        Raises :exc:`~literalizer.exceptions.CallArgNotSupportedError`
        if the rendered call contains a function application without the
        required whitespace, or more than one positional argument.
        """

        def _wrap(stmt: str) -> str:
            """Validate *call_expr* then wrap it as a ``let _ =``
            binding.
            """
            _dhall_validate_call_stmt(call_expr=stmt)
            return f"let _ = {stmt}"

        return _wrap

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Join declarations and calls into a Dhall let-chain.

        Delegates to :meth:`wrap_in_file` with an empty variable name,
        which appends the ``in {=}`` terminator needed by both
        this path and the ``wrap_in_file=True`` call path.
        """
        content = "\n".join((*declarations, calls)) if declarations else calls
        return self.wrap_in_file(
            content=content,
            variable_name="",
            body_preamble=body_preamble,
        )

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return _dhall_format_call_target

    @cached_property
    def format_call_ref_identifier(
        self,
    ) -> Callable[[str, Value | None], str]:
        """Raise for any ``$ref`` argument.

        Dhall's stub parameter type is ``DVal``; a ref variable holds a
        concrete type that Dhall's type-checker cannot unify with it.
        """
        return _dhall_reject_ref_identifier

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
            narrowed_empty_form=_dhall_narrowed_empty_form,
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
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=_format_dhall_dict_entry,
            empty_dict="{=}",
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
            ordered_map_open=fixed_open(open_str="{"),
            close="}",
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
        """Per-instance scalar preamble (Dhall needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Dhall needs none)."""
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
