"""Haskell language specification."""

import datetime
import enum
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import (
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value


@beartype
def _format_date_haskell(value: datetime.date) -> str:
    """Format a date as a Haskell ``HDate`` constructor."""
    return f"HDate (fromGregorian {value.year} {value.month} {value.day})"


@beartype
def _format_datetime_haskell(value: datetime.datetime) -> str:
    """Format a datetime as a Haskell ``HDatetime`` constructor.

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
        f"HDatetime (UTCTime "
        f"(fromGregorian {value.year} {value.month} {value.day}) "
        f"({time_part}))"
    )


@beartype
def _format_haskell_dict_entry(key: str, value: str) -> str:
    """Format a Haskell dict entry as a tuple pair."""
    return f"({key}, {value})"


@beartype
def _format_haskell_ordered_map_entry(key: str, value: str) -> str:
    """Format a Haskell ordered-map entry as a tuple pair."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a Haskell variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Haskell variable assignment."""
    return f"{name} = {value}"


_string_format: Callable[[str], str] = format_string_backslash

_is_string_import = "import Data.String (IsString(fromString))"

_is_string_instance = "instance IsString Val where\n    fromString = HStr"

_num_instance = (
    "instance Num Val where\n"
    "    fromInteger = HInt\n"
    '    a + b = error "not implemented"\n'
    '    a * b = error "not implemented"\n'
    '    abs a = error "not implemented"\n'
    '    signum a = error "not implemented"\n'
    "    negate (HInt n) = HInt (negate n)\n"
    "    negate (HFloat f) = HFloat (negate f)\n"
    '    negate _ = error "not implemented"'
)

_fractional_instance = (
    "instance Fractional Val where\n"
    "    fromRational r = HFloat (realToFrac r)\n"
    '    a / b = error "not implemented"'
)


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
    """

    extension = ".hs"
    pygments_name = "haskell"

    class DateFormats(enum.Enum):
        """Date format options for Haskell."""

        HASKELL = DateFormatConfig(formatter=_format_date_haskell)
        ISO = DateFormatConfig(
            formatter=format_date_iso,
            preamble_lines=(
                "{-# LANGUAGE OverloadedStrings #-}",
                _is_string_import,
                _is_string_instance,
            ),
            produces_string=True,
        )

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Haskell."""

        HASKELL = DatetimeFormatConfig(formatter=_format_datetime_haskell)
        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
            preamble_lines=(
                "{-# LANGUAGE OverloadedStrings #-}",
                _is_string_import,
                _is_string_instance,
            ),
            produces_string=True,
        )

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

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
            empty_sequence=None,
            preamble_lines=(),
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

        ASSIGN = "assign"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        NO = "no"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        NONE = "none"

    variable_type_hints_formats = VariableTypeHints
    declaration_styles = DeclarationStyles
    dict_formats = DictFormats
    integer_formats = IntegerFormats
    numeric_separators = NumericSeparators
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.HASKELL,
        datetime_format: DatetimeFormats = DatetimeFormats.HASKELL,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.DOUBLE_DASH,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
    ) -> None:
        """Initialize Haskell language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "HNull"
        self.true_literal = "HBool True"
        self.false_literal = "HBool False"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="HMap ["),
            close="]",
            format_entry=_format_haskell_dict_entry,
            empty_dict=None,
            preamble_lines=(),
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_format = comment_format
        self.declaration_style = declaration_style
        self.dict_format = dict_format
        self.integer_format = integer_format
        self.numeric_separator = numeric_separator
        self.string_format = string_format
        self.trailing_comma = trailing_comma
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="HMap [",
                close="]",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_haskell_ordered_map_entry
        )
        self.multiline_close_indent = "    "
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        _overloaded_strings = ("{-# LANGUAGE OverloadedStrings #-}",)
        self.scalar_preamble: dict[type, tuple[str, ...]] = {
            str: (
                *_overloaded_strings,
                _is_string_import,
                _is_string_instance,
            ),
            bytes: (
                *_overloaded_strings,
                _is_string_import,
                _is_string_instance,
            ),
            int: (_num_instance,),
            float: (_num_instance, _fractional_instance),
            **{
                t: p
                for t, p in (
                    (datetime.date, date_format.value.preamble_lines),
                    (datetime.datetime, datetime_format.value.preamble_lines),
                )
                if p
            },
        }
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
