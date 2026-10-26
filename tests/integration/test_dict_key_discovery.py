"""Discover key constraints from the producer grammar."""

from pathlib import Path

import pytest

from literalizer._language import NewVariableNameSyntax

from .case_discovery import (
    CaseData,
    cases_with_invalid_dict_keys,
    has_invalid_dict_keys,
)


@pytest.mark.parametrize(
    argnames=("data", "syntax", "invalid"),
    argvalues=[
        ({"_": 1}, NewVariableNameSyntax.ASCII, False),
        ({"_": 1}, NewVariableNameSyntax.ASCII_LETTER_START, True),
        ({"a-b": 1}, NewVariableNameSyntax.ASCII, True),
        ({"a-b": 1}, NewVariableNameSyntax.ASCII_KEBAB, False),
        ([{"ok": [{"_": 1}]}], NewVariableNameSyntax.ASCII, False),
        ([{"ok": [{"_": 1}]}], NewVariableNameSyntax.ASCII_LETTER_START, True),
        ({"": None}, NewVariableNameSyntax.ASCII, True),
        (["not-a-key", 1, None], NewVariableNameSyntax.ASCII, False),
        ({1: "not-a-key"}, NewVariableNameSyntax.ASCII, False),
    ],
)
def test_nested_keys_follow_the_declared_grammar(
    data: CaseData,
    syntax: NewVariableNameSyntax,
    *,
    invalid: bool,
) -> None:
    """The same input can satisfy one key grammar and violate another."""
    assert has_invalid_dict_keys(data=data, key_syntax=syntax) is invalid


def test_discovery_caches_key_constraints_independently(
    tmp_path: Path,
) -> None:
    """Discover format constraints without naming a backend."""
    for name, source in (("underscore", '{"_": 1}'), ("dash", '{"a-b": 1}')):
        folder = tmp_path / name
        folder.mkdir()
        _ = (folder / "input.json").write_text(data=source, encoding="utf-8")
        _ = (folder / "case.toml").write_text(
            data='schema_version = 1\nsuites = ["base"]\n',
            encoding="utf-8",
        )
    assert (
        cases_with_invalid_dict_keys(cases_dir=tmp_path, key_syntax=None)
        == frozenset()
    )
    assert cases_with_invalid_dict_keys(
        cases_dir=tmp_path, key_syntax=NewVariableNameSyntax.ASCII
    ) == frozenset({"dash"})
    assert cases_with_invalid_dict_keys(
        cases_dir=tmp_path, key_syntax=NewVariableNameSyntax.ASCII_LETTER_START
    ) == frozenset({"underscore", "dash"})
