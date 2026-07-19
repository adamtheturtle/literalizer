"""PureScript language specification."""

import dataclasses
import datetime
import enum
import math
from collections.abc import Callable, Sequence
from functools import cached_property
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
    dict_entry_with_template,
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
    I64_MAX,
    I64_MIN,
    format_integer_hex,
)
from literalizer._formatters.format_json_value import format_json_value_text
from literalizer._formatters.format_strings import (
    format_string_backslash_control,
)
from literalizer._language import (
    NO_CALL_PARAMETER_LIMIT,
    NO_HETEROGENEOUS_BEHAVIOR,
    NON_KEBAB_REF_CASES,
    BareIntegerWidthStrategies,
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
    NestedMapWideningVariant,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    VariantMetadata,
    default_format_call_variable_assignment,
    default_sequence_binding_declarations,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_beyond_i64,
    no_format_integer_widened,
    no_leading_preamble,
    no_pygments_name,
    no_type_hint_preamble,
    no_validate_call_arg,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    UnrepresentableInputError,
    UnrepresentableIntegerError,
    UnrepresentableSpecialFloatError,
    WrapCombinedInFileNotSupportedError,
)


@beartype
def _apply_purescript_date_iso(value: datetime.date, prefix: str) -> str:
    """Format a date as a PureScript string via ISO 8601."""
    return f"{prefix}Str {format_date_iso(value=value)}"


@beartype
def _build_purescript_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_date_iso(value=value, prefix=prefix)

    return _format


@beartype
def _apply_purescript_time_iso(value: datetime.time, prefix: str) -> str:
    """Format a time as a PureScript string via ISO 8601."""
    return f"{prefix}Str {format_time_iso(value=value)}"


@beartype
def _build_purescript_time_iso(
    prefix: str,
) -> Callable[[datetime.time], str]:
    """Build a time formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.time) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_time_iso(value=value, prefix=prefix)

    return _format


@beartype
def _apply_purescript_datetime_iso(
    value: datetime.datetime, prefix: str
) -> str:
    """Format a datetime as a PureScript string via ISO 8601."""
    return f"{prefix}Str {format_datetime_iso(value=value)}"


@beartype
def _build_purescript_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_datetime_iso(value=value, prefix=prefix)

    return _format


@beartype
def _build_purescript_datetime_epoch(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Int`` from
    Unix epoch seconds.
    """
    return datetime_epoch_formatter(
        format_integer=_build_purescript_integer_formatter(
            prefix=prefix,
            base=str,
        ),
    )


@beartype
def _apply_purescript_bytes_hex(value: bytes, prefix: str) -> str:
    """Format bytes as a PureScript hex string."""
    return f"{prefix}Str {format_bytes_hex(value=value)}"


@beartype
def _build_purescript_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_bytes_hex(value=value, prefix=prefix)

    return _format


@beartype
def _apply_purescript_bytes_base64(value: bytes, prefix: str) -> str:
    """Format bytes as a PureScript base64 string."""
    return f"{prefix}Str {format_bytes_base64(value=value)}"


@beartype
def _build_purescript_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_bytes_base64(value=value, prefix=prefix)

    return _format


_PURESCRIPT_INT32_MIN = -(2**31)
_PURESCRIPT_INT32_MAX = 2**31 - 1


@beartype
def _purescript_int_fits_in_int32(value: int) -> bool:
    """Return whether *value* fits in the 32-bit ``Int`` type."""
    return _PURESCRIPT_INT32_MIN <= value <= _PURESCRIPT_INT32_MAX


@beartype
def _purescript_has_large_int(val: Value) -> bool:
    """Return True if *val* contains an integer that overflows
    PureScript's 32-bit ``Int``.
    """
    match val:
        case bool():
            return False
        case int():
            return not _purescript_int_fits_in_int32(value=val)
        case list():
            return any(_purescript_has_large_int(val=v) for v in val)
        case dict():
            return any(_purescript_has_large_int(val=v) for v in val.values())
        case set():
            return any(
                _purescript_has_large_int(val=v)
                for v in val
                if isinstance(v, int) and not isinstance(v, bool)
            )
        case _:
            return False


@beartype
def _apply_purescript_integer_formatter(
    value: int, prefix: str, base: Callable[[int], str]
) -> str:
    """Format an integer with a constructor prefix."""
    if _purescript_int_fits_in_int32(value=value):
        formatted = base(value)
        if value < 0:
            return f"{prefix}Int ({formatted})"
        return f"{prefix}Int {formatted}"
    if not I64_MIN <= value <= I64_MAX:
        msg = (
            f"PureScript cannot represent integer {value} without "
            "external arbitrary-precision integer support."
        )
        raise UnrepresentableIntegerError(msg)
    if value < 0:
        return f"{prefix}Long (-{abs(value)}.0)"
    return f"{prefix}Long {value}.0"


@beartype
def _build_purescript_integer_formatter(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors, or ``{prefix}Long`` (with a ``Number`` argument) when
    *value* overflows PureScript's 32-bit ``Int``.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_integer_formatter(
            value=value, prefix=prefix, base=base
        )

    return _format


@beartype
def _apply_purescript_float_wrapper(
    value: float, prefix: str, inner: Callable[[float], str]
) -> str:
    """Format a float with a constructor prefix."""
    formatted = inner(value)
    if formatted.startswith("-"):
        return f"{prefix}Float ({formatted})"
    return f"{prefix}Float {formatted}"


@beartype
def _build_purescript_float_wrapper(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    def _format(value: float) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_float_wrapper(
            value=value, prefix=prefix, inner=inner
        )

    return _format


@beartype
def _apply_purescript_string(value: str, prefix: str) -> str:
    """Format a string with a constructor prefix."""
    escaped = format_string_backslash_control(
        value=value,
        control_char_fmt="\\x{:02x}",
    )
    return f"{prefix}Str {escaped}"


@beartype
def _build_purescript_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_string(value=value, prefix=prefix)

    return _format


@beartype
def _apply_purescript_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
    str_prefix: str,
) -> str:
    """Format a dict entry as a ``Tuple`` with a plain-string key.

    Dict keys are ``String``, not ``Val``, so the ``{prefix}Str``
    constructor must be stripped from the formatted key.
    """
    key = key.removeprefix(str_prefix)
    return f"(Tuple {key} ({formatted_value}))"


@beartype
def _build_purescript_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str "

    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_purescript_dict_entry(
            key=key,
            _raw_value=_raw_value,
            formatted_value=formatted_value,
            str_prefix=_str_prefix,
        )

    return _format


# Backward-compatible module-level aliases used by the Enum members.
_format_purescript_date_iso = _build_purescript_date_iso(prefix="P")
_format_purescript_datetime_iso = _build_purescript_datetime_iso(prefix="P")
_format_purescript_bytes_hex = _build_purescript_bytes_hex(prefix="P")
_format_purescript_bytes_base64 = _build_purescript_bytes_base64(prefix="P")
_format_purescript_integer_decimal = _build_purescript_integer_formatter(
    prefix="P",
    base=str,
)
_format_purescript_datetime_epoch = _build_purescript_datetime_epoch(
    prefix="P",
)
_format_purescript_integer_hex = _build_purescript_integer_formatter(
    prefix="P",
    base=format_integer_hex,
)
_format_purescript_float_repr = _build_purescript_float_wrapper(
    prefix="P",
    inner=format_float_repr,
)
_format_purescript_float_scientific = _build_purescript_float_wrapper(
    prefix="P",
    inner=format_float_scientific,
)
_format_purescript_float_fixed = _build_purescript_float_wrapper(
    prefix="P",
    inner=format_float_fixed,
)
_format_purescript_string = _build_purescript_str_formatter(prefix="P")
_purescript_dict_entry = _build_purescript_dict_entry(prefix="P")


@beartype
def _purescript_negative_float(val: float) -> bool:
    """Return True if *val* is a float requiring ``import Prelude``."""
    return math.copysign(1, val) < 0 or math.isinf(val) or math.isnan(val)


@beartype
def _purescript_needs_prelude(val: Value) -> bool:
    """Return True if *val* needs ``import Prelude``.

    Prelude is required for ``negate`` (any negative int or float)
    and for ``/`` (infinity / NaN expressed as ``1.0 / 0.0``).
    """
    # Check bool before int (bool is a subclass of int).
    match val:
        case bool():
            result = False
        case float():
            result = _purescript_negative_float(val=val)
        case int():
            result = val < 0
        case list():
            result = any(_purescript_needs_prelude(val=v) for v in val)
        case dict():
            result = any(
                _purescript_needs_prelude(val=v) for v in val.values()
            )
        case set():
            result = any(
                _purescript_needs_prelude(val=v)
                for v in val
                if isinstance(v, (int, float)) and not isinstance(v, bool)
            )
        case _:
            result = False
    return result


@beartype
def _build_purescript_body_preamble(
    *,
    type_name: str,
    constructor_prefix: str,
    datetime_type_produced: type,
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for PureScript.

    The callable receives the set of types present in the data and returns
    the type declaration with only the constructors that are actually
    needed, plus any necessary imports.
    """

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return body-preamble lines for the given *types*."""
        p = constructor_prefix
        needs_tuple = bool(types & {dict, OrderedMap})
        has_large_int = int in types and _purescript_has_large_int(val=data)
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
                (frozenset({bool}), f"{p}Bool Boolean"),
                (frozenset(int_types), f"{p}Int Int"),
                (frozenset({float}), f"{p}Float Number"),
                (frozenset(str_types), f"{p}Str String"),
                (frozenset({list}), f"{p}List (Array {type_name})"),
                (
                    frozenset({dict, OrderedMap}),
                    f"{p}Dict (Array (Tuple String {type_name}))",
                ),
                (frozenset({set}), f"{p}Set (Array {type_name})"),
            )
            if types & type_set
        ]
        if has_large_int:
            int_idx = next(
                i
                for i, c in enumerate(iterable=constructors)
                if c == f"{p}Int Int"
            )
            constructors.insert(int_idx + 1, f"{p}Long Number")
        needs_prelude = bool(
            types & {int, float}
        ) and _purescript_needs_prelude(val=data)
        lines: list[str] = ["import Prelude"] if needs_prelude else []
        if needs_tuple:
            lines.append("data Tuple a b = Tuple a b")
        first_line = f"data {type_name}\n    = {constructors[0]}"
        rest_lines = [f"    | {c}" for c in constructors[1:]]
        lines.append("\n".join([first_line, *rest_lines]))
        return tuple(lines)

    return _compute


@beartype
def _build_purescript_call_stub_lines(
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    type_name: str,
) -> tuple[str, ...]:
    """Return PureScript stub declarations for a call name.

    All stubs return ``Unit`` regardless of *stub_return*.
    """
    del stub_return

    if len(parts) == 1:
        name = parts[0]
        sig = " -> ".join([*[type_name] * len(params), "Unit"])
        lhs = " ".join([name, *["_"] * len(params)])
        return (f"{name} :: {sig}", f"{lhs} = unit")

    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]

    if not params:
        func_type = "Unit"
        func_body = "unit"
    else:
        arg_types = " -> ".join(type_name for _ in params)
        func_type = f"{arg_types} -> Unit"
        wildcards = " ".join("_" for _ in params)
        func_body = f"\\{wildcards} -> unit"

    inner_type = f"{{ {method} :: {func_type} }}"
    inner_val = f"{{ {method}: {func_body} }}"
    for field in reversed(fields):
        inner_type = f"{{ {field} :: {inner_type} }}"
        inner_val = f"{{ {field}: {inner_val} }}"

    return (f"{root} :: {inner_type}", f"{root} = {inner_val}")


@beartype
def _build_purescript_call_stub(
    type_name: str,
) -> Callable[
    [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
    tuple[str, ...],
]:
    """Build a call stub factory that uses *type_name* for parameter types."""

    @beartype
    def _purescript_call_stub(
        parts: Sequence[str],
        params: Sequence[str],
        stub_return: StubReturn,
        _args: Sequence[Value],
        /,
    ) -> tuple[str, ...]:
        """Delegate to module-level implementation."""
        return _build_purescript_call_stub_lines(
            parts=parts,
            params=params,
            stub_return=stub_return,
            type_name=type_name,
        )

    return _purescript_call_stub


@beartype
def _purescript_format_call_arg(_original: Value, formatted: str, /) -> str:
    """Wrap a formatted PureScript value in parentheses for curried
    application.
    """
    return f"({formatted})"


@beartype
def _indent_purescript_let_calls(calls: str, indent: str) -> str:
    """Indent call expressions for a PureScript ``let`` block.

    *calls* is one single-line call expression per line: this is the
    only shape produced by ``literalize_call`` for PureScript, which
    uses :attr:`CollectionLayout.COMPACT` for wrapped calls and rejects
    standalone comments in that path.  Each line receives two levels of
    *indent* plus ``_ = ``.
    """
    binding_prefix = indent * 2 + "_ = "
    return "\n".join(binding_prefix + line for line in calls.split(sep="\n"))


@beartype
def _hoist_purescript_imports(preamble: str) -> str:
    """Move every ``import ...`` line to the top of *preamble* and
    drop duplicates.

    PureScript rejects ``import`` declarations that appear after any
    other declaration.  Call-binding and ``json_type`` preambles can
    interleave imports with stub declarations (or repeat
    ``import Prelude`` in both halves of a composed preamble); this
    helper restores a single block of imports at the top while
    preserving the relative order of non-import lines.
    """
    lines = preamble.split(sep="\n")
    # ``dict.fromkeys`` drops repeats while preserving first-seen order;
    # using ``list(dict.fromkeys(...))`` keeps the helper branch-free so
    # coverage does not depend on a fixture that happens to assemble two
    # of the same import line.
    imports = list(
        dict.fromkeys(line for line in lines if line.startswith("import ")),
    )
    if not imports:
        return preamble
    other = [line for line in lines if not line.startswith("import ")]
    return "\n".join([*imports, *other])


@beartype
def _build_purescript_call_output(
    preamble: str,
    decl_part: str,
    calls: str,
    indent: str,
) -> str:
    """Build a complete PureScript module string for call mode.

    Ensures ``import Prelude`` is present (needed for ``Unit`` and
    ``unit``), hoists every ``import`` line above the declarations in
    *decl_part*, and wraps the call expressions in a ``let … in unit``
    block.  *decl_part* is an optional newline-prefixed block of
    module-scope declarations to insert before ``main``.
    """
    if "import Prelude" not in preamble:
        preamble = (
            "import Prelude\n" + preamble if preamble else "import Prelude"
        )
    preamble = _hoist_purescript_imports(preamble=preamble)
    return (
        "module Check where\n\n\n"
        + preamble
        + decl_part
        + "\n\n\nmain :: Unit\nmain =\n"
        + indent
        + "let\n"
        + _indent_purescript_let_calls(calls=calls, indent=indent)
        + "\n"
        + indent
        + "in\n"
        + indent
        + "unit"
    )


_INT_BASE: dict[str, Callable[[int], str]] = {
    "DECIMAL": str,
    "HEX": format_integer_hex,
}

_FLOAT_BASE: dict[str, Callable[[float], str]] = {
    "REPR": format_float_repr,
    "SCIENTIFIC": format_float_scientific,
    "FIXED": format_float_fixed,
}

_BYTES_FORMATTERS: dict[
    str,
    Callable[[str], Callable[[bytes], str]],
] = {
    "HEX": _build_purescript_bytes_hex,
    "BASE64": _build_purescript_bytes_base64,
}


# Imports emitted under ``json_type=ARGONAUT_JSON``.  The data flows
# through a single ``jsonParser`` call, so the generated module only
# needs Argonaut's ``Json`` type, the parser entry point, and
# ``Data.Either.fromRight`` for the (statically unreachable) failure arm.
_ARGONAUT_JSON_BODY_PREAMBLE: tuple[str, ...] = (
    "import Data.Argonaut.Core (Json, jsonNull)",
    "import Data.Argonaut.Parser (jsonParser)",
    "import Data.Either (fromRight)",
)


# Sequence/dict/set/ordered-map format definitions used while ``json_type`` is
# active.  The framework still walks the data to produce a formatted
# value, but that string is discarded by
# :func:`_format_purescript_json_declaration` and friends in favor of a
# fresh :func:`format_json_value_text` of the raw data.  These
# format definitions only need to be permissive enough that the format
# pass does not error on heterogeneous data or nulls inside containers.
_ARGONAUT_JSON_SEQUENCE_CONFIG = SequenceFormatConfig(
    sequence_open=fixed_open(open_str="["),
    close="]",
    supports_heterogeneity=True,
    single_element_trailing_comma=False,
    supports_trailing_comma=True,
    empty_sequence="[]",
    preamble_lines=(),
    format_entry=passthrough_sequence_entry,
    typed_opener_fallback=None,
    uses_typed_literal_for_scalars=False,
    requires_uniform_record_shapes=False,
    declared_type=None,
    narrowed_empty_form=None,
)

_ARGONAUT_JSON_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="["),
    close="]",
    empty_set="[]",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=True,
)

_ARGONAUT_JSON_DICT_CONFIG = DictFormatConfig(
    dict_open=fixed_open(open_str="{"),
    close="}",
    format_entry=dict_entry_with_template(
        template="{key}: {value}",
        format_value=passthrough_sequence_entry,
    ),
    empty_dict="{}",
    preamble_lines=(),
    narrowed_open=None,
    supports_trailing_comma=True,
    narrowed_empty_form=None,
)

_ARGONAUT_JSON_ORDERED_MAP_CONFIG = OrderedMapFormatConfig(
    ordered_map_open=fixed_open(open_str="{"),
    close="}",
    preamble_lines=(),
)


@beartype
def _argonaut_value_body_preamble(
    _types: frozenset[type], _data: Value, /
) -> tuple[str, ...]:
    """Return the ``Data.Argonaut.Core`` import preamble lines."""
    return _ARGONAUT_JSON_BODY_PREAMBLE


@beartype
def _argonaut_parse_expression(data: Value) -> str:
    """Render a ``fromRight jsonNull (jsonParser "...")`` expression.

    ``jsonParser`` returns ``Either String Json``.  The literalizer
    always emits a JSON document produced by :func:`json.dumps`, so the
    ``Left`` branch is statically unreachable; ``fromRight jsonNull`` is
    used instead of a partial ``fromRight'`` to keep the generated
    module free of ``unsafePartial``.
    """
    json_text = format_json_value_text(data=data)
    purescript_literal = format_string_backslash_control(
        value=json_text,
        control_char_fmt="\\x{:06x}",
    )
    return f"fromRight jsonNull (jsonParser {purescript_literal})"


@beartype
def _format_purescript_json_declaration(
    name: str,
    _value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a ``Json`` declaration backed by ``jsonParser``."""
    expression = _argonaut_parse_expression(data=data)
    return f"{name} :: Json\n{name} = {expression}"


@beartype
def _format_purescript_json_assignment(
    name: str,
    _value: str,
    data: Value,
) -> str:
    """Format a ``Json`` assignment backed by ``jsonParser``.

    PureScript top-level bindings are immutable, so an
    ``ExistingVariable`` assignment at module scope is just another
    binding.  Emit it with the same ``name :: Json`` signature as the
    declaration form so the rendered file keeps the ``Json`` import
    live and matches the declaration's shape.
    """
    expression = _argonaut_parse_expression(data=data)
    return f"{name} :: Json\n{name} = {expression}"


@beartype
def _format_purescript_json_call_arg(raw_value: Value, _formatted: str) -> str:
    """Format a direct call argument as a ``Json`` parse expression.

    PureScript curried calls parenthesize each argument so the inner
    ``fromRight ...`` application is not parsed as additional arguments
    to the outer call.
    """
    return f"({_argonaut_parse_expression(data=raw_value)})"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class PureScript(metaclass=LanguageCls):
    """PureScript language specification.

    The generated output uses custom constructors (``PNull``, ``PBool``,
    ``PList``, ``PDict``, ``PSet``) that are **not** built-in PureScript
    types. To compile the generated code, define a ``Val`` ADT in the
    consuming module:

    .. code-block:: haskell

       import Prelude

       data Tuple a b = Tuple a b

       data Val
           = PNull
           | PBool Boolean
           | PInt Int
           | PFloat Number
           | PStr String
           | PList (Array Val)
           | PDict (Array (Tuple String Val))
           | PSet (Array Val)

    The body preamble automatically emits only the constructors that are
    actually used by the data.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``PStr "2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``PStr "2024-01-15T12:30:00"``.

        type_name: Name of the generated custom type.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"P"``, producing constructors like ``PNull``,
            ``PBool``, ``PInt``, etc.
    """

    format_integer_widened = no_format_integer_widened
    format_integer_beyond_i64 = no_format_integer_beyond_i64
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".purs"
    pygments_name: ClassVar[str | None] = no_pygments_name
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    reserved_variable_identifiers_case_sensitive: bool = True
    reserved_variable_identifiers: frozenset[str] = frozenset(
        {
            "ado",
            "as",
            "case",
            "class",
            "data",
            "derive",
            "do",
            "else",
            "false",
            "forall",
            "foreign",
            "if",
            "import",
            "in",
            "infix",
            "infixl",
            "infixr",
            "instance",
            "let",
            "module",
            "newtype",
            "of",
            "then",
            "type",
            "where",
        }
    )
    allows_empty_call_parens = True
    supports_dotted_call_stub = True
    call_returns_expression = True
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = False
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
    non_default_kwargs: ClassVar[dict[str, str]] = {
        "type_name": "JsonVal",
        "constructor_prefix": "J",
    }
    declaration_style_sequence_format_overrides: ClassVar[dict[str, str]] = {}
    json_type_variant_name_suffix: ClassVar[str | None] = None
    supports_non_ascii_string_literals = True
    variant_metadata: ClassVar[VariantMetadata] = VariantMetadata(
        pre_indent_comment_scalar_variant=False,
        fixture_module_name_template=None,
        fixture_module_name_lowercase=False,
        golden_filename_lowercase=False,
        collection_layout_category="collection_layout",
        record_variants=frozenset(),
        nested_map_widening=NestedMapWideningVariant.NONE,
        modifier_sequence_format_overrides={},
    )
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for PureScript."""

        ISO = DateFormatConfig(
            formatter=_format_purescript_date_iso,
            type_produced=str,
            preamble_lines=(),
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for PureScript."""

        ISO = DatetimeFormatConfig(
            formatter=_format_purescript_datetime_iso,
            type_produced=str,
            preamble_lines=(),
        )

        EPOCH = DatetimeFormatConfig(
            formatter=_format_purescript_datetime_epoch,
            type_produced=int,
            preamble_lines=(),
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_purescript_bytes_hex)
        BASE64 = enum.member(value=_format_purescript_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for PureScript."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="PList ["),
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
            declared_type="Val",
            narrowed_empty_form=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for PureScript."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="PSet ["),
            close="]",
            empty_set=None,
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
        BLOCK = CommentConfig(
            prefix="{-",
            suffix=" -}",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} = {value}"
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
        positive_infinity="PFloat (1.0 / 0.0)",
        negative_infinity="PFloat (-(1.0 / 0.0))",
        nan="PFloat (0.0 / 0.0)",
    ):
        """Float format options."""

        REPR = enum.member(value=_format_purescript_float_repr)
        SCIENTIFIC = enum.member(value=_format_purescript_float_scientific)
        FIXED = enum.member(value=_format_purescript_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=_format_purescript_integer_decimal)
        HEX = enum.member(value=_format_purescript_integer_hex)

        def __call__(self, value: int, /) -> str:
            """Format an integer."""
            formatter: Callable[[int], str] = self.value
            return formatter(value)

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
    integer_width_strategies = BareIntegerWidthStrategies
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
        """PureScript call style options."""

        COMMAND = CommandCallStyle(
            arg_separator=" ",
        )

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

    class BoolFormats(enum.Enum):
        """Empty: this language has no alternative boolean formats."""

    bool_formats = BoolFormats

    class JsonTypes(enum.Enum):
        """JSON value type options for PureScript."""

        ARGONAUT_JSON = "Data.Argonaut.Core.Json"
        """``Data.Argonaut.Core.Json`` -- the dynamic JSON value type
        from the ``argonaut-core`` package.
        """

    json_types = JsonTypes

    class VersionFormats(enum.Enum):
        """Version options for PureScript."""

        V0_15 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    def validate_spec_for_data(self, data: Value) -> None:
        """Raise if the spec cannot produce valid code for *data*.

        Under :attr:`json_type` the data must round-trip through a JSON
        document, so walk *data* to reject non-string dict keys and
        non-finite floats -- both inputs JSON cannot represent.
        """
        if self._json_type_active:
            self._validate_json_value(data)

    def _validate_json_value(self, data: Value, /) -> None:
        """Reject inputs that JSON cannot represent under
        ``json_type``.
        """
        match data:
            case bool():
                return
            case float() if math.isinf(data) or math.isnan(data):
                msg = (
                    "PureScript json_type=ARGONAUT_JSON cannot represent "
                    "the special float value "
                    f"{data!r} because JSON has no syntax for NaN or "
                    "infinity."
                )
                raise UnrepresentableSpecialFloatError(msg)
            case OrderedMap() | dict():
                for key, value in data.items():
                    if not isinstance(key, str):
                        msg = (
                            "PureScript json_type=ARGONAUT_JSON can only "
                            "represent dict keys as JSON object "
                            f"strings, not {type(key).__name__}."
                        )
                        raise UnrepresentableInputError(msg)
                    self._validate_json_value(value)
            case list() | set():
                for item in data:
                    self._validate_json_value(item)
            case _:
                return

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether PureScript should render via
        ``Data.Argonaut.Core.Json``.
        """
        return self.json_type is not None

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
        """Wrap declarations and calls in a PureScript module.

        Variable declarations go at module scope before ``main``; call
        expressions are bound inside a ``let … in unit`` block so that
        bare expressions are not required at the top level.
        """
        preamble = "\n".join(body_preamble)
        declaration_block = "\n".join(declarations)
        decl_part = "\n" + declaration_block if declaration_block else ""
        return _build_purescript_call_output(
            preamble=preamble,
            decl_part=decl_part,
            calls=calls,
            indent=self.indent,
        )

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a PureScript value declaration in a module."""
        preamble = "\n".join(body_preamble)
        if not variable_name:
            return _build_purescript_call_output(
                preamble=preamble,
                decl_part="",
                calls=content,
                indent=self.indent,
            )
        # An inference-bound call result contributes its own
        # ``import Prelude`` (for the stub's ``Unit``) on top of any
        # ``import Prelude`` the data already required, and under
        # ``json_type`` the Argonaut imports must also precede the
        # stub declarations; hoist every import to the top of the
        # preamble.
        preamble = _hoist_purescript_imports(preamble=preamble)
        return f"module Check where\n\n\n{preamble}\n\n\n{content}"

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
    comment_format: CommentFormats = CommentFormats.DOUBLE_DASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
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
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.COMMAND
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    # ``V0_15`` (PureScript 0.15.x) matches the ``purescript: 0.15.15``
    # pin in the ``lint-haskell-family`` job of
    # ``.github/workflows/lint.yml``; keep them in sync.
    language_version: VersionFormats = VersionFormats.V0_15
    indent: str = "    "
    type_name: str = "Val"
    constructor_prefix: str = "P"

    indent_closing_delimiter: ClassVar[bool] = True
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
            return _format_purescript_json_assignment
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config.

        Under :attr:`json_type` heterogeneous scalars all flow through
        the JSON text, so the framework's scalar-uniformity checks are
        skipped.
        """
        if self._json_type_active:
            return dataclasses.replace(
                self.heterogeneous_strategy.value,
                skip_scalar_checks=True,
            )
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
        """Return stub declarations for a call expression.

        Under :attr:`json_type` the stub's parameter types are ``Json``
        rather than the generated ``Val`` ADT.
        """
        stub_type_name = "Json" if self._json_type_active else self.type_name
        return _build_purescript_call_stub(type_name=stub_type_name)

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each formatted call argument in parentheses.

        Under :attr:`json_type` the argument is rendered as a ``Json``
        value produced by ``jsonParser`` instead of the framework's
        formatted ``Val`` literal.
        """
        if self._json_type_active:
            return _format_purescript_json_call_arg
        return _purescript_format_call_arg

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

    scalar_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}
    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

    @cached_property
    def null_literal(self) -> str:
        """Null literal using the configured constructor prefix."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """True literal using the configured constructor prefix."""
        return f"{self.constructor_prefix}Bool true"

    @cached_property
    def false_literal(self) -> str:
        """False literal using the configured constructor prefix."""
        return f"{self.constructor_prefix}Bool false"

    @cached_property
    def _seq_open(self) -> Callable[[list[Value]], str]:
        """Sequence opener built from the configured constructor
        prefix.
        """
        return fixed_open(
            open_str=f"{self.constructor_prefix}List [",
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return _ARGONAUT_JSON_SEQUENCE_CONFIG
        return dataclasses.replace(
            self.sequence_format.value,
            sequence_open=self._seq_open,
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        if self._json_type_active:
            return _ARGONAUT_JSON_SEQUENCE_CONFIG.sequence_open
        return self._seq_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return _ARGONAUT_JSON_SET_CONFIG
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set [",
            ),
        )

    @cached_property
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter using the configured prefix."""
        return _build_purescript_dict_entry(prefix=self.constructor_prefix)

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return _ARGONAUT_JSON_DICT_CONFIG
        return DictFormatConfig(
            dict_open=fixed_open(
                open_str=f"{self.constructor_prefix}Dict [",
            ),
            close="]",
            format_entry=self._dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
            narrowed_empty_form=None,
        )

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        if self.constructor_prefix == "P":
            return self.bytes_format
        return _BYTES_FORMATTERS[self.bytes_format.name](
            self.constructor_prefix
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self.constructor_prefix == "P":
            return self.date_format
        return _build_purescript_date_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self.datetime_format.name == "EPOCH":
            return _build_purescript_datetime_epoch(
                prefix=self.constructor_prefix,
            )
        if self.constructor_prefix == "P":
            return self.datetime_format
        return _build_purescript_datetime_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        return _build_purescript_time_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        if self.constructor_prefix == "P":
            return _format_purescript_string
        return _build_purescript_str_formatter(
            prefix=self.constructor_prefix,
        )

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self.constructor_prefix == "P":
            return self.integer_format
        return _build_purescript_integer_formatter(
            prefix=self.constructor_prefix,
            base=_INT_BASE[self.integer_format.name],
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        if self.constructor_prefix == "P":
            return self.float_format
        prefix = self.constructor_prefix
        _pos_inf = f"{prefix}Float (1.0 / 0.0)"
        _neg_inf = f"{prefix}Float (-(1.0 / 0.0))"
        _nan_val = f"{prefix}Float (0.0 / 0.0)"
        _float_finite = _build_purescript_float_wrapper(
            prefix=prefix,
            inner=_FLOAT_BASE[self.float_format.name],
        )

        @beartype
        def _format_float_with_specials(value: float) -> str:
            """Format a float, handling inf and nan."""
            if math.isinf(value):
                return _neg_inf if value < 0 else _pos_inf
            if math.isnan(value):
                return _nan_val
            return _float_finite(value)

        return _format_float_with_specials

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return _ARGONAUT_JSON_ORDERED_MAP_CONFIG
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(
                open_str=f"{self.constructor_prefix}Dict [",
            ),
            close="]",
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
        if self._json_type_active:
            return _format_purescript_json_declaration
        _base_declaration = self.declaration_style.value.formatter
        _raw_declared = self.sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("Val", self.type_name)
            if _raw_declared is not None
            else None
        )
        _scalar_type = self.type_name

        @beartype
        def _purescript_declaration(
            name: str,
            value: str,
            data: Value,
            _modifiers: frozenset[enum.Enum],
        ) -> str:
            """Format a variable declaration with type annotation."""
            base = _base_declaration(name, value, data, _modifiers)
            decl_type = (
                _sequence_declared_type
                if isinstance(data, list)
                else _scalar_type
            )
            return f"{name} :: {decl_type}\n{base}"

        return _purescript_declaration

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call expression.

        The literal-binding declaration is prepended with a
        ``name :: Type`` annotation derived from the bound value's
        runtime tagged-enum type (``PInt``, ``PStr``, ...); a call
        expression has no such tag, so the annotation is omitted and
        PureScript infers the call's return type instead.
        """
        return self.declaration_style.value.formatter

    @staticmethod
    def format_call_binding_body_preamble() -> tuple[str, ...]:
        """Module-internal preamble lines for an inference-bound call
        result.

        The call stub returns ``Unit`` (``make_widget _ = unit``), so a
        ``wrap_in_file`` scaffold whose top level binds a call result
        must ``import Prelude`` to bring ``Unit`` / ``unit`` into scope.
        The literal binding for the same data needs no such import, so
        this is emitted only on the call-binding path.
        """
        return ("import Prelude",)

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map.

        Under :attr:`json_type` the body preamble is reduced to the
        ``Data.Argonaut.Core``, ``Data.Argonaut.Parser``, and
        ``Data.Either`` imports needed by the ``jsonParser``-backed
        binding, so the custom ``Val`` algebraic type and its
        ``Tuple`` helper are not emitted.
        """
        if self._json_type_active:
            return _argonaut_value_body_preamble
        return _build_purescript_body_preamble(
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
            datetime_type_produced=self.datetime_format.value.type_produced,
        )
