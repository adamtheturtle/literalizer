"""Elm language specification."""

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
from literalizer._formatters.format_integers import format_integer_hex
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
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    default_format_call_variable_assignment,
    default_sequence_binding_declarations,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_call_binding_file_pragmas,
    no_call_stub,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import (
    UnrepresentableInputError,
    WrapCombinedInFileNotSupportedError,
)


@beartype
def _apply_elm_date_iso(value: datetime.date, prefix: str) -> str:
    """Format a date as an Elm string via ISO 8601."""
    return f"{prefix}Str {format_date_iso(value=value)}"


@beartype
def _build_elm_date_iso(
    prefix: str,
) -> Callable[[datetime.date], str]:
    """Build a date formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.date) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_date_iso(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_time_iso(value: datetime.time, prefix: str) -> str:
    """Format a time as an Elm string via ISO 8601."""
    return f"{prefix}Str {format_time_iso(value=value)}"


@beartype
def _build_elm_time_iso(
    prefix: str,
) -> Callable[[datetime.time], str]:
    """Build a time formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.time) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_time_iso(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_datetime_iso(value: datetime.datetime, prefix: str) -> str:
    """Format a datetime as an Elm string via ISO 8601."""
    return f"{prefix}Str {format_datetime_iso(value=value)}"


@beartype
def _build_elm_datetime_iso(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_datetime_iso(value=value, prefix=prefix)

    return _format


@beartype
def _build_elm_datetime_epoch(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Int`` from
    Unix epoch seconds.
    """
    return datetime_epoch_formatter(
        format_integer=_build_elm_integer_formatter(prefix=prefix, base=str),
    )


@beartype
def _apply_elm_bytes_hex(value: bytes, prefix: str) -> str:
    """Format bytes as an Elm hex string."""
    return f"{prefix}Str {format_bytes_hex(value=value)}"


@beartype
def _build_elm_bytes_hex(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` hex
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_bytes_hex(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_bytes_base64(value: bytes, prefix: str) -> str:
    """Format bytes as an Elm base64 string."""
    return f"{prefix}Str {format_bytes_base64(value=value)}"


@beartype
def _build_elm_bytes_base64(
    prefix: str,
) -> Callable[[bytes], str]:
    """Build a bytes formatter that produces ``{prefix}Str`` base64
    constructors.
    """

    def _format(value: bytes) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_bytes_base64(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_integer_formatter(
    value: int, prefix: str, base: Callable[[int], str]
) -> str:
    """Format an integer with a constructor prefix."""
    formatted = base(value)
    if value < 0:
        return f"{prefix}Int ({formatted})"
    return f"{prefix}Int {formatted}"


@beartype
def _build_elm_integer_formatter(
    prefix: str,
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter that produces ``{prefix}Int``
    constructors.
    """

    def _format(value: int) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_integer_formatter(
            value=value, prefix=prefix, base=base
        )

    return _format


@beartype
def _apply_elm_float_wrapper(
    value: float, prefix: str, inner: Callable[[float], str]
) -> str:
    """Format a float with a constructor prefix."""
    formatted = inner(value)
    if formatted.startswith("-"):
        return f"{prefix}Float ({formatted})"
    return f"{prefix}Float {formatted}"


@beartype
def _build_elm_float_wrapper(
    prefix: str,
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter that produces ``{prefix}Float``
    constructors.
    """

    def _format(value: float) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_float_wrapper(
            value=value, prefix=prefix, inner=inner
        )

    return _format


@beartype
def _apply_elm_string(value: str, prefix: str) -> str:
    """Format a string with a constructor prefix."""
    escaped = format_string_backslash_control(
        value=value,
        control_char_fmt="\\u{{{:04x}}}",
    )
    return f"{prefix}Str {escaped}"


@beartype
def _build_elm_str_formatter(
    prefix: str,
) -> Callable[[str], str]:
    """Build a string formatter that produces ``{prefix}Str``
    constructors.
    """

    def _format(value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_string(value=value, prefix=prefix)

    return _format


@beartype
def _apply_elm_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
    str_prefix: str,
) -> str:
    """Format a dict entry as a tuple with a plain-string key.

    Dict keys are ``String``, not ``Val``, so the ``{prefix}Str``
    constructor must be stripped from the formatted key.
    """
    key = key.removeprefix(str_prefix)
    return f"({key}, {formatted_value})"


@beartype
def _build_elm_dict_entry(
    prefix: str,
) -> Callable[[str, Value, str], str]:
    """Build a dict-entry formatter that strips the ``{prefix}Str`` prefix
    from keys.
    """
    _str_prefix = f"{prefix}Str "

    def _format(key: str, _raw_value: Value, formatted_value: str) -> str:
        """Delegate to module-level implementation."""
        return _apply_elm_dict_entry(
            key=key,
            _raw_value=_raw_value,
            formatted_value=formatted_value,
            str_prefix=_str_prefix,
        )

    return _format


# Backward-compatible module-level aliases used by the Enum members.
_format_elm_date_iso = _build_elm_date_iso(prefix="E")
_format_elm_datetime_iso = _build_elm_datetime_iso(prefix="E")
_format_elm_datetime_epoch = _build_elm_datetime_epoch(prefix="E")
_format_elm_bytes_hex = _build_elm_bytes_hex(prefix="E")
_format_elm_bytes_base64 = _build_elm_bytes_base64(prefix="E")
_format_elm_integer_decimal = _build_elm_integer_formatter(
    prefix="E",
    base=str,
)
_format_elm_integer_hex = _build_elm_integer_formatter(
    prefix="E",
    base=format_integer_hex,
)
_format_elm_float_repr = _build_elm_float_wrapper(
    prefix="E",
    inner=format_float_repr,
)
_format_elm_float_scientific = _build_elm_float_wrapper(
    prefix="E",
    inner=format_float_scientific,
)
_format_elm_float_fixed = _build_elm_float_wrapper(
    prefix="E",
    inner=format_float_fixed,
)
_format_elm_string = _build_elm_str_formatter(prefix="E")
_elm_dict_entry = _build_elm_dict_entry(prefix="E")


@beartype
def _build_elm_body_preamble(
    *,
    type_name: str,
    constructor_prefix: str,
    datetime_type_produced: type,
    indent: str,
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for Elm.

    The callable receives the set of types present in the data and returns
    the type declaration with only the constructors that are actually
    needed.
    """

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return body-preamble lines for the given *types*."""
        del data  # unused
        p = constructor_prefix
        int_types: set[type] = {int}
        str_types: set[type] = {str, bytes, datetime.date}
        if datetime_type_produced is int:
            int_types.add(datetime.datetime)
        else:
            str_types.add(datetime.datetime)
        constructors = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), f"{p}Null"),
                (frozenset({bool}), f"{p}Bool Bool"),
                (frozenset(int_types), f"{p}Int Int"),
                (frozenset({float}), f"{p}Float Float"),
                (frozenset(str_types), f"{p}Str String"),
                (frozenset({list}), f"{p}List (List {type_name})"),
                (
                    frozenset({dict, OrderedMap}),
                    f"{p}Dict (List ( String, {type_name} ))",
                ),
                (frozenset({set}), f"{p}Set (List {type_name})"),
            )
            if types & type_set
        ]
        first_line = f"type {type_name}\n{indent}= {constructors[0]}"
        rest_lines = [f"{indent}| {c}" for c in constructors[1:]]
        return ("\n".join([first_line, *rest_lines]),)

    return _compute


@beartype
def _elm_flatten_dotted(parts: Sequence[str]) -> str:
    """Flatten call target parts to an Elm identifier.

    Elm identifiers cannot contain ``.``, so ``["app", "client", "fetch"]``
    becomes ``appClientFetch`` (the first character of each part after
    the first is upper-cased; the remaining characters are kept as-is).
    """
    if len(parts) == 1:
        return parts[0]
    first = parts[0]
    rest = "".join(p[0].upper() + p[1:] if p else "" for p in parts[1:])
    return first + rest


@beartype
def _elm_type_var(*, index: int) -> str:
    """Return a unique lowercase identifier for an Elm type variable.

    Indices ``0``..``25`` map to ``a``..``z``; higher indices append a
    numeric suffix (``a1``..``z1``, ``a2``..``z2``, ...) so that
    27-or-more parameter stubs do not overflow the alphabet into
    non-letter ASCII like ``{``.
    """
    letter = chr(ord("a") + index % 26)
    group = index // 26
    if group == 0:
        return letter
    return f"{letter}{group}"


@beartype
def _elm_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Elm top-level stub declarations for a call target.

    Dotted names are flattened (the first character of each part after
    the first is upper-cased).  Elm calls are curried, so the stub
    chains its type variables with ``->`` (``a -> ()``,
    ``a -> b -> ()``, ``a -> b -> c -> d -> ()``) and the
    implementation takes one ``_`` per parameter.
    """
    flat_name = _elm_flatten_dotted(parts=parts)
    parameter_count = len(params)
    type_variables = [
        _elm_type_var(index=position) for position in range(parameter_count)
    ]
    type_signature = f"{flat_name} : {' -> '.join([*type_variables, '()'])}"
    implementation = f"{flat_name} {' '.join(['_'] * parameter_count)} = ()"
    return (type_signature, implementation)


@beartype
def _elm_format_call_arg(_original: Value, formatted: str, /) -> str:
    """Wrap a formatted Elm value in parentheses for curried application.

    Every literal Elm value is a constructor application (``EInt 1``,
    ``EList […]``), so each argument must be parenthesized to avoid
    being parsed as additional arguments to the outer call.
    """
    return f"({formatted})"


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
    "HEX": _build_elm_bytes_hex,
    "BASE64": _build_elm_bytes_base64,
}


@beartype
def _elm_platform_worker_suffix(indent: str) -> str:
    """Return the Elm ``Platform.worker`` suffix indented by
    ``indent``.
    """
    one = indent
    two = indent * 2
    return (
        f"\n{one}in\n"
        f"{one}Platform.worker\n"
        f"{two}{{ init = \\_ -> ( (), Cmd.none )\n"
        f"{two}, update = \\_ m -> ( m, Cmd.none )\n"
        f"{two}, subscriptions = \\_ -> Sub.none\n"
        f"{two}}}"
    )


# ----- Json.Encode.Value rendering helpers -----
#
# When ``Elm(json_type=JsonTypes.JSON_ENCODE_VALUE)`` is active, every
# value is rendered as a direct ``Json.Encode.*`` function application
# rather than wrapped in the per-fixture ``Val`` ADT.  The output is
# idiomatic ``elm/json`` code; no walker is needed to convert it to a
# JSON document at runtime.

_JSON_ENC_NULL = "Json.Encode.null"
_JSON_ENC_TRUE = "Json.Encode.bool True"
_JSON_ENC_FALSE = "Json.Encode.bool False"
_JSON_ENC_LIST_OPEN = "Json.Encode.list identity ["
_JSON_ENC_OBJECT_OPEN = "Json.Encode.object ["
_JSON_ENCODE_VALUE_TYPE = "Json.Encode.Value"


@beartype
def _format_elm_json_with_ctor(formatted: str, ctor: str) -> str:
    """Apply ``ctor`` to a ``formatted`` numeric literal.

    Elm parses ``Json.Encode.int -3`` as the subtraction
    ``Json.Encode.int - 3``, so negative numeric arguments are wrapped in
    parentheses; positive numerals pass through bare.
    """
    if formatted.startswith("-"):
        return f"{ctor} ({formatted})"
    return f"{ctor} {formatted}"


@beartype
def _build_elm_json_int_formatter(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Build an integer formatter producing ``Json.Encode.int <n>``."""

    def _format(value: int) -> str:
        """Apply the ``Json.Encode.int`` constructor."""
        return _format_elm_json_with_ctor(
            formatted=base(value), ctor="Json.Encode.int"
        )

    return _format


@beartype
def _build_elm_json_float_formatter(
    inner: Callable[[float], str],
) -> Callable[[float], str]:
    """Build a float formatter producing ``Json.Encode.float <n>``."""

    def _format(value: float) -> str:
        """Apply the ``Json.Encode.float`` constructor."""
        return _format_elm_json_with_ctor(
            formatted=inner(value), ctor="Json.Encode.float"
        )

    return _format


@beartype
def _format_elm_json_string(value: str) -> str:
    """Format a string as ``Json.Encode.string "..."``."""
    escaped = format_string_backslash_control(
        value=value,
        control_char_fmt="\\u{{{:04x}}}",
    )
    return f"Json.Encode.string {escaped}"


@beartype
def _format_elm_json_date_iso(value: datetime.date) -> str:
    """Format a date as ``Json.Encode.string`` of its ISO 8601 form."""
    return f"Json.Encode.string {format_date_iso(value=value)}"


@beartype
def _format_elm_json_time_iso(value: datetime.time) -> str:
    """Format a time as ``Json.Encode.string`` of its ISO 8601 form."""
    return f"Json.Encode.string {format_time_iso(value=value)}"


@beartype
def _format_elm_json_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as ``Json.Encode.string`` of its ISO form."""
    return f"Json.Encode.string {format_datetime_iso(value=value)}"


@beartype
def _format_elm_json_bytes_hex(value: bytes) -> str:
    """Format bytes as ``Json.Encode.string`` of their hex form."""
    return f"Json.Encode.string {format_bytes_hex(value=value)}"


@beartype
def _format_elm_json_bytes_base64(value: bytes) -> str:
    """Format bytes as ``Json.Encode.string`` of their base64 form."""
    return f"Json.Encode.string {format_bytes_base64(value=value)}"


_JSON_BYTES_FORMATTERS: dict[str, Callable[[bytes], str]] = {
    "HEX": _format_elm_json_bytes_hex,
    "BASE64": _format_elm_json_bytes_base64,
}


@beartype
def _elm_json_dict_entry(
    key: str, _raw_value: Value, formatted_value: str
) -> str:
    """Format one ``Json.Encode.object`` entry as ``( "k", v )``.

    The framework has already formatted the key with the
    ``Json.Encode.string`` constructor, so strip that prefix to keep the
    bare quoted string that ``Json.Encode.object`` requires.
    """
    raw_key = key.removeprefix("Json.Encode.string ")
    return f"({raw_key}, {formatted_value})"


@beartype
def _validate_elm_json_data(*, data: Value) -> None:
    """Reject inputs ``Json.Encode.Value`` rendering cannot represent.

    ``Json.Encode.object`` keys must be strings.  Walks the data
    recursively so a non-string key nested inside a collection is caught
    upfront, before rendering.
    """
    match data:
        case dict():
            for key, value in data.items():
                if not isinstance(key, str):
                    msg = (
                        "Elm(json_type=JSON_ENCODE_VALUE) cannot represent "
                        f"dict key {key!r}: Json.Encode.object keys must be "
                        "strings."
                    )
                    raise UnrepresentableInputError(msg)
                _validate_elm_json_data(data=value)
        case list() | set():
            for item in data:
                _validate_elm_json_data(data=item)
        case _:
            return


@beartype
def _elm_json_call_stub(
    parts: Sequence[str],
    params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Return Elm call stubs typed as returning ``Json.Encode.Value``.

    Under ``json_type`` the bound call must agree with the surrounding
    ``Json.Encode.Value`` annotation, so the curried stub's return type
    is ``Json.Encode.Value`` rather than ``()``.  The implementation
    returns ``Json.Encode.null`` so the placeholder type-checks.
    """
    flat_name = _elm_flatten_dotted(parts=parts)
    parameter_count = len(params)
    type_variables = [
        _elm_type_var(index=position) for position in range(parameter_count)
    ]
    type_signature = (
        f"{flat_name} : "
        f"{' -> '.join([*type_variables, _JSON_ENCODE_VALUE_TYPE])}"
    )
    implementation = (
        f"{flat_name} {' '.join(['_'] * parameter_count)} = {_JSON_ENC_NULL}"
    )
    return (type_signature, implementation)


@beartype
def _elm_call_module(preamble: str, let_lines: list[str], indent: str) -> str:
    """Build a complete Elm call-mode module from preamble and let-
    bindings.
    """
    return (
        f"module Check exposing (..)\n\n\n"
        f"{preamble}\n\n\n"
        f"main : Program () () Never\nmain =\n{indent}let\n"
        + "\n".join(let_lines)
        + _elm_platform_worker_suffix(indent=indent)
    )


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Elm(metaclass=LanguageCls):
    """Elm language specification.

    The generated output uses custom constructors (``ENull``, ``EBool``,
    ``EList``, ``EDict``, ``ESet``) that are **not** built-in Elm types.
    To compile the generated code, define a ``Val`` custom type in the
    consuming module:

    .. code-block:: elm

       type Val
           = ENull
           | EBool Bool
           | EInt Int
           | EFloat Float
           | EStr String
           | EList (List Val)
           | EDict (List ( String, Val ))
           | ESet (List Val)

    The body preamble automatically emits only the constructors that are
    actually used by the data.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.ISO`` — ISO 8601 string,
              e.g. ``EStr "2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.ISO`` — ISO 8601 string,
              e.g. ``EStr "2024-01-15T12:30:00"``.

        type_name: Name of the generated custom type.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"E"``, producing constructors like ``ENull``,
            ``EBool``, ``EInt``, etc.
    """

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble
    format_call_binding_file_pragmas = no_call_binding_file_pragmas

    leading_preamble = no_leading_preamble
    extension = ".elm"
    pygments_name = "elm"
    supports_special_floats = True
    supports_variable_names = True
    supports_no_variable_wrap_in_file = False
    dict_supports_heterogeneous_values = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_empty_call_parens = True
    supports_dotted_call_stub = False
    call_returns_expression = True
    supports_zero_parameter_calls = False
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
    supports_record_struct_name_prefix = False
    supports_record_shape_names = False
    supports_non_string_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Elm."""

        ISO = DateFormatConfig(
            formatter=_format_elm_date_iso,
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Elm."""

        ISO = DatetimeFormatConfig(
            formatter=_format_elm_datetime_iso,
            type_produced=str,
        )

        EPOCH = DatetimeFormatConfig(
            formatter=_format_elm_datetime_epoch,
            type_produced=int,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_elm_bytes_hex)
        BASE64 = enum.member(value=_format_elm_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Elm."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="EList ["),
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
        """Set type options for Elm."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="ESet ["),
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
        positive_infinity="EFloat (1 / 0)",
        negative_infinity="EFloat (-(1 / 0))",
        nan="EFloat (0 / 0)",
    ):
        """Float format options."""

        REPR = enum.member(value=_format_elm_float_repr)
        SCIENTIFIC = enum.member(value=_format_elm_float_scientific)
        FIXED = enum.member(value=_format_elm_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=_format_elm_integer_decimal)
        HEX = enum.member(value=_format_elm_integer_hex)

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
        """Elm call style options."""

        CURRIED = CommandCallStyle(
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

    class VersionFormats(enum.Enum):
        """Version options for Elm."""

        V0_19 = enum.auto()

    version_formats = VersionFormats

    class JsonTypes(enum.Enum):
        """JSON value type options for Elm."""

        JSON_ENCODE_VALUE = enum.auto()
        """Render values directly as ``elm/json`` ``Json.Encode.*`` calls
        producing :class:`Json.Encode.Value`.

        With this mode the generated module contains no ``Val`` ADT and
        no walker: every literal is an idiomatic ``Json.Encode.bool``,
        ``Json.Encode.int``, ``Json.Encode.string``,
        ``Json.Encode.list identity [ ... ]``,
        ``Json.Encode.object [ ( "k", ... ) ]`` etc., and feeds straight
        into ``Json.Encode.encode 0`` for serialization.
        """

    json_types = JsonTypes

    modifier_combinations: ClassVar[tuple[ModifierCombination, ...]] = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.CAMEL,
        IdentifierCase.PASCAL,
    )
    supported_ref_cases: ClassVar[frozenset[IdentifierCase]] = (
        NON_KEBAB_REF_CASES
    )

    @cached_property
    def _json_active(self) -> bool:
        """``True`` when ``Json.Encode.Value`` rendering is selected."""
        return self.json_type is not None

    def validate_spec_for_data(self, data: Value) -> None:
        """Validate Elm-specific data/format combinations.

        Under :attr:`json_type` every dict key must be a string because
        ``Json.Encode.object`` only admits string keys.
        """
        if self._json_active:
            _validate_elm_json_data(data=data)

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Wrap each formatted call argument in parentheses."""
        return _elm_format_call_arg

    @cached_property
    def validate_call_arg(self) -> Callable[[Value], None]:
        """Return call-argument validation for this language."""
        return no_validate_call_arg

    @cached_property
    def format_call_statement(self) -> Callable[[str], str]:
        """Return call-statement formatting for this language."""
        return identity_call_statement

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap an Elm value declaration in a module.

        When *variable_name* is empty (call mode), each call expression
        in *content* is bound via ``_ = …`` inside a ``let`` block so
        the generated file is syntactically valid Elm.  *content* is
        one single-line call expression per line: this is the only
        shape ``literalize_call`` produces for Elm, which uses
        :attr:`CollectionLayout.COMPACT` for wrapped calls and rejects
        standalone comments in that path.
        """
        preamble = "\n".join(body_preamble)
        let_indent = self.indent * 2
        if not variable_name:
            let_lines = [
                f"{let_indent}_ = {line}" for line in content.split(sep="\n")
            ]
            return _elm_call_module(
                preamble=preamble,
                let_lines=let_lines,
                indent=self.indent,
            )
        return f"module Check exposing (..)\n\n\n{preamble}\n\n\n{content}"

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Elm declarations and call expressions in a module.

        Both variable declarations and call statements are placed inside
        a ``let`` block so the generated file is a valid Elm module.
        Declarations are indented without a ``_ =`` prefix; call
        statements are bound via ``_ = …`` to satisfy Elm's requirement
        that every ``let`` binding produces a value.  *calls* is one
        single-line call expression per line: this is the only shape
        ``literalize_call`` produces for Elm, which uses
        :attr:`CollectionLayout.COMPACT` for wrapped calls and rejects
        standalone comments in that path.
        """
        preamble = "\n".join(body_preamble)
        let_indent = self.indent * 2
        let_lines: list[str] = []
        for decl in declarations:
            let_lines.extend(
                f"{let_indent}{line}" for line in decl.split(sep="\n")
            )
        let_lines.extend(
            f"{let_indent}_ = {line}" for line in calls.split(sep="\n")
        )
        return _elm_call_module(
            preamble=preamble,
            let_lines=let_lines,
            indent=self.indent,
        )

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
    call_style: CallStyles = CallStyles.CURRIED
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    # Keep in sync with the exact ``elm`` dependency pin in
    # ``.github/npm-linters/package.json``, which is pinned to a version
    # ``>=`` this ``V0_19`` default.
    language_version: VersionFormats = VersionFormats.V0_19
    indent: str = "    "
    type_name: str = "Val"
    constructor_prefix: str = "E"
    json_type: JsonTypes | None = None

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
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

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
    def call_style_config(self) -> CallStyle:
        """Configuration for Elm's call style."""
        return self.call_style.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Return stub declarations for a call expression.

        Under :attr:`json_type` the stub returns
        ``Json.Encode.Value`` (and defaults to ``Json.Encode.null``) so
        the bound call type-checks against the ``Json.Encode.Value``
        annotation on the enclosing declaration.
        """
        if self._json_active:
            return _elm_json_call_stub
        return _elm_call_stub

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
        """Rewrite call target parts into an Elm identifier.

        The first character of each part after the first is upper-cased
        and the parts are concatenated (e.g. ``["app", "client",
        "fetch"]`` becomes ``appClientFetch``).
        """
        return _elm_flatten_dotted

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
        if self._json_active:
            return _JSON_ENC_NULL
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        if self._json_active:
            return _JSON_ENC_TRUE
        return f"{self.constructor_prefix}Bool True"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        if self._json_active:
            return _JSON_ENC_FALSE
        return f"{self.constructor_prefix}Bool False"

    @cached_property
    def _seq_open(self) -> Callable[[list[Value]], str]:
        """Shared sequence opener.

        Under :attr:`json_type` lists render as
        ``Json.Encode.list identity [...]``; otherwise the configured
        ADT ``{prefix}List [...]`` form applies.
        """
        if self._json_active:
            return fixed_open(open_str=_JSON_ENC_LIST_OPEN)
        return fixed_open(
            open_str=f"{self.constructor_prefix}List [",
        )

    @cached_property
    def _dict_entry(self) -> Callable[[str, Value, str], str]:
        """Shared dict-entry formatter used by dict and ordered-map."""
        if self._json_active:
            return _elm_json_dict_entry
        return _build_elm_dict_entry(prefix=self.constructor_prefix)

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return dataclasses.replace(
            self.sequence_format.value,
            sequence_open=self._seq_open,
        )

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format.

        Under :attr:`json_type` sets render as a JSON array
        (``Json.Encode.list identity [...]``) because JSON has no set
        type; otherwise the configured ADT ``{prefix}Set [...]`` form
        applies.
        """
        if self._json_active:
            return dataclasses.replace(
                self.set_format.value,
                set_open=fixed_open(open_str=_JSON_ENC_LIST_OPEN),
            )
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set [",
            ),
        )

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self._seq_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting.

        Under :attr:`json_type` dicts render as
        ``Json.Encode.object [ ( "k", v ) ]`` rather than the ADT
        ``{prefix}Dict [ ( "k", v ) ]`` form.
        """
        open_str = (
            _JSON_ENC_OBJECT_OPEN
            if self._json_active
            else f"{self.constructor_prefix}Dict ["
        )
        return DictFormatConfig(
            dict_open=fixed_open(open_str=open_str),
            close="]",
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
        if self._json_active:
            return _JSON_BYTES_FORMATTERS[self.bytes_format.name]
        if self.constructor_prefix == "E":
            return self.bytes_format
        return _BYTES_FORMATTERS[self.bytes_format.name](
            self.constructor_prefix,
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        if self._json_active:
            return _format_elm_json_date_iso
        if self.constructor_prefix == "E":
            return self.date_format
        return _build_elm_date_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if self._json_active:
            if self.datetime_format.name == "EPOCH":
                return datetime_epoch_formatter(
                    format_integer=_build_elm_json_int_formatter(base=str),
                )
            return _format_elm_json_datetime_iso
        if self.datetime_format.name == "EPOCH":
            return _build_elm_datetime_epoch(prefix=self.constructor_prefix)
        if self.constructor_prefix == "E":
            return self.datetime_format
        return _build_elm_datetime_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        if self._json_active:
            return _format_elm_json_time_iso
        return _build_elm_time_iso(prefix=self.constructor_prefix)

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        if self._json_active:
            return _format_elm_json_string
        if self.constructor_prefix == "E":
            return _format_elm_string
        return _build_elm_str_formatter(prefix=self.constructor_prefix)

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self._json_active:
            return _build_elm_json_int_formatter(
                base=_INT_BASE[self.integer_format.name],
            )
        if self.constructor_prefix == "E":
            return self.integer_format
        return _build_elm_integer_formatter(
            prefix=self.constructor_prefix,
            base=_INT_BASE[self.integer_format.name],
        )

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        if self._json_active:
            return self._json_format_float
        if self.constructor_prefix == "E":
            return self.float_format
        _pos_inf = f"{self.constructor_prefix}Float (1 / 0)"
        _neg_inf = f"{self.constructor_prefix}Float (-(1 / 0))"
        _nan_val = f"{self.constructor_prefix}Float (0 / 0)"
        _float_finite = _build_elm_float_wrapper(
            prefix=self.constructor_prefix,
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
        open_str = (
            _JSON_ENC_OBJECT_OPEN
            if self._json_active
            else f"{self.constructor_prefix}Dict ["
        )
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=open_str),
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
        """Callable that formats a new variable declaration.

        Under :attr:`json_type` the annotation is the flat
        ``Json.Encode.Value`` regardless of whether the top-level shape
        is a list, dict, set, or scalar; every literal flows through the
        same ``Json.Encode.*`` constructor pipeline.
        """
        _base_declaration = self.declaration_style.value.formatter
        if self._json_active:

            @beartype
            def _elm_json_declaration(
                name: str,
                value: str,
                data: Value,
                _modifiers: frozenset[enum.Enum],
            ) -> str:
                """Format a ``Json.Encode.Value`` declaration."""
                base = _base_declaration(name, value, data, _modifiers)
                return f"{name} : {_JSON_ENCODE_VALUE_TYPE}\n{base}"

            return _elm_json_declaration

        _raw_declared = self.sequence_format.value.declared_type
        _type_name = self.type_name
        _sequence_declared_type = (
            _raw_declared.replace("Val", _type_name)
            if _raw_declared is not None
            else None
        )

        @beartype
        def _elm_declaration(
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
                else _type_name
            )
            return f"{name} : {decl_type}\n{base}"

        return _elm_declaration

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call expression.

        The literal-binding declaration is prepended with a
        ``name : Val`` annotation derived from the bound value's
        runtime tagged-enum type; a call expression has no such tag,
        so the annotation is omitted and Elm infers the call's return
        type instead.
        """
        return self.declaration_style.value.formatter

    def wrap_call_variable_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a call-result variable binding in an Elm module.

        The literal-binding scaffold emits a top-level ``name : Val`` /
        ``name = …`` pair that the test driver forces externally via a
        ``Check.my_data`` reference.  A call-mode fixture is instead
        driven through ``Check.main``, so the binding is placed inside
        the ``main`` ``let`` block; evaluating the block forces the
        call.  *content* is the single-line ``name = call …`` binding
        produced by :attr:`format_call_variable_declaration`.
        """
        del variable_name  # the binding text already carries the name
        preamble = "\n".join(body_preamble)
        let_indent = self.indent * 2
        let_lines = [f"{let_indent}{line}" for line in content.split(sep="\n")]
        return _elm_call_module(
            preamble=preamble,
            let_lines=let_lines,
            indent=self.indent,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Elm needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Elm needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines.

        Under :attr:`json_type` the preamble is a single
        ``import Json.Encode`` line; otherwise the per-fixture ``Val``
        ADT declaration is emitted with only the constructors actually
        referenced by the data.
        """
        if self._json_active:

            def _json_preamble(
                _types: frozenset[type], _data: Value, /
            ) -> tuple[str, ...]:
                """Return the single ``import Json.Encode`` line."""
                return ("import Json.Encode",)

            return _json_preamble
        return _build_elm_body_preamble(
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
            datetime_type_produced=self.datetime_format.value.type_produced,
            indent=self.indent,
        )

    @cached_property
    def _json_format_float(self) -> Callable[[float], str]:
        """Float formatter for :attr:`json_type` mode."""
        _finite = _build_elm_json_float_formatter(
            inner=_FLOAT_BASE[self.float_format.name],
        )
        _pos_inf = "Json.Encode.float (1 / 0)"
        _neg_inf = "Json.Encode.float (-(1 / 0))"
        _nan_val = "Json.Encode.float (0 / 0)"

        @beartype
        def _format(value: float) -> str:
            """Format a float, handling inf and nan."""
            if math.isinf(value):
                return _neg_inf if value < 0 else _pos_inf
            if math.isnan(value):
                return _nan_val
            return _finite(value)

        return _format
