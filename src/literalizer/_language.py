"""Language protocol and internal spec dataclass."""

from __future__ import annotations

import dataclasses
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    import datetime
    import enum
    from collections.abc import Callable

    from literalizer._types import Value


@dataclasses.dataclass(frozen=True)
class SequenceFormatConfig:
    """Configuration for a single sequence format."""

    open_str: str
    close: str
    supports_heterogeneity: bool
    single_element_trailing_comma: bool
    empty_sequence: str | None


@dataclasses.dataclass(frozen=True)
class SetFormatConfig:
    """Configuration for a single set format."""

    open_str: str
    close: str
    empty_set: str | None


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


@dataclasses.dataclass(frozen=True)
class OrderedMapFormatConfig:
    """Configuration for ordered-map formatting."""

    open_str: str
    close: str


class SequenceFormat(Protocol):
    """Protocol for sequence format Enum members."""

    @property
    def supports_heterogeneity(self) -> bool:
        """Whether this sequence format supports mixed-type elements."""
        ...  # pylint: disable=unnecessary-ellipsis


class HasFormatEnums(type):
    """Meta-class that declares the nested format Enum class attributes.

    Language classes use ``metaclass=HasFormatEnums`` so that downstream
    code can write ``dict[str, HasFormatEnums]`` and access
    ``cls.DateFormats``, ``cls.SequenceFormats``, etc. without ``cast``
    or ``type: ignore``.
    """

    DateFormats: type[enum.Enum]
    DatetimeFormats: type[enum.Enum]
    BytesFormats: type[enum.Enum]
    SequenceFormats: type[enum.Enum]
    SetFormats: type[enum.Enum]
    CommentFormats: type[enum.Enum]


@runtime_checkable
class Language(Protocol):
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
    def format_variable_declaration(self) -> Callable[[str, str], str]:
        """Callable that formats a new variable declaration.

        Called as ``format_variable_declaration(name, value)`` where *name* is
        the variable name and *value* is the already-formatted literal value.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_variable_assignment(self) -> Callable[[str, str], str]:
        """Callable that formats an assignment to an existing variable.

        Called as ``format_variable_assignment(name, value)`` where *name* is
        the variable name and *value* is the already-formatted literal value.
        """
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def format_string(self) -> Callable[[str], str]:
        """Callable that formats a string value as a quoted literal."""
        ...  # pylint: disable=unnecessary-ellipsis

    @property
    def sequence_format(self) -> SequenceFormat:
        """The sequence format chosen for this language instance."""
        ...  # pylint: disable=unnecessary-ellipsis
