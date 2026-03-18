"""PowerShell language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    passthrough_set_entry,
)
from literalizer._language import Language


@beartype
def _format_sequence_entry(item: str) -> str:
    """Prevent nested array flattening with a unary comma prefix.

    In PowerShell ``@()`` collects pipeline output and arrays written to the
    pipeline are automatically unrolled.  Prefixing a nested ``@(…)`` with
    the unary comma operator keeps it as a single array element.

    Example: ``"@(1; 2)"`` → ``",@(1; 2)"``; ``"42"`` → ``"42"``.
    """
    if item.startswith("@("):
        return f",{item}"
    return item


def _format_string(value: str) -> str:
    """Format a string using PowerShell back-tick escaping."""
    escaped = (
        value.replace("`", "``")
        .replace('"', '`"')
        .replace("\n", "`n")
        .replace("\t", "`t")
    )
    return f'"{escaped}"'


def _format_variable_declaration(name: str, value: str) -> str:
    """Format a PowerShell variable declaration."""
    return f"${name} = {value}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format a PowerShell variable assignment."""
    return f"${name} = {value}"


POWERSHELL = Language(
    null_literal="$null",
    true_literal="$true",
    false_literal="$false",
    sequence_open="@(",
    sequence_close=")",
    dict_open="@{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=" = "),
    multiline_trailing_comma=False,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="@(",
    set_close=")",
    empty_set=None,
    format_sequence_entry=_format_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="#",
    comment_suffix="",
    omap_open="[ordered]@{",
    omap_close="}",
    format_omap_entry=dict_entry_with_separator(separator=" = "),
    multiline_close_indent="",
    element_separator="; ",
    skip_null_dict_values=False,
    format_variable_declaration=_format_variable_declaration,
    format_variable_assignment=_format_variable_assignment,
    format_string=_format_string,
)
