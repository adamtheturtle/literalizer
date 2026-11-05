"""Tests that deep input reaches the shared guard, not the stack limit.

A document deeper than the parse-depth guard allows is refused with a
typed error.  Anything below it has to render, which means a per-value
walk must not call itself: a beartype-wrapped call costs several
interpreter frames per level, so such a walk runs out of stack long
before the guard is reached (issue #4560).

This pins the unwrapped API at 400 levels. Wrapped rendering and golden
fixture loading have separate depth limits, so this boundary remains a
direct test alongside shallower compiling cases.
"""

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import literalize
from tests.integration.case_manifests import CallInputFormat, ManifestLanguage
from tests.toml_cases import load_toml_cases


class _DepthCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """A compact recipe for a deep input and its rendering invariant."""

    name: str
    opener: str
    closer: str
    depth: int
    payload: str
    input_format: CallInputFormat
    language: ManifestLanguage
    expected_fragment: str
    expected_count: int


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The declarative depth-limit controls."""

    cases: tuple[_DepthCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="deep_nesting_controls")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_below_guard_depth_renders(case: _DepthCase) -> None:
    """Input the guard admits renders rather than exhausting the stack."""
    source = case.opener * case.depth + case.payload + case.closer * case.depth
    result = literalize(
        source=source, input_format=case.input_format, language=case.language()
    )
    assert (
        result.declaration_code.count(case.expected_fragment)
        == case.expected_count
    )
