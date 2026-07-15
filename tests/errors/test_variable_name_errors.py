"""Variable bindings reject names that are invalid in their language."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import InvalidVariableNameError
from literalizer.languages import ALL_LANGUAGES

if TYPE_CHECKING:
    from literalizer._language import Language


LANGUAGES = {language.__name__.lower(): language for language in ALL_LANGUAGES}


@pytest.mark.parametrize(
    argnames="language_name",
    argvalues=[
        "c",
        "cpp",
        "crystal",
        "d",
        "elixir",
        "erlang",
        "fortran",
        "gleam",
        "go",
        "groovy",
        "haskell",
        "haxe",
        "java",
        "javascript",
        "rust",
        "scala",
        "sml",
        "swift",
        "typescript",
        "v",
        "zig",
    ],
)
def test_malformed_variable_name_is_rejected(language_name: str) -> None:
    """A binding name cannot contain an infix hyphen."""
    language_cls = LANGUAGES[language_name]
    language: Language = language_cls()

    with pytest.raises(expected_exception=InvalidVariableNameError):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="a-b", modifiers=frozenset()),
        )


@pytest.mark.parametrize(
    argnames=("language_name", "name"),
    argvalues=[
        ("c", "switch"),
        ("cobol", "PROGRAM"),
        ("cpp", "class"),
        ("crystal", "def"),
        ("d", "class"),
        ("gleam", "let"),
        ("go", "type"),
        ("groovy", "class"),
        ("haskell", "type"),
        ("haxe", "class"),
        ("java", "class"),
        ("javascript", "class"),
        ("ruby", "class"),
        ("rust", "type"),
        ("scala", "type"),
        ("sml", "val"),
        ("swift", "class"),
        ("typescript", "class"),
        ("v", "type"),
        ("zig", "error"),
    ],
)
def test_reserved_variable_name_is_rejected(
    language_name: str, name: str
) -> None:
    """A binding name cannot be a language keyword."""
    language_cls = LANGUAGES[language_name]
    language: Language = language_cls()

    with pytest.raises(expected_exception=InvalidVariableNameError):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name=name, modifiers=frozenset()),
        )
