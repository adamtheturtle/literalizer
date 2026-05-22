"""Haskell language specification."""

import dataclasses
import datetime
import enum
import json
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    datetime_epoch_formatter,
    format_date_iso,
    format_datetime_epoch,
    format_datetime_iso,
    format_time_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_template,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
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
)
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
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    date_scalar_preamble,
    default_format_call_variable_assignment,
    default_sequence_binding_declarations,
    identity_call_arg,
    identity_call_ref_identifier,
    identity_call_statement,
    identity_call_target,
    identity_constructor_target,
    never_inhibits_consuming_form,
    no_call_binding_body_preamble,
    no_data_preamble,
    no_format_integer_widened,
    no_leading_preamble,
    no_type_hint_preamble,
    no_validate_call_arg,
    no_validate_spec_for_data,
)
from literalizer._types import OrderedMap, Value
from literalizer.exceptions import WrapCombinedInFileNotSupportedError


@beartype
def _haskell_call_preamble_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    _args: Sequence[Value],
    /,
) -> tuple[str, ...]:
    """Emit ``OverloadedRecordDot`` when the call target contains dots."""
    if len(parts) > 1:
        return ("{-# LANGUAGE OverloadedRecordDot #-}",)
    return ()


@beartype
def _haskell_arg_type_str(
    *, params: Sequence[str], type_name: str, curried: bool
) -> str | None:
    """Return the Haskell argument-type string for a call signature.

    Curried: ``Val -> Val -> Val``, or ``None`` for the zero-parameter case
    (which is a thunk binding ``f :: IO Val`` with no arrow).
    Positional: ``Val`` for one param, or a tuple ``(Val, ...)`` for
    many (including ``()`` for zero, since :class:`PositionalCallStyle`
    emits ``f()`` at the call site).
    """
    if curried:
        if not params:
            return None
        return " -> ".join(type_name for _ in params)
    if len(params) == 1:
        return type_name
    return "(" + ", ".join(type_name for _ in params) + ")"


@beartype
def _build_haskell_call_stub_lines(
    *,
    parts: Sequence[str],
    params: Sequence[str],
    stub_return: StubReturn,
    type_name: str,
    curried: bool,
) -> tuple[str, ...]:
    """Return Haskell stub declarations for a call name."""
    if stub_return is StubReturn.VALUE:
        ret = f"IO {type_name}"
        body = "return undefined"
    else:
        ret = "IO ()"
        body = "return ()"
    # Transform-wrapper stubs are passed a single placeholder param
    # starting with ``_`` and receive the (already typed) result of
    # another call. Declare them with a polymorphic argument so GHC
    # never needs to default the wrapped expression's type.
    is_wrapper_stub = len(params) == 1 and params[0].startswith("_")
    effective_curried = curried and not is_wrapper_stub
    arg_type = _haskell_arg_type_str(
        params=params, type_name=type_name, curried=effective_curried
    )
    lhs_wildcards = " ".join("_" for _ in params) if effective_curried else "_"
    lambda_wildcards = lhs_wildcards
    if len(parts) == 1:
        if is_wrapper_stub:
            sig = f"{parts[0]} :: a -> IO ()"
            return (sig, f"{parts[0]} _ = {body}")
        if arg_type is None:
            return (f"{parts[0]} :: {ret}", f"{parts[0]} = {body}")
        sig = f"{parts[0]} :: {arg_type} -> {ret}"
        return (sig, f"{parts[0]} {lhs_wildcards} = {body}")
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if arg_type is None:
        field_type = ret
        construction_lambda = body
    else:
        field_type = f"{arg_type} -> {ret}"
        construction_lambda = f"\\{lambda_wildcards} -> {body}"
    if not fields:
        cls = root.capitalize() + "Type_"
        return (
            f"data {cls} = {cls} {{ {method} :: {field_type} }}",
            f"{root} :: {cls}",
            f"{root} = {cls} {{ {method} = {construction_lambda} }}",
        )
    lines: list[str] = []
    inner_cls = fields[-1].capitalize() + "Type_"
    lines.append(
        f"data {inner_cls} = {inner_cls} {{ {method} :: {field_type} }}",
    )
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = fields[i].capitalize() + "Type_"
        lines.append(
            f"data {cls} = {cls} {{ {fields[i + 1]} :: {prev_cls} }}",
        )
        prev_cls = cls
    root_cls = root.capitalize() + "Type_"
    lines.append(
        f"data {root_cls} = {root_cls} {{ {fields[0]} :: {prev_cls} }}",
    )
    construction = f"{inner_cls} {{ {method} = {construction_lambda} }}"
    for i in range(len(fields) - 2, -1, -1):
        cls = fields[i].capitalize() + "Type_"
        construction = f"{cls} {{ {fields[i + 1]} = {construction} }}"
    construction = f"{root_cls} {{ {fields[0]} = {construction} }}"
    lines.append(f"{root} :: {root_cls}")
    lines.append(f"{root} = {construction}")
    return tuple(lines)


@beartype
def _build_haskell_call_stub(
    *,
    type_name: str,
    curried: bool,
) -> Callable[
    [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
    tuple[str, ...],
]:
    """Build a call stub function that uses *type_name* for field
    types.
    """

    def _haskell_call_stub(
        parts: Sequence[str],
        params: Sequence[str],
        stub_return: StubReturn,
        _args: Sequence[Value],
        /,
    ) -> tuple[str, ...]:
        """Delegate to module-level implementation."""
        return _build_haskell_call_stub_lines(
            parts=parts,
            params=params,
            stub_return=stub_return,
            type_name=type_name,
            curried=curried,
        )

    return _haskell_call_stub


@beartype
def _haskell_format_call_arg(_original: Value, formatted: str, /) -> str:
    """Wrap a formatted Haskell value in parentheses for curried
    application.
    """
    return f"({formatted})"


@beartype
def _format_haskell_datetime(value: datetime.datetime, prefix: str) -> str:
    """Format a datetime as a Haskell datetime constructor.

    Timezone-aware datetimes are converted to UTC first, since
    ``UTCTime`` represents a point in time in UTC.
    """
    if value.tzinfo is not None:
        value = value.astimezone(tz=datetime.UTC)
    total_seconds = value.hour * 3600 + value.minute * 60 + value.second
    if value.microsecond:
        picos = total_seconds * 10**12 + value.microsecond * 10**6
        time_part = f"picosecondsToDiffTime {picos}"
    else:
        time_part = f"secondsToDiffTime {total_seconds}"
    return (
        f"{prefix}Datetime (UTCTime "
        f"(fromGregorian {value.year} {value.month} {value.day}) "
        f"({time_part}))"
    )


@beartype
def _build_haskell_datetime_formatter(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Datetime``
    constructors.
    """

    def _format(value: datetime.datetime) -> str:
        """Delegate to module-level implementation."""
        return _format_haskell_datetime(value=value, prefix=prefix)

    return _format


_format_datetime_haskell = _build_haskell_datetime_formatter(prefix="H")


@dataclasses.dataclass(frozen=True)
class _DateTimeFormatters:
    """Resolved date and datetime formatters."""

    format_date: Callable[[datetime.date], str]
    format_datetime: Callable[[datetime.datetime], str]


@beartype
def _wrap_with_str_constructor_date(
    value: datetime.date,
    str_prefix: str,
    formatter: Callable[[datetime.date], str],
) -> str:
    """Wrap an ISO date string with the HStr constructor."""
    return f"{str_prefix}{formatter(value)}"


@beartype
def _wrap_with_str_constructor_datetime(
    value: datetime.datetime,
    str_prefix: str,
    formatter: Callable[[datetime.datetime], str],
) -> str:
    """Wrap an ISO datetime string with the HStr constructor."""
    return f"{str_prefix}{formatter(value)}"


@beartype
def _build_date_formatters(
    *,
    date_format_name: str,
    date_formatter: Callable[[datetime.date], str],
    datetime_format_name: str,
    datetime_formatter: Callable[[datetime.datetime], str],
    constructor_prefix: str,
    is_explicit: bool,
) -> _DateTimeFormatters:
    """Build date and datetime formatters based on format settings."""
    match date_format_name:
        case "HASKELL":
            fmt_date: Callable[[datetime.date], str] = date_ymd_formatter(
                template=(
                    f"{constructor_prefix}Date "
                    f"(fromGregorian {{year}} {{month}} {{day}})"
                ),
            )
        case _ if is_explicit:
            _str_pfx = f"{constructor_prefix}Str "

            def _explicit_date(value: datetime.date) -> str:
                """Delegate to module-level implementation."""
                return _wrap_with_str_constructor_date(
                    value=value, str_prefix=_str_pfx, formatter=date_formatter
                )

            fmt_date = _explicit_date
        case _:
            fmt_date = date_formatter

    match datetime_format_name:
        case "HASKELL":
            fmt_datetime: Callable[[datetime.datetime], str] = (
                _build_haskell_datetime_formatter(prefix=constructor_prefix)
            )
        case "EPOCH":
            fmt_datetime = datetime_formatter
        case _ if is_explicit:
            _str_pfx_dt = f"{constructor_prefix}Str "

            def _explicit_datetime(value: datetime.datetime) -> str:
                """Delegate to module-level implementation."""
                return _wrap_with_str_constructor_datetime(
                    value=value,
                    str_prefix=_str_pfx_dt,
                    formatter=datetime_formatter,
                )

            fmt_datetime = _explicit_datetime
        case _:
            fmt_datetime = datetime_formatter

    return _DateTimeFormatters(
        format_date=fmt_date,
        format_datetime=fmt_datetime,
    )


@dataclasses.dataclass(frozen=True)
class _StringFormatters:
    """String, bytes, and dict-entry formatters."""

    format_string: Callable[[str], str]
    format_bytes: Callable[[bytes], str]
    format_dict_entry: Callable[[str, Value, str], str]
    is_explicit: bool


@beartype
def _wrap_str_with_constructor(
    value: str,
    string_constructor: str,
    base_format_string: Callable[[str], str],
) -> str:
    """Wrap a formatted string with the constructor prefix."""
    return f"{string_constructor}{base_format_string(value)}"


@beartype
def _wrap_bytes_with_constructor(
    data: bytes,
    string_constructor: str,
    base_format_bytes: Callable[[bytes], str],
) -> str:
    """Wrap formatted bytes with the constructor prefix."""
    return f"{string_constructor}{base_format_bytes(data)}"


@beartype
def _format_explicit_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
    string_constructor: str,
) -> str:
    """Format a dict entry, stripping the constructor from the key."""
    clean_key = key.removeprefix(string_constructor)
    return f"({clean_key}, {formatted_value})"


@beartype
def _build_string_formatters(
    *,
    string_format_name: str,
    constructor_prefix: str,
    base_format_bytes: Callable[[bytes], str],
) -> _StringFormatters:
    """Build string/bytes/dict-entry formatters.

    For ``EXPLICIT`` format, string and bytes values are wrapped with the
    constructor prefix (e.g. ``HStr "hello"``), and dict keys are
    unwrapped since they are ``String``, not ``Val``.

    For ``DOUBLE`` format, values pass through unmodified, and dict
    entries use tuple formatting.
    """

    def base_format_string(value: str) -> str:
        r"""Format a Haskell string with ``\x..`` control-char escapes."""
        return format_string_backslash_control(
            value=value,
            control_char_fmt="\\x{:02x}",
        )

    if string_format_name != "EXPLICIT":
        return _StringFormatters(
            format_string=base_format_string,
            format_bytes=base_format_bytes,
            format_dict_entry=tuple_dict_entry(
                format_value=passthrough_sequence_entry,
            ),
            is_explicit=False,
        )

    string_constructor = f"{constructor_prefix}Str "

    def _format_string(value: str) -> str:
        """Delegate to module-level implementation."""
        return _wrap_str_with_constructor(
            value=value,
            string_constructor=string_constructor,
            base_format_string=base_format_string,
        )

    def _format_bytes(data: bytes) -> str:
        """Delegate to module-level implementation."""
        return _wrap_bytes_with_constructor(
            data=data,
            string_constructor=string_constructor,
            base_format_bytes=base_format_bytes,
        )

    def _format_dict_entry(
        key: str,
        _raw_value: Value,
        formatted_value: str,
    ) -> str:
        """Delegate to module-level implementation."""
        return _format_explicit_dict_entry(
            key=key,
            _raw_value=_raw_value,
            formatted_value=formatted_value,
            string_constructor=string_constructor,
        )

    return _StringFormatters(
        format_string=_format_string,
        format_bytes=_format_bytes,
        format_dict_entry=_format_dict_entry,
        is_explicit=True,
    )


@beartype
def _num_instance(
    *,
    has_int: bool,
    has_float: bool,
    needs_catchall: bool,
    type_name: str,
    constructor_prefix: str,
    indent: str,
) -> str:
    """Build the ``Num`` instance with only relevant constructors.

    *needs_catchall* controls whether a trailing ``negate _`` clause is
    emitted. When the ``Val`` type has only numeric constructors, the
    specific ``negate (HInt n)`` / ``negate (HFloat f)`` patterns are
    exhaustive, and a catch-all would be redundant.
    """
    if has_int:
        from_integer = f"{indent}fromInteger = {constructor_prefix}Int"
    else:
        from_integer = (
            f"{indent}fromInteger n = "
            f"{constructor_prefix}Float (fromIntegral n)"
        )
    negate_parts: list[str] = []
    if has_int:
        negate_parts.append(
            f"{indent}negate ({constructor_prefix}Int n) = "
            f"{constructor_prefix}Int (negate n)"
        )
    if has_float:
        negate_parts.append(
            f"{indent}negate ({constructor_prefix}Float f) = "
            f"{constructor_prefix}Float (negate f)"
        )
    if needs_catchall:
        negate_parts.append(f'{indent}negate _ = error "not implemented"')
    return "\n".join(
        [
            f"instance Num {type_name} where",
            from_integer,
            f'{indent}_ + _ = error "not implemented"',
            f'{indent}_ * _ = error "not implemented"',
            f'{indent}abs _ = error "not implemented"',
            f'{indent}signum _ = error "not implemented"',
            *negate_parts,
        ]
    )


@beartype
def _has_microsecond_datetime(*, data: Value) -> bool:
    """Return whether *data* contains any datetime with microseconds."""
    match data:
        case datetime.datetime():
            return bool(data.microsecond)
        case datetime.date():
            return False
        case dict():
            return any(
                _has_microsecond_datetime(data=v) for v in data.values()
            )
        case list() | set():
            return any(_has_microsecond_datetime(data=v) for v in data)
        case _:
            return False


@beartype
def _has_nonmicrosecond_datetime(*, data: Value) -> bool:
    """Return whether *data* contains any datetime without
    microseconds.
    """
    match data:
        case datetime.datetime():
            return not data.microsecond
        case datetime.date():
            return False
        case dict():
            return any(
                _has_nonmicrosecond_datetime(data=v) for v in data.values()
            )
        case list() | set():
            return any(_has_nonmicrosecond_datetime(data=v) for v in data)
        case _:
            return False


@beartype
def _datetime_import_items(
    *,
    has_from_gregorian: bool,
    has_microsecond: bool,
    has_nonmicrosecond: bool,
) -> list[str]:
    """Return ``Data.Time`` import names needed for datetime values.

    ``secondsToDiffTime`` is imported only when at least one datetime
    has no microsecond component; otherwise every datetime is rendered
    via ``picosecondsToDiffTime`` and the seconds helper would be
    flagged as unused.
    """
    items = ["UTCTime(..)"]
    if not has_from_gregorian:
        items.append("fromGregorian")
    if has_nonmicrosecond:
        items.append("secondsToDiffTime")
    if has_microsecond:
        items.append("picosecondsToDiffTime")
    return items


@dataclasses.dataclass(frozen=True, kw_only=True)
class _HaskellPreambleConfig:
    """Captured configuration for the Haskell body preamble
    computation.
    """

    include_hdate: bool
    include_hdatetime: bool
    datetime_produces_int: bool
    date_needs_is_string: bool
    datetime_needs_is_string: bool
    date_needs_str_explicit: bool
    datetime_needs_str_explicit: bool
    is_string_import: str
    is_string_instance: str
    type_name: str
    constructor_prefix: str
    emit_is_string: bool
    emit_num: bool
    indent: str


@beartype
def _haskell_base_constructors(
    *,
    types: frozenset[type],
    constructor_prefix: str,
    type_name: str,
) -> list[str]:
    """Return base data-type constructors for the types present in
    data.
    """
    p = constructor_prefix
    return [
        constructor
        for type_set, constructor in (
            (frozenset({type(None)}), f"{p}Null"),
            (frozenset({bool}), f"{p}Bool Bool"),
            (frozenset({int}), f"{p}Int Integer"),
            (frozenset({float}), f"{p}Float Double"),
            (frozenset({str, bytes}), f"{p}Str String"),
            (frozenset({list}), f"{p}List [{type_name}]"),
            (
                frozenset({dict, OrderedMap}),
                f"{p}Map [(String, {type_name})]",
            ),
            (frozenset({set}), f"{p}Set [{type_name}]"),
        )
        if types & type_set
    ]


@beartype
def _haskell_extend_for_dates(
    *,
    cfg: _HaskellPreambleConfig,
    types: frozenset[type],
    data: Value,
    data_val_parts: list[str],
) -> list[str]:
    """Append date/datetime constructors and return the import-item
    list.
    """
    p = cfg.constructor_prefix
    import_items: list[str] = []
    if cfg.include_hdate and datetime.date in types:
        data_val_parts.append(f"{p}Date Day")
        import_items.extend(["Day", "fromGregorian"])
    if cfg.include_hdatetime and datetime.datetime in types:
        data_val_parts.append(f"{p}Datetime UTCTime")
        import_items.extend(
            _datetime_import_items(
                has_from_gregorian="fromGregorian" in import_items,
                has_microsecond=_has_microsecond_datetime(data=data),
                has_nonmicrosecond=_has_nonmicrosecond_datetime(data=data),
            ),
        )
    if (
        cfg.datetime_produces_int
        and datetime.datetime in types
        and f"{p}Int Integer" not in data_val_parts
    ):
        data_val_parts.append(f"{p}Int Integer")
    return import_items


@beartype
def _haskell_needs_str_constructor(
    *,
    cfg: _HaskellPreambleConfig,
    types: frozenset[type],
) -> bool:
    """Return True if an ``HStr String`` constructor must be present."""
    return (
        bool(types & {str, bytes})
        or (cfg.date_needs_is_string and datetime.date in types)
        or (cfg.datetime_needs_is_string and datetime.datetime in types)
        or (cfg.date_needs_str_explicit and datetime.date in types)
        or (cfg.datetime_needs_str_explicit and datetime.datetime in types)
    )


@beartype
def _haskell_num_instances(
    *,
    cfg: _HaskellPreambleConfig,
    types: frozenset[type],
    data_val_parts: list[str],
) -> list[str]:
    """Return ``Num``/``Fractional`` instance lines for the data types."""
    if not cfg.emit_num:
        return []
    p = cfg.constructor_prefix
    has_float = float in types
    has_int = int in types or (
        cfg.datetime_produces_int and datetime.datetime in types
    )
    instances: list[str] = []
    if has_float or has_int:
        # The numeric catch-all for ``negate`` is redundant when ``Val``
        # has only numeric constructors, because the specific
        # ``HInt`` / ``HFloat`` clauses cover the type.
        num_constructor_count = (1 if has_int else 0) + (1 if has_float else 0)
        needs_catchall = len(data_val_parts) > num_constructor_count
        instances.append(
            _num_instance(
                has_int=has_int,
                has_float=has_float,
                needs_catchall=needs_catchall,
                type_name=cfg.type_name,
                constructor_prefix=cfg.constructor_prefix,
                indent=cfg.indent,
            ),
        )
    if has_float:
        instances.append(
            f"instance Fractional {cfg.type_name} where\n"
            f"{cfg.indent}fromRational r = {p}Float (realToFrac r)\n"
            f'{cfg.indent}_ / _ = error "not implemented"'
        )
    return instances


@beartype
def _haskell_compute_preamble(
    *,
    cfg: _HaskellPreambleConfig,
    types: frozenset[type],
    data: Value,
) -> tuple[str, ...]:
    """Return body-preamble lines for the given *types* and *data*."""
    p = cfg.constructor_prefix
    data_val_parts = _haskell_base_constructors(
        types=types,
        constructor_prefix=p,
        type_name=cfg.type_name,
    )
    import_items = _haskell_extend_for_dates(
        cfg=cfg,
        types=types,
        data=data,
        data_val_parts=data_val_parts,
    )

    needs_is_string = cfg.emit_is_string and (
        bool(types & {str, bytes})
        or (cfg.date_needs_is_string and datetime.date in types)
        or (cfg.datetime_needs_is_string and datetime.datetime in types)
    )
    if (
        _haskell_needs_str_constructor(cfg=cfg, types=types)
        and f"{p}Str String" not in data_val_parts
    ):
        data_val_parts.append(f"{p}Str String")

    # Emit imports first, then data declaration, then instances.
    imports: list[str] = []
    if import_items:
        imports.append("import Data.Time (" + ", ".join(import_items) + ")")
    if needs_is_string:
        imports.append(cfg.is_string_import)

    instances: list[str] = []
    if needs_is_string:
        instances.append(cfg.is_string_instance)
    instances.extend(
        _haskell_num_instances(
            cfg=cfg,
            types=types,
            data_val_parts=data_val_parts,
        ),
    )

    lines: list[str] = imports
    lines.append(f"data {cfg.type_name} = " + " | ".join(data_val_parts))
    lines.extend(instances)
    return tuple(lines)


@beartype
def _build_scalar_body_preamble(
    *,
    date_format: enum.Enum,
    datetime_format: enum.Enum,
    is_string_import: str,
    is_string_instance: str,
    type_name: str,
    constructor_prefix: str,
    emit_is_string: bool,
    emit_num: bool,
    indent: str,
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for Haskell.

    The callable receives the set of types present in the data and the
    original data value, and returns only the imports, the type
    declaration, and typeclass instances that are actually needed.

    The returned lines are ordered: imports first, then the data type,
    then typeclass instances.

    When *emit_is_string* is ``False``, the ``IsString`` import and
    instance are suppressed (used by the ``EXPLICIT`` string format).

    When *emit_num* is ``False``, the ``Num`` and ``Fractional``
    instances are suppressed (used by the ``EXPLICIT`` numeric style).
    """
    cfg = _HaskellPreambleConfig(
        include_hdate=date_format.value.type_produced is datetime.date,
        include_hdatetime=(
            datetime_format.value.type_produced is datetime.datetime
        ),
        datetime_produces_int=datetime_format.value.type_produced is int,
        date_needs_is_string=bool(
            emit_is_string and date_format.value.preamble_lines
        ),
        datetime_needs_is_string=bool(
            emit_is_string and datetime_format.value.preamble_lines
        ),
        # In EXPLICIT mode, ISO dates/datetimes produce HStr-wrapped
        # strings, so HStr String must appear in the data type.
        date_needs_str_explicit=bool(
            not emit_is_string and date_format.value.type_produced is str
        ),
        datetime_needs_str_explicit=bool(
            not emit_is_string and datetime_format.value.type_produced is str
        ),
        is_string_import=is_string_import,
        is_string_instance=is_string_instance,
        type_name=type_name,
        constructor_prefix=constructor_prefix,
        emit_is_string=emit_is_string,
        emit_num=emit_num,
        indent=indent,
    )

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return body-preamble lines for the given *types*."""
        return _haskell_compute_preamble(cfg=cfg, types=types, data=data)

    return _compute


@dataclasses.dataclass(frozen=True)
class _SequenceSetup:
    """Sequence format configuration and opener."""

    format_config: SequenceFormatConfig
    sequence_open: Callable[[list[Value]], str]


@beartype
def _build_sequence_setup(
    *,
    sequence_format: enum.Enum,
    constructor_prefix: str,
) -> _SequenceSetup:
    """Build sequence format config, customizing the opener for LIST."""
    fmt: SequenceFormatConfig = sequence_format.value
    if sequence_format.name == "LIST":
        seq_open = fixed_open(
            open_str=f"{constructor_prefix}List [",
        )
        return _SequenceSetup(
            format_config=dataclasses.replace(fmt, sequence_open=seq_open),
            sequence_open=seq_open,
        )
    return _SequenceSetup(
        format_config=fmt,
        sequence_open=fmt.sequence_open,
    )


@dataclasses.dataclass(frozen=True)
class _DeclarationFormatters:
    """Variable declaration and assignment formatters."""

    format_variable_declaration: Callable[
        [str, str, Value, frozenset[enum.Enum]], str
    ]
    format_variable_assignment: Callable[[str, str, Value], str]


@beartype
def _format_haskell_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    modifiers: frozenset[enum.Enum],
    base_declaration: Callable[[str, str, Value, frozenset[enum.Enum]], str],
    sequence_declared_type: str | None,
    type_name: str,
) -> str:
    """Format a variable declaration with type annotation."""
    base = base_declaration(name, value, data, modifiers)
    if isinstance(data, list):
        if sequence_declared_type is None:
            # TUPLE sequence format: pin each slot to ``Val`` so bare
            # numeric literals in the tuple resolve via ``fromInteger``
            # instead of triggering ``-Wtype-defaults``.
            tuple_type = "(" + ", ".join(type_name for _ in data) + ")"
            return f"{name} :: {tuple_type}\n{base}"
        return f"{name} :: {sequence_declared_type}\n{base}"
    return f"{name} :: {type_name}\n{base}"


@beartype
def _build_declaration_formatters(
    *,
    declaration_style: enum.Enum,
    sequence_format: enum.Enum,
    type_name: str,
) -> _DeclarationFormatters:
    """Build declaration/assignment formatters with type annotations."""
    base_declaration: Callable[
        [str, str, Value, frozenset[enum.Enum]], str
    ] = declaration_style.value.formatter
    raw_declared = sequence_format.value.declared_type
    sequence_declared_type = (
        raw_declared.replace("Val", type_name)
        if raw_declared is not None
        else None
    )

    def _haskell_declaration(
        name: str,
        value: str,
        data: Value,
        modifiers: frozenset[enum.Enum],
    ) -> str:
        """Delegate to module-level implementation."""
        return _format_haskell_declaration(
            name=name,
            value=value,
            data=data,
            modifiers=modifiers,
            base_declaration=base_declaration,
            sequence_declared_type=sequence_declared_type,
            type_name=type_name,
        )

    return _DeclarationFormatters(
        format_variable_declaration=_haskell_declaration,
        format_variable_assignment=variable_formatter(
            template="{name} = {value}",
        ),
    )


@dataclasses.dataclass(frozen=True)
class _PreambleSetup:
    """Preamble configuration for Haskell output."""

    scalar_preamble: dict[type, tuple[str, ...]]
    compute_body_preamble: Callable[[frozenset[type], Value], tuple[str, ...]]


@beartype
def _build_preamble_setup(
    *,
    date_format: enum.Enum,
    datetime_format: enum.Enum,
    integer_format: enum.Enum,
    is_explicit: bool,
    type_name: str,
    constructor_prefix: str,
    emit_num: bool,
    indent: str,
) -> _PreambleSetup:
    """Build scalar preamble and body-preamble computation."""
    _overloaded_strings = ("{-# LANGUAGE OverloadedStrings #-}",)
    if is_explicit:
        # EXPLICIT mode wraps dates/datetimes with HStr, so no
        # OverloadedStrings pragma is needed for ISO formats.
        scalar_preamble: dict[type, tuple[str, ...]] = {}
    else:
        str_extra: dict[type, tuple[str, ...]] = {
            str: _overloaded_strings,
            bytes: _overloaded_strings,
        }
        scalar_preamble = date_scalar_preamble(
            date_format=date_format,
            datetime_format=datetime_format,
            extra=str_extra,
        )
    # Binary integer literals (``0b...``) are not part of Haskell 2010
    # and need the ``BinaryLiterals`` extension. ``GHC2021`` bundles
    # it already, so the pragma is redundant under that base, but
    # emitting it unconditionally lets the generated code build under
    # either base without ceremony. Hex (``0x``) and octal (``0o``)
    # are standard either way.
    if integer_format.name == "BINARY":
        scalar_preamble = {
            **scalar_preamble,
            int: (
                *scalar_preamble.get(int, ()),
                "{-# LANGUAGE BinaryLiterals #-}",
            ),
        }
    return _PreambleSetup(
        scalar_preamble=scalar_preamble,
        compute_body_preamble=_build_scalar_body_preamble(
            date_format=date_format,
            datetime_format=datetime_format,
            is_string_import="import Data.String (IsString(fromString))",
            is_string_instance=(
                f"instance IsString {type_name} where\n"
                f"{indent}fromString = {constructor_prefix}Str"
            ),
            type_name=type_name,
            constructor_prefix=constructor_prefix,
            emit_is_string=not is_explicit,
            emit_num=emit_num,
            indent=indent,
        ),
    )


@beartype
def _wrap_integer_with_constructor(
    value: int,
    int_prefix: str,
    base_format_integer: Callable[[int], str],
) -> str:
    """Wrap an integer with the constructor prefix."""
    formatted = base_format_integer(value)
    if value < 0:
        return f"{int_prefix}({formatted})"
    return f"{int_prefix}{formatted}"


@beartype
def _wrap_float_with_constructor(
    value: float,
    float_prefix: str,
    base_format_float: Callable[[float], str],
) -> str:
    """Wrap a float with the constructor prefix."""
    formatted = base_format_float(value)
    return f"{float_prefix}({formatted})"


_AESON_VALUE_STATIC_PREAMBLE: tuple[str, ...] = (
    "{-# LANGUAGE OverloadedStrings #-}",
)

_AESON_VALUE_BODY_PREAMBLE: tuple[str, ...] = (
    "import Data.Aeson (Value, eitherDecodeStrict)",
    "import Data.Text.Encoding (encodeUtf8)",
)


@beartype
def _aeson_value_body_preamble(
    _types: frozenset[type], _data: Value, /
) -> tuple[str, ...]:
    """Return the ``Data.Aeson.Value`` import preamble lines."""
    return _AESON_VALUE_BODY_PREAMBLE


# Sequence/dict format definitions used while ``json_type`` is active.
# The framework still walks the data to compute a formatted ``value``,
# but that string is discarded by :func:`_format_haskell_json_declaration`
# and friends in favor of a fresh ``json.dumps`` of the raw data.  These
# definitions only need to be permissive enough that the formatting pass
# does not error on heterogeneous data or nulls inside containers.
_AESON_VALUE_SEQUENCE_CONFIG = SequenceFormatConfig(
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

_AESON_VALUE_SET_CONFIG = SetFormatConfig(
    set_open=fixed_open(open_str="["),
    close="]",
    empty_set="[]",
    preamble_lines=(),
    set_opener_template="",
    supports_heterogeneity=True,
    supports_trailing_comma=True,
)

_AESON_VALUE_DICT_CONFIG = DictFormatConfig(
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
)

_AESON_VALUE_ORDERED_MAP_CONFIG = OrderedMapFormatConfig(
    ordered_map_open=fixed_open(open_str="{"),
    close="}",
    preamble_lines=(),
)


@beartype
def _aeson_temporal_to_iso(data: datetime.date | datetime.time) -> str:
    """Return ISO-8601 text for a date / datetime / time value.

    Naive datetimes are anchored to UTC so the rendered JSON document
    round-trips through ``Data.Aeson`` without a missing-offset error.
    """
    if isinstance(data, datetime.datetime):
        iso = data.isoformat()
        if data.tzinfo is None:
            iso += "Z"
        return iso
    return data.isoformat()


@beartype
def _aeson_to_jsonable(data: Value) -> object:
    """Convert *data* into a value that :func:`json.dumps` can serialize.

    Dates, datetimes, and times become ISO-8601 strings (JSON has no
    temporal type).  Bytes become a hex-encoded string.  Sets and
    :class:`OrderedMap` are folded into list/dict respectively.  Non-string
    dict keys are not handled here; the caller validates first.
    """
    match data:
        case datetime.datetime() | datetime.date() | datetime.time():
            return _aeson_temporal_to_iso(data=data)
        case bytes():
            return data.hex()
        case OrderedMap() | dict():
            return {
                key: _aeson_to_jsonable(data=value)
                for key, value in data.items()
            }
        case set():
            items = [_aeson_to_jsonable(data=item) for item in data]
            items.sort(key=repr)
            return items
        case list():
            return [_aeson_to_jsonable(data=item) for item in data]
        case _:
            return data


@beartype
def _format_aeson_value_json_text(data: Value) -> str:
    """Serialize *data* as a single-line JSON expression."""
    return json.dumps(obj=_aeson_to_jsonable(data=data), ensure_ascii=False)


@beartype
def _aeson_decode_expression(data: Value) -> str:
    """Render ``either error id (eitherDecodeStrict (encodeUtf8 "..."))``.

    With the ``OverloadedStrings`` pragma the embedded literal resolves
    to :class:`Data.Text.Text`; ``encodeUtf8`` widens it to a strict
    ``ByteString`` that :func:`Data.Aeson.eitherDecodeStrict` accepts.
    """
    json_text = _format_aeson_value_json_text(data=data)
    haskell_literal = format_string_backslash_control(
        value=json_text,
        control_char_fmt="\\x{:02x}",
    )
    return (
        f"either error id (eitherDecodeStrict (encodeUtf8 {haskell_literal}))"
    )


@beartype
def _format_haskell_json_declaration(
    name: str,
    _value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
) -> str:
    """Format a ``Value`` declaration backed by ``eitherDecodeStrict``."""
    expression = _aeson_decode_expression(data=data)
    return f"{name} :: Value\n{name} = {expression}"


@beartype
def _format_haskell_json_assignment(
    name: str,
    _value: str,
    data: Value,
) -> str:
    """Format a ``Value`` assignment backed by ``eitherDecodeStrict``."""
    return f"{name} = {_aeson_decode_expression(data=data)}"


@beartype
def _format_haskell_json_call_arg(raw_value: Value, _formatted: str) -> str:
    """Format a direct call argument as a parenthesized ``Value`` literal.

    Haskell curried calls parenthesize each argument to keep
    constructor / operator applications from being parsed as additional
    arguments to the outer call.
    """
    return f"({_aeson_decode_expression(data=raw_value)})"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
class Haskell(metaclass=LanguageCls):
    """Haskell language specification.

    The generated output uses custom constructors (``HNull``, ``HBool``,
    ``HList``, ``HMap``, ``HSet``) that are **not** built-in Haskell types.
    To compile the generated code, define a ``Val`` ADT and typeclass
    instances in the consuming module:

    .. code-block:: haskell

       data Val
         = HNull
         | HBool Bool
         | HInt Integer
         | HFloat Double
         | HStr String
         | HList [Val]
         | HMap [(String, Val)]
         | HSet [Val]

       instance Num Val where
           fromInteger = HInt
           negate (HInt n)   = HInt (negate n)
           negate (HFloat f) = HFloat (negate f)
           ...

       instance Fractional Val where
           fromRational r = HFloat (realToFrac r)
           ...

    The ``Num`` / ``Fractional`` instances let numeric literals resolve to
    ``HInt`` / ``HFloat``.

    With the default ``EXPLICIT`` string format, strings are wrapped
    explicitly (e.g. ``HStr "hi"``).  The ``DOUBLE`` format instead uses
    ``OverloadedStrings`` so bare ``"hi"`` literals resolve to ``HStr "hi"``
    via an ``IsString`` instance.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.HASKELL`` — ``fromGregorian`` call,
              e.g. ``fromGregorian 2024 1 15``.
              Requires the ``time`` package.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.HASKELL`` — ``UTCTime`` constructor,
              e.g. ``UTCTime (fromGregorian 2024 1 15)
              (secondsToDiffTime 45000)``.
              Requires the ``time`` package.
            * ``datetime_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15T12:30:00"``.

        type_name: Name of the generated custom type.  Defaults to
            ``"Val"``.

        constructor_prefix: Prefix for generated constructor names.
            Defaults to ``"H"``, producing constructors like ``HNull``,
            ``HBool``, ``HInt``, etc.

        numeric_style: How numeric literals are represented.

            * ``numeric_styles.OVERLOADED`` — emit ``Num`` and
              ``Fractional`` typeclass instances so that bare literals
              like ``42`` and ``3.14`` resolve to the custom type.
            * ``numeric_styles.EXPLICIT`` — wrap every numeric literal
              with its constructor (``HInt 42``, ``HFloat (3.14)``)
              and omit the typeclass instances.

        json_type: When set to ``json_types.AESON_VALUE``, render values
            through :func:`Data.Aeson.eitherDecodeStrict` so the output
            produces a :class:`Data.Aeson.Value` instead of Haskell's
            narrow custom ``Val`` algebraic type.  Dict keys must be
            strings so they remain valid JSON object keys.
    """

    format_integer_widened = no_format_integer_widened
    format_constructor_target: ClassVar["staticmethod[[str], str]"] = (
        staticmethod(identity_constructor_target)
    )
    format_call_variable_assignment = default_format_call_variable_assignment
    sequence_binding_declarations = default_sequence_binding_declarations
    format_call_binding_body_preamble = no_call_binding_body_preamble

    leading_preamble = no_leading_preamble
    extension = ".hs"
    pygments_name = "haskell"
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
    supports_zero_parameter_calls = True
    max_call_parameters = NO_CALL_PARAMETER_LIMIT
    supports_inline_multiline_dict_args = True
    supports_standalone_comments_in_wrapped_calls = False
    supports_multi_param_call_wrapper_stub = True
    supports_dict_literal_as_free_expression = True
    supports_module_name = True
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
        """Date format options for Haskell."""

        HASKELL = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="HDate (fromGregorian {year} {month} {day})",
            ),
        )
        ISO = DateFormatConfig(
            formatter=format_date_iso,
            preamble_lines=("{-# LANGUAGE OverloadedStrings #-}",),
            type_produced=str,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Haskell."""

        HASKELL = DatetimeFormatConfig(formatter=_format_datetime_haskell)
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=("{-# LANGUAGE OverloadedStrings #-}",),
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
        """Sequence type options for Haskell."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="HList ["),
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
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            supports_trailing_comma=False,
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
        """Set type options for Haskell."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="HSet ["),
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
        positive_infinity="(1/0)",
        negative_infinity="(-1/0)",
        nan="(0/0)",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = enum.member(value=str)
        HEX = enum.member(value=format_integer_hex)
        OCTAL = enum.member(value=format_integer_octal)
        BINARY = enum.member(value=format_integer_binary)

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
        """Numeric literal style options.

        ``OVERLOADED`` emits ``Num`` and ``Fractional`` typeclass
        instances so that bare numeric literals (``42``, ``3.14``)
        resolve to the custom type via ``fromInteger`` /
        ``fromRational``.

        ``EXPLICIT`` wraps every numeric literal with its constructor
        (``HInt 42``, ``HFloat 3.14``) and omits the typeclass
        instances.
        """

        OVERLOADED = enum.auto()
        EXPLICIT = enum.auto()

    numeric_styles = NumericStyles

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.auto()
        EXPLICIT = enum.auto()

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
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class StatementTerminatorStyles(enum.Enum):
        """Statement terminator options."""

        SEMICOLON = enum.auto()

    statement_terminator_styles = StatementTerminatorStyles

    class CallStyles(enum.Enum):
        """Haskell call style options."""

        CURRIED = CommandCallStyle(
            arg_separator=" ",
        )
        POSITIONAL = PositionalCallStyle(
            arg_separator=", ", parenthesize_each_arg=False
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

    class JsonTypes(enum.Enum):
        """JSON value type options for Haskell."""

        AESON_VALUE = "Data.Aeson.Value"
        """``Data.Aeson.Value`` — the dynamic JSON value type from the
        ``aeson`` package.
        """

    json_types = JsonTypes

    class VersionFormats(enum.Enum):
        """Version options for Haskell."""

        GHC2021 = enum.auto()

    version_formats = VersionFormats

    module_name_case: ClassVar[IdentifierCase] = IdentifierCase.PASCAL
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

    def wrap_in_file(
        self,
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Haskell variable binding in a module."""
        preamble = "\n".join(body_preamble)
        if not variable_name:
            # Call mode: bare expressions are not valid at module
            # top level in Haskell, so wrap them in ``main``. Each call
            # statement is bound via ``_ <- `` so that stubs returning
            # ``IO Val`` (``StubReturn.VALUE``) do not trigger
            # ``-Wunused-do-bind``. ``_ <-`` is also valid when the
            # action returns ``IO ()``.
            indented = "\n".join(
                f"{self.indent}_ <- {line}" if line.strip() else line
                for line in content.split(sep="\n")
            )
            return (
                f"module {self.module_name} where\n"
                + preamble
                + "\nmain :: IO ()\nmain = do\n"
                + indented
                + f"\n{self.indent}pure ()"
            )
        return (
            f"module {self.module_name} where\n"
            + preamble
            + "\n"
            + content
            + f"\nmain :: IO ()\nmain = seq {variable_name} (return ())"
        )

    def wrap_calls_with_declarations(
        self,
        declarations: tuple[str, ...],
        calls: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a sequence of top-level *declarations* alongside a
        block of bare call expressions.

        Top-level ``name :: Type`` / ``name = value`` bindings stay at
        module scope and only the *calls* go inside ``main = do``.  The
        integration harness pairs each ``$ref`` declaration's
        ``bare_code`` with a downstream call and uses this hook to
        avoid concatenating both halves into one ``content`` string,
        which would otherwise force the bindings into a ``do``-block
        where they would need ``let`` injection.
        """
        preamble = "\n".join(body_preamble)
        indented_calls = "\n".join(
            f"{self.indent}_ <- {line}" if line.strip() else line
            for line in calls.split(sep="\n")
        )
        declaration_block = "\n".join(declarations)
        return (
            f"module {self.module_name} where\n"
            + preamble
            + "\n"
            + (declaration_block + "\n" if declaration_block else "")
            + "main :: IO ()\nmain = do\n"
            + indented_calls
            + f"\n{self.indent}pure ()"
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

    date_format: DateFormats = DateFormats.HASKELL
    datetime_format: DatetimeFormats = DatetimeFormats.HASKELL
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
    string_format: StringFormats = StringFormats.EXPLICIT
    trailing_comma: TrailingCommas = TrailingCommas.NO
    statement_terminator_style: StatementTerminatorStyles = (
        StatementTerminatorStyles.SEMICOLON
    )
    call_style: CallStyles = CallStyles.CURRIED
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    json_type: JsonTypes | None = None
    # Keep in sync with the `-XGHC2021` flag passed to the Haskell
    # linter in `.github/workflows/lint.yml`.
    language_version: VersionFormats = VersionFormats.GHC2021
    indent: str = "    "
    module_name: str = "Check"
    type_name: str = "Val"
    constructor_prefix: str = "H"

    indent_closing_delimiter: ClassVar[bool] = True
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def _json_type_active(self) -> bool:
        """Return whether Haskell should render via
        ``Data.Aeson.Value``.
        """
        return self.json_type is not None

    @cached_property
    def static_preamble(self) -> Sequence[str]:
        """Static preamble lines emitted once per file.

        When :attr:`json_type` is active the ``OverloadedStrings``
        pragma is emitted here so the embedded JSON literal resolves to
        :class:`Data.Text.Text` before ``encodeUtf8`` widens it to a
        strict ``ByteString``.
        """
        if self._json_type_active:
            return _AESON_VALUE_STATIC_PREAMBLE
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
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        if self._json_type_active:
            return dataclasses.replace(
                NO_HETEROGENEOUS_BEHAVIOR,
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
    def null_literal(self) -> str:
        """Literal representing ``None``."""
        return f"{self.constructor_prefix}Null"

    @cached_property
    def true_literal(self) -> str:
        """Literal representing ``True``."""
        return f"{self.constructor_prefix}Bool True"

    @cached_property
    def false_literal(self) -> str:
        """Literal representing ``False``."""
        return f"{self.constructor_prefix}Bool False"

    @cached_property
    def _seq_setup(self) -> _SequenceSetup:
        """Shared sequence format setup."""
        return _build_sequence_setup(
            sequence_format=self.sequence_format,
            constructor_prefix=self.constructor_prefix,
        )

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        if self._json_type_active:
            return _AESON_VALUE_SEQUENCE_CONFIG
        return self._seq_setup.format_config

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        if self._json_type_active:
            return _AESON_VALUE_SEQUENCE_CONFIG.sequence_open
        return self._seq_setup.sequence_open

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        if self._json_type_active:
            return _AESON_VALUE_SET_CONFIG
        return dataclasses.replace(
            self.set_format.value,
            set_open=fixed_open(
                open_str=f"{self.constructor_prefix}Set [",
            ),
        )

    @cached_property
    def _string_fmts(self) -> _StringFormatters:
        """Shared string/bytes/dict-entry formatters."""
        return _build_string_formatters(
            string_format_name=self.string_format.name,
            constructor_prefix=self.constructor_prefix,
            base_format_bytes=self.bytes_format,
        )

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self._string_fmts.format_string

    @cached_property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a bytes value as a string literal."""
        return self._string_fmts.format_bytes

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        if self._json_type_active:
            return _AESON_VALUE_DICT_CONFIG
        map_open = f"{self.constructor_prefix}Map ["
        return DictFormatConfig(
            dict_open=fixed_open(open_str=map_open),
            close="]",
            format_entry=self._string_fmts.format_dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
        )

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        if self._json_type_active:
            return _AESON_VALUE_ORDERED_MAP_CONFIG
        map_open = f"{self.constructor_prefix}Map ["
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str=map_open),
            close="]",
            preamble_lines=(),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return self._string_fmts.format_dict_entry

    @cached_property
    def trailing_comma_config(self) -> TrailingCommaConfig:
        """Configuration for trailing-comma behavior."""
        return self.trailing_comma.value

    @cached_property
    def _date_fmts(self) -> _DateTimeFormatters:
        """Shared date/datetime formatter bundle."""
        return _build_date_formatters(
            date_format_name=self.date_format.name,
            date_formatter=self.date_format,
            datetime_format_name=self.datetime_format.name,
            datetime_formatter=self.datetime_format,
            constructor_prefix=self.constructor_prefix,
            is_explicit=self._string_fmts.is_explicit,
        )

    @cached_property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a date as a string literal."""
        return self._date_fmts.format_date

    @cached_property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a datetime as a string literal."""
        if (
            self.datetime_format.name == "EPOCH"
            and self.numeric_style.name == "EXPLICIT"
        ):
            return datetime_epoch_formatter(format_integer=self.format_integer)
        return self._date_fmts.format_datetime

    @cached_property
    def format_time(self) -> Callable[[datetime.time], str]:
        """Callable that formats a time as a string literal."""
        if self._string_fmts.is_explicit:
            _str_pfx = f"{self.constructor_prefix}Str "

            def _explicit_time(value: datetime.time) -> str:
                """Wrap a bare ISO time literal with the HStr
                constructor.
                """
                return f"{_str_pfx}{format_time_iso(value=value)}"

            return _explicit_time
        return format_time_iso

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        if self.numeric_style.name == "EXPLICIT":
            _float_prefix = f"{self.constructor_prefix}Float "
            _base_format_float: Callable[[float], str] = self.float_format

            def _wrap_float(value: float) -> str:
                """Delegate to module-level implementation."""
                return _wrap_float_with_constructor(
                    value=value,
                    float_prefix=_float_prefix,
                    base_format_float=_base_format_float,
                )

            return _wrap_float
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        if self.numeric_style.name == "EXPLICIT":
            _int_prefix = f"{self.constructor_prefix}Int "
            _base_format_integer: Callable[[int], str] = self.integer_format

            def _wrap_integer(value: int) -> str:
                """Delegate to module-level implementation."""
                return _wrap_integer_with_constructor(
                    value=value,
                    int_prefix=_int_prefix,
                    base_format_integer=_base_format_integer,
                )

            return _wrap_integer
        return self.integer_format

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def _decl_fmts(self) -> _DeclarationFormatters:
        """Shared declaration/assignment formatter bundle."""
        return _build_declaration_formatters(
            declaration_style=self.declaration_style,
            sequence_format=self.sequence_format,
            type_name=self.type_name,
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        if self._json_type_active:
            return _format_haskell_json_declaration
        return self._decl_fmts.format_variable_declaration

    @cached_property
    def format_variable_assignment(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable."""
        if self._json_type_active:
            return _format_haskell_json_assignment
        return self._decl_fmts.format_variable_assignment

    @cached_property
    def format_call_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a declaration binding a call expression.

        The literal-binding declaration is prepended with a
        ``name :: Type`` annotation derived from the bound value's
        runtime tagged-enum type; a call expression has no such tag,
        so the annotation is omitted and Haskell infers the call's
        return type instead.
        """
        return self.declaration_style.value.formatter

    @staticmethod
    def format_call_binding_file_pragmas() -> tuple[str, ...]:
        """File-level pragma emitted alongside a ``wrap_in_file``
        scaffold whose top level contains an inference-bound call
        result.

        Without an explicit signature the binding trips
        ``-Wmissing-signatures`` under ``-Wall -Werror``; the
        literalizer cannot synthesize a signature because the call's
        return type is not known at render time.
        """
        return ("{-# OPTIONS_GHC -Wno-missing-signatures #-}",)

    @cached_property
    def _preamble(self) -> _PreambleSetup:
        """Shared preamble setup bundle."""
        return _build_preamble_setup(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
            integer_format=self.integer_format,
            is_explicit=self._string_fmts.is_explicit,
            type_name=self.type_name,
            constructor_prefix=self.constructor_prefix,
            emit_num=self.numeric_style.name != "EXPLICIT",
            indent=self.indent,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble for Haskell imports.

        Under :attr:`json_type` every temporal value is folded into the
        JSON text as an ISO-8601 string and every string ships inside
        that same JSON literal, so the per-scalar Haskell extension
        directives and imports that the configured ``date_format`` /
        ``datetime_format`` would otherwise add do not apply.
        """
        if self._json_type_active:
            return {}
        return self._preamble.scalar_preamble

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Haskell needs none)."""
        return {}

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines for Haskell data declarations.

        Under :attr:`json_type` the body preamble is reduced to the
        ``Data.Aeson`` and ``Data.Text.Encoding`` imports needed by the
        ``eitherDecodeStrict (encodeUtf8 ...)`` rendering, so the custom
        ``Val`` algebraic type and its ``Num`` / ``IsString`` instances
        are not emitted.
        """
        if self._json_type_active:
            return _aeson_value_body_preamble
        return self._preamble.compute_body_preamble

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Callable that returns Haskell stub declarations for a call."""
        stub_type_name = "Value" if self._json_type_active else self.type_name
        return _build_haskell_call_stub(
            type_name=stub_type_name,
            curried=isinstance(self.call_style.value, CommandCallStyle),
        )

    @cached_property
    def format_call_arg(self) -> Callable[[Value, str], str]:
        """Callable that rewrites a formatted direct call argument.

        Curried calls parenthesize each argument so that constructor
        applications (``HInt 1``) are not parsed as additional arguments
        to the outer call.
        """
        if self._json_type_active:
            return _format_haskell_json_call_arg
        if isinstance(self.call_style.value, CommandCallStyle):
            return _haskell_format_call_arg
        return identity_call_arg

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[
        [Sequence[str], Sequence[str], StubReturn, Sequence[Value]],
        tuple[str, ...],
    ]:
        """Callable that returns preamble stub declarations."""
        return _haskell_call_preamble_stub

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
