"""Language protocol and internal spec dataclass."""

import dataclasses
import datetime
from collections.abc import Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class Language(Protocol):
    """Protocol describing how a language formats scalar literals and
    sequences.

    Predefined instances for common languages are available as module-level
    constants in :mod:`literalizer.languages` (e.g.
    :data:`~literalizer.languages.PYTHON`,
    :data:`~literalizer.languages.JAVASCRIPT`). To support additional
    languages or override defaults, write a class that provides all the
    required attributes, or use :class:`~literalizer.LanguageSpec`.
    """

    null_literal: str
    """The literal representing null/None."""

    true_literal: str
    """The literal representing true/True."""

    false_literal: str
    """The literal representing false/False."""

    sequence_open: str
    """The opening delimiter for sequences."""

    sequence_close: str
    """The closing delimiter for sequences."""

    dict_open: str
    """The opening delimiter for dict literals."""

    dict_close: str
    """The closing delimiter for dict literals."""

    format_dict_entry: Callable[[str, str], str]
    """Callable that formats a dict entry from a pre-formatted key and
    value string.
    """

    multiline_trailing_comma: bool
    """Whether to append a trailing comma after the last entry."""

    single_element_trailing_comma: bool
    """Whether a single-element sequence requires a trailing comma."""

    format_bytes: Callable[[bytes], str]
    """Callable that formats a :class:`bytes` value as a string
    literal.
    """

    format_date: Callable[[datetime.date], str]
    """Callable that formats a :class:`datetime.date` as a string
    literal.
    """

    format_datetime: Callable[[datetime.datetime], str]
    """Callable that formats a :class:`datetime.datetime` as a string
    literal.
    """

    empty_sequence: str | None
    """Override for empty sequence literals, or ``None``."""

    empty_dict: str | None
    """Override for empty dict literals, or ``None``."""

    set_open: str
    """The opening delimiter for set literals."""

    set_close: str
    """The closing delimiter for set literals."""

    empty_set: str | None
    """Override for empty set literals, or ``None``."""

    format_sequence_entry: Callable[[str], str]
    """Callable that formats a sequence entry."""

    format_set_entry: Callable[[str], str]
    """Callable that formats a set entry."""

    comment_prefix: str
    """The comment prefix for the language."""

    comment_suffix: str
    """The comment suffix for the language."""

    omap_open: str
    """The opening delimiter for ordered-map literals."""

    omap_close: str
    """The closing delimiter for ordered-map literals."""

    format_omap_entry: Callable[[str, str], str]
    """Callable that formats one ordered-map entry."""

    multiline_close_indent: str
    """The prefix to prepend to the closing delimiter of multi-line
    structures.
    """

    element_separator: str
    """The separator placed between elements in inline sequences."""

    skip_null_dict_values: bool
    """Whether to omit dict entries whose value is ``None``."""

    format_variable_declaration: Callable[[str, str], str]
    """Callable that formats a new variable declaration."""

    format_variable_assignment: Callable[[str, str], str]
    """Callable that formats an assignment to an existing variable."""

    format_string: Callable[[str], str]
    """Callable that formats a string value as a quoted literal."""


@dataclasses.dataclass
class LanguageSpec:
    """Dataclass implementing :class:`Language`.

    Use this to build fully custom language specifications without
    writing a dedicated class.
    """

    null_literal: str
    true_literal: str
    false_literal: str
    sequence_open: str
    sequence_close: str
    dict_open: str
    dict_close: str
    format_dict_entry: Callable[[str, str], str]
    multiline_trailing_comma: bool
    single_element_trailing_comma: bool
    format_bytes: Callable[[bytes], str]
    format_date: Callable[[datetime.date], str]
    format_datetime: Callable[[datetime.datetime], str]
    empty_sequence: str | None
    empty_dict: str | None
    set_open: str
    set_close: str
    empty_set: str | None
    format_sequence_entry: Callable[[str], str]
    format_set_entry: Callable[[str], str]
    comment_prefix: str
    comment_suffix: str
    omap_open: str
    omap_close: str
    format_omap_entry: Callable[[str, str], str]
    multiline_close_indent: str
    element_separator: str
    skip_null_dict_values: bool
    format_variable_declaration: Callable[[str, str], str]
    format_variable_assignment: Callable[[str, str], str]
    format_string: Callable[[str], str]
