"""Rendering stack exhaustion preserves the input format's public
error.
"""

from typing import Never

import pytest
from pydantic import BaseModel, TypeAdapter

import literalizer
from literalizer.languages import ALL_LANGUAGES
from tests.errors.rejection_manifests import ExceptionType
from tests.integration.manifest_values import (
    CallInputFormat,
)
from tests.toml_cases import load_toml_cases


class _RecursionCase(BaseModel, extra="forbid", frozen=True):
    """One input format and its public stack-exhaustion diagnostic."""

    name: str
    input_format: CallInputFormat
    error: ExceptionType
    source: str
    message: str


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The input-format error boundary matrix."""

    cases: tuple[_RecursionCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="rendering_recursion_errors")
)


def _exhaust_stack(**_kwargs: object) -> Never:
    """Reproduce stack exhaustion without relying on rendering depth."""
    msg = "rendering exhausted the stack"
    raise RecursionError(msg)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_rendering_recursion_has_a_typed_error(
    case: _RecursionCase, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Every language translates stack failures at the API boundary."""
    monkeypatch.setattr(
        target="literalizer._literalize._literalize_pre_form_impl",
        name=_exhaust_stack,
    )
    for language in ALL_LANGUAGES:
        with pytest.raises(expected_exception=case.error, match=case.message):
            _ = literalizer.literalize(
                source=case.source,
                input_format=case.input_format,
                language=language(),
            )
