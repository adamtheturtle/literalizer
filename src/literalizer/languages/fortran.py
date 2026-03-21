"""Fortran language specification."""

from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_fortran,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    HasFormatEnums,
    OmapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)

if TYPE_CHECKING:
    import datetime
    from collections.abc import Callable

    from literalizer._types import Value

_FVAL_PREFIXES = (
    "fnull()",
    "fbool(",
    "fint(",
    "freal(",
    "fstr(",
    "flist(",
    "fmap(",
    "fset(",
    "fentry(",
)


@beartype
def _to_fval(value: str) -> str:
    """Convert a pre-formatted value string to an ``fval_t`` constructor.

    Inspects the string representation to determine the appropriate
    constructor: ``fstr``, ``fint``, ``freal``, or passes through values
    that are already ``fval_t`` expressions (``fnull``, ``fbool``,
    ``flist``, ``fmap``, ``fset``, ``fentry``).
    """
    if any(value.startswith(p) for p in _FVAL_PREFIXES):
        return value
    if (value.startswith("'") and value.endswith("'")) or (
        value.startswith('"') and value.endswith('"')
    ):
        return f"fstr({value})"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"fint({value})"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"freal({value})"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


def _fortran_comment_pos(line: str) -> int | None:
    """Return the index of the ``!`` comment character in *line* that
    lies outside any string literal, or ``None`` if there is no comment.
    """
    in_single_quote = False
    in_double_quote = False
    i = 0
    while i < len(line):
        c = line[i]
        if c == "'" and not in_double_quote:
            if in_single_quote and i + 1 < len(line) and line[i + 1] == "'":
                i += 2
                continue
            in_single_quote = not in_single_quote
        elif c == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
        elif c == "!" and not in_single_quote and not in_double_quote:
            return i
        i += 1
    return None


@beartype
def _add_continuation(value: str) -> str:
    """Add Fortran ``&`` line-continuation to non-comment, non-last
    lines.

    In Fortran free-form source a logical line may span multiple physical
    lines.  The ``&`` continuation character must be the last
    non-whitespace, non-comment character on the physical line.  Pure
    comment lines (blank or starting with ``!``) are transparent to the
    continuation mechanism and receive no ``&``.
    """
    lines = value.splitlines()
    if len(lines) <= 1:
        return value
    result: list[str] = []
    for i, line in enumerate(iterable=lines):
        is_last = i == len(lines) - 1
        stripped = line.strip()
        is_pure_comment = not stripped or stripped.startswith("!")
        if is_last or is_pure_comment:
            result.append(line)
        else:
            pos = _fortran_comment_pos(line=line)
            if pos is not None:
                result.append(line[:pos].rstrip() + " &  " + line[pos:])
            else:
                result.append(line + " &")
    return "\n".join(result)


@beartype
def _format_fortran_dict_entry(key: str, value: str) -> str:
    """Format a Fortran dict entry as an ``fentry(key, fval_t value)``
    call.
    """
    return f"fentry({key}, {_to_fval(value=value)})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    r"""Format a Fortran variable declaration and initialisation.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"type(fval_t) :: x\nx = flist([fval_t :: fint(1)])"``
    """
    fval = _to_fval(value=value)
    continued = _add_continuation(value=fval)
    return f"type(fval_t) :: {name}\n{name} = {continued}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Fortran assignment to an existing ``fval_t`` variable.

    Example: ``"x"`` and ``"flist([fval_t :: fint(1)])"`` →
    ``"x = flist([fval_t :: fint(1)])"``
    """
    fval = _to_fval(value=value)
    continued = _add_continuation(value=fval)
    return f"{name} = {continued}"


_string_format: Callable[[str], str] = format_string_fortran


@beartype
class Fortran(metaclass=HasFormatEnums):
    """Fortran language specification."""

    class DateFormats(enum.Enum):
        """Date format options for Fortran."""

        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime format options for Fortran."""

        ISO = enum.member(value=format_datetime_iso)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options."""

        HEX = enum.member(value=format_bytes_hex)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Fortran."""

        LIST = SequenceFormatConfig(
            open_str="flist([fval_t :: ",
            close="])",
            supports_heterogeneity=True,
            single_element_trailing_comma=False,
            empty_sequence=None,
        )

        @property
        def supports_heterogeneity(self) -> bool:
            """Whether this sequence format supports mixed-type
            elements.
            """
            return self.value.supports_heterogeneity

    class SetFormats(enum.Enum):
        """Set type options for Fortran."""

        SET = SetFormatConfig(
            open_str="fset([fval_t :: ",
            close="])",
            empty_set=None,
        )

    class CommentFormats(enum.Enum):
        """Comment style options."""

        EXCLAMATION = CommentConfig(
            prefix="!",
            suffix="",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.ISO,
        datetime_format: DatetimeFormats = DatetimeFormats.ISO,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.LIST,
        set_format: SetFormats = SetFormats.SET,
        comment_format: CommentFormats = CommentFormats.EXCLAMATION,
    ) -> None:
        """Initialize Fortran language specification."""
        self.sequence_format = sequence_format
        self.null_literal = "fnull()"
        self.true_literal = "fbool(.true.)"
        self.false_literal = "fbool(.false.)"
        fmt = sequence_format.value
        self.sequence_format_config: SequenceFormatConfig = fmt
        self.set_format_config: SetFormatConfig = set_format.value
        self.sequence_open: Callable[[list[Value]], str] = fixed_sequence_open(
            open_str=fmt.open_str
        )
        self.dict_format_config: DictFormatConfig = DictFormatConfig(
            open_fn=fixed_dict_open(open_str="fmap([fval_t :: "),
            close="])",
            format_entry=_format_fortran_dict_entry,
            empty_dict=None,
        )
        self.multiline_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.format_sequence_entry: Callable[[str], str] = _to_fval
        self.format_set_entry: Callable[[str], str] = _to_fval
        self.comment_config: CommentConfig = comment_format.value
        self.omap_format_config: OmapFormatConfig = OmapFormatConfig(
            open_str="fmap([fval_t :: ",
            close="])",
        )
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_fortran_dict_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
