"""Go language specification."""

from __future__ import annotations

from beartype import beartype

from literalizer._language import Language
from literalizer.formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_go,
    format_variable_declaration_go,
    passthrough_sequence_entry,
)


@beartype
def _format_go_set_entry(item: str) -> str:
    """Format a Go set entry as a map entry with empty struct value.

    Example: ``"apple"`` → ``"apple": struct{}{}``.
    """
    return f"{item}: struct{{}}{{}}"


def _format_go_omap_entry(key: str, value: str) -> str:
    """Format a Go ordered-map entry as a ``{key, value}`` pair."""
    return f"{{{key}, {value}}}"


GO = Language(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="[]any{",
    sequence_close="}",
    dict_open="map[string]any{",
    dict_close="}",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence=None,
    empty_dict=None,
    set_open="map[any]struct{}{",
    set_close="}",
    empty_set=None,
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=_format_go_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[][2]any{",
    omap_close="}",
    format_omap_entry=_format_go_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_go,
    format_variable_assignment=format_variable_assignment_go,
)
