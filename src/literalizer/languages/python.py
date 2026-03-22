"""Python language specification."""

import datetime
import enum
import functools
from collections import OrderedDict
from collections.abc import Callable, Sequence

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters import (
    dict_entry_with_separator,
    fixed_dict_open,
    fixed_sequence_open,
    format_bytes_hex,
    format_bytes_python,
    format_date_iso,
    format_date_python,
    format_datetime_epoch,
    format_datetime_python,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import (
    CommentConfig,
    DictFormatConfig,
    LanguageCls,
    OrderedMapFormatConfig,
    SequenceFormatConfig,
    SetFormatConfig,
)
from literalizer._types import Value


@beartype
def _format_python_ordered_map_entry(key: str, value: str) -> str:
    """Format one Python ``OrderedDict`` entry as a ``(key, value)`` tuple."""
    return f"({key}, {value})"


@beartype
def _preamble(code: str) -> Sequence[str]:
    """Return preamble lines for the generated code."""
    lines: list[str] = []
    if "OrderedDict(" in code:
        lines.append("from collections import OrderedDict")
    if "datetime." in code:
        lines.append("import datetime")
    if "[Any" in code or "Any]" in code:
        lines.append("from typing import Any")
    return lines


@beartype
def _format_variable_declaration(name: str, value: str, _data: Value) -> str:
    """Format a Python variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_inline_type_hint_declaration(
    name: str,
    value: str,
    data: Value,
    *,
    sequence_config: SequenceFormatConfig,
    set_config: SetFormatConfig,
) -> str:
    """Format a Python variable declaration with an inline type hint."""
    hint = _python_type_hint(
        data=data,
        sequence_config=sequence_config,
        set_config=set_config,
    )
    return f"{name}: {hint} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str, _data: Value) -> str:
    """Format a Python variable assignment."""
    return f"{name} = {value}"


# Ordered by priority: bool before int, datetime before date.
_SCALAR_TYPE_HINTS: tuple[tuple[type, str], ...] = (
    (bool, "bool"),
    (int, "int"),
    (float, "float"),
    (str, "str"),
    (bytes, "bytes"),
    (datetime.datetime, "datetime.datetime"),
    (datetime.date, "datetime.date"),
)


@beartype
def _python_type_hint(
    data: Value,
    *,
    sequence_config: SequenceFormatConfig,
    set_config: SetFormatConfig,
) -> str:
    """Derive a Python type hint from the original data structure."""
    if data is None:
        return "None"
    for scalar_type, hint in _SCALAR_TYPE_HINTS:
        if isinstance(data, scalar_type):
            return hint
    if isinstance(data, dict):
        return (
            "OrderedDict[str, Any]"
            if isinstance(data, (ordereddict, OrderedDict))
            else "dict[str, Any]"
        )
    if isinstance(data, (set, frozenset)):
        return (
            "frozenset[Any]"
            if set_config.open_str.startswith("frozenset")
            else "set[Any]"
        )
    # The only remaining Value type is list.
    return "list[Any]" if sequence_config.close == "]" else "tuple[Any, ...]"


@beartype
class Python(metaclass=LanguageCls):
    """Python language specification.

    Args:
        date_format: How to format :class:`datetime.date` values.

            * ``date_formats.PYTHON`` — ``datetime.date`` constructor call,
              e.g. ``datetime.date(year=2024, month=1, day=15)``.
            * ``date_formats.ISO`` — ISO 8601 quoted string,
              e.g. ``"2024-01-15"``.

        datetime_format: How to format :class:`datetime.datetime` values.

            * ``datetime_formats.PYTHON`` — ``datetime.datetime`` constructor
              call, e.g. ``datetime.datetime(year=2024, month=1,
              day=15, hour=12, minute=30, second=0)``.
            * ``datetime_formats.EPOCH`` — Unix epoch float,
              e.g. ``1705312200.0``.

        bytes_format: How to format :class:`bytes` values.

            * ``bytes_formats.HEX`` — lowercase hex string,
              e.g. ``"48656c6c6f"``.
            * ``bytes_formats.PYTHON`` — Python bytes literal,
              e.g. ``b'Hello'``.

        sequence_format: Which Python sequence type to use.

            * ``sequence_formats.TUPLE`` — tuple literal,
              e.g. ``(1, 2, 3)``.
            * ``sequence_formats.LIST`` — list literal,
              e.g. ``[1, 2, 3]``.

        set_format: Which Python set type to use.

            * ``set_formats.SET`` — mutable set literal,
              e.g. ``{1, 2, 3}``.
            * ``set_formats.FROZENSET`` — immutable frozenset,
              e.g. ``frozenset({1, 2, 3})``.

        variable_type_hints: Whether to add inline type hints to
            variable declarations.

            * ``VariableTypeHints.NONE`` — bare assignment,
              e.g. ``my_var = {...}``.
            * ``VariableTypeHints.INLINE`` — with type annotation,
              e.g. ``my_var: dict[str, Any] = {...}``.
    """

    extension = ".py"
    pygments_name = "python"

    class DateFormats(enum.Enum):
        """Date formatting options for Python."""

        PYTHON = enum.member(value=format_date_python)
        ISO = enum.member(value=format_date_iso)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value(value=date_value)

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Python."""

        PYTHON = enum.member(value=format_datetime_python)
        EPOCH = enum.member(value=format_datetime_epoch)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value(value=dt_value)

    class BytesFormats(enum.Enum):
        """Bytes formatting options for Python."""

        HEX = enum.member(value=format_bytes_hex)
        PYTHON = enum.member(value=format_bytes_python)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

    class SequenceFormats(enum.Enum):
        """Sequence type options for Python."""

        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            empty_sequence=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=fixed_sequence_open(open_str="["),
            close="]",
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
        """Set type options for Python."""

        SET = SetFormatConfig(
            open_str="{",
            close="}",
            empty_set="set()",
        )
        FROZENSET = SetFormatConfig(
            open_str="frozenset({",
            close="})",
            empty_set="frozenset()",
        )

    class VariableTypeHints(enum.Enum):
        """Variable type hint options for Python."""

        NONE = "none"
        INLINE = "inline"

        def formatter(
            self,
            *,
            sequence_config: SequenceFormatConfig,
            set_config: SetFormatConfig,
        ) -> Callable[[str, str, Value], str]:
            """Return the variable declaration formatter for this hint
            style.
            """
            if self is type(self).INLINE:
                return functools.partial(
                    _format_inline_type_hint_declaration,
                    sequence_config=sequence_config,
                    set_config=set_config,
                )
            return _format_variable_declaration

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    date_formats = DateFormats
    datetime_formats = DatetimeFormats
    bytes_formats = BytesFormats
    sequence_formats = SequenceFormats
    set_formats = SetFormats
    comment_formats = CommentFormats
    variable_type_hints_formats = VariableTypeHints

    def __init__(
        self,
        *,
        date_format: DateFormats = DateFormats.PYTHON,
        datetime_format: DatetimeFormats = DatetimeFormats.PYTHON,
        bytes_format: BytesFormats = BytesFormats.HEX,
        sequence_format: SequenceFormats = SequenceFormats.TUPLE,
        set_format: SetFormats = SetFormats.SET,
        variable_type_hints: VariableTypeHints = VariableTypeHints.NONE,
        comment_format: CommentFormats = CommentFormats.HASH,
    ) -> None:
        """Initialize Python language specification."""
        self.variable_type_hints = variable_type_hints
        self.sequence_format = sequence_format
        self.null_literal = "None"
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
            format_entry=dict_entry_with_separator(separator=": "),
            empty_dict=None,
        )
        self.multiline_trailing_comma = True

        self.format_bytes: Callable[[bytes], str] = bytes_format
        self.format_date: Callable[[datetime.date], str] = date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            datetime_format
        )

        self.format_string: Callable[[str], str] = format_string_backslash
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_format = comment_format
        self.comment_config: CommentConfig = comment_format.value
        self.ordered_map_format_config: OrderedMapFormatConfig = (
            OrderedMapFormatConfig(
                open_str="OrderedDict([",
                close="])",
            )
        )
        self.format_ordered_map_entry: Callable[[str, str], str] = (
            _format_python_ordered_map_entry
        )
        self.multiline_close_indent = ""
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.supports_collection_comments = True
        decl_fmt: Callable[[str, str, Value], str] = (
            variable_type_hints.formatter(
                sequence_config=self.sequence_format_config,
                set_config=self.set_format_config,
            )
        )
        self.format_variable_declaration = decl_fmt
        self.format_variable_assignment: Callable[[str, str, Value], str] = (
            _format_variable_assignment
        )
        self.preamble: Callable[[str], Sequence[str]] = _preamble
