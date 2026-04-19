"""Dhall language specification."""

import dataclasses
import datetime
import enum
import re
from collections.abc import Callable, Sequence
from functools import cached_property
from typing import ClassVar

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
    CallStyle,
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
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    no_call_stub,
    no_data_preamble,
    no_type_hint_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value
from literalizer.exceptions import InvalidDictKeyError

_IDENTIFIER_RE = re.compile(pattern=r"^[A-Za-z_][A-Za-z0-9_/\-]*$")

_DHALL_UNESCAPE_RE = re.compile(pattern=r"\\([$\"\\nrt]|u\{([0-9A-Fa-f]+)\})")

# Dhall backtick labels allow printable ASCII excluding backtick:
# %x20-5F / %x61-7E (space through underscore, a-z plus {|}~).
_BACKTICK_LABEL_RE = re.compile(pattern=r"^[\x20-\x5f\x61-\x7e]+$")


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
def _format_dhall_dict_entry(
    key: str,
    _raw_value: Value,
    formatted_value: str,
) -> str:
    """Format a Dhall record entry as ``key = value``.

    If the key is a valid Dhall simple label (letter or underscore
    followed by letters, digits, hyphens, underscores, or slashes),
    the quotes are stripped for idiomatic bare output.  Otherwise the
    key is wrapped in backticks, which Dhall uses for non-identifier
    labels.
    """
    inner = key[1:-1]
    if _IDENTIFIER_RE.match(string=inner):
        return f"{inner} = {formatted_value}"
    raw = _unescape_dhall_string(value=inner)
    if not raw or not _BACKTICK_LABEL_RE.match(string=raw):
        msg = (
            f"Dhall does not support the dict key {key}. "
            "Backtick-quoted labels must be non-empty and contain only "
            "printable ASCII (no backticks or control characters)."
        )
        raise InvalidDictKeyError(msg)
    return f"`{raw}` = {formatted_value}"


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
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

    Dict keys that cannot be represented as Dhall backtick-quoted labels
    raise :class:`~literalizer.exceptions.InvalidDictKeyError`.  This
    includes empty keys and keys containing control characters or
    backticks, since Dhall labels only allow printable ASCII.
    """

    extension = ".dhall"
    pygments_name = None
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = False
    supports_variable_names = True
    supports_dotted_calls = True

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
            declared_type=None,
        )

    class SetFormats(enum.Enum):
        """Set type options for Dhall."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str="["),
            close="]",
            empty_set="[] : List {}",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
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

        DEFAULT = enum.auto()

    class DictFormats(enum.Enum):
        """Dict/map format options."""

        DEFAULT = enum.auto()

    class EmptyDictKey(enum.Enum):
        """Empty dict key options.

        Dhall backtick-quoted labels must be non-empty and contain only
        printable ASCII, so unsupported dict keys always raise
        :class:`~literalizer.exceptions.InvalidDictKeyError`.
        """

        ERROR = enum.auto()

    class FloatFormats(
        FloatSpecialsMixin,
        enum.Enum,
        positive_infinity="Infinity",
        negative_infinity="-Infinity",
        nan="NaN",
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

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
    numeric_styles = NumericStyles
    string_formats = StringFormats
    trailing_commas = TrailingCommas
    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Dhall call style options."""

    call_styles = CallStyles

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

    date_format: DateFormats = DateFormats.ISO
    datetime_format: DatetimeFormats = DatetimeFormats.ISO
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.LIST
    set_format: SetFormats = SetFormats.SET
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.LINE
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
    line_ending: LineEndings = LineEndings.SEMICOLON
    indent: str = "  "

    null_literal: ClassVar[str] = '""'
    true_literal: ClassVar[str] = "True"
    false_literal: ClassVar[str] = "False"
    indent_closing_delimiter: ClassVar[bool] = False
    skip_null_dict_values: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = True
    supports_scalar_inline_comments: ClassVar[bool] = False
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()
    call_style_config: ClassVar[CallStyle | None] = None

    @cached_property
    def format_string(self) -> Callable[[str], str]:
        """Format a string value as a quoted literal."""
        return _format_dhall_string

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Format an int value as a literal."""
        return _format_dhall_integer

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Format one ordered-map entry."""
        return _format_dhall_dict_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="let {name} = {value} in {name}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Return preamble lines for empty-collection type hints."""
        return no_type_hint_preamble

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[str, Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def sequence_format_config(self) -> SequenceFormatConfig:
        """Configuration for the chosen sequence format."""
        return self.sequence_format.value

    @cached_property
    def set_format_config(self) -> SetFormatConfig:
        """Configuration for the chosen set format."""
        return self.set_format.value

    @cached_property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence."""
        return self.sequence_format.value.sequence_open

    @cached_property
    def dict_format_config(self) -> DictFormatConfig:
        """Configuration for dict formatting."""
        return DictFormatConfig(
            dict_open=fixed_dict_open(open_str="{"),
            close="}",
            format_entry=_format_dhall_dict_entry,
            empty_dict="{=}",
            preamble_lines=(),
            narrowed_open=None,
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
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_dict_open(open_str="{"),
            close="}",
            preamble_lines=(),
        )

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration."""
        return self.declaration_style.value.formatter

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble (Dhall needs none)."""
        return {}

    @cached_property
    def scalar_body_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar body preamble (Dhall needs none)."""
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
