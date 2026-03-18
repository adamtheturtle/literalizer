"""Language data class."""

from __future__ import annotations

import dataclasses
import datetime  # noqa: TC003
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable


@dataclasses.dataclass(frozen=True)
class Language:
    """Describes how a language formats scalar literals and sequences.

    Predefined instances for common languages are available as module-level
    constants in :mod:`literalizer.languages` (e.g.
    :data:`~literalizer.languages.PYTHON`,
    :data:`~literalizer.languages.JAVASCRIPT`). Create custom instances to
    support additional languages or override defaults.
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
    value
    string.  Use :func:`~literalizer._formatters.dict_entry_with_separator`
    for the common ``key + separator + value`` pattern.
    """

    multiline_trailing_comma: bool
    """Whether to append a trailing comma after the last entry."""

    single_element_trailing_comma: bool
    """Whether a single-element sequence requires a trailing comma to be
    syntactically unambiguous (e.g. Python tuples).
    """

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
    """Override for empty sequence literals, or ``None`` to use
    ``sequence_open + sequence_close``.
    """

    empty_dict: str | None
    """Override for empty dict literals, or ``None`` to use
    ``dict_open + dict_close``.
    """

    set_open: str
    """The opening delimiter for set literals."""

    set_close: str
    """The closing delimiter for set literals."""

    empty_set: str | None
    """Override for empty set literals, or ``None`` to use
    ``set_open + set_close``.
    """

    format_sequence_entry: Callable[[str], str]
    """Callable that formats a sequence entry from a pre-formatted item
    string.  Use
    :func:`~literalizer._formatters.passthrough_sequence_entry` when no
    transformation is needed.
    """

    format_set_entry: Callable[[str], str]
    """Callable that formats a set entry from a pre-formatted item string.
    Use :func:`~literalizer._formatters.passthrough_set_entry` when no
    transformation is needed.
    """

    comment_prefix: str
    """The comment prefix for the language (e.g. ``"#"`` or ``"//"``)."""

    comment_suffix: str
    """The comment suffix for the language (e.g. ``""`` or ``" *)"`` for
    block-comment styles).
    """

    omap_open: str
    """The opening delimiter for ordered-map literals."""

    omap_close: str
    """The closing delimiter for ordered-map literals."""

    format_omap_entry: Callable[[str, str], str]
    """Callable that formats one ordered-map entry from a pre-formatted key
    and value string.
    """

    multiline_close_indent: str
    """The prefix to prepend to the closing delimiter of multi-line
    sequences, sets, and dicts.  Defaults to ``""`` (closing delimiter at
    column 0).  Set to ``"    "`` for languages like Haskell where the
    layout rule requires the closing bracket to be indented.
    """

    element_separator: str
    """The separator placed between elements in inline sequences (e.g.
    ``", "`` for most languages, ``" "`` for Clojure).  The stripped form
    is used as the per-element suffix in multi-line sequences.
    """

    skip_null_dict_values: bool
    """Whether to omit dict entries whose value is ``None``."""

    format_variable_declaration: Callable[[str, str], str]
    """Callable that formats a new variable declaration from a name and
    value string.
    """

    format_variable_assignment: Callable[[str, str], str]
    """Callable that formats an assignment to an existing variable from a
    name and value string.
    """

    format_string: Callable[[str], str]
    """Callable that formats a string value as a quoted literal.

    Use :func:`~literalizer._formatters.format_string_backslash` for the
    common backslash-escape convention, or provide a custom callable for
    languages with a different escape convention (e.g. PowerShell uses
    back-tick escaping).
    """
