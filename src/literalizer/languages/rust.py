"""Rust language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never, cast

from beartype import beartype

from literalizer._formatters.collection_openers import fixed_open
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
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
)
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_raw_rust,
)
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    iter_wrapped_scalars,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
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
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    prepend_body_preamble,
    value_contains,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import IncompatibleFormatsError

_I32_MIN = -(2**31)
_I32_MAX = 2**31 - 1
_I64_MIN = -(2**63)
_I64_MAX = 2**63 - 1


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
def _unify_rust_types(types: Sequence[str]) -> str:
    """Return a single Rust type that covers *types*.

    All-integer type lists widen to the largest integer; otherwise,
    returns the single type present.  Mixed-family inputs never reach
    this function because
    :func:`~literalizer._checks.check_data` raises for them.

    Callers must pass a non-empty sequence.
    """
    unique = list(dict.fromkeys(types))
    match unique:
        case [only]:
            return only
        case _:
            return max(unique, key=("i32", "i64", "i128").index)


@beartype
def _rust_scalar_type(  # noqa: PLR0911
    *,
    data: Scalar,
    date_type: str,
    datetime_type: str,
) -> str:
    """Return the Rust type annotation for a scalar value."""
    match data:
        case bool():
            return "bool"
        case int():
            return _rust_integer_type(value=data)
        case float():
            return "f64"
        case str():
            return "&str"
        case bytes():
            return "&str"
        case datetime.datetime():
            return datetime_type
        case datetime.date():
            return date_type
        case None:
            return "Option<()>"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _rust_homogeneous_element_type(
    *,
    elements: Sequence[Value],
    infer: Callable[[Value], str],
    default_type: str,
) -> str:
    """Return the element type for a homogeneous Rust collection."""
    if not elements:
        return default_type
    types = [infer(element) for element in elements]
    return _unify_rust_types(types=types)


@beartype
def _rust_type_annotation(
    *,
    data: Value,
    date_type: str,
    datetime_type: str,
    sequence_format_type_annotation: Callable[[str, int], str],
    sequence_supports_heterogeneity: bool,
    set_format_type_annotation: Callable[[str], str],
    dict_format_type_annotation: Callable[[str, str], str] | None,
    default_sequence_element_type: str,
    default_set_element_type: str,
    default_dict_key_type: str,
    default_dict_value_type: str,
) -> str:
    """Derive a Rust type annotation string from a ``Value``.

    When ``dict_format_type_annotation`` is ``None`` (``CONST`` /
    ``STATIC``), :meth:`Rust.validate_spec_for_data` rejects dict data
    upstream (Rust has no const-expression dict format), so the
    ``case dict()`` arm is unreachable at runtime but still required
    so the final ``case _`` narrows to ``Scalar`` for
    ``_rust_scalar_type``.  When it is a callable (``LAZY_STATIC``),
    dict data is supported and the arm emits ``HashMap<K, V>`` or
    ``BTreeMap<K, V>``.
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

    match data:
        case set():
            element_type = _rust_homogeneous_element_type(
                elements=list(data),
                infer=recurse,
                default_type=default_set_element_type,
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
            )
            return sequence_format_type_annotation(element_type, len(data))
        case dict():
            if dict_format_type_annotation is None:  # pragma: no cover
                # Defensive: unreachable at runtime because
                # validate_spec_for_data rejects dict data for
                # CONST/STATIC before this function is called.
                msg = (
                    "Rust CONST/STATIC reject dict data in "
                    "validate_spec_for_data"
                )
                raise AssertionError(msg)
            keys: list[Value] = list(data)
            key_type = _rust_homogeneous_element_type(
                elements=keys,
                infer=recurse,
                default_type=default_dict_key_type,
            )
            value_type = _rust_homogeneous_element_type(
                elements=list(data.values()),
                infer=recurse,
                default_type=default_dict_value_type,
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
    set_format_type_annotation: Callable[[str], str],
    default_sequence_element_type: str,
    default_set_element_type: str,
) -> str:
    """Format a ``const`` or ``static`` declaration with a type
    annotation.
    """
    type_annotation = _rust_type_annotation(
        data=data,
        date_type=date_type,
        datetime_type=datetime_type,
        sequence_format_type_annotation=(sequence_format_type_annotation),
        sequence_supports_heterogeneity=(sequence_supports_heterogeneity),
        set_format_type_annotation=set_format_type_annotation,
        dict_format_type_annotation=None,
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
def _heterogeneous_variant_for_scalar(  # noqa: PLR0911
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
            return _VariantSignature(name="Bool", inner_type="bool")
        case int():
            int_type = _rust_integer_type(value=value)
            return _VariantSignature(
                name=int_type.upper(),
                inner_type=int_type,
            )
        case float():
            return _VariantSignature(name="F64", inner_type="f64")
        case str():
            return _VariantSignature(
                name="Str",
                inner_type="&'static str",
            )
        case bytes():
            return _VariantSignature(
                name="Bytes",
                inner_type="&'static str",
            )
        case datetime.datetime():
            return _VariantSignature(
                name="DateTime",
                inner_type=datetime_type,
            )
        case datetime.date():
            return _VariantSignature(name="Date", inner_type=date_type)
        case None:
            return _VariantSignature(name="Null", inner_type=None)
        case _ as unreachable:
            assert_never(unreachable)


@dataclasses.dataclass(frozen=True)
class _HeterogeneousStrategyConfig:
    """Configuration for one Rust heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Rust instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the tagged-enum declaration lines).  Both
    receive the Rust instance's configurable enum name and scalar
    type names so the resulting functions can close over them.
    """

    build_behavior: Callable[[str, str, str], HeterogeneousBehavior]
    build_preamble: Callable[
        [str, str, str],
        Callable[[Value], tuple[str, ...]],
    ]


def _build_error_behavior(
    _enum_name: str,
    _date_type: str,
    _datetime_type: str,
    /,
) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


def _build_error_preamble(
    _enum_name: str,
    _date_type: str,
    _datetime_type: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


def _build_tagged_enum_behavior(
    enum_name: str,
    date_type: str,
    datetime_type: str,
    /,
) -> HeterogeneousBehavior:
    """TAGGED_ENUM strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should wrap."""
        return collect_heterogeneous_container_ids(data=data)

    def _wrap(raw_value: Value, formatted: str) -> str:
        """Wrap a scalar in ``{enum_name}::{Variant}(formatted)``.

        :func:`~literalizer._literalize._maybe_wrap_child` filters
        non-scalar values before dispatching, so *raw_value* is always
        a scalar.
        """
        signature = _heterogeneous_variant_for_scalar(
            value=cast("Scalar", raw_value),
            date_type=date_type,
            datetime_type=datetime_type,
        )
        if signature.inner_type is None:
            return f"{enum_name}::{signature.name}"
        return f"{enum_name}::{signature.name}({formatted})"

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
    )


def _build_tagged_enum_preamble(
    enum_name: str,
    date_type: str,
    datetime_type: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """TAGGED_ENUM strategy: emit a minimal ``enum`` declaration."""

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the tagged-enum declaration for *data*."""
        wrap_ids = collect_heterogeneous_container_ids(data=data)
        if not wrap_ids:
            return ()
        scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
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
        lines: list[str] = [f"enum {enum_name} {{"]
        for variant in variants:
            body = (
                variant.name
                if variant.inner_type is None
                else f"{variant.name}({variant.inner_type})"
            )
            lines.append(f"    {body},")
        lines.append("}")
        return tuple(lines)

    return _preamble


def _rust_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return Rust stub declarations for a call name."""
    # Use generic type parameters so any argument type is accepted.
    type_vars = [chr(ord("A") + i) for i in range(len(params))]
    generic_decl = ", ".join(type_vars)
    if len(parts) == 1:
        param_list = ", ".join(
            f"_{p}: {t}" for p, t in zip(params, type_vars, strict=True)
        )
        return (f"fn {parts[0]}<{generic_decl}>({param_list}) {{}}",)
    root = parts[0]
    method = parts[-1]
    param_list = ", ".join(
        f"_{p}: {t}" for p, t in zip(params, type_vars, strict=True)
    )
    fields = parts[1:-1]
    if not fields:
        type_name = f"{root.title()}Type_"
        return (
            f"struct {type_name};",
            f"impl {type_name} {{"
            f" fn {method}<{generic_decl}>"
            f"(&self, {param_list}) {{}} }}",
            f"let {root} = {type_name};",
        )
    lines: list[str] = []
    inner_type = f"{fields[-1].title()}Type_"
    lines.append(f"struct {inner_type};")
    lines.append(
        f"impl {inner_type} {{"
        f" fn {method}<{generic_decl}>"
        f"(&self, {param_list}) {{}} }}"
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
    """

    extension = ".rs"
    pygments_name = "rust"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True

    class DateFormats(enum.Enum):
        """Date format options for Rust."""

        RUST = DateFormatConfig(
            formatter=_format_date_rust,
            preamble_lines=("use chrono::NaiveDate;",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

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
        )
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
        """Sequence type options for Rust."""

        VEC = enum.member(
            value=sequence_format_factory(
                open_template="vec![",
                close="]",
                supports_heterogeneity=False,
                single_element_trailing_comma=False,
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
                supports_trailing_comma=True,
                empty_template=None,
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
                single_element_trailing_comma=False,
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
            suffix=" */",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value};"
            ),
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
                    set_format_type_annotation=set_format_type_annotation,
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

        DOUBLE = enum.member(value=format_string_backslash)
        RAW = enum.member(value=format_string_raw_rust)

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

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Rust call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

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

    heterogeneous_strategies = HeterogeneousStrategies

    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.PASCAL,
        IdentifierCase.UPPER_SNAKE,
    )

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
        indented = textwrap.indent(text=content, prefix=self.indent)
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
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.LET
    dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT
    dict_format: DictFormats = DictFormats.HASH_MAP
    float_format: FloatFormats = FloatFormats.REPR
    integer_format: IntegerFormats = IntegerFormats.DECIMAL
    numeric_literal_suffix: NumericLiteralSuffixes = (
        NumericLiteralSuffixes.NONE
    )
    numeric_separator: NumericSeparators = NumericSeparators.NONE
    numeric_style: NumericStyles = NumericStyles.OVERLOADED
    string_format: StringFormats = StringFormats.DOUBLE
    trailing_comma: TrailingCommas = TrailingCommas.YES
    line_ending: LineEndings = LineEndings.SEMICOLON
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    heterogeneous_value_enum_name: str = "Value"
    indent: str = "    "

    null_literal: ClassVar[str] = "None::<()>"
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
        return (
            "&'static str"
            if self.datetime_format.value.type_produced is str
            else "NaiveDateTime"
        )

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        return self.heterogeneous_strategy.value.build_behavior(
            self.heterogeneous_value_enum_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
        )

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.TAGGED_ENUM`` emits a minimal
        ``enum`` declaration listing only the variants actually used in
        heterogeneous positions in the data.  Other strategies produce
        no preamble.
        """
        return self.heterogeneous_strategy.value.build_preamble(
            self.heterogeneous_value_enum_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
        )

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _rust_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

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

    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    def __post_init__(self) -> None:
        """Validate that incompatible formats are not combined."""
        _decl_cls = type(self.declaration_style)
        _seq_cls = type(self.sequence_format)
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

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid code for *data*.

        Rust's only dict/map formats (``HashMap::from`` and
        ``BTreeMap::from``) are runtime calls, so ``CONST`` and
        ``STATIC`` declarations cannot accept dict data.
        """
        _decl_cls = type(self.declaration_style)
        if self.declaration_style not in {_decl_cls.CONST, _decl_cls.STATIC}:
            return
        if value_contains(data=data, predicate=lambda v: isinstance(v, dict)):
            msg = (
                f"Rust {self.declaration_style.name} requires a "
                f"constant-expression initializer, but the "
                f"{self.dict_format.name} dict format produces a "
                f"runtime ::from([…]) call which is not a constant "
                f"expression."
            )
            raise IncompatibleFormatsError(msg)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format(
            default_type=self.default_sequence_element_type,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format(default_type=self.default_set_element_type)

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
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self.string_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return _make_rust_integer_suffix_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="HashMap::from(["),
            close="])",
            preamble_lines=("use std::collections::HashMap;",),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return tuple_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.build_formatter(
            date_type=(
                "&str"
                if self.date_format.value.type_produced is str
                else "NaiveDate"
            ),
            datetime_type=(
                "&str"
                if self.datetime_format.value.type_produced is str
                else "NaiveDateTime"
            ),
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
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
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
