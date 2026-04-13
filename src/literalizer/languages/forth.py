"""Forth language specification."""

import base64
import datetime
import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters.collection_openers import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
)
from literalizer._formatters.format_entries import (
    passthrough_sequence_entry,
)
from literalizer._formatters.format_floats import format_float_scientific
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
    body_preamble_from_scalars,
    no_call_stub,
    no_type_hint_preamble,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence


@beartype
def _format_string_forth(value: str) -> str:
    r"""Format a string as a Forth ``s\"`` literal.

    Example: ``"hello"`` -> ``s\" hello"``.
    """
    escaped = (
        value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "\\n")
        .replace("\r", "\\r")
        .replace("\t", "\\t")
    )
    return f's\\" {escaped}"'


@beartype
def _format_float_forth(value: float) -> str:
    """Format a float as a Forth floating-point literal.

    Forth requires the ``e`` exponent marker to distinguish floats
    from integers.  Uses scientific notation so every value includes
    the marker.

    Example: ``1.5`` -> ``1.5e0``.
    """
    result = format_float_scientific(value=value)
    if "e" not in result:
        return f"{result}e0"
    return result


@beartype
def _format_date_forth(value: datetime.date) -> str:
    r"""Format a date as a Forth ``s\"`` ISO 8601 string.

    Example: ``datetime.date(2024, 1, 15)`` -> ``s\" 2024-01-15"``.
    """
    return f's\\" {value.isoformat()}"'


@beartype
def _format_datetime_forth(value: datetime.datetime) -> str:
    r"""Format a datetime as a Forth ``s\"`` ISO 8601 string.

    Example: ``datetime.datetime(2024, 1, 15, 12, 30)`` ->
    ``s\" 2024-01-15T12:30:00"``.
    """
    return f's\\" {value.isoformat()}"'


@beartype
def _format_bytes_hex_forth(value: bytes) -> str:
    r"""Format bytes as a Forth hex ``s\"`` string.

    Example: ``b"Hello"`` -> ``s\" 48656c6c6f"``.
    """
    return f's\\" {value.hex()}"'


@beartype
def _format_bytes_base64_forth(value: bytes) -> str:
    r"""Format bytes as a Forth base64 ``s\"`` string.

    Example: ``b"Hello"`` -> ``s\" SGVsbG8="``.
    """
    encoded = base64.b64encode(s=value)
    return f's\\" {encoded.decode(encoding="ascii")}"'


@beartype
def _format_forth_declaration(name: str, value: str, _data: Value) -> str:
    r"""Format a Forth colon definition.

    Example (single line): ``: my_data 42 ;``

    Example (multi-line)::

        : my_data
            s\" name" s\" Alice"
            s\" age" 30
        ;
    """
    stripped = value.strip("\n")
    if not stripped.strip():
        return f": {name} ;"
    if "\n" in stripped:
        return f": {name}\n{stripped}\n;"
    return f": {name} {stripped} ;"


@beartype
def _format_forth_dict_entry(key: str, _val: Value, value: str) -> str:
    r"""Format a dict entry as ``key value``.

    Example: ``s\" name" s\" Alice"``.
    """
    return f"{key} {value}"


@beartype
class Forth(metaclass=LanguageCls):
    """Forth language specification."""

    extension = ".fth"
    pygments_name = "forth"
    supports_default_set_element_type = False
    supports_default_sequence_element_type = False
    supports_default_dict_value_type = False
    supports_default_dict_key_type = False
    supports_default_ordered_map_value_type = False
    supports_non_printable_ascii_dict_keys = True
    supports_variable_names = True

    class DateFormats(enum.Enum):
        """Date format options."""

        ISO = DateFormatConfig(
            formatter=_format_date_forth,
            type_produced=str,
        )

    class DatetimeFormats(enum.Enum):
        """Datetime format options."""

        ISO = DatetimeFormatConfig(
            formatter=_format_datetime_forth,
            type_produced=str,
        )

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=_format_bytes_hex_forth)
        BASE64 = enum.member(value=_format_bytes_base64_forth)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options."""

        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str=""),
            close="",
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
        """Set type options."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str=""),
            close="",
            empty_set=None,
            preamble_lines=(),
            set_opener_template="",
            coerce_mixed_to_str=False,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        BACKSLASH = CommentConfig(
            prefix="\\",
            suffix="",
        )
        PAREN = CommentConfig(
            prefix="(",
            suffix=" )",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        COLON = DeclarationStyleConfig(
            formatter=_format_forth_declaration,
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
        positive_infinity="1.0e0 0.0e0 f/",
        negative_infinity="-1.0e0 0.0e0 f/",
        nan="0.0e0 0.0e0 f/",
    ):
        """Float format options."""

        REPR = enum.member(value=_format_float_forth)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = "decimal"

    class NumericLiteralSuffixes(enum.Enum):
        """Numeric literal suffix options."""

        NONE = enum.auto()

    class NumericSeparators(enum.Enum):
        """Numeric separator options."""

        NONE = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        ESCAPED = enum.member(value=_format_string_forth)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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

        NONE = "none"

    line_endings = LineEndings

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

    def __init__(  # noqa: PLR0915
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO,
        comment_format: CommentFormats = CommentFormats.BACKSLASH,
        declaration_style: DeclarationStyles = DeclarationStyles.COLON,
        dict_entry_style: DictEntryStyles = DictEntryStyles.DEFAULT,
        dict_format: DictFormats = DictFormats.DEFAULT,
        float_format: FloatFormats = FloatFormats.REPR,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_literal_suffix: NumericLiteralSuffixes = (
            NumericLiteralSuffixes.NONE
        ),
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.ESCAPED,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
        line_ending: LineEndings = LineEndings.NONE,
        indent: str = "    ",
    ) -> None:
        """Initialize Forth language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.null_literal = "0"
        self.true_literal = "true"
        self.false_literal = "false"
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            dict_open=fixed_dict_open(open_str=""),
            close="",
            format_entry=_format_forth_dict_entry,
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
        )
        self.trailing_comma_config: TrailingCommaConfig = trailing_comma.value
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = (
            date_format.value.formatter
        )
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format.value.formatter
        )
        self.format_string: Callable[[str], str] = string_format
        self.format_float: Callable[[float], str] = float_format
        self.format_integer: Callable[[int], str] = str
        self.format_sequence_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[Value, str], str] = (
            passthrough_sequence_entry
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
                open_str="",
                close="",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, Value, str], str] = (
            _format_forth_dict_entry
        )
        self.indent = indent
        self.indent_closing_delimiter = False
        self.element_separator = " "
        self.skip_null_dict_values = False
        self.supports_collection_comments = False
        self.supports_scalar_before_comments = False
        self.supports_scalar_inline_comments = False
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            declaration_style.value.formatter
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

        self.type_hint_collection_preamble_lines = no_type_hint_preamble
        self.special_float_preamble: tuple[str, ...] = ()
        self.call_style_config: CallStyleConfig = CallStyleConfig(
            kind=CallStyleKind.POSITIONAL,
        )
        self.statement_terminator = ""
        self.format_call_stub = no_call_stub
        self.format_call_preamble_stub = no_call_stub
