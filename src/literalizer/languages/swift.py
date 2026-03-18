"""Swift language specification."""

from __future__ import annotations

from literalizer._formatters import (
    dict_entry_with_separator,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_variable_assignment_swift,
    format_variable_declaration_swift,
    passthrough_sequence_entry,
    passthrough_set_entry,
)
from literalizer._language import Language


def _format_swift_omap_entry(key: str, value: str) -> str:
    """Format a Swift dictionary entry."""
    return f"{key}: {value}"


SWIFT = Language(
    null_literal="nil",
    true_literal="true",
    false_literal="false",
    sequence_open="[",
    sequence_close="]",
    dict_open="[",
    dict_close="]",
    format_dict_entry=dict_entry_with_separator(separator=": "),
    multiline_trailing_comma=True,
    single_element_trailing_comma=False,
    format_bytes=format_bytes_hex,
    format_date=format_date_iso,
    format_datetime=format_datetime_iso,
    empty_sequence="[Any]()",
    empty_dict="[String: Any]()",
    set_open="Set<AnyHashable>([",
    set_close="])",
    empty_set="Set<AnyHashable>()",
    format_sequence_entry=passthrough_sequence_entry,
    format_set_entry=passthrough_set_entry,
    comment_prefix="//",
    comment_suffix="",
    omap_open="[",
    omap_close="]",
    format_omap_entry=_format_swift_omap_entry,
    multiline_close_indent="",
    element_separator=", ",
    skip_null_dict_values=False,
    format_variable_declaration=format_variable_declaration_swift,
    format_variable_assignment=format_variable_assignment_swift,
    format_collection_open=None,
)
