"""Rendering stack exhaustion preserves the input format's public
error.
"""

from typing import Never

import pytest

import literalizer
from literalizer.exceptions import (
    JSON5ParseError,
    JSONCParseError,
    JSONParseError,
    ParseError,
    TOMLParseError,
    YAMLParseError,
)
from literalizer.languages import ALL_LANGUAGES


def _exhaust_stack(**_kwargs: object) -> Never:
    """Reproduce stack exhaustion independently of a renderer's depth."""
    msg = "rendering exhausted the stack"
    raise RecursionError(msg)


@pytest.mark.parametrize(
    argnames=("input_format", "error"),
    argvalues=[
        (literalizer.InputFormat.JSON, JSONParseError),
        (literalizer.InputFormat.JSON5, JSON5ParseError),
        (literalizer.InputFormat.JSONC, JSONCParseError),
        (literalizer.InputFormat.TOML, TOMLParseError),
        (literalizer.InputFormat.YAML, YAMLParseError),
    ],
)
def test_rendering_recursion_has_a_typed_error(
    input_format: literalizer.InputFormat,
    error: type[ParseError],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Every language translates stack failures at the API boundary."""
    monkeypatch.setattr(
        target="literalizer._literalize._literalize_pre_form_impl",
        name=_exhaust_stack,
    )
    for language in ALL_LANGUAGES:
        with pytest.raises(
            expected_exception=error,
            match="input exceeds the supported nesting depth",
        ):
            _ = literalizer.literalize(
                source="",
                input_format=input_format,
                language=language(),
            )
