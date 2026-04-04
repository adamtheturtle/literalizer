"""Dhall language specification."""

import datetime
import enum
import functools
import re
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
from literalizer._formatters.format_strings import (
    escape_control_chars,
)
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
from literalizer.exceptions import EmptyDictKeyError

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

_IDENTIFIER_RE = re.compile(pattern=r"^[A-Za-z_][A-Za-z0-9_/\-]*$")

_DHALL_UNESCAPE_RE = re.compile(pattern=r"\\([$\"\\nrt]|u\{([0-9A-Fa-f]+)\})")


def _unescape_dhall_string(value: str) -> str:
    """Reverse Dhall double-quoted string escapes to produce raw
    content.
    """
    _simple_escapes = {
        "$": "$",
        '"': '"',
        "\\": "\\",
        "n": "\n",
        "r": "\r",
        "t": "\t",
    }

    def _replace(match: re.Match[str]) -> str:
        """Replace a single escape sequence with its raw character."""
        hex_digits: str | None = match.group(2)
        if hex_digits is not None:
            return chr(int(hex_digits, base=16))
        return _simple_escapes[match.group(1)]

    return _DHALL_UNESCAPE_RE.sub(repl=_replace, string=value)


@beartype
def _format_dhall_integer(value: int) -> str:
    """Format an integer for Dhall.

    Dhall distinguishes ``Natural`` (non-negative, no prefix) from
    ``Integer`` (signed, requires ``+`` or ``-`` prefix).  To keep
    lists type-homogeneous we always emit the ``Integer`` form.
    """
    if value >= 0:
        return f"+{value}"
    return f"{value}"


@beartype
def _format_dhall_string(value: str) -> str:
    r"""Format a string for Dhall using backslash escaping.

    Escapes backslashes, double quotes, dollar signs (Dhall uses
    ``${...}`` for interpolation), newlines, tabs, and C0 control
    characters, then wraps the result in double quotes.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("$", "\\$")
        .replace("\r", "\\r")
        .replace("\n", "\\n")
        .replace("\t", "\\t")
    )
    escaped = escape_control_chars(value=escaped, fmt="\\u{{{:04X}}}")
    return f'"{escaped}"'


@beartype
def _format_dhall_dict_entry(key: str, _val: Value, value: str) -> str:
    """Format a Dhall record entry as ``key = value``.

    If the key is a valid Dhall simple label (letter or underscore
    followed by letters, digits, hyphens, underscores, or slashes),
    the quotes are stripped for idiomatic bare output.  Otherwise the
    key is wrapped in backticks, which Dhall uses for non-identifier
    labels.
    """
    inner = key[1:-1]
    if _IDENTIFIER_RE.match(string=inner):
        return f"{inner} = {value}"
    raw = _unescape_dhall_string(value=inner)
    if not raw:
        msg = (
            "Dhall does not support empty-string dict keys. "
            "Backtick-quoted labels must contain at least one character."
        )
        raise EmptyDictKeyError(msg)
    return f"`{raw}` = {value}"


@beartype
class Dhall(metaclass=LanguageCls):
    """Dhall language specification.

    Produces Dhall values — records for mappings, and lists for
    sequences and sets — following `Dhall <https://dhall-lang.org/>`_
    syntax.

    Dhall is a programmable configuration language that is not
    Turing-complete.  It supports records (``{ key = value }``), lists
    (``[1, 2, 3]``), ``Text``, ``Natural``, ``Double``, and ``Bool``
    types.

    Dhall has no ``null`` type; ``null`` values are rendered as the
    empty string ``""``.

    Dates and datetimes are rendered as quoted ISO 8601 strings because
    Dhall has no native date type.

    Empty-string dict keys raise
    :class:`~literalizer.exceptions.EmptyDictKeyError` because Dhall's
    backtick-quoted labels must contain at least one character.
    """

    extension = ".dhall"
    pygments_name = "text"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_empty_dict_keys = False

    class DateFormats(enum.Enum):
        """Date format options for Dhall."""

        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Dhall."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
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
        """Sequence type options for Dhall."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
            supports_heterogeneity=False,
            single_element_trailing_comma=False,
            supports_trailing_comma=True,
            empty_sequence="[] : List {}",
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=True,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Dhall."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="["),
            close="]",
            empty_set="[] : List {}",
            preamble_lines=(),
            set_opener_template="",
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        LINE = CommentConfig(
            prefix="--",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        LET = DeclarationStyleConfig(
            formatter=variable_formatter(
                template="let {name} = {value} in {name}",
            ),
            supports_redefinition=False,
        )

    class DictEntryStyles(enum.Enum):
        """Dict entry style options."""

        DEFAULT = "default"

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = "default"

    class EmptyDictKey(enum.Enum):
        """Empty dict key options.

        Dhall backtick-quoted labels must contain at least one character,
        so empty-string dict keys always raise
        :class:`~literalizer.exceptions.EmptyDictKeyError`.
        """

        ERROR = "error"

    class FloatFormats(enum.Enum):
        """Float format options."""

        REPR = enum.member(
            value=functools.partial(
                format_float_repr,
                inf_literal="Infinity",
                neg_inf_literal="-Infinity",
                nan_literal="NaN",
            )
        )
        SCIENTIFIC = enum.member(
            value=functools.partial(
                format_float_scientific,
                inf_literal="Infinity",
                neg_inf_literal="-Infinity",
                nan_literal="NaN",
            )
        )
        FIXED = enum.member(
            value=functools.partial(
                format_float_fixed,
                inf_literal="Infinity",
                neg_inf_literal="-Infinity",
                nan_literal="NaN",
            )
        )

        def __call__(self, value: float, /) -> str:
            """Format a float."""
            return self.value(value=value)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = "none"

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = "none"

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = "double"

    class TrailingCommas(enum.Enum):
        """Trailing comma options."""

        YES = TrailingCommaConfig(multiline_trailing_comma=True)
        NO = TrailingCommaConfig(multiline_trailing_comma=False)

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = "semicolon"

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    class VariableTypeHints(enum.Enum):
        """Variable type hint options."""

        AUTO = "auto"

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
    line_endings = LineEndings

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.LINE,
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
        line_ending: LineEndings = LineEndings.SEMICOLON,
        indent: str = "  ",
    ) -> None:
        """Initialize Dhall language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = '""'
        self.true_literal = "True"
        self.false_literal = "False"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=_format_dhall_dict_entry,
            empty_dict="{=}",
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _format_dhall_string
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = _format_dhall_integer
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
                open_str="{",
                close="}",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            _format_dhall_dict_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = self.skip_null_dict_values = False
        self.element_separator = ", "
        self.supports_collection_comments = True
        self.supports_scalar_before_comments = True
        self.supports_scalar_inline_comments = False
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            variable_formatter(
                template="let {name} = {value} in {name}",
            )
        )
        self.static_preamble: Sequence[str] = ()
        self.static_body_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.scalar_body_preamble: dict[type, tuple[str, ...]] = {}
        self.compute_body_preamble: Callable[
            [frozenset[type], Value], tuple[str, ...]
        ] = body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
        )

        self.special_float_preamble: tuple[str, ...] = ()
        self.type_hint_collection_preamble_lines = no_type_hint_preamble
