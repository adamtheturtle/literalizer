"""Tests for small source-value classification paths."""

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer.languages import Ada, Cobol

if TYPE_CHECKING:
    from literalizer._types import Value


def test_ada_character_widening_uses_source_string() -> None:
    """Only a sole C0 character needs an empty-string prefix."""
    format_string = Ada().format_string

    assert format_string("\x01") == '"" & Character\'Val(1)'
    assert format_string("\x01x") == 'Character\'Val(1) & "x"'
    assert format_string("\u2028") == (
        "Character'Val(226) & Character'Val(128) & Character'Val(168)"
    )


def test_cobol_picture_clause_uses_source_scalar_type() -> None:
    """COBOL does not infer numeric storage from rendered digits."""
    language = Cobol()

    assert language.format_sequence_entry(1, "3.14") == (
        "05 FILLER PIC S9(18) COMP-5 VALUE 3.14."
    )
    assert language.format_sequence_entry(3.14, "42") == (
        "05 FILLER COMP-2 VALUE 42."
    )
    assert language.format_sequence_entry("42", '"text"') == (
        '05 FILLER PIC X(4) VALUE "text".'
    )


def test_cobol_mapping_and_binding_shape_use_source_value() -> None:
    """COBOL group-item selection comes from the source container."""
    language = Cobol()
    collection: list[Value] = []
    collection.append(1)
    formatted_key = language.dict_format_config.format_key(
        raw_key='source"key', formatted_key='"misleading"'
    )

    assert (
        language.dict_format_config.format_entry(
            formatted_key, collection, "not-a-data-entry"
        )
        == "05 F-SOURCE-KEY.\n    not-a-data-entry"
    )
    assert (
        language.format_variable_declaration(
            "value",
            "not-a-data-entry",
            collection,
            frozenset(),
        )
        == "01 VALUE.\nnot-a-data-entry"
    )
    assert (
        language.format_variable_assignment("value", "05 FILLER.", 1)
        == "MOVE 05 FILLER. TO VALUE."
    )
