"""Haskell language specification."""

import dataclasses
import datetime
import enum
import functools
from collections.abc import Callable
from typing import TYPE_CHECKING

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
    CallStyleConfig,
    CallStyleKind,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
    date_scalar_preamble,
    no_call_stub,
    no_type_hint_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


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
) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
    """Build a callable that computes body-preamble lines for Haskell.

    The callable receives the set of types present in the data and the
    original data value, and returns only the imports, the type
    declaration, and typeclass instances that are actually needed.

    The returned lines are ordered: imports first, then the data type,
    then typeclass instances.
    """
    include_hdate = date_format.value.type_produced is datetime.date
    include_hdatetime = (
        datetime_format.value.type_produced is datetime.datetime
    )
    date_needs_is_string = bool(date_format.value.preamble_lines)
    datetime_needs_is_string = bool(datetime_format.value.preamble_lines)

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

        needs_is_string = (
            bool(types & {str, bytes})
            or (date_needs_is_string and datetime.date in types)
            or (datetime_needs_is_string and datetime.datetime in types)
        )
        if needs_is_string and f"{p}Str String" not in data_val_parts:
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
        if has_float or has_int:
            instances.append(
                _num_instance(
                    has_int=has_int,
                    has_float=has_float,
                    type_name=type_name,
                    constructor_prefix=constructor_prefix,
                ),
            )
        if has_float:
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


@beartype
class Haskell(metaclass=LanguageCls):
    """Haskell language specification.

    The generated output uses custom constructors (``HNull``, ``HBool``,
    ``HList``, ``HMap``, ``HSet``) that are **not** built-in Haskell types.
    To compile the generated code, define a ``Val`` ADT and typeclass
    instances in the consuming module:

    .. code-block:: haskell

       {-# LANGUAGE OverloadedStrings #-}

       import Data.String (IsString(fromString))

       data Val
         = HNull
         | HBool Bool
         | HInt Integer
         | HFloat Double
         | HStr String
         | HList [Val]
         | HMap [(String, Val)]
         | HSet [Val]

       instance IsString Val where
           fromString = HStr

       instance Num Val where
           fromInteger = HInt
           negate (HInt n)   = HInt (negate n)
           negate (HFloat f) = HFloat (negate f)
           ...

       instance Fractional Val where
           fromRational r = HFloat (realToFrac r)
           ...

    ``OverloadedStrings`` lets bare string literals like ``"hi"`` resolve to
    ``HStr "hi"`` via ``IsString``, and the ``Num`` / ``Fractional`` instances
    let numeric literals resolve to ``HInt`` / ``HFloat``.

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
    supports_call = False

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

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

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

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

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

    call_styles = CallStyles

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap a Haskell variable binding in a module."""
        del variable_name
        preamble = "\n".join(body_preamble)
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
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "    ",
        type_name: str = "Val",
        constructor_prefix: str = "H",
    ) -> None:
        """Initialize Haskell language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal: str = f"{constructor_prefix}Null"
        self.true_literal: str = f"{constructor_prefix}Bool True"
        self.false_literal: str = f"{constructor_prefix}Bool False"
        fmt = sequence_format.value
        if sequence_format.name == "LIST":
            _seq_open = fixed_sequence_open(
                open_str=f"{constructor_prefix}List [",
            )
            self.sequence_format_config: SequenceFormatConfig = (
                dataclasses.replace(fmt, sequence_open=_seq_open)
            )
            self.sequence_open: Callable[[list[Value]], str] = _seq_open
        else:
            self.sequence_format_config = fmt
            self.sequence_open = fmt.sequence_open
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = dataclasses.replace(
            set_format.value,
            set_open=fixed_set_open(
                open_str=f"{constructor_prefix}Set [",
            ),
        )

        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(
                open_str=f"{constructor_prefix}Map [",
            ),
            close="]",
            format_entry=tuple_dict_entry(
                format_value=passthrough_sequence_entry
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        if date_format.name == "HASKELL":
            self.format_date: Callable[[datetime.date], str] = (
                date_ymd_formatter(
                    template=(
                        f"{constructor_prefix}Date "
                        f"(fromGregorian {{year}} {{month}} {{day}})"
                    ),
                )
            )
        else:
            self.format_date = date_format
        if datetime_format.name == "HASKELL":
            self.format_datetime: Callable[[datetime.datetime], str] = (
                _build_haskell_datetime_formatter(
                    prefix=constructor_prefix,
                )
            )
        else:
            self.format_datetime = datetime_format
        self.format_string: Callable[[str], str] = functools.partial(
            format_string_backslash_control,
            control_char_fmt="\\x{:02x}",
        )
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = integer_format
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_set_entry
        )
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_entry_style = dict_entry_style
        self.dict_format = dict_format
        self.float_format = float_format
        self.integer_format = integer_format
        self.numeric_literal_suffix = numeric_literal_suffix
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.line_ending = line_ending
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str=f"{constructor_prefix}Map [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            tuple_dict_entry(format_value=passthrough_sequence_entry)
        )
        self.indent = indent
        self.indent_closing_delimiter = True
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = True
        _base_declaration = declaration_style.value.formatter
        _raw_declared = sequence_format.value.declared_type
        _sequence_declared_type = (
            _raw_declared.replace("Val", type_name)
            if _raw_declared is not None
            else None
        )

        @beartype
        def _haskell_declaration(name: str, value: str, data: Value) -> str:
            """Format a variable declaration with type annotation."""
            base = _base_declaration(name, value, data)
            if isinstance(data, list):
                if _sequence_declared_type is None:
                    return base
                return f"{name} :: {_sequence_declared_type}\n{base}"
            return f"{name} :: {type_name}\n{base}"

        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _haskell_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="{name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        _overloaded_strings = ("{-# LANGUAGE OverloadedStrings #-}",)
        self.scalar_preamble: dict[type, tuple[str, ...]] = (
            date_scalar_preamble(
                date_format=date_format,
                datetime_format=datetime_format,
                extra={
                    str: _overloaded_strings,
                    bytes: _overloaded_strings,
                },
            )
        )

        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = _build_scalar_body_preamble(
            date_format=date_format,
            datetime_format=datetime_format,
            is_string_import="import Data.String (IsString(fromString))",
            is_string_instance=(
                f"instance IsString {type_name} where\n"
                f"    fromString = {constructor_prefix}Str"
            ),
            type_name=type_name,
            constructor_prefix=constructor_prefix,
        )
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.POSITIONAL,
        )
        self.statement_terminator = ""
        self.format_call_stub = no_call_stub
        self.format_call_preamble_stub = no_call_stub
