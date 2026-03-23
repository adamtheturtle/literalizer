"""COBOL language specification (GnuCOBOL free-format)."""

import datetime
import enum
import re
from collections.abc import Callable, Sequence

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    fixed_set_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
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

_COBOL_CONTROL_CHAR_REPLACEMENTS: dict[str, str] = {
    "\n": " ",
    "\r": " ",
    "\t": " ",
}

_MAX_COBOL_LEVEL: int = 49


@beartype
def _format_string_cobol(value: str) -> str:
    """Format a COBOL alphanumeric string literal.

    Control characters (newlines, tabs, carriage returns) are replaced
    with spaces because COBOL string literals cannot span multiple lines
    and have no escape sequences.  Double quotes are escaped by doubling
    them, then the whole string is wrapped in double quotes.

    Example: ``say "hi" loud`` becomes ``"say ""hi"" loud"``.
    """
    cleaned = value
    for char, replacement in _COBOL_CONTROL_CHAR_REPLACEMENTS.items():
        cleaned = cleaned.replace(char, replacement)
    escaped = cleaned.replace('"', '""')
    return f'"{escaped}"'


@beartype
def _is_data_entry(s: str) -> bool:
    """Return True if *s* looks like a COBOL DATA DIVISION entry.

    A DATA DIVISION entry starts with two decimal digits followed by a
    space (e.g. ``05 FILLER ...``).
    """
    return bool(re.match(pattern=r"^\d{2} ", string=s))


@beartype
def _pic_from_value(value: str) -> str:
    """Return a COBOL PIC (or storage) clause for a formatted literal.

    Inspects the pre-formatted value string to choose the narrowest
    appropriate clause.
    """
    if value == "SPACES":
        return "PIC X(1)"
    if value in {'"TRUE"', '"FALSE"'}:
        return "PIC X(5)"
    if value.startswith('"') and value.endswith('"'):
        inner = value[1:-1].replace('""', '"')
        return f"PIC X({max(1, len(inner))})"
    if re.match(pattern=r"^-?\d+$", string=value):
        return "PIC S9(18) COMP-5"
    # Float or other numeric
    return "COMP-2"


@beartype
def _to_cobol_entry(value: str, name: str, level: int) -> str:
    """Wrap a scalar literal in a COBOL DATA DIVISION entry.

    Example: ``"42"`` → ``"05 FILLER PIC S9(18) COMP-5 VALUE 42."``
    """
    pic = _pic_from_value(value=value)
    return f"{level:02d} {name} {pic} VALUE {value}."


@beartype
def _bump_levels(content: str) -> str:
    """Increment every COBOL level number in *content* by 5.

    Only lines whose first non-space token is a two-digit level number
    are modified.
    """
    lines = content.split(sep="\n")
    result: list[str] = []
    for line in lines:
        m = re.match(pattern=r"^(\s*)(\d{2})(\s)", string=line)
        if not m:
            msg = f"Expected COBOL level-number line, got: {line!r}"
            raise ValueError(msg)
        new_level = min(int(m.group(2)) + 5, _MAX_COBOL_LEVEL)
        result.append(
            f"{m.group(1)}{new_level:02d}{m.group(3)}{line[m.end() :]}"
        )
    return "\n".join(result)


@beartype
def _format_cobol_sequence_entry(item: str) -> str:
    """Format a sequence item as a COBOL DATA DIVISION entry.

    Scalar values become ``05 FILLER PIC … VALUE …`` items.
    Nested collections (detected by an embedded newline) are wrapped in
    a ``05 FILLER.`` group with inner level numbers bumped by 5.
    """
    if "\n" in item:
        bumped = _bump_levels(content=item)
        return f"05 FILLER.\n{bumped}"
    if _is_data_entry(s=item.strip()):
        return item.strip()
    return _to_cobol_entry(value=item, name="FILLER", level=5)


@beartype
def _key_to_cobol_name(key_str: str) -> str:
    """Convert a formatted COBOL string literal to a valid COBOL data name.

    Strips outer quotes, converts doubled double-quotes back to single,
    converts the result to upper case, replaces non-alphanumeric characters
    with hyphens, and adds the ``F-`` prefix to avoid clashes with COBOL
    reserved words.  The result is truncated to 28 characters (leaving
    room for the prefix).
    """
    name = key_str[1:-1].replace('""', '"')
    name = name.upper()
    name = re.sub(pattern=r"[^A-Z0-9]", repl="-", string=name)
    name = re.sub(pattern=r"-+", repl="-", string=name).strip("-")
    name = name[:28].strip("-") or "FILLER"
    return f"F-{name}"


@beartype
def _format_cobol_dict_entry(key: str, value: str) -> str:
    """Format a COBOL DATA DIVISION entry for a dict key-value pair.

    The key string is converted to a valid COBOL data name.  Scalar
    values produce elementary items; nested collections produce group
    items with bumped level numbers.
    """
    name = _key_to_cobol_name(key_str=key)
    if "\n" in value:
        bumped = _bump_levels(content=value)
        return f"05 {name}.\n{bumped}"
    if _is_data_entry(s=value.strip()):
        bumped = _bump_levels(content=value.strip())
        return f"05 {name}.\n{bumped}"
    pic = _pic_from_value(value=value)
    return f"05 {name} {pic} VALUE {value}."


@beartype
def _to_cobol_name(python_name: str) -> str:
    """Convert a Python-style identifier to a COBOL data name.

    Converts the name to upper case and replaces underscores with hyphens.
    """
    return python_name.upper().replace("_", "-")


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a COBOL 01-level variable declaration.

    Scalars become an elementary 01-level item; collections become a
    group 01-level item containing 05-level sub-items.
    """
    cob_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(s=scalar):
        return f"01 {cob_name}.\n{stripped}"
    pic = _pic_from_value(value=scalar)
    return f"01 {cob_name} {pic} VALUE {scalar}."


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a COBOL PROCEDURE DIVISION assignment statement.

    Scalars use a ``MOVE … TO …`` statement; complex group items use
    ``INITIALIZE`` (which resets alphanumeric sub-items to SPACES and
    numeric sub-items to ZEROS).
    """
    cob_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(s=scalar):
        return f"INITIALIZE {cob_name}."
    return f"MOVE {scalar} TO {cob_name}."


_string_format: Callable[[str], str] = _format_string_cobol


@beartype
class Cobol(metaclass=LanguageCls):
    """GnuCOBOL free-format language specification.

    Data is represented as COBOL WORKING-STORAGE SECTION level items:
    scalars become elementary data items with VALUE clauses, and
    sequences / dicts become group items with 05-level sub-items.
    """

    extension = ".cob"
    pygments_name = "cobol"

    class DateFormats(enum.Enum):
        """Date format options for Cobol."""

        ISO = DateFormatConfig(formatter=format_date_iso, produces_string=True)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Cobol."""

        ISO = DatetimeFormatConfig(
            formatter=format_datetime_iso,
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
        """Sequence type options for COBOL."""

        SEQUENCE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str=""),
            close="",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence="05 FILLER PIC X(1) VALUE SPACES.",
            preamble_lines=(),
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for COBOL."""

        SET = SetFormatConfig(
            set_open=fixed_set_open(open_str=""),
            close="",
            empty_set="05 FILLER PIC X(1) VALUE SPACES.",
            preamble_lines=(),
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        STAR_ANGLE = CommentConfig(
            prefix="*>",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        TYPED = "typed"

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
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.SEQUENCE,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.STAR_ANGLE,
        _variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        declaration_style: DeclarationStyles = DeclarationStyles.TYPED,
        dict_format: DictFormats = DictFormats.DEFAULT,
        integer_format: IntegerFormats = IntegerFormats.DECIMAL,
        numeric_separator: NumericSeparators = NumericSeparators.NONE,
        string_format: StringFormats = StringFormats.DOUBLE,
        trailing_comma: TrailingCommas = TrailingCommas.NO,
    ) -> None:
        """Initialize COBOL language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "SPACES"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format = set_format
        self.set_format_config: SetFormatConfig = set_format.value
        self.true_literal = '"TRUE"'
        self.false_literal = '"FALSE"'
        self.sequence_open: Callable[[list[Value]], str] = fmt.sequence_open
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str=""),
            close="",
            format_entry=_format_cobol_dict_entry,
            empty_dict="05 FILLER PIC X(1) VALUE SPACES.",
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
            _format_cobol_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = (
            _format_cobol_sequence_entry
        )
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
                open_str="",
                close="",
                preamble_lines=(),
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_cobol_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = "\n"
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str, Value], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.static_preamble: Sequence[str] = ()
        self.scalar_preamble: dict[type, tuple[str, ...]] = {}
        self.type_hint_collection_preamble_lines: tuple[str, ...] = ()
