"""Gleam language specification."""

import datetime
import enum
import functools
import math
from collections.abc import Callable
from types import MappingProxyType
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_dates import (
    format_date_iso,
    format_datetime_iso,
)
from literalizer._formatters.format_entries import (
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
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
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    no_type_hint_preamble,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Sequence


@beartype
def _gleam_nonneg_only(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap *base* so negative values fall back to decimal.

    Gleam does not support negative hex/octal/binary literals.
    """

    @beartype
    def _format(value: int) -> str:
        """Format an integer, falling back to decimal for negatives."""
        if value < 0:
            return str(object=value)
        return base(value)

    return _format


@beartype
def _format_gleam_date_iso(value: datetime.date) -> str:
    """Format a date as a Gleam ``GStr`` constructor via ISO 8601."""
    return f"GStr({format_date_iso(value=value)})"


@beartype
def _format_gleam_datetime_iso(value: datetime.datetime) -> str:
    """Format a datetime as a Gleam ``GStr`` constructor via ISO 8601."""
    return f"GStr({format_datetime_iso(value=value)})"


@beartype
def _format_gleam_bytes_hex(value: bytes) -> str:
    """Format bytes as a Gleam ``GStr`` hex constructor."""
    return f"GStr({format_bytes_hex(value=value)})"


@beartype
def _format_gleam_bytes_base64(value: bytes) -> str:
    """Format bytes as a Gleam ``GStr`` base64 constructor."""
    return f"GStr({format_bytes_base64(value=value)})"


@beartype
def _format_gleam_string(value: str) -> str:
    """Format a string as a Gleam ``GStr`` constructor."""
    escaped = format_string_backslash(value=value)
    return f"GStr({escaped})"


@beartype
def _format_gleam_integer_decimal(value: int) -> str:
    """Format an integer as a Gleam ``GInt`` constructor."""
    return f"GInt({value})"


def _gleam_integer_wrapper(
    base: Callable[[int], str],
) -> Callable[[int], str]:
    """Wrap a base integer formatter to produce ``GInt`` constructors.

    Gleam does not support negative hex/octal/binary literals, so the
    *base* formatter handles negatives by falling back to decimal.
    """

    @beartype
    def _format(value: int) -> str:
        """Format an integer with a ``GInt`` constructor."""
        return f"GInt({base(value)})"

    return _format


def _gleam_float_wrapper(
    inner: Callable[[float], str],
    *,
    inf_literal: str = "GFloat(todo)",
    neg_inf_literal: str = "GFloat(todo)",
    nan_literal: str = "GFloat(todo)",
) -> Callable[[float], str]:
    """Wrap a float formatter to produce ``GFloat`` constructors."""

    @beartype
    def _format(value: float) -> str:
        """Format a float with a ``GFloat`` constructor."""
        if math.isinf(value):
            return neg_inf_literal if value < 0 else inf_literal
        if math.isnan(value):
            return nan_literal
        return f"GFloat({inner(value)})"

    return _format


@beartype
def _gleam_dict_entry(key: str, _val: Value, value: str) -> str:
    """Format a dict entry as a hash tuple with a plain-string key.

    Dict keys are ``String``, not ``GVal``, so the ``GStr(...)``
    constructor must be stripped from the formatted key.
    """
    key = key.removeprefix("GStr(").removesuffix(")")
    return f"#({key}, {value})"


@beartype
class Gleam(metaclass=LanguageCls):
    """Gleam language specification.

    The generated output uses custom constructors (``GNull``, ``GBool``,
    ``GList``, ``GDict``, ``GSet``) that are **not** built-in Gleam types.
    To compile the generated code, a ``GVal`` custom type is emitted in
    the body preamble:

    .. code-block:: gleam

       type GVal {
         GNull
         GBool(Bool)
         GInt(Int)
         GFloat(Float)
         GStr(String)
         GList(List(GVal))
         GDict(List(#(String, GVal)))
         GSet(List(GVal))
       }

    The body preamble automatically emits only the constructors that are
    actually used by the data.

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
    """

    extension = ".gleam"
    pygments_name = "gleam"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True

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

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_gleam_bytes_hex)
        BASE64 = enum.member(value=_format_gleam_bytes_base64)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Gleam."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="GList(["),
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
        )
        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="#("),
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
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Gleam."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="GSet(["),
            close="])",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
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
            formatter=variable_formatter(template="let {name} = {value}"),
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

    class FloatFormats(enum.Enum):
        """Float format options."""

        REPR = enum.member(
            value=_gleam_float_wrapper(
                inner=functools.partial(
                    format_float_repr,
                    inf_literal="UNREACHABLE",
                    neg_inf_literal="UNREACHABLE",
                    nan_literal="UNREACHABLE",
                ),
            )
        )
        SCIENTIFIC = enum.member(
            value=_gleam_float_wrapper(
                inner=functools.partial(
                    format_float_scientific,
                    inf_literal="UNREACHABLE",
                    neg_inf_literal="UNREACHABLE",
                    nan_literal="UNREACHABLE",
                ),
            )
        )
        FIXED = enum.member(
            value=_gleam_float_wrapper(
                inner=functools.partial(
                    format_float_fixed,
                    inf_literal="UNREACHABLE",
                    neg_inf_literal="UNREACHABLE",
                    nan_literal="UNREACHABLE",
                ),
            )
        )

        def __call__(self, value: float, /) -> str:
            """Format a float."""
            formatter: Callable[[float], str] = self.value
            return formatter(value)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": _format_gleam_integer_decimal,
                "UNDERSCORE": _gleam_integer_wrapper(
                    base=format_integer_underscore,
                ),
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": _gleam_integer_wrapper(
                    base=_gleam_nonneg_only(base=format_integer_hex),
                ),
                "UNDERSCORE": _gleam_integer_wrapper(
                    base=_gleam_nonneg_only(base=format_integer_hex),
                ),
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": _gleam_integer_wrapper(
                    base=_gleam_nonneg_only(base=format_integer_octal),
                ),
                "UNDERSCORE": _gleam_integer_wrapper(
                    base=_gleam_nonneg_only(base=format_integer_octal),
                ),
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": _gleam_integer_wrapper(
                    base=_gleam_nonneg_only(base=format_integer_binary),
                ),
                "UNDERSCORE": _gleam_integer_wrapper(
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

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

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
    string_formats = StringFormats
    trailing_commas = TrailingCommas

    class LineEndings(enum.Enum):
        """Line ending options."""

        NONE = "none"

    line_endings = LineEndings

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.DOUBLE_SLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.LET,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.YES,
        line_ending: LineEndings = LineEndings.NONE,
        indent: str = "  ",
    ) -> None:
        """Initialize Gleam language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "GNull"
        self.true_literal = "GBool(True)"
        self.false_literal = "GBool(False)"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="GDict(["),
            close="])",
            format_entry=_gleam_dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _format_gleam_string
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = (
            integer_format.get_formatter(
                numeric_separator=numeric_separator,
            )
        )
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
                open_str="GDict([",
                close="])",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            _gleam_dict_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(template="let {name} = {value}")
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = dict.fromkeys(
            (
                type(None),
                bool,
                int,
                float,
                str,
                bytes,
                datetime.date,
                datetime.datetime,
                list,
                dict,
                set,
            ),
            (
                "pub type GVal {\n"
                "  GNull\n"
                "  GBool(Bool)\n"
                "  GInt(Int)\n"
                "  GFloat(Float)\n"
                "  GStr(String)\n"
                "  GList(List(GVal))\n"
                "  GDict(List(#(String, GVal)))\n"
                "  GSet(List(GVal))\n"
                "}",
            ),
        )
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
