"""Python language specification."""

import dataclasses
import datetime
import enum
import functools
from collections import OrderedDict
from collections.abc import Callable, Sequence
from functools import cached_property
from types import MappingProxyType
from typing import ClassVar, assert_never

from beartype import beartype
from ruamel.yaml.compat import ordereddict

from literalizer._formatters.collection_openers import (
    fixed_open,
)
from literalizer._formatters.format_dates import (
    date_ymd_formatter,
    format_date_iso,
)
from literalizer._formatters.format_entries import (
    dict_entry_with_separator,
    format_bytes_base64,
    format_bytes_hex,
    passthrough_sequence_entry,
    passthrough_set_entry,
    tuple_dict_entry,
    variable_declaration_formatter,
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
from literalizer._formatters.format_strings import (
    format_string_backslash,
    format_string_backslash_single,
    format_string_raw_python,
)
from literalizer._language import (
    NO_HETEROGENEOUS_BEHAVIOR,
    CallStyle,
    CommentConfig,
    DateFormatConfig,
    DatetimeFormatConfig,
    DeclarationStyleConfig,
    DictFormatConfig,
    FloatSpecialsMixin,
    HeterogeneousBehavior,
    IdentifierCase,
    KeywordCallStyle,
    LanguageCls,
    OrderedMapFormatConfig,
    PositionalCallStyle,
    SequenceFormatConfig,
    SetFormatConfig,
    StubReturn,
    TrailingCommaConfig,
    body_preamble_from_scalars,
    date_scalar_preamble,
    default_wrap_calls_with_declarations,
    identity_call_ref_identifier,
    identity_call_target,
    no_call_stub,
    no_data_preamble,
    no_validate_spec_for_data,
    wrap_combined_in_file_noop,
    wrap_in_file_noop,
)
from literalizer._types import Value


@beartype
def _format_datetime_python(value: datetime.datetime) -> str:
    """Format a datetime as a Python ``datetime.datetime(...)`` constructor
    call.
    """
    parts = [
        f"year={value.year}",
        f"month={value.month}",
        f"day={value.day}",
        f"hour={value.hour}",
        f"minute={value.minute}",
        f"second={value.second}",
    ]
    if value.microsecond:
        parts.append(f"microsecond={value.microsecond}")
    args = ", ".join(parts)
    return f"datetime.datetime({args})"


@beartype
def _format_datetime_epoch(value: datetime.datetime) -> str:
    """Format a datetime as seconds since the Unix epoch."""
    return repr(value.timestamp())


@beartype
def _format_bytes_python(value: bytes) -> str:
    """Format bytes as a Python ``bytes`` literal."""
    return repr(value)


@beartype
def _needs_type_annotation(data: Value) -> bool:
    """Whether *data* needs a type annotation for type-checkers.

    This is true when *data* is or contains an empty collection,
    because type-checkers cannot infer the element types.
    """
    match data:
        case dict():
            return len(data) == 0 or any(
                _needs_type_annotation(data=v) for v in data.values()
            )
        case set():
            return len(data) == 0
        case list():
            return len(data) == 0 or any(
                _needs_type_annotation(data=e) for e in data
            )
        case _:
            return False


@beartype
def _format_variable_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> str:
    """Format a Python variable declaration.

    For empty collections a type annotation is added so that
    type-checkers can infer the type.
    """
    if _needs_type_annotation(data=data):
        return _format_inline_type_hint_declaration(
            name=name,
            value=value,
            data=data,
            _modifiers=_modifiers,
            bytes_hint=bytes_hint,
            date_hint=date_hint,
            datetime_hint=datetime_hint,
            sequence_hint=sequence_hint,
            set_hint=set_hint,
            default_set_element_type=default_set_element_type,
            default_sequence_element_type=default_sequence_element_type,
            default_dict_value_type=default_dict_value_type,
            default_dict_key_type=default_dict_key_type,
        )
    return f"{name} = {value}"


@beartype
def _format_inline_type_hint_declaration(
    *,
    name: str,
    value: str,
    data: Value,
    _modifiers: frozenset[enum.Enum],
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> str:
    """Format a Python variable declaration with an inline type hint."""
    hint = _python_type_hint(
        data=data,
        bytes_hint=bytes_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        sequence_hint=sequence_hint,
        set_hint=set_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        default_dict_key_type=default_dict_key_type,
    )
    return f"{name}: {hint} = {value}"


@beartype
def _element_union(*, types: list[str]) -> str:
    """Remove duplicate *types* and join them into a union."""
    unique: list[str] = list(dict.fromkeys(types))
    match unique:
        case [only]:
            return only
        case _:
            return " | ".join(unique)


@beartype
def _collection_element_union(
    *,
    elements: list[Value],
    recurse: Callable[..., str],
    sort: bool,
    merge_dicts: bool,
    default_type: str,
) -> str:
    """Return the element union for a collection, or *default_type* if
    empty.

    When *merge_dicts* is ``True``, all dict elements are merged so
    that their values produce a single ``dict[str, …]`` hint.  This
    avoids ``dict[str, X] | dict[str, Y]`` unions that mypy rejects
    because ``dict`` is invariant in its type parameters.
    """
    if not elements:
        return default_type
    if merge_dicts:
        elements = _merge_dict_elements(elements=elements)
    types = [recurse(data=e) for e in elements]
    if sort:
        types.sort()
    return _element_union(types=types)


@beartype
def _merge_dict_elements(*, elements: list[Value]) -> list[Value]:
    """Pool values from like-typed dicts into single representatives."""
    plain_vals: list[Value] = []
    ordered_vals: list[Value] = []
    non_dict: list[Value] = []
    has_plain = False
    has_ordered = False
    for elem in elements:
        match elem:
            case ordereddict() | OrderedDict():
                has_ordered = True
                ordered_vals.extend(elem.values())  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
            case dict():
                has_plain = True
                plain_vals.extend(elem.values())
            case _:
                non_dict.append(elem)
    merged: list[Value] = list(non_dict)
    if has_plain:
        merged.append(
            {str(object=i): v for i, v in enumerate(iterable=plain_vals)}
        )
    if has_ordered:
        merged.append(
            OrderedDict(
                {str(object=i): v for i, v in enumerate(iterable=ordered_vals)}
            )
        )
    return merged


@beartype
def _python_type_hint(  # pylint: disable=too-complex,too-many-branches  # noqa: C901, PLR0911, PLR0912
    *,
    data: Value,
    bytes_hint: str,
    date_hint: str,
    datetime_hint: str,
    sequence_hint: str,
    set_hint: str,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> str:
    """Derive a Python type hint from the original data and format
    config.
    """
    recurse = functools.partial(
        _python_type_hint,
        bytes_hint=bytes_hint,
        date_hint=date_hint,
        datetime_hint=datetime_hint,
        sequence_hint=sequence_hint,
        set_hint=set_hint,
        default_set_element_type=default_set_element_type,
        default_sequence_element_type=default_sequence_element_type,
        default_dict_value_type=default_dict_value_type,
        default_dict_key_type=default_dict_key_type,
    )

    # Order matters: datetime before date (datetime is a date subclass),
    # bool before int (bool is an int subclass).
    match data:
        case bool():
            return "bool"
        case int():
            return "int"
        case float():
            return "float"
        case str():
            return "str"
        case bytes():
            return bytes_hint
        case datetime.datetime():
            return datetime_hint
        case datetime.date():
            return date_hint
        case None:
            return "None"
        case dict():
            outer = (
                "OrderedDict"
                if isinstance(data, (ordereddict, OrderedDict))
                else "dict"
            )
            key_hint = default_dict_key_type if not data else "str"
            val_union = _collection_element_union(
                elements=list(data.values()),  # pyright: ignore[reportUnknownMemberType,reportUnknownArgumentType]
                recurse=recurse,
                sort=False,
                merge_dicts=False,
                default_type=default_dict_value_type,
            )
            return f"{outer}[{key_hint}, {val_union}]"
        case set():
            elem_union = _collection_element_union(
                elements=list(data),
                recurse=recurse,
                sort=True,
                merge_dicts=False,
                default_type=default_set_element_type,
            )
            return f"{set_hint}[{elem_union}]"
        case list():
            elem_union = _collection_element_union(
                elements=data,
                recurse=recurse,
                sort=False,
                merge_dicts=True,
                default_type=default_sequence_element_type,
            )
            if sequence_hint == "tuple":
                return f"{sequence_hint}[{elem_union}, ...]"
            return f"{sequence_hint}[{elem_union}]"
        case _ as unreachable:
            assert_never(unreachable)


@beartype
def _build_type_hint_preamble(
    *,
    default_set_element_type: str,
    default_sequence_element_type: str,
    default_dict_value_type: str,
    default_dict_key_type: str,
) -> Callable[[frozenset[type]], tuple[str, ...]]:
    """Build a callable that returns preamble lines for type hints.

    The returned callable checks which empty collection types are
    present in the data and only emits ``from typing import Any``
    when at least one of them would produce an ``Any`` type hint.
    """
    # Pre-compute which collection types need "Any".
    _any_types: frozenset[type] = frozenset(
        t
        for t, needs in (
            (
                dict,
                default_dict_value_type == "Any"
                or default_dict_key_type == "Any",
            ),
            (set, default_set_element_type == "Any"),
            (list, default_sequence_element_type == "Any"),
        )
        if needs
    )

    def _preamble(
        empty_collection_types: frozenset[type],
        /,
    ) -> tuple[str, ...]:
        """Return ``from typing import Any`` if needed."""
        if _any_types.intersection(empty_collection_types):
            return ("from typing import Any",)
        return ()

    return _preamble


def _python_call_stub(
    parts: Sequence[str],
    _params: Sequence[str],
    _stub_return: StubReturn,
    /,
) -> tuple[str, ...]:
    """Return Python stub declarations for a call name."""
    variadic = "*_args: object, **_kwargs: object"
    if len(parts) == 1:
        return (f"def {parts[0]}({variadic}) -> object: ...",)
    root = parts[0]
    method = parts[-1]
    fields = parts[1:-1]
    if not fields:
        cls = f"_{root.capitalize()}Type"
        return (
            f"class {cls}:",
            f"    def {method}(self, {variadic}) -> object: ...",
            f"{root} = {cls}()",
        )
    lines: list[str] = []
    inner_cls = f"_{fields[-1].capitalize()}Type"
    lines.append(f"class {inner_cls}:")
    lines.append(f"    def {method}(self, {variadic}) -> object: ...")
    prev_cls = inner_cls
    for i in range(len(fields) - 2, -1, -1):
        cls = f"_{fields[i].capitalize()}Type"
        lines.append(f"class {cls}:")
        lines.append(f"    {fields[i + 1]} = {prev_cls}()")
        prev_cls = cls
    root_cls = f"_{root.capitalize()}Type"
    lines.append(f"class {root_cls}:")
    lines.append(f"    {fields[0]} = {prev_cls}()")
    lines.append(f"{root} = {root_cls}()")
    return tuple(lines)


@beartype
@dataclasses.dataclass(frozen=True, kw_only=True)
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

        default_set_element_type: Type name used for empty set type
            hints.  Defaults to ``"Any"``.

        default_sequence_element_type: Type name used for empty
            list/tuple type hints.  Defaults to ``"Any"``.

        default_dict_key_type: Type name used for empty dict key
            type hints.  Defaults to ``"str"``.

        default_dict_value_type: Type name used for empty dict value
            type hints.  Defaults to ``"Any"``.

        variable_type_hints: Whether to add inline type hints to
            variable declarations.

            * ``VariableTypeHints.AUTO`` — bare assignment,
              e.g. ``my_var = {...}``.  Empty collections still
              receive a type annotation so that type-checkers can
              infer the element types,
              e.g. ``my_var: dict[str, Any] = {}``.
            * ``VariableTypeHints.ALWAYS`` — every declaration has
              a type annotation,
              e.g. ``my_var: dict[str, Any] = {...}``.
    """

    extension = ".py"
    pygments_name = "python"
    supports_default_set_element_type = True
    supports_default_sequence_element_type = True
    supports_default_dict_value_type = True
    supports_default_dict_key_type = True
    supports_default_ordered_map_value_type = False
    supports_special_floats = True
    supports_variable_names = True
    supports_dotted_calls = True
    has_free_function_calls = True
    reserved_identifiers: ClassVar[frozenset[str]] = frozenset()
    allows_bare_call_statement = True
    call_returns_expression = True
    supports_inline_multiline_dict_args = True

    class DateFormats(enum.Enum):
        """Date formatting options for Python."""

        PYTHON = DateFormatConfig(
            formatter=date_ymd_formatter(
                template="datetime.date("
                "year={year}, month={month}, day={day})",
            ),
            preamble_lines=("import datetime",),
        )
        ISO = DateFormatConfig(formatter=format_date_iso, type_produced=str)

        def __call__(self, date_value: datetime.date, /) -> str:
            """Format a date."""
            return self.value.formatter(date_value)

        @property
        def type_hint(self) -> str:
            """The Python type hint for this date format."""
            if self is type(self).PYTHON:
                return "datetime.date"
            return "str"

    class DatetimeFormats(enum.Enum):
        """Datetime formatting options for Python."""

        PYTHON = DatetimeFormatConfig(
            formatter=_format_datetime_python,
            preamble_lines=("import datetime",),
        )
        EPOCH = DatetimeFormatConfig(formatter=_format_datetime_epoch)

        def __call__(self, dt_value: datetime.datetime, /) -> str:
            """Format a datetime."""
            return self.value.formatter(dt_value)

        @property
        def type_hint(self) -> str:
            """The Python type hint for this datetime format."""
            if self is type(self).PYTHON:
                return "datetime.datetime"
            return "float"

    class BytesFormats(enum.Enum):
        """Bytes formatting options for Python."""

        HEX = enum.member(value=format_bytes_hex)
        BASE64 = enum.member(value=format_bytes_base64)
        PYTHON = enum.member(value=_format_bytes_python)

        def __call__(self, data: bytes, /) -> str:
            """Format bytes."""
            return self.value(value=data)

        @property
        def type_hint(self) -> str:
            """The Python type hint for this bytes format."""
            if self is type(self).PYTHON:
                return "bytes"
            return "str"

    class SequenceFormats(enum.Enum):
        """Sequence type options for Python."""

        TUPLE = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="("),
            close=")",
            supports_heterogeneity=True,
            single_element_trailing_comma=True,
            supports_trailing_comma=True,
            empty_sequence=None,
            preamble_lines=(),
            format_entry=passthrough_sequence_entry,
            typed_opener_fallback=None,
            uses_typed_literal_for_scalars=False,
            requires_uniform_record_shapes=False,
            declared_type=None,
            narrowed_empty_form=None,
        )
        LIST = SequenceFormatConfig(
            sequence_open=fixed_open(open_str="["),
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
            declared_type=None,
            narrowed_empty_form=None,
        )

        @property
        def type_hint(self) -> str:
            """Python type hint name for this sequence format."""
            return "tuple" if self is type(self).TUPLE else "list"

    class SetFormats(enum.Enum):
        """Set type options for Python."""

        SET = SetFormatConfig(
            set_open=fixed_open(open_str="{"),
            close="}",
            empty_set="set()",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )
        FROZENSET = SetFormatConfig(
            set_open=fixed_open(open_str="frozenset({"),
            close="})",
            empty_set="frozenset()",
            preamble_lines=(),
            set_opener_template="",
            supports_heterogeneity=True,
            supports_trailing_comma=True,
        )

        @property
        def type_hint(self) -> str:
            """Python type hint name for this set format."""
            return "frozenset" if self is type(self).FROZENSET else "set"

    class VariableTypeHints(enum.Enum):
        """Variable type hint options for Python."""

        AUTO = enum.auto()
        ALWAYS = enum.auto()

        def formatter(
            self,
            *,
            bytes_hint: str,
            date_hint: str,
            datetime_hint: str,
            sequence_hint: str,
            set_hint: str,
            default_set_element_type: str,
            default_sequence_element_type: str,
            default_dict_value_type: str,
            default_dict_key_type: str,
        ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
            """Return the variable declaration formatter for this hint
            style.
            """
            if self is type(self).ALWAYS:

                def _always_formatter(
                    name: str,
                    value: str,
                    data: Value,
                    modifiers: frozenset[enum.Enum],
                ) -> str:
                    """Adapt the inline-hint declaration to the positional
                    formatter interface.
                    """
                    return _format_inline_type_hint_declaration(
                        name=name,
                        value=value,
                        data=data,
                        _modifiers=modifiers,
                        bytes_hint=bytes_hint,
                        date_hint=date_hint,
                        datetime_hint=datetime_hint,
                        sequence_hint=sequence_hint,
                        set_hint=set_hint,
                        default_set_element_type=default_set_element_type,
                        default_sequence_element_type=(
                            default_sequence_element_type
                        ),
                        default_dict_value_type=default_dict_value_type,
                        default_dict_key_type=default_dict_key_type,
                    )

                return _always_formatter

            def _auto_formatter(
                name: str,
                value: str,
                data: Value,
                modifiers: frozenset[enum.Enum],
            ) -> str:
                """Adapt the variable declaration to the positional
                formatter interface.
                """
                return _format_variable_declaration(
                    name=name,
                    value=value,
                    data=data,
                    _modifiers=modifiers,
                    bytes_hint=bytes_hint,
                    date_hint=date_hint,
                    datetime_hint=datetime_hint,
                    sequence_hint=sequence_hint,
                    set_hint=set_hint,
                    default_set_element_type=default_set_element_type,
                    default_sequence_element_type=(
                        default_sequence_element_type
                    ),
                    default_dict_value_type=default_dict_value_type,
                    default_dict_key_type=default_dict_key_type,
                )

            return _auto_formatter

    class CommentFormats(enum.Enum):
        """Comment style options."""

        HASH = CommentConfig(
            prefix="#",
            suffix="",
        )

    class DeclarationStyles(enum.Enum):
        """Declaration style options."""

        ASSIGN = DeclarationStyleConfig(
            formatter=variable_declaration_formatter(
                template="{name} = {value}"
            ),
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
        positive_infinity='float("inf")',
        negative_infinity='float("-inf")',
        nan='float("nan")',
    ):
        """Float format options."""

        REPR = enum.member(value=format_float_repr)
        SCIENTIFIC = enum.member(value=format_float_scientific)
        FIXED = enum.member(value=format_float_fixed)

    class IntegerFormats(enum.Enum):
        """Integer format options."""

        DECIMAL = MappingProxyType(
            mapping={
                "NONE": str,
                "UNDERSCORE": format_integer_underscore,
            }
        )
        HEX = MappingProxyType(
            mapping={
                "NONE": format_integer_hex,
                "UNDERSCORE": format_integer_hex,
            }
        )
        OCTAL = MappingProxyType(
            mapping={
                "NONE": format_integer_octal,
                "UNDERSCORE": format_integer_octal,
            }
        )
        BINARY = MappingProxyType(
            mapping={
                "NONE": format_integer_binary,
                "UNDERSCORE": format_integer_binary,
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

    class NumericStyles(enum.Enum):
        """Numeric literal style options."""

        OVERLOADED = enum.auto()

    class StringFormats(enum.Enum):
        """String format options."""

        DOUBLE = enum.member(value=format_string_backslash)
        SINGLE = enum.member(value=format_string_backslash_single)
        RAW = enum.member(value=format_string_raw_python)

        def __call__(self, value: str, /) -> str:
            """Format a string."""
            return self.value(value=value)

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

    class LineEndings(enum.Enum):
        """Line ending options."""

        SEMICOLON = enum.auto()

    line_endings = LineEndings

    class CallStyles(enum.Enum):
        """Call style options for Python."""

        KEYWORD = KeywordCallStyle(separator="=")
        POSITIONAL = PositionalCallStyle()

    call_styles = CallStyles

    class Modifiers(enum.Enum):
        """C++/Java/C#-style declaration modifiers: this language has none."""

    modifiers = Modifiers

    class HeterogeneousStrategies(enum.Enum):
        """Heterogeneous-scalar strategy options — this language only
        supports raising.
        """

        ERROR = NO_HETEROGENEOUS_BEHAVIOR

    heterogeneous_strategies = HeterogeneousStrategies

    class VersionFormats(enum.Enum):
        """Version options for Python."""

        PY_3_12 = enum.auto()

    version_formats = VersionFormats

    modifier_combinations = ()
    identifier_cases: ClassVar[tuple[IdentifierCase, ...]] = (
        IdentifierCase.SNAKE,
        IdentifierCase.UPPER_SNAKE,
        IdentifierCase.PASCAL,
    )

    validate_spec_for_data = no_validate_spec_for_data
    wrap_calls_with_declarations = default_wrap_calls_with_declarations

    @staticmethod
    def wrap_in_file(
        content: str,
        variable_name: str,
        body_preamble: tuple[str, ...],
    ) -> str:
        """Wrap Python code in a valid file (no-op)."""
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
        """Wrap Python declaration + assignment in a valid file."""
        return wrap_combined_in_file_noop(
            declaration=declaration,
            assignment=assignment,
            variable_name=variable_name,
            body_preamble=body_preamble,
        )

    date_format: DateFormats = DateFormats.PYTHON
    datetime_format: DatetimeFormats = DatetimeFormats.PYTHON
    bytes_format: BytesFormats = BytesFormats.HEX
    sequence_format: SequenceFormats = SequenceFormats.TUPLE
    set_format: SetFormats = SetFormats.SET
    default_set_element_type: str = "Any"
    default_sequence_element_type: str = "Any"
    default_dict_key_type: str = "str"
    default_dict_value_type: str = "Any"
    variable_type_hints: VariableTypeHints = VariableTypeHints.AUTO
    comment_format: CommentFormats = CommentFormats.HASH
    declaration_style: DeclarationStyles = DeclarationStyles.ASSIGN
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
    call_style: CallStyles = CallStyles.KEYWORD
    heterogeneous_strategy: HeterogeneousStrategies = (
        HeterogeneousStrategies.ERROR
    )
    language_version: VersionFormats = VersionFormats.PY_3_12
    indent: str = "    "

    null_literal: ClassVar[str] = "None"
    true_literal: ClassVar[str] = "True"
    false_literal: ClassVar[str] = "False"
    indent_closing_delimiter: ClassVar[bool] = False
    element_separator: ClassVar[str] = ", "
    skip_null_dict_values: ClassVar[bool] = False
    supports_collection_comments: ClassVar[bool] = True
    supports_scalar_before_comments: ClassVar[bool] = False
    supports_scalar_inline_comments: ClassVar[bool] = True
    statement_terminator: ClassVar[str] = ""
    static_preamble: ClassVar[Sequence[str]] = ()
    static_body_preamble: ClassVar[Sequence[str]] = ()
    special_float_preamble: ClassVar[tuple[str, ...]] = ()

    @cached_property
    def format_sequence_entry(self) -> Callable[[Value, str], str]:
        """Format a sequence entry."""
        return passthrough_sequence_entry

    @cached_property
    def format_set_entry(self) -> Callable[[Value, str], str]:
        """Format a set entry."""
        return passthrough_set_entry

    @cached_property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Format an assignment to an existing variable."""
        return variable_formatter(template="{name} = {value}")

    @cached_property
    def data_dependent_preamble(self) -> Callable[[Value], tuple[str, ...]]:
        """Return data-dependent preamble lines."""
        return no_data_preamble

    @cached_property
    def heterogeneous_behavior(self) -> HeterogeneousBehavior:
        """Return the heterogeneous-behavior config."""
        return self.heterogeneous_strategy.value

    @cached_property
    def format_call_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return stub declarations for a call expression."""
        return _python_call_stub

    @cached_property
    def format_call_preamble_stub(
        self,
    ) -> Callable[[Sequence[str], Sequence[str], StubReturn], tuple[str, ...]]:
        """Return file-scope stubs for a call expression."""
        return no_call_stub

    @cached_property
    def format_call_target(self) -> Callable[[Sequence[str]], str]:
        """Rewrite a dotted call target into the language's call
        syntax.
        """
        return identity_call_target

    @cached_property
    def format_call_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier into the
        language's call expression syntax.
        """
        return identity_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier(self) -> Callable[[str], str]:
        """Rewrite a ``{"$ref": "name"}`` identifier in a call-argument
        context.

        Delegates to :attr:`format_call_ref_identifier`.  Override this to
        allow call-argument ``$ref`` values that would otherwise be rejected.
        """
        return self.format_call_ref_identifier

    @cached_property
    def format_call_arg_ref_identifier_consumable(
        self,
    ) -> Callable[[str], str]:
        """Format a ``$ref`` the caller authorized as consumable.

        Delegates to :attr:`format_call_arg_ref_identifier`.  Override
        this to opt into a consuming form (e.g. C++ ``std::move``).
        """
        return self.format_call_arg_ref_identifier

    scalar_body_preamble: ClassVar[dict[type, tuple[str, ...]]] = {}

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
            dict_open=fixed_open(open_str="{"),
            close="}",
            format_entry=dict_entry_with_separator(
                separator=": ",
                format_value=passthrough_sequence_entry,
            ),
            empty_dict=None,
            preamble_lines=(),
            narrowed_open=None,
            supports_trailing_comma=True,
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
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        return self.string_format

    @cached_property
    def format_float(self) -> Callable[[float], str]:
        """Callable that formats a float value as a literal."""
        return self.float_format

    @cached_property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        return self.integer_format.get_formatter(
            numeric_separator=self.numeric_separator,
        )

    @cached_property
    def comment_config(self) -> CommentConfig:
        """Configuration for the language's comment syntax."""
        return self.comment_format.value

    @cached_property
    def ordered_map_format_config(self) -> OrderedMapFormatConfig:
        """Configuration for ordered-map formatting."""
        return OrderedMapFormatConfig(
            ordered_map_open=fixed_open(open_str="OrderedDict(["),
            close="])",
            preamble_lines=("from collections import OrderedDict",),
        )

    @cached_property
    def format_ordered_map_entry(self) -> Callable[[str, Value, str], str]:
        """Callable that formats one ordered-map entry."""
        return tuple_dict_entry(format_value=passthrough_sequence_entry)

    @cached_property
    def format_variable_declaration(
        self,
    ) -> Callable[[str, str, Value, frozenset[enum.Enum]], str]:
        """Callable that formats a new variable declaration."""
        return self.variable_type_hints.formatter(
            bytes_hint=self.bytes_format.type_hint,
            date_hint=self.date_format.type_hint,
            datetime_hint=self.datetime_format.type_hint,
            sequence_hint=self.sequence_format.type_hint,
            set_hint=self.set_format.type_hint,
            default_set_element_type=self.default_set_element_type,
            default_sequence_element_type=self.default_sequence_element_type,
            default_dict_value_type=self.default_dict_value_type,
            default_dict_key_type=self.default_dict_key_type,
        )

    @cached_property
    def scalar_preamble(self) -> dict[type, tuple[str, ...]]:
        """Per-instance scalar preamble computed from date/datetime format."""
        return date_scalar_preamble(
            date_format=self.date_format,
            datetime_format=self.datetime_format,
        )

    @cached_property
    def compute_body_preamble(
        self,
    ) -> Callable[[frozenset[type], Value], tuple[str, ...]]:
        """Compute body-preamble lines from the scalar map."""
        return body_preamble_from_scalars(
            scalar_body_preamble=self.scalar_body_preamble,
            format_lines=tuple,
        )

    @cached_property
    def type_hint_collection_preamble_lines(
        self,
    ) -> Callable[[frozenset[type]], tuple[str, ...]]:
        """Type-hint preamble computed from the configured default
        types.
        """
        return _build_type_hint_preamble(
            default_set_element_type=self.default_set_element_type,
            default_sequence_element_type=self.default_sequence_element_type,
            default_dict_value_type=self.default_dict_value_type,
            default_dict_key_type=self.default_dict_key_type,
        )

    @cached_property
    def call_style_config(self) -> CallStyle:
        """Configuration for the chosen call style."""
        config: CallStyle = self.call_style.value
        return config
