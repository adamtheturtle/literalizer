"""Mojo language specification."""

import dataclasses
import datetime
import enum
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from typing import ClassVar, assert_never, cast

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
    make_element_to_type,
    make_narrowed_empty_form,
    make_type_to_opener,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    variable_declaration_formatter,
    variable_formatter,
)
from literalizer._formatters.format_factories import (
    dict_format_factory,
    set_format_factory,
)
from literalizer._formatters.format_floats import (
    format_float_fixed,
    format_float_repr,
    format_float_scientific,
)
from literalizer._formatters.format_strings import format_string_backslash
from literalizer._formatters.type_inference import infer_element_type
from literalizer._heterogeneous import (
    collect_heterogeneous_container_ids,
    iter_wrapped_scalars,
)
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
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import (
    CallArgNotSupportedError,
    NullInCollectionError,
)

_mojo_element_to_type = make_element_to_type(
    str_type="String",
    bool_type="Bool",
    int_type="Int",
    float_type="Float64",
    mixed_numeric_type="String",
    bytes_type="String",
    date_type="String",
    datetime_type="String",
    list_template="List[{inner}]",
    dict_type_template="Dict[String, {inner}]",
    fallback_value_type="String",
)


def _value_to_mojo_type(value: Value, /) -> str | None:
    """Map one call-argument value to its Mojo type string.

    Routes list values through :func:`infer_element_type` so a list
    slot resolves to a recursive ``List[...]`` type (e.g.
    ``[1, 2, 3]`` -> ``List[Int]``).  Non-list values, including
    dicts (ref-marker dicts on the ``wrap_in_file=True`` production
    path that bypasses ref substitution, ordered maps, real dicts),
    look up their Python ``type`` directly so only the scalar Mojo
    mappings are typed and any other shape falls back to the generic
    ``[*Ts: AnyType](*args: *Ts)`` form.  An empty or inhomogeneous
    list short-circuits via ``or list`` to the bare ``list`` type,
    which has no Mojo mapping and so also triggers the fallback.
    """
    if isinstance(value, list):
        return _mojo_element_to_type(infer_element_type(items=[value]) or list)
    return _mojo_element_to_type(type(value))


def _mojo_typed_param_list(
    params: Sequence[str],
    arg_values: Sequence[Value],
) -> tuple[str, ...] | None:
    """Return ``("name: Type", ...)`` for a typed Mojo signature.

    Returns ``None`` to signal the caller should fall back to the
    generic ``[*Ts: AnyType](*args: *Ts)`` form.  Falls back when any
    per-call value at a parameter slot has no Mojo type (a ref-marker
    dict, ``None``, an inhomogeneous list, etc.), when any slot has
    no values (e.g. transform-stub callers pass an empty
    ``arg_values``), or when types disagree across calls at the same
    slot.  A zero-parameter call returns ``()`` (typed, empty) so the
    caller emits a bare ``fn name():`` form rather than the generic
    stub.
    """
    if not params:
        return ()
    slots: list[list[Value]] = []
    for element in arg_values:
        per_arg = element if isinstance(element, list) else [element]
        for slot_index, arg_value in enumerate(iterable=per_arg):
            if slot_index >= len(slots):
                slots.append([])
            slots[slot_index].append(arg_value)
    if len(slots) != len(params):
        return None
    typed: list[str] = []
    for name, slot_values in zip(params, slots, strict=True):
        types = {_value_to_mojo_type(v) for v in slot_values}
        if None in types or len(types) != 1:
            return None
        (mojo_type,) = types
        typed.append(f"{name}: {mojo_type}")
    return tuple(typed)


def _mojo_init_expr(parts: Sequence[str]) -> str:
    """Return the constructor expression for a multi-part call target.

    For a 2-part target like ``throttler.check``, returns
    ``_ThrottlerType()``.  For a 3-part target like
    ``app.client.fetch``, returns ``_AppType(_ClientType())``.
    ``@fieldwise_init`` generates a field-by-field init, so each struct
    that holds a field is constructed by passing the inner instance.
    """
    root = parts[0]
    fields = parts[1:-1]
    root_type = f"_{root.capitalize()}Type"
    if not fields:
        return f"{root_type}()"
    inner_type = f"_{fields[-1].capitalize()}Type"
    expr = f"{inner_type}()"
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"_{fields[i].capitalize()}Type"
        expr = f"{curr_type}({expr})"
    return f"{root_type}({expr})"


@beartype
def _mojo_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Mojo body stub declarations for a call name.

    1-part names (e.g. ``process``) are handled entirely in the file-
    scope preamble stub; the body stub is empty.  Multi-part names
    (e.g. ``app.client.fetch``) need a ``var`` declaration inside
    ``def main()`` to instantiate the root object.
    """
    if len(parts) == 1:
        return ()
    root = parts[0]
    init_expr = _mojo_init_expr(parts=parts)
    return (f"var {root} = {init_expr}",)


@beartype
def _args_contain_dict(args: Sequence[Value]) -> bool:
    """Return ``True`` if any per-call slot value is a plain dict.

    Ref-marker dicts are stripped before this point, so any ``dict``
    seen here is a real dict-literal argument.
    """
    for element in args:
        per_arg = element if isinstance(element, list) else [element]
        for slot_value in per_arg:
            match slot_value:
                case dict():
                    return True
                case _:
                    continue
    return False


@beartype
def _mojo_call_preamble_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return Mojo file-scope stubs for a call name.

    1-part names become a module-level ``fn``; multi-part names become
    ``@fieldwise_init`` struct types whose innermost type holds the
    method.  Both stub kinds emit typed per-parameter signatures when
    every call's argument values at each slot share a scalar Python
    type that maps to a Mojo scalar, and the generic
    ``[*Ts: AnyType](*args: *Ts)`` form otherwise.
    """
    typed_params = _mojo_typed_param_list(
        params=params,
        arg_values=args,
    )
    if typed_params is None and _args_contain_dict(args=args):
        raise CallArgNotSupportedError(
            language_name="Mojo",
            reason=(
                "Mojo's generic ``[*Ts: AnyType](*args: *Ts)`` stub "
                "cannot infer the type of a dict literal argument; "
                "typed dict-value call stubs are not yet implemented "
                "(see #1966)"
            ),
        )
    if len(parts) == 1:
        if typed_params is not None:
            param_list = ", ".join(typed_params)
            return (f"fn {parts[0]}({param_list}):\n{indent}pass",)
        return (f"fn {parts[0]}[*Ts: AnyType](*args: *Ts):\n{indent}pass",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    struct_header = "(Copyable, Movable)"
    if typed_params is not None:
        method_param_list = ", ".join(("self", *typed_params))
        method_stub = (
            f"{indent}fn {method}({method_param_list}):\n{indent}{indent}pass"
        )
    else:
        method_stub = (
            f"{indent}fn {method}[*Ts: AnyType](self, *args: *Ts):\n"
            f"{indent}{indent}pass"
        )
    if not fields:
        type_name = f"_{root.capitalize()}Type"
        return (
            f"@fieldwise_init\n"
            f"struct {type_name}{struct_header}:\n"
            f"{method_stub}",
        )
    blocks: list[str] = []
    inner_type = f"_{fields[-1].capitalize()}Type"
    blocks.append(
        f"@fieldwise_init\nstruct {inner_type}{struct_header}:\n{method_stub}"
    )
    prev_type = inner_type
    for i in range(len(fields) - 2, -1, -1):
        curr_type = f"_{fields[i].capitalize()}Type"
        field = fields[i + 1]
        blocks.append(
            f"@fieldwise_init\n"
            f"struct {curr_type}{struct_header}:\n"
            f"{indent}var {field}: {prev_type}"
        )
        prev_type = curr_type
    root_type = f"_{root.capitalize()}Type"
    blocks.append(
        f"@fieldwise_init\n"
        f"struct {root_type}{struct_header}:\n"
        f"{indent}var {fields[0]}: {prev_type}"
    )
    return ("\n".join(blocks),)


_mojo_narrowed_empty_form = make_narrowed_empty_form(
    element_to_type=_mojo_element_to_type,
    template="List[{type}]()",
    fallback_type="String",
)


@beartype
def _format_mojo_ordered_map_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format one Mojo ordered-map entry as a ``Tuple(key, value)``."""
    return f"Tuple({key}, {formatted_value})"


_VARIANT_PAYLOAD_VALUE_PLACEHOLDER = "{value}"


@dataclasses.dataclass(frozen=True)
class _VariantSignature:
    """Mojo ``Variant`` alternative for one scalar bucket.

    ``type_name`` is the Mojo type listed in the ``Variant[...]`` alias
    (e.g. ``"Bool"``, ``"Int"``, ``"String"``, ``"NoneType"``).
    ``payload_template`` is the expression rendered between the outer
    ``Value(...)`` parentheses; occurrences of ``{value}`` are replaced
    with the formatted scalar, and a template without the placeholder
    (e.g. ``"NoneType()"``) ignores the formatted scalar entirely.
    """

    type_name: str
    payload_template: str


@beartype
def _mojo_variant_for_scalar(value: Scalar, /) -> _VariantSignature:  # noqa: PLR0911
    """Return the Mojo Variant alternative for *value*.

    Strings, bytes, dates, and datetimes all map to ``String`` because
    the default Mojo date / datetime formats produce ISO strings and
    the bytes formats produce hex or base64 strings.  ``None`` maps to
    ``NoneType`` and renders as ``Value(NoneType())`` because the
    ``Variant`` constructor in Mojo cannot infer ``NoneType`` from the
    bare ``None`` literal.
    """
    _string_signature = _VariantSignature(
        type_name="String",
        payload_template="String({value})",
    )
    match value:
        case bool():
            return _VariantSignature(
                type_name="Bool",
                payload_template=_VARIANT_PAYLOAD_VALUE_PLACEHOLDER,
            )
        case int():
            return _VariantSignature(
                type_name="Int",
                payload_template=_VARIANT_PAYLOAD_VALUE_PLACEHOLDER,
            )
        case float():
            return _VariantSignature(
                type_name="Float64",
                payload_template="Float64({value})",
            )
        case str():
            return _string_signature
        case bytes():
            return _string_signature
        case datetime.datetime():
            return _string_signature
        case datetime.date():
            return _string_signature
        case None:
            return _VariantSignature(
                type_name="NoneType",
                payload_template="NoneType()",
            )
        case _ as unreachable:
            assert_never(unreachable)


@dataclasses.dataclass(frozen=True)
class _HeterogeneousStrategyConfig:
    """Configuration for one Mojo heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Mojo instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the ``Variant`` alias declaration).  Both
    receive the Mojo instance's configurable variant-type name so the
    resulting functions can close over it.
    """

    build_behavior: Callable[[str], HeterogeneousBehavior]
    build_preamble: Callable[[str], Callable[[Value], tuple[str, ...]]]


def _build_error_behavior(_variant_name: str, /) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


def _build_error_preamble(
    _variant_name: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


_VARIANT_IMPORT_LINE = "from std.utils.variant import Variant"


def _build_variant_behavior(
    variant_name: str,
    /,
) -> HeterogeneousBehavior:
    """VARIANT strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should wrap."""
        return collect_heterogeneous_container_ids(data=data)

    def _wrap(raw_value: Value, formatted: str) -> str:
        """Wrap a scalar as ``{variant_name}({payload})`` where the
        payload comes from the signature's ``payload_template`` (with
        ``{value}`` substituted by the formatted scalar).
        """
        signature = _mojo_variant_for_scalar(cast("Scalar", raw_value))
        payload = signature.payload_template.replace(
            _VARIANT_PAYLOAD_VALUE_PLACEHOLDER,
            formatted,
        )
        return f"{variant_name}({payload})"

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
    )


def _build_variant_preamble(
    variant_name: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """VARIANT strategy: emit the ``Variant`` declaration preamble."""

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the ``Variant`` import + ``comptime`` declaration for
        *data*.
        """
        wrap_ids = collect_heterogeneous_container_ids(data=data)
        if not wrap_ids:
            return ()
        scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
        type_names: list[str] = []
        seen: set[str] = set()
        for scalar in scalars:
            signature = _mojo_variant_for_scalar(scalar)
            if signature.type_name in seen:
                continue
            seen.add(signature.type_name)
            type_names.append(signature.type_name)
        joined = ", ".join(type_names)
        return (
            _VARIANT_IMPORT_LINE,
            f"comptime {variant_name} = Variant[{joined}]",
        )

    return _preamble


@beartype
def _mojo_list_open(items: list[Value]) -> str:
    """Return ``[`` after checking for null elements.

    Mojo cannot infer a list type from null-only elements.
    """
    if any(item is None for item in items):
        msg = (
            f"Mojo's list literal cannot contain null elements "
            f"(got {len(items)} items, including null)."
        )
        raise NullInCollectionError(msg)
    return "["


def _mojo_list_format(default_type: str, /) -> SequenceFormatConfig:
    """Build a Mojo LIST ``SequenceFormatConfig`` for the given type."""
    return SequenceFormatConfig(
        sequence_open=_mojo_list_open,
        close="]",
        supports_heterogeneity=False,
        single_element_trailing_comma=False,
        supports_trailing_comma=True,
        empty_sequence=f"List[{default_type}]()",
        preamble_lines=(),
        format_entry=passthrough_sequence_entry,
        typed_opener_fallback=None,
        uses_typed_literal_for_scalars=False,
        requires_uniform_record_shapes=False,
        declared_type=None,
        narrowed_empty_form=None,
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Mojo(metaclass=LanguageCls):
    """Mojo language specification.

    By default Mojo raises on heterogeneous input because its native
    collections require a single element type.  Opt into
    :attr:`HeterogeneousStrategies.VARIANT` to wrap mixed scalars in a
    generated ``comptime Value = Variant[...]`` and render each scalar
    as ``Value(...)`` so heterogeneous dicts and lists become
    homogeneous in the Variant type.
    """

    extension = ".mojo"
    pygments_name = "mojo"
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = True
    supports_commented_dict_call_args = False
    supports_module_name = False
    supports_call_refs_in_dict_literals = False

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Mojo."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Mojo."""

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
        """Sequence type options for Mojo."""

        LIST = enum.member(value=_mojo_list_format)

        def __call__(self, default_type: str) -> SequenceFormatConfig:
            """Create a sequence format config for the given type."""
            return self.value(default_type)

    class SetFormats(enum.Enum):
        """Set type options for Mojo."""

        SET = enum.member(
            value=set_format_factory(
                open_template="Set[{type}](",
                close=")",
                empty_template="Set[{type}]()",
                preamble_lines=("from std.collections import Set",),
                set_opener_template="Set[{type_name}](",
                supports_heterogeneity=True,
                supports_trailing_comma=True,
            )
        )

        def __call__(self, default_type: str) -> SetFormatConfig:
            """Create a set format config for the given type."""
            return self.value(default_type)

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
            ),
            supports_redefinition=True,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.member(
            value=dict_format_factory(
                open_template="{{",
                close="}",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_template="Dict[{key_type}, {type}]()",
                preamble_lines=(),
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
        positive_infinity="std.math.inf[DType.float64]()",
        negative_infinity="-std.math.inf[DType.float64]()",
        nan="std.math.nan[DType.float64]()",
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

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Mojo call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for representing dicts or lists whose scalar values
        span more than one Mojo type.
        """

        ERROR = _HeterogeneousStrategyConfig(
            build_behavior=_build_error_behavior,
            build_preamble=_build_error_preamble,
        )
        """Raise
        :exc:`~literalizer.exceptions.HeterogeneousScalarCollectionError`
        (or :exc:`~literalizer.exceptions.HeterogeneousSiblingListsError`)
        when scalar values of mixed types appear in a container that
        cannot represent them.  This is the default, matching the
        single-element-type convention of the Mojo ``List``, ``Dict``,
        and ``Set`` containers.
        """

        VARIANT = _HeterogeneousStrategyConfig(
            build_behavior=_build_variant_behavior,
            build_preamble=_build_variant_preamble,
        )
        """Auto-generate a ``comptime`` binding in the preamble for the
        configured name to a ``Variant[...]`` over only the Mojo types
        actually present in heterogeneous positions, together with a
        ``from std.utils.variant import Variant`` import, and wrap each
        such scalar as ``{Name}(value)`` (with an explicit ``String(...)``
        or ``Float64(...)`` cast when needed so the constructor resolves
        to the intended Variant alternative, and ``NoneType()`` for
        nulls).

        The alias name is configurable via
        :attr:`Mojo.heterogeneous_value_variant_name` (default
        ``"Value"``).
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for Mojo."""

        V24_5 = enum.auto()

    version_formats = VersionFormats

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

    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Mojo variable declaration in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        if variable_name:
            content = content + f"\n_ = {variable_name}"
        indented = textwrap.indent(text=content, prefix=self.indent)
        return f"def main():\n{indented}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Mojo declaration and assignment in a main function."""
        declaration = prepend_body_preamble(
            content=declaration,
            body_preamble=body_preamble,
        )
        use = f"_ = {variable_name}"
        return self.wrap_in_file(
            content=declaration + f"\n{use}\n" + assignment,
            variable_name=variable_name,
            body_preamble=(),
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "String"
    default_sequence_element_type: str = "String"
    default_dict_key_type: str = "String"
    default_dict_value_type: str = "String"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
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
    heterogeneous_value_variant_name: str = "Value"
    language_version: VersionFormats = VersionFormats.V24_5
    indent: str = "    "

    null_literal: ClassVar[str] = "None"
    true_literal: ClassVar[str] = "True"
    false_literal: ClassVar[str] = "False"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ("import std.math",)
    call_style: CallStyles = CallStyles.POSITIONAL

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return str

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def skip_null_dict_values(self) -> bool:
        """Drop ``None`` dict values for the default ERROR strategy so
        the homogeneous-dict rendering stays valid Mojo.

        ``VARIANT`` wraps every scalar as ``Value(...)``, so ``None``
        values must flow through unchanged to be wrapped as
        ``Value(None)`` against a ``NoneType`` Variant alternative.
        """
        cls = type(self.heterogeneous_strategy)
        return self.heterogeneous_strategy is cls.ERROR

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.VARIANT`` emits an ``alias`` line
        declaring the ``Variant`` over only the Mojo types actually used
        in heterogeneous positions.  Other strategies produce no
        preamble.
        """
        return self.heterogeneous_strategy.value.build_preamble(
            self.heterogeneous_value_variant_name,
        )

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        return self.heterogeneous_strategy.value.build_behavior(
            self.heterogeneous_value_variant_name,
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
        return _mojo_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return partial(_mojo_call_preamble_stub, indent=self.indent)

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Append ``^`` to trigger move/transfer semantics in Mojo.

        Mojo ``Dict`` does not implement ``Copyable``, so a bare
        variable reference fails to compile.  Using ``^`` transfers
        ownership instead of copying.
        """

        def _format_mojo_ref_identifier(name: str, /) -> str:
            """Append ``^`` for the Mojo transfer operator."""
            return f"{name}^"

        return _format_mojo_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Emit a call-argument ``$ref`` as the bare identifier.

        The Mojo transfer operator ``^`` consumes the variable, which
        is unsafe when the caller may use it again in a later call (or
        after the ``literalize_call`` block).  Callers opt in to
        transferring a specific ref by listing it in
        ``literalize_call``'s ``consumable_refs`` set; in that case
        :attr:`format_call_arg_ref_identifier_consumable` is used
        instead and appends ``^``.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
        """Append ``^`` to a consumable call-argument ``$ref``.

        Used only for refs the caller declared as consumable on
        :func:`~literalizer.literalize_call` and that appear in just
        one call argument, so the transfer cannot strand a later use.
        """
        return self.format_call_ref_identifier

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        base = self.sequence_format(
            default_type=self.default_sequence_element_type,
        )
        return dataclasses.replace(
            base,
            narrowed_empty_form=_mojo_narrowed_empty_form,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        base = self.set_format(default_type=self.default_set_element_type)
        return base.with_typed_opener(
            type_to_opener=make_type_to_opener(
                element_to_type=make_element_to_type(
                    str_type="String",
                    bool_type="Bool",
                    int_type="Int",
                    float_type="Float64",
                    mixed_numeric_type="String",
                    bytes_type=None,
                    date_type=None,
                    datetime_type=None,
                    list_template="List[{inner}]",
                    dict_type_template=None,
                    fallback_value_type=None,
                ),
                opener_template="Set[{type_name}](",
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
            ordered_map_open=fixed_open(open_str="["),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return _format_mojo_ordered_map_entry

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Mojo needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Mojo needs none)."""
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
