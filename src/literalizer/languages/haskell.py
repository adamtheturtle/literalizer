"""Haskell language specification."""

import dataclasses
import datetime
import enum
import functools
import textwrap
from collections.abc import Callable, Sequence

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
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
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    date_scalar_preamble,
    no_data_preamble,
    no_type_hint_preamble,
)
from literalizer._types import Value


@beartype
def _haskell_call_preamble_stub(
    name: str,
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Emit ``OverloadedRecordDot`` when the call target contains dots."""
    if "." in name:
        return ("{-# LANGUAGE OverloadedRecordDot #-}",)
    return ()


def _build_haskell_call_stub(
    type_name: str,
) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
    """Build a call stub function that uses *type_name* for field
    types.
    """
    ret = "IO ()"
    body = "return ()"

    @beartype
    def _haskell_call_stub(
        name: str,
        params: Sequence[str],
        _stub_return: StubReturn,
        /,
    ) -> tuple[str, ...]:
        """Return Haskell stub declarations for a call name."""
        parts = name.split(sep=".")
        if len(parts) == 1:
            return (f"{parts[0]} _ = {body}",)
        root = parts[0]
        method = parts[-1]
        fields = parts[1:-1]
        if len(params) == 1:
            arg_type = type_name
        else:
            arg_type = "(" + ", ".join(type_name for _ in params) + ")"
        field_type = f"{arg_type} -> {ret}"
        if not fields:
            cls = root.capitalize() + "Type_"
            return (
                f"data {cls} = {cls} {{ {method} :: {field_type} }}",
                f"{root} = {cls} {{ {method} = \\_ -> {body} }}",
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
        # Build nested construction from inside out.
        construction = f"{inner_cls} {{ {method} = \\_ -> {body} }}"
        for i in range(len(fields) - 2, -1, -1):
            cls = fields[i].capitalize() + "Type_"
            construction = f"{cls} {{ {fields[i + 1]} = {construction} }}"
        construction = f"{root_cls} {{ {fields[0]} = {construction} }}"
        lines.append(f"{root} = {construction}")
        return tuple(lines)

    return _haskell_call_stub


def _build_haskell_datetime_formatter(
    prefix: str,
) -> Callable[[datetime.datetime], str]:
    """Build a datetime formatter that produces ``{prefix}Datetime``
    constructors.
    """

    @beartype
    def _format(value: datetime.datetime) -> str:
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

    return _format


_format_datetime_haskell = _build_haskell_datetime_formatter(prefix="H")


@dataclasses.dataclass(frozen=True)
class _DateTimeFormatters:
    """Resolved date and datetime formatters."""

    format_date: Callable[[datetime.date], str]
    format_datetime: Callable[[datetime.datetime], str]


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
    if date_format_name == "HASKELL":
        fmt_date: Callable[[datetime.date], str] = date_ymd_formatter(
            template=(
                f"{constructor_prefix}Date "
                f"(fromGregorian {{year}} {{month}} {{day}})"
            ),
        )
    elif is_explicit:
        _str_pfx = f"{constructor_prefix}Str "

        @beartype
        def _explicit_date(value: datetime.date) -> str:
            """Wrap an ISO date string with the HStr constructor."""
            return f"{_str_pfx}{date_formatter(value)}"

        fmt_date = _explicit_date
    else:
        fmt_date = date_formatter

    if datetime_format_name == "HASKELL":
        fmt_datetime: Callable[[datetime.datetime], str] = (
            _build_haskell_datetime_formatter(prefix=constructor_prefix)
        )
    elif is_explicit:
        _str_pfx_dt = f"{constructor_prefix}Str "

        @beartype
        def _explicit_datetime(value: datetime.datetime) -> str:
            """Wrap an ISO datetime string with the HStr constructor."""
            return f"{_str_pfx_dt}{datetime_formatter(value)}"

        fmt_datetime = _explicit_datetime
    else:
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
    base_format_string: Callable[[str], str] = functools.partial(
        format_string_backslash_control,
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

    @beartype
    def _format_string(value: str) -> str:
        """Wrap a formatted string with the constructor prefix."""
        return f"{string_constructor}{base_format_string(value)}"

    @beartype
    def _format_bytes(data: bytes) -> str:
        """Wrap formatted bytes with the constructor prefix."""
        return f"{string_constructor}{base_format_bytes(data)}"

    @beartype
    def _format_dict_entry(
        key: str,
        _raw_value: Value,
        formatted_value: str,
    ) -> str:
        """Format a dict entry, stripping the constructor from the key."""
        clean_key = key.removeprefix(string_constructor)
        return f"({clean_key}, {formatted_value})"

    return _StringFormatters(
        format_string=_format_string,
        format_bytes=_format_bytes,
        format_dict_entry=_format_dict_entry,
        is_explicit=True,
    )


def _num_instance(
    *,
    has_int: bool,
    has_float: bool,
    type_name: str,
    constructor_prefix: str,
) -> str:
    """Build the ``Num`` instance with only relevant constructors."""
    if has_int:
        from_integer = f"    fromInteger = {constructor_prefix}Int"
    else:
        from_integer = (
            f"    fromInteger n = {constructor_prefix}Float (fromIntegral n)"
        )
    negate_parts: list[str] = []
    if has_int:
        negate_parts.append(
            f"    negate ({constructor_prefix}Int n) = "
            f"{constructor_prefix}Int (negate n)"
        )
    if has_float:
        negate_parts.append(
            f"    negate ({constructor_prefix}Float f) = "
            f"{constructor_prefix}Float (negate f)"
        )
    negate_parts.append('    negate _ = error "not implemented"')
    return "\n".join(
        [
            f"instance Num {type_name} where",
            from_integer,
            '    a + b = error "not implemented"',
            '    a * b = error "not implemented"',
            '    abs a = error "not implemented"',
            '    signum a = error "not implemented"',
            *negate_parts,
        ]
    )


def _has_microsecond_datetime(*, data: Value) -> bool:
    """Return whether *data* contains any datetime with microseconds."""
    if isinstance(data, datetime.datetime):
        return bool(data.microsecond)
    if isinstance(data, datetime.date):
        return False
    if isinstance(data, (ordereddict, dict)):
        return any(
            _has_microsecond_datetime(data=v)  # pyright: ignore[reportUnknownArgumentType]
            for v in data.values()  # pyright: ignore[reportUnknownMemberType,reportUnknownVariableType]
        )
    if isinstance(data, (list, set)):
        return any(_has_microsecond_datetime(data=v) for v in data)
    return False


def _datetime_import_items(
    *,
    has_from_gregorian: bool,
    has_microsecond: bool,
) -> list[str]:
    """Return ``Data.Time`` import names needed for datetime values."""
    items = ["UTCTime(..)"]
    if not has_from_gregorian:
        items.append("fromGregorian")
    items.append("secondsToDiffTime")
    if has_microsecond:
        items.append("picosecondsToDiffTime")
    return items


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
    include_hdate = date_format.value.type_produced is datetime.date
    include_hdatetime = (
        datetime_format.value.type_produced is datetime.datetime
    )
    date_needs_is_string = bool(
        emit_is_string and date_format.value.preamble_lines
    )
    datetime_needs_is_string = bool(
        emit_is_string and datetime_format.value.preamble_lines
    )
    # In EXPLICIT mode, ISO dates/datetimes produce HStr-wrapped strings,
    # so HStr String must appear in the data type.
    date_needs_str_explicit = bool(not emit_is_string and not include_hdate)
    datetime_needs_str_explicit = bool(
        not emit_is_string and not include_hdatetime
    )

    def _compute(types: frozenset[type], data: Value, /) -> tuple[str, ...]:
        """Return body-preamble lines for the given *types*."""
        p = constructor_prefix
        data_val_parts = [
            constructor
            for type_set, constructor in (
                (frozenset({type(None)}), f"{p}Null"),
                (frozenset({bool}), f"{p}Bool Bool"),
                (frozenset({int}), f"{p}Int Integer"),
                (frozenset({float}), f"{p}Float Double"),
                (frozenset({str, bytes}), f"{p}Str String"),
                (frozenset({list}), f"{p}List [{type_name}]"),
                (
                    frozenset({dict, ordereddict}),
                    f"{p}Map [(String, {type_name})]",
                ),
                (frozenset({set}), f"{p}Set [{type_name}]"),
            )
            if types & type_set
        ]
        import_items: list[str] = []
        if include_hdate and datetime.date in types:
            data_val_parts.append(f"{p}Date Day")
            import_items.extend(["Day", "fromGregorian"])
        if include_hdatetime and datetime.datetime in types:
            data_val_parts.append(f"{p}Datetime UTCTime")
            import_items.extend(
                _datetime_import_items(
                    has_from_gregorian="fromGregorian" in import_items,
                    has_microsecond=_has_microsecond_datetime(data=data),
                ),
            )

        needs_is_string = emit_is_string and (
            bool(types & {str, bytes})
            or (date_needs_is_string and datetime.date in types)
            or (datetime_needs_is_string and datetime.datetime in types)
        )
        needs_str_constructor = (
            bool(types & {str, bytes})
            or (date_needs_is_string and datetime.date in types)
            or (datetime_needs_is_string and datetime.datetime in types)
            or (date_needs_str_explicit and datetime.date in types)
            or (datetime_needs_str_explicit and datetime.datetime in types)
        )
        if needs_str_constructor and f"{p}Str String" not in data_val_parts:
            data_val_parts.append(f"{p}Str String")

        # Emit imports first, then data declaration, then instances.
        imports: list[str] = []
        if import_items:
            imports.append(
                "import Data.Time (" + ", ".join(import_items) + ")"
            )
        if needs_is_string:
            imports.append(is_string_import)

        instances: list[str] = []
        if needs_is_string:
            instances.append(is_string_instance)

        has_float = float in types
        has_int = int in types
        if emit_num and (has_float or has_int):
            instances.append(
                _num_instance(
                    has_int=has_int,
                    has_float=has_float,
                    type_name=type_name,
                    constructor_prefix=constructor_prefix,
                ),
            )
        if emit_num and has_float:
            instances.append(
                f"instance Fractional {type_name} where\n"
                f"    fromRational r = {p}Float (realToFrac r)\n"
                '    a / b = error "not implemented"'
            )

        lines: list[str] = imports
        lines.append(f"data {type_name} = " + " | ".join(data_val_parts))
        lines.extend(instances)
        return tuple(lines)

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
        seq_open = fixed_sequence_open(
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

    format_variable_declaration: Callable[[str, str, Value], str]
    format_variable_assignment: Callable[[str, str, Value], str]


@beartype
def _build_declaration_formatters(
    *,
    declaration_style: enum.Enum,
    sequence_format: enum.Enum,
    type_name: str,
) -> _DeclarationFormatters:
    """Build declaration/assignment formatters with type annotations."""
    base_declaration: Callable[[str, str, Value], str] = (
        declaration_style.value.formatter
    )
    raw_declared = sequence_format.value.declared_type
    sequence_declared_type = (
        raw_declared.replace("Val", type_name)
        if raw_declared is not None
        else None
    )

    @beartype
    def _haskell_declaration(name: str, value: str, data: Value) -> str:
        """Format a variable declaration with type annotation."""
        base = base_declaration(name, value, data)
        if isinstance(data, list):
            if sequence_declared_type is None:
                return base
            return f"{name} :: {sequence_declared_type}\n{base}"
        return f"{name} :: {type_name}\n{base}"

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
    is_explicit: bool,
    type_name: str,
    constructor_prefix: str,
    emit_num: bool,
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
    return _PreambleSetup(
        scalar_preamble=scalar_preamble,
        compute_body_preamble=_build_scalar_body_preamble(
            date_format=date_format,
            datetime_format=datetime_format,
            is_string_import="import Data.String (IsString(fromString))",
            is_string_instance=(
                f"instance IsString {type_name} where\n"
                f"    fromString = {constructor_prefix}Str"
            ),
            type_name=type_name,
            constructor_prefix=constructor_prefix,
            emit_is_string=not is_explicit,
            emit_num=emit_num,
        ),
    )


@beartype
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
    """

    extension = ".hs"
    pygments_name = "haskell"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True
    supports_dotted_calls = True

    indent_closing_delimiter = True
    element_separator = ", "
    skip_null_dict_values = False
    supports_collection_comments = True
    supports_scalar_before_comments = False
    supports_scalar_inline_comments = True
    statement_terminator = ""
    static_preamble: Sequence[str] = ()
    static_body_preamble: Sequence[str] = ()
    special_float_preamble: tuple[str, ...] = ()

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
            sequence_open=fixed_sequence_open(open_str="HList ["),
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
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
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
        )

    class SetFormats(enum.Enum):
        """Set type options for Haskell."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="HSet ["),
            close="]",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
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
            formatter=variable_formatter(template="{name} = {value}"),
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

        OVERLOADED = "overloaded"
        EXPLICIT = "explicit"

    numeric_styles = NumericStyles

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"
        EXPLICIT = "explicit"

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
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Haskell call style options."""

        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Haskell variable binding in a module."""
        preamble = "\n".join(body_preamble)
        if not variable_name:
            # Call mode: bare expressions are not valid at module
            # top level in Haskell, so wrap them in ``main``.
            indented = textwrap.indent(text=content, prefix="    ")
            return (
                "module Check where\n"
                + preamble
                + "\nmain :: IO ()\nmain = do\n"
                + indented
                + "\n    pure ()"
            )
        return "module Check where\n" + preamble + "\n" + content

    @staticmethod
    def wrap_combined_in_file(
        declaration: str,
        assignment: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Haskell declaration + assignment in a module."""
        return Haskell.wrap_in_file(
            content=declaration + "\n" + assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.HASKELL,
        datetime_format: DatetimeFormats = DatetimeFormats.HASKELL,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_DASH,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        numeric_style: NumericStyles = NumericStyles.OVERLOADED,
        string_format: StringFormats = StringFormats.EXPLICIT,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        call_style: CallStyles = CallStyles.POSITIONAL,
        indent: str = "    ",
        type_name: str = "Val",
        constructor_prefix: str = "H",
    ) -> None:
        """Initialize Haskell language specification."""
        # Enum selections.
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.set_format = set_format
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_entry_style = dict_entry_style
        self.dict_format = dict_format
        self.float_format = float_format
        self.integer_format = integer_format
        self.numeric_literal_suffix = numeric_literal_suffix
        self.numeric_separator = numeric_separator
        self.numeric_style = numeric_style
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending

        # Literals.
        self.null_literal: str = f"{constructor_prefix}Null"
        self.true_literal: str = f"{constructor_prefix}Bool True"
        self.false_literal: str = f"{constructor_prefix}Bool False"

        # Sequence.
        seq_setup = _build_sequence_setup(
            sequence_format=sequence_format,
            constructor_prefix=constructor_prefix,
        )
        self.sequence_format_config: SequenceFormatConfig = (
            seq_setup.format_config
        )
        self.sequence_open: Callable[[list[Value]], str] = (
            seq_setup.sequence_open
        )

        # Set.
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=fixed_set_open(
                open_str=f"{constructor_prefix}Set [",
            ),
        )

        # String / bytes / dict entry.
        string_fmts = _build_string_formatters(
            string_format_name=string_format.name,
            constructor_prefix=constructor_prefix,
            base_format_bytes=bytes_format,
        )
        self.format_string: Callable[[str], str] = string_fmts.format_string
        self.format_bytes: Callable[[bytes], str] = string_fmts.format_bytes

        # Dict / ordered map.
        _map_open = f"{constructor_prefix}Map ["
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(open_str=_map_open),
            close="]",
            format_entry=string_fmts.format_dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                ordered_map_open=fixed_dict_open(open_str=_map_open),
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            string_fmts.format_dict_entry
        )

        # Trailing comma.
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value

        # Date / datetime.
        date_fmts = _build_date_formatters(
            date_format_name=date_format.name,
            date_formatter=date_format,
            datetime_format_name=datetime_format.name,
            datetime_formatter=datetime_format,
            constructor_prefix=constructor_prefix,
            is_explicit=string_fmts.is_explicit,
        )
        self.format_date: Callable[[datetime.date], str] = (
            date_fmts.format_date
        )
        self.format_datetime: Callable[[datetime.datetime], str] = (
            date_fmts.format_datetime
        )

        # Scalar formatters.
        _explicit_numeric = numeric_style.name == "EXPLICIT"
        if _explicit_numeric:
            _int_prefix = f"{constructor_prefix}Int "
            _float_prefix = f"{constructor_prefix}Float "
            _base_format_float: Callable[[float], str] = float_format
            _base_format_integer: Callable[[int], str] = integer_format

            @beartype
            def _wrap_integer(value: int) -> str:
                """Wrap an integer with the constructor prefix."""
                formatted = _base_format_integer(value)
                if value < 0:
                    return f"{_int_prefix}({formatted})"
                return f"{_int_prefix}{formatted}"

            @beartype
            def _wrap_float(value: float) -> str:
                """Wrap a float with the constructor prefix."""
                formatted = _base_format_float(value)
                return f"{_float_prefix}({formatted})"

            self.format_float: Callable[[float], str] = _wrap_float
            self.format_integer: Callable[[int], str] = _wrap_integer
        else:
            self.format_float = float_format
            self.format_integer = integer_format
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
        )
        self.comment_config: CommentConfig = comment_format.value

        self.indent = indent

        # Declaration.
        decl_fmts = _build_declaration_formatters(
            declaration_style=declaration_style,
            sequence_format=sequence_format,
            type_name=type_name,
        )
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            decl_fmts.format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            decl_fmts.format_variable_assignment
        )

        # Preamble.
        preamble = _build_preamble_setup(
            date_format=date_format,
            datetime_format=datetime_format,
            is_explicit=string_fmts.is_explicit,
            type_name=type_name,
            constructor_prefix=constructor_prefix,
            emit_num=not _explicit_numeric,
        )
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            preamble.scalar_preamble
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = preamble.compute_body_preamble
        self.data_dependent_preamble = no_data_preamble
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.call_style_config: CallStyle | None = call_style.value
        self.format_call_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = _build_haskell_call_stub(
            type_name=type_name,
        )
        self.format_call_preamble_stub: Callable[
            [str, Sequence[str], StubReturn], tuple[str, ...]
        ] = _haskell_call_preamble_stub
