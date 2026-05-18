"""Gleam language specification."""

import dataclasses
import datetime
import enum
import math
import textwrap
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
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
from literalizer._formatters.format_integers import (
    format_integer_binary,
    format_integer_hex,
    format_integer_octal,
    format_integer_underscore,
)
from literalizer._formatters.format_strings import format_string_backslash
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
    LanguageCls,
    ModifierCombination,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    default_format_call_variable_assignment,
    default_format_call_variable_declaration,
    default_sequence_binding_declarations,
    default_wrap_calls_with_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
    prepend_body_preamble,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import UnrepresentableSpecialFloatError


@beartype
def _gleam_nonneg_only_impl(value: int, base: Callable[[int], str]) -> str:
    """Format an integer, falling back to decimal for negatives."""
    if value < 0:
        return str(object=value)
    return base(value)


@beartype
def _gleam_nonneg_only(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap *base* so negative values fall back to decimal.

    Gleam does not support negative hex/octal/binary literals.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _gleam_nonneg_only_impl(value=value, base=base)

    return _format


@beartype
def _apply_gleam_str_wrapped_date(value: datetime.date, prefix: str) -> str:
    """Format a date as a Gleam string via ISO 8601."""
    return f"{prefix}Str({format_date_iso(value=value)})"


@beartype
def _build_gleam_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_str_wrapped_date(value=value, prefix=prefix)

    return _format


@beartype
def _apply_gleam_str_wrapped_time(value: datetime.time, prefix: str) -> str:
    """Format a time as a Gleam string via ISO 8601."""
    return f"{prefix}Str({format_time_iso(value=value)})"


@beartype
def _build_gleam_time_iso(
    prefix: str,
) -> Callable[[datetime.time], str]:
    """Build a time formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.time) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_str_wrapped_time(value=value, prefix=prefix)

    return _format


@beartype
def _apply_gleam_str_wrapped_datetime(
    value: datetime.datetime, prefix: str
) -> str:
    """Format a datetime as a Gleam string via ISO 8601."""
    return f"{prefix}Str({format_datetime_iso(value=value)})"


@beartype
def _build_gleam_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_str_wrapped_datetime(value=value, prefix=prefix)

    return _format


@beartype
def _build_gleam_datetime_epoch(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Int`` from
    Unix epoch seconds.
    """
    return datetime_epoch_formatter(
        format_integer=_build_gleam_integer_wrapper(prefix=prefix, base=str),
    )


@beartype
def _apply_gleam_bytes_hex(value: bytes, prefix: str) -> str:
    """Format bytes as a Gleam hex string."""
    return f"{prefix}Str({format_bytes_hex(value=value)})"


@beartype
def _build_gleam_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_bytes_hex(value=value, prefix=prefix)

    return _format


@beartype
def _apply_gleam_bytes_base64(value: bytes, prefix: str) -> str:
    """Format bytes as a Gleam base64 string."""
    return f"{prefix}Str({format_bytes_base64(value=value)})"


@beartype
def _build_gleam_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_bytes_base64(value=value, prefix=prefix)

    return _format


@beartype
def _apply_gleam_string(value: str, prefix: str) -> str:
    """Format a string with a constructor prefix."""
    escaped = format_string_backslash(value)
    return f"{prefix}Str({escaped})"


@beartype
def _build_gleam_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_string(value=value, prefix=prefix)

    return _format


@beartype
def _apply_gleam_integer_wrapped(
    value: int, prefix: str, base: Callable[[int], str]
) -> str:
    """Format an integer with a ``{prefix}Int`` constructor."""
    return f"{prefix}Int({base(value)})"


@beartype
def _build_gleam_integer_wrapper(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_integer_wrapped(
            value=value, prefix=prefix, base=base
        )

    return _format


@beartype
def _apply_gleam_float_wrapped(
    value: float, prefix: str, inner: Callable[[float], str]
) -> str:
    """Format a float with a ``{prefix}Float`` constructor."""
    return f"{prefix}Float({inner(value)})"


@beartype
def _build_gleam_float_wrapper(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    def _format(value: float) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_float_wrapped(
            value=value, prefix=prefix, inner=inner
        )

    return _format


@beartype
def _apply_gleam_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
    str_prefix: str,
) -> str:
    """Format a dict entry as a hash tuple with a plain-string key.

    Dict keys are ``String``, not ``GVal``, so the ``{prefix}Str(...)``
    constructor must be stripped from the formatted key.
    """
    key = key.removeprefix(str_prefix).removesuffix(")")
    return f"#({key}, {formatted_value})"


@beartype
def _build_gleam_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str("

    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_gleam_dict_entry(
            key=key,
            _raw_value=_raw_value,
            formatted_value=formatted_value,
            str_prefix=_str_prefix,
        )

    return _format


# Backward-compatible module-level aliases used by the Enum members.
_format_gleam_date_iso = _build_gleam_date_iso(prefix="G")
_format_gleam_datetime_iso = _build_gleam_datetime_iso(prefix="G")
_format_gleam_bytes_hex = _build_gleam_bytes_hex(prefix="G")
_format_gleam_bytes_base64 = _build_gleam_bytes_base64(prefix="G")
_format_gleam_string = _build_gleam_str_formatter(prefix="G")
_format_gleam_integer_decimal = _build_gleam_integer_wrapper(
    prefix="G",
    base=str,
)
_format_gleam_datetime_epoch = _build_gleam_datetime_epoch(prefix="G")
_gleam_integer_wrapper = _build_gleam_integer_wrapper
_gleam_float_wrapper = _build_gleam_float_wrapper
_gleam_dict_entry = _build_gleam_dict_entry(prefix="G")


_GLEAM_INT_BASE: dict[tuple[str, str], Callable[[int], str]] = {
    ("DECIMAL", "NONE"): str,
    ("DECIMAL", "UNDERSCORE"): format_integer_underscore,
    ("HEX", "NONE"): _gleam_nonneg_only(base=format_integer_hex),
    ("HEX", "UNDERSCORE"): _gleam_nonneg_only(base=format_integer_hex),
    ("OCTAL", "NONE"): _gleam_nonneg_only(base=format_integer_octal),
    ("OCTAL", "UNDERSCORE"): _gleam_nonneg_only(base=format_integer_octal),
    ("BINARY", "NONE"): _gleam_nonneg_only(base=format_integer_binary),
    ("BINARY", "UNDERSCORE"): _gleam_nonneg_only(base=format_integer_binary),
}

_GLEAM_FLOAT_BASE: dict[str, Callable[[float], str]] = {
    "REPR": format_float_repr,
    "SCIENTIFIC": format_float_scientific,
    "FIXED": format_float_fixed,
}

_GLEAM_BYTES_FORMATTERS: dict[
    str,
    Callable[[str], Callable[[bytes], str]],
] = {
    "HEX": _build_gleam_bytes_hex,
    "BASE64": _build_gleam_bytes_base64,
}


@beartype
def _gleam_type_var(index: int) -> str:
    """Return a unique lowercase identifier for a type variable.

    Indices ``0``..``25`` map to ``a``..``z``; higher indices append a
    numeric suffix (``a1``..``z1``, ``a2``..``z2``, ...).  The numeric
    suffix avoids collisions with Gleam reserved words like ``as`` and
    ``fn`` that could otherwise appear in a pure-letter scheme.
    """
    letter = chr(ord("a") + index % 26)
    group = index // 26
    if group == 0:
        return letter
    return f"{letter}{group}"


@beartype
def _gleam_call_preamble_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Gleam module-level function stubs for a call target.

    Dotted names are flattened to underscored identifiers — Gleam
    identifiers cannot contain ``.``, so ``app.client.fetch`` becomes
    ``app_client_fetch``.  Each parameter gets a fresh type variable
    so the stub is polymorphic across call sites that pass different
    argument types.  Return type is ``Nil``.
    """
    flat_name = "_".join(parts)
    param_list = ", ".join(
        f"_{p}: {_gleam_type_var(index=i)}"
        for i, p in enumerate(iterable=params)
    )
    return (f"pub fn {flat_name}({param_list}) -> Nil {{ Nil }}",)


@beartype
def _gleam_format_call_target(parts: Sequence[str]) -> str:
    """Flatten a sequence of call target parts to an underscored Gleam
    identifier.
    """
    return "_".join(parts)


@beartype
def _scalar_gleam_type(*, value: Value) -> type:
    """Return the preamble-relevant type bucket for a scalar *value*."""
    match value:
        case datetime.datetime():
            return datetime.datetime
        case datetime.date():
            return datetime.date
        case None:
            return type(None)
        case _:
            return type(value)


@beartype
def _collect_gleam_types(*, value: Value) -> frozenset[type]:
    """Return the set of Python types present in *value*.

    Walks lists, dicts, and sets recursively, collecting the scalar
    types needed to decide which ``GVal`` constructors to emit.
    """
    match value:
        case dict():
            child: frozenset[type] = frozenset()
            for v in value.values():
                child = child | _collect_gleam_types(value=v)
            return frozenset({dict}) | child
        case set():
            child = frozenset()
            for v in value:
                child = child | _collect_gleam_types(value=v)
            return frozenset({set}) | child
        case list():
            child = frozenset()
            for v in value:
                child = child | _collect_gleam_types(value=v)
            return frozenset({list}) | child
        case _:
            return frozenset({_scalar_gleam_type(value=value)})


@beartype
def _build_gleam_data_dependent_preamble(
    *,
    type_name: str,
    constructor_prefix: str,
    datetime_type_produced: type,
) -> Callable[[Value], tuple[str, ...]]:
    """Build a ``data_dependent_preamble`` callable for Gleam.

    The callable walks *data* to collect the scalar types present and
    emits a ``pub type`` declaration containing only the constructors
    that are actually needed.
    """

    def _compute(data: Value, /) -> tuple[str, ...]:
        """Return the ``pub type`` declaration for *data*."""
        types = _collect_gleam_types(value=data)
        p = constructor_prefix
        int_types: set[type] = {int}
        str_types: set[type] = {str, bytes, datetime.date, datetime.time}
        if datetime_type_produced is int:
            int_types.add(datetime.datetime)
        else:
            str_types.add(datetime.datetime)
        constructors = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), f"{p}Null"),
                (frozenset({bool}), f"{p}Bool(Bool)"),
                (frozenset(int_types), f"{p}Int(Int)"),
                (frozenset({float}), f"{p}Float(Float)"),
                (frozenset(str_types), f"{p}Str(String)"),
                (frozenset({list}), f"{p}List(List({type_name}))"),
                (
                    frozenset({dict, OrderedMap}),
                    f"{p}Dict(List(#(String, {type_name})))",
                ),
                (frozenset({set}), f"{p}Set(List({type_name}))"),
            )
            if types & type_set
        ]
        body = "\n".join(f"  {c}" for c in constructors)
        return (f"pub type {type_name} {{\n{body}\n}}",)

    return _compute


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Gleam(metaclass=LanguageCls):
    """Gleam language specification.

    The generated output uses custom constructors (``GNull``, ``GBool``,
    ``GList``, ``GDict``, ``GSet``) that are **not** built-in Gleam types.
    To compile the generated code, a ``GVal`` custom type is emitted in
    the body preamble, containing only the constructors actually used by
    the data.  For example, data consisting solely of an integer yields:

    .. code-block:: gleam

       pub type GVal {
         GInt(Int)
       }

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``GStr("2024-01-15")``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``GStr("2024-01-15T12:30:00")``.

        sequence_format: Which Gleam sequence type to use.

            * ``sequence_formats.LIST`` — list literal,
              e.g. ``GList([GInt(1), GInt(2), GInt(3)])``.
            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``#(GInt(1), GInt(2), GInt(3))``.

        type_name: Name of the generated custom type.  Defaults to
            ``"GVal"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"G"``, producing constructors like ``GNull``,
            ``GBool``, ``GInt``, etc.
    """

    format_integer_widened = no_format_integer_widened
    format_call_variable_declaration = default_format_call_variable_declaration
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".gleam"
    pygments_name = "gleam"
    supports_special_floats = False
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
    call_returns_expression = True
    supports_zero_parameter_calls = True
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

    format_call_arg: ClassVar["staticmethod[[Value, str], str]"] = (
        staticmethod(
            identity_call_arg,
        )
    )
    """Callable that rewrites a formatted direct call argument."""

    class DateFormats(enum.Enum):
        """Date format options for Gleam."""

        ISO = DateFormatConfig(
            formatter=_format_gleam_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Gleam."""

        ISO = DatetimeFormatConfig(
            formatter=_format_gleam_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=_format_gleam_datetime_epoch,
            type_produced=int,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_gleam_bytes_hex)
        BASE64 = enum.member(value=_format_gleam_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Gleam."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="GList(["),
            close="])",
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
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="#("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="#()",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Gleam."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="GSet(["),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        DOUBLE_SLASH = CommentConfig(
            prefix="//",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="let {name} = {value}"
            ),
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
        positive_infinity="GFloat(todo)",
        negative_infinity="GFloat(todo)",
        nan="GFloat(todo)",
    ):
        """Float format options."""

        REPR = enum.member(
            value=_build_gleam_float_wrapper(
                prefix="G",
                inner=format_float_repr,
            )
        )
        SCIENTIFIC = enum.member(
            value=_build_gleam_float_wrapper(
                prefix="G",
                inner=format_float_scientific,
            )
        )
        FIXED = enum.member(
            value=_build_gleam_float_wrapper(
                prefix="G",
                inner=format_float_fixed,
            )
        )

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": _format_gleam_integer_decimal,
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=format_integer_underscore,
                ),
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_hex),
                ),
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_hex),
                ),
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_octal),
                ),
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_octal),
                ),
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_binary),
                ),
                "UNDERSCORE": _build_gleam_integer_wrapper(
                    prefix="G",
                    base=_gleam_nonneg_only(base=format_integer_binary),
                ),
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

        NONE = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Gleam call style options."""

        POSITIONAL = PositionalCallStyle()

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
        """Version options for Gleam."""

        V1 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
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

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Gleam let binding in a main function."""
        content = prepend_body_preamble(
            content=content,
            body_preamble=body_preamble,
        )
        indented = textwrap.indent(text=content, prefix=self.indent)
        use_line = (
            f"\n{self.indent}let _ = {variable_name}" if variable_name else ""
        )
        return f"\npub fn main() {{\n{indented}{use_line}\n}}"

    def wrap_combined_in_file(
        self,
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Gleam declaration + assignment in a main function."""
        return self.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.NEVER
    comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH
    declaration_style: DeclarationStyles = DeclarationStyles.LET
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
        StatementTerminatorStyles.NONE
    )
    call_style: CallStyles = CallStyles.POSITIONAL
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.V1
    indent: str = "  "
    type_name: str = "GVal"
    constructor_prefix: str = "G"

    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for Gleam's call style."""
        return self.call_style.value

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return the ``pub type`` declaration tailored to *data*."""
        return _build_gleam_data_dependent_preamble(
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
            datetime_type_produced=self.datetime_format.value.type_produced,
        )

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
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return file-scope stubs for a call expression."""
        return _gleam_call_preamble_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return _gleam_format_call_target

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
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"{self.constructor_prefix}Bool(True)"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"{self.constructor_prefix}Bool(False)"

    @cached_property
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        return _build_gleam_dict_entry(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        fmt = self.sequence_format.value
        if self.sequence_format.name == "LIST":
            return dataclasses.replace(
                fmt,
                sequence_open=fixed_open(
                    open_str=f"{self.constructor_prefix}List([",
                ),
            )
        return fmt

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format_config.sequence_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set([",
            ),
        )

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_open(
                open_str=f"{self.constructor_prefix}Dict([",
            ),
            close="])",
            format_entry=self._dict_entry,
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
        if self.constructor_prefix == "G":
            return self.bytes_format
        return _GLEAM_BYTES_FORMATTERS[self.bytes_format.name](
            self.constructor_prefix,
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self.constructor_prefix == "G":
            return self.date_format
        return _build_gleam_date_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.datetime_format.name == "EPOCH":
            return _build_gleam_datetime_epoch(prefix=self.constructor_prefix)
        if self.constructor_prefix == "G":
            return self.datetime_format
        return _build_gleam_datetime_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return _build_gleam_time_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        if self.constructor_prefix == "G":
            return _format_gleam_string
        return _build_gleam_str_formatter(prefix=self.constructor_prefix)

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self.constructor_prefix == "G":
            return self.integer_format.get_formatter(
                numeric_separator=self.numeric_separator,
            )
        base = _GLEAM_INT_BASE[
            (self.integer_format.name, self.numeric_separator.name)
        ]
        return _build_gleam_integer_wrapper(
            prefix=self.constructor_prefix,
            base=base,
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal.

        Non-finite values raise :class:`UnrepresentableSpecialFloatError`
        because Gleam's Erlang target has no expression that evaluates
        to a non-finite float.
        """
        finite: Callable[[float], str]
        if self.constructor_prefix == "G":
            finite = self.float_format
        else:
            finite = _build_gleam_float_wrapper(
                prefix=self.constructor_prefix,
                inner=_GLEAM_FLOAT_BASE[self.float_format.name],
            )

        @beartype
        def _format(value: float) -> str:
            """Delegate finite values; raise for inf and nan."""
            if not math.isfinite(value):
                msg = (
                    f"Gleam cannot represent special float {value!r} on "
                    "the Erlang target."
                )
                raise UnrepresentableSpecialFloatError(msg)
            return finite(value)

        return _format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"{self.constructor_prefix}Dict([",
            ),
            close="])",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._dict_entry

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
        return variable_formatter(template="let {name} = {value}")

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Gleam needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Gleam needs none)."""
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
