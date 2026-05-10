"""Nim language specification."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from functools import cached_property, partial
from types import MappingProxyType
from typing import ClassVar, assert_never, cast

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_ymdhms_formatter,
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
from literalizer._formatters.format_strings import format_string_backslash
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
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Scalar, Value
from literalizer.exceptions import IncompatibleFormatsError


@beartype
def _apply_nim_variable_declaration(
    *,
    name: str,
    value: str,
    _data: Value,
    uses_typed_literal_for_scalars: bool,
    keyword: str,
    force_sequence: bool,
    uses_json_wrap: bool,
) -> str:
    """Format a declaration, using ``@`` for flat sequences of
    simple scalars.
    """
    use_sequence = (
        isinstance(_data, list)
        and _data
        and (
            force_sequence
            or (
                uses_typed_literal_for_scalars
                and all(
                    isinstance(item, (str, int, float, bool, bytes))
                    for item in _data
                )
            )
        )
    )
    if use_sequence:
        return f"{keyword} {name} = @{value}"
    if force_sequence or not uses_json_wrap:
        return f"{keyword} {name} = {value}"
    return f"{keyword} {name} = %* {value}"


@beartype
def _make_variable_declaration(
    *,
    uses_typed_literal_for_scalars: bool,
    keyword: str,
    force_sequence: bool,
    uses_json_wrap: bool,
) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
    """Create a Nim variable declaration formatter."""

    def _format(
        name: str,
        value: str,
        _data: Value,
        _modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _apply_nim_variable_declaration(
            name=name,
            value=value,
            _data=_data,
            uses_typed_literal_for_scalars=uses_typed_literal_for_scalars,
            keyword=keyword,
            force_sequence=force_sequence,
            uses_json_wrap=uses_json_wrap,
        )

    return _format


@beartype
def _apply_nim_variable_assignment(
    *,
    name: str,
    value: str,
    _data: Value,
    uses_typed_literal_for_scalars: bool,
    uses_json_wrap: bool,
) -> str:
    """Format an assignment, using ``@`` for flat sequences of
    simple scalars.
    """
    if (
        uses_typed_literal_for_scalars
        and isinstance(_data, list)
        and _data
        and all(
            isinstance(item, (str, int, float, bool, bytes)) for item in _data
        )
    ):
        return f"{name} = @{value}"
    if not uses_json_wrap:
        return f"{name} = {value}"
    return f"{name} = %* {value}"


@beartype
def _make_variable_assignment(
    *,
    uses_typed_literal_for_scalars: bool,
    uses_json_wrap: bool,
) -> Callable[[str, str, Value], str]:
    """Create a Nim variable assignment formatter."""

    def _format(name: str, value: str, _data: Value) -> str:
        """Delegate to module-level implementation."""
        return _apply_nim_variable_assignment(
            name=name,
            value=value,
            _data=_data,
            uses_typed_literal_for_scalars=uses_typed_literal_for_scalars,
            uses_json_wrap=uses_json_wrap,
        )

    return _format


@dataclasses.dataclass(frozen=True)
class _VariantSignature:
    """Name and optional field info for one Nim object variant branch.

    ``field_name`` and ``field_type`` are ``None`` for unit variants
    (e.g. ``vkNull``); for payload-carrying variants they're the field
    identifier and Nim type used inside the ``of`` branch.
    """

    kind_name: str
    field_name: str | None
    field_type: str | None


@beartype
def _nim_variant_for_scalar(  # noqa: PLR0911
    *,
    value: Scalar,
    date_type: str,
    datetime_type: str,
) -> _VariantSignature:
    """Return the Nim object-variant signature for *value*."""
    match value:
        case bool():
            return _VariantSignature(
                kind_name="vkBool",
                field_name="boolVal",
                field_type="bool",
            )
        case int():
            return _VariantSignature(
                kind_name="vkInt",
                field_name="intVal",
                field_type="int",
            )
        case float():
            return _VariantSignature(
                kind_name="vkFloat",
                field_name="floatVal",
                field_type="float",
            )
        case str():
            return _VariantSignature(
                kind_name="vkStr",
                field_name="strVal",
                field_type="string",
            )
        case bytes():
            return _VariantSignature(
                kind_name="vkBytes",
                field_name="bytesVal",
                field_type="string",
            )
        case datetime.datetime():
            return _VariantSignature(
                kind_name="vkDateTime",
                field_name="dateTimeVal",
                field_type=datetime_type,
            )
        case datetime.date():
            return _VariantSignature(
                kind_name="vkDate",
                field_name="dateVal",
                field_type=date_type,
            )
        case None:
            return _VariantSignature(
                kind_name="vkNull",
                field_name=None,
                field_type=None,
            )
        case _ as unreachable:
            assert_never(unreachable)


@dataclasses.dataclass(frozen=True)
class _HeterogeneousStrategyConfig:
    """Configuration for one Nim heterogeneous-values strategy.

    ``build_behavior`` produces the
    :class:`~literalizer._language.HeterogeneousBehavior` exposed on a
    Nim instance.  ``build_preamble`` produces the data-dependent
    preamble callable (e.g. the object-variant type declaration).  Both
    receive the Nim instance's configurable variant-type name and
    scalar type names so the resulting functions can close over them.
    """

    build_behavior: Callable[[str, str, str], HeterogeneousBehavior]
    build_preamble: Callable[
        [str, str, str, str],
        Callable[[Value], tuple[str, ...]],
    ]


def _build_error_behavior(
    _variant_name: str,
    _date_type: str,
    _datetime_type: str,
    /,
) -> HeterogeneousBehavior:
    """ERROR strategy: no wrapping, no skipping of checks."""
    return NO_HETEROGENEOUS_BEHAVIOR


def _build_error_preamble(
    _variant_name: str,
    _date_type: str,
    _datetime_type: str,
    _indent: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """ERROR strategy: no data-dependent preamble."""
    return no_data_preamble


def _needs_json_wrap_for_field(field_type: str | None) -> bool:
    """Return whether *field_type* requires ``%*`` to convert a
    formatted scalar into the variant payload.

    The Nim ``NIM`` date / datetime formats emit a table-literal string
    like ``{"year": ..., ...}`` that only becomes a value when
    ``%*``-converted to a :class:`json.JsonNode`.
    """
    return field_type == "JsonNode"


def _build_object_variant_behavior(
    variant_name: str,
    date_type: str,
    datetime_type: str,
    /,
) -> HeterogeneousBehavior:
    """OBJECT_VARIANT strategy: wrap scalars and skip scalar checks."""

    def _compute(data: Value) -> frozenset[int]:
        """Return container ids whose scalar children should wrap."""
        return collect_heterogeneous_container_ids(data=data)

    def _wrap(raw_value: Value, formatted: str) -> str:
        """Wrap a scalar as ``{variant_name}(kind: ..., ...Val: ...)``."""
        signature = _nim_variant_for_scalar(
            value=cast("Scalar", raw_value),
            date_type=date_type,
            datetime_type=datetime_type,
        )
        if signature.field_name is None:
            return f"{variant_name}(kind: {signature.kind_name})"
        payload = (
            f"%*{formatted}"
            if _needs_json_wrap_for_field(field_type=signature.field_type)
            else formatted
        )
        return (
            f"{variant_name}(kind: {signature.kind_name}, "
            f"{signature.field_name}: {payload})"
        )

    return HeterogeneousBehavior(
        skip_scalar_checks=True,
        compute_wrap_ids=_compute,
        wrap_scalar=_wrap,
    )


def _build_object_variant_preamble(
    variant_name: str,
    date_type: str,
    datetime_type: str,
    indent: str,
    /,
) -> Callable[[Value], tuple[str, ...]]:
    """OBJECT_VARIANT strategy: emit an object-variant ``type`` block."""

    def _preamble(data: Value, /) -> tuple[str, ...]:
        """Build the object-variant type declaration for *data*."""
        wrap_ids = collect_heterogeneous_container_ids(data=data)
        if not wrap_ids:
            return ()
        scalars = iter_wrapped_scalars(data=data, wrap_ids=wrap_ids)
        variants: list[_VariantSignature] = []
        seen: set[str] = set()
        for scalar in scalars:
            signature = _nim_variant_for_scalar(
                value=scalar,
                date_type=date_type,
                datetime_type=datetime_type,
            )
            if signature.kind_name in seen:
                continue
            seen.add(signature.kind_name)
            variants.append(signature)
        half_indent = " " * (len(indent) // 2)
        kind_type = f"{variant_name}Kind"
        lines: list[str] = [
            "type",
            f"{half_indent}{kind_type} = enum",
            f"{indent}{', '.join(v.kind_name for v in variants)}",
            f"{half_indent}{variant_name} = object",
            f"{indent}case kind: {kind_type}",
        ]
        for variant in variants:
            if variant.field_name is None:
                lines.append(f"{indent}of {variant.kind_name}: discard")
            else:
                lines.append(
                    f"{indent}of {variant.kind_name}: "
                    f"{variant.field_name}: {variant.field_type}"
                )
        return tuple(lines)

    return _preamble


@beartype
def _nim_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    stub_return: StubReturn,
    _args: Sequence[Value],
    /,
    *,
    indent: str,
) -> tuple[str, ...]:
    """Return Nim stub declarations for a call name.

    VOID stubs use templates with ``varargs[untyped]``.  VALUE stubs use
    generic ``proc`` definitions with ``{.discardable.}`` because the
    ``{.discardable.}`` pragma is not valid on templates in Nim 2.x, and
    calling a value-returning template at statement level raises a
    compiler error without it.

    For single-part names the stub is emitted at module scope.  For
    dotted names object types are built bottom-up so that the Uniform
    Function Call Syntax of Nim lets the caller write
    ``app.client.fetch(x)`` as sugar for ``fetch(app.client, x)``.
    """
    method = parts[-1]

    if stub_return is StubReturn.VOID:
        if len(parts) == 1:
            return (f"template {method}(args: varargs[untyped]) = discard",)
        chain = list(parts[:-1])
        holder = chain[-1]
        holder_type = f"{holder.title()}Type"
        lines: list[str] = [f"type {holder_type} = object"]
        for i in range(len(chain) - 2, -1, -1):
            outer = chain[i]
            inner = chain[i + 1]
            inner_type = f"{inner.title()}Type"
            outer_type = f"{outer.title()}Type"
            lines.extend(
                [
                    f"type {outer_type} = object",
                    f"{indent}{inner}: {inner_type}",
                ]
            )
        lines.append(
            f"template {method}(self: {holder_type};"
            f" args: varargs[untyped]) = discard"
        )
        root = chain[0]
        root_type = f"{root.title()}Type"
        lines.append(f"var {root}: {root_type}")
        return tuple(lines)

    # VALUE: use a generic proc instead of a template
    type_params = [f"T{i}" for i in range(len(_params))]
    type_clause = f"[{', '.join(type_params)}]" if type_params else ""
    if len(parts) == 1:
        params_str = "; ".join(
            f"{p}: {t}" for p, t in zip(_params, type_params, strict=True)
        )
        return (
            f"proc {method}{type_clause}"
            f"({params_str}): int {{.discardable.}} = 0",
        )
    chain = list(parts[:-1])
    holder = chain[-1]
    holder_type = f"{holder.title()}Type"
    lines = [f"type {holder_type} = object"]
    for i in range(len(chain) - 2, -1, -1):
        outer = chain[i]
        inner = chain[i + 1]
        inner_type = f"{inner.title()}Type"
        outer_type = f"{outer.title()}Type"
        lines.extend(
            [
                f"type {outer_type} = object",
                f"{indent}{inner}: {inner_type}",
            ]
        )
    params_str = "; ".join(
        f"{p}: {t}" for p, t in zip(_params, type_params, strict=True)
    )
    self_and_params = (
        f"self: {holder_type}; {params_str}"
        if params_str
        else f"self: {holder_type}"
    )
    lines.append(
        f"proc {method}{type_clause}"
        f"({self_and_params}): int {{.discardable.}} = 0"
    )
    root = chain[0]
    root_type = f"{root.title()}Type"
    lines.append(f"var {root}: {root_type}")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Nim(metaclass=LanguageCls):
    """Nim language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.NIM`` — table literal,
              e.g. ``{"year": 2024, "month": 1, "day": 15}``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.NIM`` — table literal,
              e.g. ``{"year": 2024, "month": 1, "day": 15,
              "hour": 12, "minute": 30, "second": 0}``.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.
    """

    extension = ".nim"
    pygments_name = "nim"
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
    supports_commented_dict_call_args = True
    supports_module_name = False
    supports_call_refs_in_dict_literals = True

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Nim."""

        NIM = DateFormatConfig(
            formatter=date_ymd_formatter(
                template='{{"year": {year}, "month": {month}, "day": {day}}}',
            ),
            preamble_lines=(),
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso,
            preamble_lines=(),
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Nim."""

        NIM = DatetimeFormatConfig(
            formatter=datetime_ymdhms_formatter(
                template='{{"year": {year}, "month": {month}, '
                '"day": {day}, "hour": {hour}, '
                '"minute": {minute}, "second": {second}}}',
            ),
            preamble_lines=(),
        )
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=(),
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
        """Sequence type options for Nim."""

        SEQ = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=True,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
        ARRAY = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
            close="]",
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
        """Set type options for Nim."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )
        BLOCK = CommentConfig(
            prefix="#[",
            suffix=" ]#",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        VAR = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="var {name} = {value}"
            ),
            supports_redefinition=True,
        )
        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value}"
            ),
            supports_redefinition=False,
        )
        CONST = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="const {name} = {value}"
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
        """Empty dict key options."""

        ALLOW = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Inf",
        negative_infinity="-Inf",
        nan="NaN",
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
        """Nim call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Strategy for representing dicts or lists whose scalar values
        span more than one Nim type.
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
        cannot represent them.  This is the default, matching the
        strict-typing convention of Nim when tables and sequences are
        used without JSON wrapping.
        """

        OBJECT_VARIANT = _HeterogeneousStrategyConfig(
            build_behavior=_build_object_variant_behavior,
            build_preamble=_build_object_variant_preamble,
        )
        """Auto-generate a Nim object variant in the preamble containing
        only the branches actually present in the data, and wrap each
        heterogeneous scalar value as
        ``{VariantName}(kind: vkX, xVal: value)``.

        Switches the dict rendering from ``%* {key: value}`` (which
        relies on the ``json`` module) to ``{key: value}.toTable`` so
        that the object-variant values can be stored directly.  Nested
        sequences emit ``@[...]`` at every level, and the ``json``
        import is dropped unless a date or datetime format still
        produces a ``JsonNode`` payload.

        The variant-type name is configurable via
        :attr:`Nim.heterogeneous_value_variant_name` (default
        ``"Value"``).  Incompatible with ``DeclarationStyles.CONST``:
        ``.toTable`` and ``@[]`` are runtime constructors, so
        ``CONST`` requires a compile-time-expressible initializer.
        """

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for Nim."""

        V2 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
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

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap code in a valid file (no-op)."""
        return wrap_in_file_noop(
            content=content,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap declaration and assignment in a valid file (no-op)."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.NIM
    datetime_format: DatetimeFormats = DatetimeFormats.NIM
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.SEQ
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.VAR
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
    heterogeneous_value_variant_name: str = "Value"
    call_style: CallStyles = CallStyles.POSITIONAL
    language_version: VersionFormats = VersionFormats.V2
    indent: str = "    "

    def __post_init__(self) -> None:
        """Validate that incompatible formats are not combined.

        ``OBJECT_VARIANT`` replaces the JSON-based rendering for Nim
        with runtime ``.toTable`` / ``@[]`` constructors, so ``CONST``
        (which requires a compile-time-expressible initializer)
        cannot be combined with it.
        """
        _decl_cls = type(self.declaration_style)
        _strategy_cls = type(self.heterogeneous_strategy)
        if (
            self.declaration_style is _decl_cls.CONST
            and self.heterogeneous_strategy is _strategy_cls.OBJECT_VARIANT
        ):
            msg = (
                "Nim CONST requires a constant-expression initializer, "
                "but OBJECT_VARIANT produces runtime .toTable / @[] "
                "calls which are not constant expressions. "
                "Use VAR or LET instead."
            )
            raise IncompatibleFormatsError(msg)

    null_literal: ClassVar[str] = "nil"
    true_literal: ClassVar[str] = "true"
    false_literal: ClassVar[str] = "false"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        return self.call_style.value

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return format_string_backslash

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def _heterogeneous_variant_date_type(self) -> str:
        """Nim type used for :class:`datetime.date` variant payloads."""
        return (
            "string"
            if self.date_format.value.type_produced is str
            else "JsonNode"
        )

    @cached_property
    def _heterogeneous_variant_datetime_type(self) -> str:
        """Nim type used for :class:`datetime.datetime` variant
        payloads.
        """
        produced = self.datetime_format.value.type_produced
        if produced is str:
            return "string"
        if produced is int:
            return "int"
        return "JsonNode"

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines.

        For ``HeterogeneousStrategies.OBJECT_VARIANT`` emits a Nim
        ``type`` block declaring the object variant used to wrap
        heterogeneous scalars.  For ``HeterogeneousStrategies.ERROR``
        emits ``("import json",)`` when the rendered output will use
        the ``%*`` JSON-construction operator (every variable
        declaration / assignment except ``const`` declarations and
        ``@``-prefixed sequences of simple scalars); importing
        ``json`` unconditionally would trigger the Nim compiler's
        ``UnusedImport`` warning.
        """
        strategy_preamble = self.heterogeneous_strategy.value.build_preamble(
            self.heterogeneous_value_variant_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
            self.indent,
        )
        if self._uses_object_variant:
            return strategy_preamble
        is_const = self.declaration_style is self.declaration_styles.CONST
        uses_typed_literal = (
            self.sequence_format.value.uses_typed_literal_for_scalars
        )

        def _preamble(data: Value, /) -> tuple[str, ...]:
            """Decide whether ``import json`` is required for *data*."""
            if is_const:
                return ()
            renders_as_at_sequence = (
                isinstance(data, list)
                and bool(data)
                and uses_typed_literal
                and all(
                    isinstance(item, (str, int, float, bool, bytes))
                    for item in data
                )
            )
            if renders_as_at_sequence:
                return ()
            return ("import json",)

        return _preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the behavior for the chosen heterogeneous strategy."""
        return self.heterogeneous_strategy.value.build_behavior(
            self.heterogeneous_value_variant_name,
            self._heterogeneous_variant_date_type,
            self._heterogeneous_variant_datetime_type,
        )

    @cached_property
    def _uses_object_variant(self) -> bool:
        """Whether the instance is configured for the OBJECT_VARIANT
        heterogeneous strategy.
        """
        cls = type(self.heterogeneous_strategy)
        return self.heterogeneous_strategy is cls.OBJECT_VARIANT

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
        return partial(_nim_call_stub, indent=self.indent)

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
    def call_data_dependent_preamble(
        self,
    ) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines for a call context.

        For ``HeterogeneousStrategies.OBJECT_VARIANT`` emits the Nim
        ``type`` block declaring the object variant used to wrap
        heterogeneous scalars; the call rendering references that type
        by name, so the declaration must be present.  For other
        strategies, call arguments are inline literals that never use
        ``%*``, so ``import json`` is never needed in a call context.
        """
        if self._uses_object_variant:
            strategy_preamble = (
                self.heterogeneous_strategy.value.build_preamble(
                    self.heterogeneous_value_variant_name,
                    self._heterogeneous_variant_date_type,
                    self._heterogeneous_variant_datetime_type,
                    self.indent,
                )
            )

            def _preamble(data: Value, /) -> tuple[str, ...]:
                """Suppress UnusedImport for ``tables`` and emit the
                object-variant type block.

                The ``import tables`` line is contributed by
                :attr:`dict_format_config` so that ``{...}.toTable``
                renders correctly, but the call stub uses
                ``varargs[untyped]`` and never evaluates its arguments,
                so the Nim compiler treats the import as unused.
                """
                return (
                    "{.warning[UnusedImport]:off.}",
                    *strategy_preamble(data),
                )

            return _preamble
        return no_data_preamble

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
        """Configuration for the chosen sequence format.

        ``OBJECT_VARIANT`` replaces the JSON-array opener with
        ``@[`` so nested sequences render as Nim-native ``seq``
        literals at every level (the declaration formatter no longer
        adds a leading ``@`` because ``uses_typed_literal_for_scalars``
        is turned off).
        """
        base = self.sequence_format.value
        if not self._uses_object_variant:
            return base
        return dataclasses.replace(
            base,
            sequence_open=fixed_open(open_str="@["),
            uses_typed_literal_for_scalars=False,
            preamble_lines=(),
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        ``OBJECT_VARIANT`` appends ``.toTable`` to the closing brace so
        every rendered dict becomes a runtime :class:`tables.Table`,
        and imports the ``tables`` module instead of ``json``.
        """
        if self._uses_object_variant:
            return DictFormatConfig(
                dict_open=fixed_open(open_str="{"),
                close="}.toTable",
                format_entry=dict_entry_with_separator(
                    separator=": ",
                    format_value=passthrough_sequence_entry,
                ),
                empty_dict=None,
                preamble_lines=("import tables",),
                narrowed_open=None,
                supports_trailing_comma=True,
            )
        return DictFormatConfig(
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
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
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return make_overflow_fallback_formatter(
            base=self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            ),
            fallback=raise_for_unrepresentable_int(language_name="Nim"),
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._uses_object_variant:
            return OrderedMapFormatConfig(
                ordered_map_open=fixed_open(open_str="{"),
                close="}.toOrderedTable",
                preamble_lines=("import tables",),
            )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return dict_entry_with_separator(
            separator=": ",
            format_value=passthrough_sequence_entry,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        is_const = self.declaration_style is self.declaration_styles.CONST
        return _make_variable_declaration(
            uses_typed_literal_for_scalars=(
                self.sequence_format_config.uses_typed_literal_for_scalars
            ),
            keyword=self.declaration_style.name.lower(),
            force_sequence=is_const,
            uses_json_wrap=not self._uses_object_variant,
        )

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return _make_variable_assignment(
            uses_typed_literal_for_scalars=(
                self.sequence_format_config.uses_typed_literal_for_scalars
            ),
            uses_json_wrap=not self._uses_object_variant,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble for Nim scalar types.

        Under the default ``ERROR`` heterogeneous strategy
        ``import json`` is added by :attr:`data_dependent_preamble`
        only when the rendered output uses ``%*``.  Under
        ``OBJECT_VARIANT`` scalars are emitted as native Nim values,
        except that the ``NIM`` date / datetime formats still
        produce a :class:`json.JsonNode` payload and require
        ``import json`` whenever a date or datetime is present.
        """
        if self._uses_object_variant:
            json_import = ("import json",)
            date_preamble = (
                ()
                if self.date_format.value.type_produced is str
                else json_import
            )
            datetime_preamble = (
                ()
                if self.datetime_format.value.type_produced in {str, int}
                else json_import
            )
            return {
                datetime.date: date_preamble,
                datetime.datetime: datetime_preamble,
            }
        return {
            datetime.date: self.date_format.value.preamble_lines,
            datetime.datetime: self.datetime_format.value.preamble_lines,
        }

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Nim needs none)."""
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
