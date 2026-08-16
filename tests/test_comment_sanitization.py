"""Regression tests for target-language comment lexer hazards."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer._language import Language
from literalizer.languages import (
    Haskell,
    Kotlin,
    PureScript,
    Rust,
    Scala,
    Swift,
)


@pytest.mark.parametrize(
    argnames=("language", "unsafe_opener", "safe_opener"),
    argvalues=[
        (
            Swift(comment_format=Swift.comment_formats.BLOCK),
            "/*",
            "/ *",
        ),
        (
            Rust(comment_format=Rust.comment_formats.BLOCK),
            "/*",
            "/ *",
        ),
        (
            Scala(comment_format=Scala.comment_formats.BLOCK),
            "/*",
            "/ *",
        ),
        (
            Kotlin(comment_format=Kotlin.comment_formats.BLOCK),
            "/*",
            "/ *",
        ),
        (
            Haskell(comment_format=Haskell.comment_formats.BLOCK),
            "{-",
            "{ -",
        ),
        (
            PureScript(comment_format=PureScript.comment_formats.BLOCK),
            "{-",
            "{ -",
        ),
    ],
)
def test_nested_block_comment_openers_are_neutralized(
    language: Language,
    unsafe_opener: str,
    safe_opener: str,
) -> None:
    """Preserved source text cannot open an unclosed nested comment."""
    result = literalize(
        source=f"# nested opener {unsafe_opener} remains\nx: 1\n",
        input_format=InputFormat.YAML,
        language=language,
        variable_form=NewVariable(
            name="my_data",
            modifiers=frozenset(),
        ),
        wrap_in_file=True,
    )
    assert f"nested opener {safe_opener} remains" in result.code
    assert f"nested opener {unsafe_opener} remains" not in result.code
