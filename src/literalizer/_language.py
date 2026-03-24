"""Language protocol and internal spec dataclass."""

import dataclasses
import datetime
import enum
from collections.abc import Callable, Sequence
from typing import Protocol, cast, runtime_checkable

from literalizer._types import Value


@dataclasses.dataclass(frozen=True)
class SequenceFormatConfig:
    """Configuration for a single sequence format."""

    sequence_open: Callable[[list[Value]], str]
    close: str
    supports_heterogeneity: bool
    single_element_trailing_comma: bool
    empty_sequence: str | None
    preamble_lines: tuple[str, ...]
    format_entry: Callable[[str], str]


@dataclasses.dataclass(frozen=True)
class DateFormatConfig:
    """Configuration for a single date format."""

    formatter: Callable[[datetime.date], str]
    preamble_lines: tuple[str, ...] = ()
    type_produced: type = datetime.date


@dataclasses.dataclass(frozen=True)
class DatetimeFormatConfig:
    """Configuration for a single datetime format."""

    formatter: Callable[[datetime.datetime], str]
    preamble_lines: tuple[str, ...] = ()
    type_produced: type = datetime.datetime


def date_scalar_preamble(
    *,
    date_format: enum.Enum,
    datetime_format: enum.Enum,
    extra: dict[type, tuple[str, ...]] | None = None,
) -> dict[type, tuple[str, ...]]:
    """Build the ``scalar_preamble`` dict for date/datetime formats.

    Args:
        date_format: The date format enum member whose ``.value`` has
            a ``preamble_lines`` attribute.
        datetime_format: The datetime format enum member whose ``.value``
            has a ``preamble_lines`` attribute.
        extra: Optional additional type→preamble mappings to include
            unconditionally (e.g. for C++ ``#include <string>``).

    Returns:
        A dict mapping Python types to their required preamble lines,
        omitting entries whose preamble is empty.
    """
    return {
        **(extra or {}),
        **{
            t: p
            for t, p in (
                (datetime.date, date_format.value.preamble_lines),
                (datetime.datetime, datetime_format.value.preamble_lines),
            )
            if p
        },
    }


@dataclasses.dataclass(frozen=True)
class SetFormatConfig:
    """Configuration for a single set format."""

    set_open: Callable[[list[Value]], str]
    close: str
    empty_set: str | None
    preamble_lines: tuple[str, ...]
    set_opener_template: str


@dataclasses.dataclass(frozen=True)
class CommentConfig:
    """Configuration for language comment syntax."""

    prefix: str
    suffix: str


@dataclasses.dataclass(frozen=True)
class DictFormatConfig:
    """Configuration for dict formatting."""

    open_fn: Callable[[dict[str, Value]], str]
    close: str
    format_entry: Callable[[str, str], str]
    empty_dict: str | None
    preamble_lines: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class OrderedMapFormatConfig:
    """Configuration for ordered-map formatting."""

    open_str: str
    close: str
    preamble_lines: tuple[str, ...]


@dataclasses.dataclass(frozen=True)
class DeclarationStyleConfig:
    """Configuration for a single declaration style."""

    formatter: Callable[[str, str, Value], str]


class SequenceFormat(Protocol):
    """Protocol for sequence format Enum members."""

    @property
    def supports_heterogeneity(self) -> bool:
        """Whether this sequence format supports mixed-type elements."""
        ...  # pylint: disable=unnecessary-ellipsis


class SupportsHeterogeneityMixin:
    """Mixin for ``SequenceFormats`` enums.

    Provides the :attr:`supports_heterogeneity` property by delegating
    to the underlying :class:`SequenceFormatConfig` value.  Use as::

        class SequenceFormats(SupportsHeterogeneityMixin, enum.Enum):
            ARRAY = SequenceFormatConfig(...)
    """

    @property
    def supports_heterogeneity(self) -> bool:
        """Whether this sequence format supports mixed-type elements."""
        config = cast("SequenceFormatConfig", cast("enum.Enum", self).value)
        return config.supports_heterogeneity


class LanguageCls(type):
    """Meta-class that declares the nested format Enum class attributes.

    Language classes use ``metaclass=LanguageCls`` so that downstream
    code can write ``dict[str, LanguageCls]`` and access
    ``cls.DateFormats``, ``cls.SequenceFormats``, etc. without ``cast``
    or ``type: ignore``.
    """

    DateFormats: type[enum.Enum]
    DatetimeFormats: type[enum.Enum]
    BytesFormats: type[enum.Enum]
    SequenceFormats: type[enum.Enum]
    SetFormats: type[enum.Enum]
    CommentFormats: type[enum.Enum]
    VariableTypeHints: type[enum.Enum]
    DeclarationStyles: type[enum.Enum]
    DictFormats: type[enum.Enum]
    IntegerFormats: type[enum.Enum]
    NumericSeparators: type[enum.Enum]
    StringFormats: type[enum.Enum]
    TrailingCommas: type[enum.Enum]
    extension: str
    pygments_name: str


@runtime_checkable
class Language(Protocol):  # pylint: disable=too-many-public-methods
    """Protocol describing how a language formats scalar literals and
    sequences.

    Predefined instances for common languages are available as module-level
    constants in :mod:`literalizer.languages` (e.g.
    :data:`~literalizer.languages.PYTHON`,
    :data:`~literalizer.languages.JAVASCRIPT`). To support additional
    languages or override defaults, write a class that provides all the
    required attributes.
    """

    # Each language class defines PascalCase nested Enum classes
    # (``DateFormats``, ``SequenceFormats``, …) and snake_case class
    # attributes that alias them (``date_formats = DateFormats``, …).
    # The aliases look redundant but are required: nested classes are
    # class-level (ClassVar) attributes, while Protocol properties are
    # instance-level.  No single declaration style (``@property``,
    # ``ClassVar``, or plain annotation) satisfies mypy, pyright, *and*
    # pyrefly simultaneously for PascalCase names that shadow nested
    # classes.  The snake_case aliases sidestep the issue entirely.

    @property
    def bytes_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the bytes formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the sequence formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the set formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def date_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the date formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def datetime_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the datetime formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the comment formats this language
        supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_type_hints_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the variable type hint options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def declaration_styles(self) -> type[enum.Enum]:
        """Enum class whose members list the declaration style options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the dict/map format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def integer_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the integer format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_separators(self) -> type[enum.Enum]:
        """Enum class whose members list the numeric separator options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def string_formats(self) -> type[enum.Enum]:
        """Enum class whose members list the string format options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_commas(self) -> type[enum.Enum]:
        """Enum class whose members list the trailing comma options
        this language supports.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    extension: str
    """The file extension for this language, including the leading dot."""

    pygments_name: str
    """The Pygments lexer short name for syntax highlighting."""

    null_literal: str
    """The literal representing null/None."""

    true_literal: str
    """The literal representing true/True."""

    false_literal: str
    """The literal representing false/False."""

    @property
    def sequence_open(self) -> Callable[[list[Value]], str]:
        """Callable that returns the opening delimiter for a sequence.

        Receives the list of items about to be formatted, so the delimiter
        can depend on the element types when needed.  For a fixed delimiter
        use :func:`~literalizer.fixed_sequence_open`.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    sequence_format_config: SequenceFormatConfig
    """Configuration for the chosen sequence format."""

    dict_format_config: DictFormatConfig
    """Configuration for dict formatting."""

    multiline_trailing_comma: bool
    """Whether to append a trailing comma after the last entry."""

    @property
    def format_bytes(self) -> Callable[[bytes], str]:
        """Callable that formats a :class:`bytes` value as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_date(self) -> Callable[[datetime.date], str]:
        """Callable that formats a :class:`datetime.date` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_datetime(self) -> Callable[[datetime.datetime], str]:
        """Callable that formats a :class:`datetime.datetime` as a string
        literal.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    set_format_config: SetFormatConfig
    """Configuration for the chosen set format."""

    @property
    def format_sequence_entry(self) -> Callable[[str], str]:
        """Callable that formats a sequence entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_set_entry(self) -> Callable[[str], str]:
        """Callable that formats a set entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    comment_config: CommentConfig
    """Configuration for the language's comment syntax."""

    ordered_map_format_config: OrderedMapFormatConfig
    """Configuration for ordered-map formatting."""

    @property
    def format_ordered_map_entry(self) -> Callable[[str, str], str]:
        """Callable that formats one ordered-map entry."""
        ...  # pylint: disable=unnecessary-ellipsis

    multiline_close_indent: str
    """The prefix to prepend to the closing delimiter of multi-line
    structures.
    """

    element_separator: str
    """The separator placed between elements in inline sequences."""

    skip_null_dict_values: bool
    """Whether to omit dict entries whose value is ``None``."""

    supports_collection_comments: bool
    """Whether the language supports comments inside collection
    initializers.

    When ``False``, YAML comments on collection elements are emitted as
    standalone comment lines immediately before the collection (or before
    the variable declaration when a variable name is supplied) rather than
    being placed inside the ``{...}`` block.
    """

    @property
    def format_variable_declaration(self) -> Callable[[str, str, Value], str]:
        """Callable that formats a new variable declaration.

        Called as ``format_variable_declaration(name, value, data)`` where
        *name* is the variable name, *value* is the already-formatted literal
        value, and *data* is the original parsed data structure.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_assignment(self) -> Callable[[str, str, Value], str]:
        """Callable that formats an assignment to an existing variable.

        Called as ``format_variable_assignment(name, value, data)`` where
        *name* is the variable name, *value* is the already-formatted literal
        value, and *data* is the original parsed data structure.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_integer(self) -> Callable[[int], str]:
        """Callable that formats an int value as a literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def variable_type_hints(self) -> enum.Enum:
        """The variable type hint option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_format(self) -> SequenceFormat:
        """The sequence format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def set_format(self) -> enum.Enum:
        """The set format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def comment_format(self) -> enum.Enum:
        """The comment format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def declaration_style(self) -> enum.Enum:
        """The declaration style chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def dict_format(self) -> enum.Enum:
        """The dict/map format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def integer_format(self) -> enum.Enum:
        """The integer format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def numeric_separator(self) -> enum.Enum:
        """The numeric separator option chosen for this language
        instance.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def string_format(self) -> enum.Enum:
        """The string format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def trailing_comma(self) -> enum.Enum:
        """The trailing comma option chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis

    static_preamble: Sequence[str]
    """Lines (imports, package declarations, etc.) that are always
    emitted before the generated code, regardless of what types appear
    in the data.  Use an empty sequence when none are needed.
    """

    scalar_preamble: dict[type, tuple[str, ...]]
    """Maps Python scalar types to the preamble lines required when
    that type appears in the data.  For example, a language that needs
    ``import datetime`` when dates are present would include
    ``{datetime.date: ("import datetime",)}``.
    """

    scalar_body_preamble: dict[type, tuple[str, ...]]
    """Maps Python scalar types to body-preamble lines that are
    prepended to the generated code.

    Most languages leave this empty.  Haskell uses it for typeclass
    instance definitions.
    """

    type_hint_collection_preamble_lines: tuple[str, ...]
    """Preamble lines required when the language produces type-hinted
    variable declarations *and* the data contains collections.
    Empty for most languages; Python sets this to
    ``("from typing import Any",)`` when inline hints are enabled.
    """
