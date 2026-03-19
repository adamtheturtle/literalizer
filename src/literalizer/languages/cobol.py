"""COBOL language specification (GnuCOBOL free-format)."""

import datetime
import re
from collections.abc import Callable
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
)

if TYPE_CHECKING:
    from literalizer._types import Value


@beartype
def _format_string_cobol(value: str) -> str:
    """Format a COBOL alphanumeric string literal.

    Double quotes inside the string are escaped by doubling them, then
    the whole string is wrapped in double quotes.

    Example: ``say "hi" loud`` becomes ``"say ""hi"" loud"``.
    """
    escaped = value.replace('"', '""')
    return f'"{escaped}"'


@beartype
def _is_data_entry(s: str) -> bool:
    """Return True if *s* looks like a COBOL DATA DIVISION entry.

    A DATA DIVISION entry starts with two decimal digits followed by a
    space (e.g. ``05 FILLER ...``).
    """
    return bool(re.match(r"^\d{2} ", s))


@beartype
def _pic_from_value(value: str) -> str:
    """Return a COBOL PIC (or storage) clause for a formatted literal.

    Inspects the pre-formatted value string to choose the narrowest
    appropriate clause.
    """
    if value == "SPACES":
        return "PIC X(1)"
    if value in ('"TRUE"', '"FALSE"'):
        return "PIC X(5)"
    if value.startswith('"') and value.endswith('"'):
        inner = value[1:-1].replace('""', '"')
        return f"PIC X({max(1, len(inner))})"
    if re.match(r"^-?\d+$", value):
        return "PIC S9(18) COMP-5"
    # Float or other numeric
    return "COMP-2"


@beartype
def _to_cobol_entry(value: str, name: str = "FILLER", level: int = 5) -> str:
    """Wrap a scalar literal in a COBOL DATA DIVISION entry.

    Example: ``"42"`` → ``"05 FILLER PIC S9(18) COMP-5 VALUE 42."``
    """
    pic = _pic_from_value(value)
    return f"{level:02d} {name} {pic} VALUE {value}."


@beartype
def _bump_levels(content: str) -> str:
    """Increment every COBOL level number in *content* by 5.

    Only lines whose first non-space token is a two-digit level number
    are modified.
    """
    lines = content.split("\n")
    result = []
    for line in lines:
        m = re.match(r"^(\s*)(\d{2})(\s)", line)
        if m:
            new_level = int(m.group(2)) + 5
            result.append(
                f"{m.group(1)}{new_level:02d}{m.group(3)}{line[m.end() :]}"
            )
        else:
            result.append(line)
    return "\n".join(result)


@beartype
def _format_cobol_sequence_entry(item: str) -> str:
    """Format a sequence item as a COBOL DATA DIVISION entry.

    Scalar values become ``05 FILLER PIC … VALUE …`` items.
    Nested collections (detected by an embedded newline) are wrapped in
    a ``05 FILLER.`` group with inner level numbers bumped by 5.
    """
    if "\n" in item:
        bumped = _bump_levels(item)
        return f"05 FILLER.\n{bumped}"
    if _is_data_entry(item.strip()):
        return item.strip()
    return _to_cobol_entry(item)


@beartype
def _key_to_cobol_name(key_str: str) -> str:
    """Convert a formatted COBOL string literal to a valid COBOL data name.

    Strips outer quotes, unescapes doubled double-quotes, uppercases the
    result, replaces non-alphanumeric characters with hyphens, and
    prepends ``F-`` to avoid clashes with COBOL reserved words.  The
    result is truncated to 28 characters (leaving room for the prefix).
    """
    if key_str.startswith('"') and key_str.endswith('"'):
        name = key_str[1:-1].replace('""', '"')
    else:
        name = key_str
    name = name.upper()
    name = re.sub(r"[^A-Z0-9]", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    name = name[:28] or "FILLER"
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
        bumped = _bump_levels(value)
        return f"05 {name}.\n{bumped}"
    if _is_data_entry(value.strip()):
        bumped = _bump_levels(value.strip())
        return f"05 {name}.\n{bumped}"
    pic = _pic_from_value(value)
    return f"05 {name} {pic} VALUE {value}."


@beartype
def _to_cobol_name(python_name: str) -> str:
    """Convert a Python-style identifier to a COBOL data name.

    Uppercases the name and replaces underscores with hyphens.
    """
    return python_name.upper().replace("_", "-")


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a COBOL 01-level variable declaration.

    Scalars become an elementary 01-level item; collections become a
    group 01-level item containing 05-level sub-items.
    """
    cob_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(scalar):
        return f"01 {cob_name}.\n{stripped}"
    pic = _pic_from_value(scalar)
    return f"01 {cob_name} {pic} VALUE {scalar}."


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a COBOL PROCEDURE DIVISION assignment statement.

    Scalars use a ``MOVE … TO …`` statement; complex group items use
    ``INITIALIZE`` (which resets all sub-items to their VALUE-clause
    defaults).
    """
    cob_name = _to_cobol_name(python_name=name)
    stripped = value.strip("\n")
    scalar = stripped.strip()
    if "\n" in stripped or _is_data_entry(scalar):
        return f"INITIALIZE {cob_name}."
    return f"MOVE {scalar} TO {cob_name}."


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = _format_string_cobol


class Cobol:
    """GnuCOBOL free-format language specification.

    Data is represented as COBOL WORKING-STORAGE SECTION level items:
    scalars become elementary data items with VALUE clauses, and
    sequences / dicts become group items with 05-level sub-items.
    """

    @beartype
    def __init__(self) -> None:
        """Initialize COBOL language specification."""
        self.null_literal = "SPACES"
        self.true_literal = '"TRUE"'
        self.false_literal = '"FALSE"'
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=""
        )
        self.sequence_close = ""
        self.dict_open = ""
        self.dict_close = ""
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_cobol_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = "05 FILLER PIC X(1) VALUE SPACES."
        self.empty_dict: str | None = "05 FILLER PIC X(1) VALUE SPACES."
        self.set_open = ""
        self.set_close = ""
        self.empty_set: str | None = "05 FILLER PIC X(1) VALUE SPACES."
        self.format_sequence_entry: Callable[[str], str] = (
            _format_cobol_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = (
            _format_cobol_sequence_entry
        )
        self.comment_prefix = "*>"
        self.comment_suffix = ""
        self.omap_open = ""
        self.omap_close = ""
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_cobol_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = "\n"
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
