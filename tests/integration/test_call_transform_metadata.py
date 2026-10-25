"""Operand metadata for fixture transforms without native-language
syntax.
"""

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import CallContext
from tests.toml_cases import load_toml_cases

from .call_cases import GroupedCallTransform
from .case_manifests import CallTransform


class _GroupCase(BaseModel, extra="forbid", frozen=True):
    """One abstract grouping pipeline and its operand contract."""

    name: str
    body: str
    outer: str
    suffix: str
    uses_zipped: bool
    expected: str


class _GroupCases(BaseModel, extra="forbid", frozen=True):
    """The manifest-owned metadata corpus."""

    cases: tuple[_GroupCase, ...]


_CASES = TypeAdapter(type=_GroupCases).validate_python(
    load_toml_cases(name="grouped_call_transforms")
)


def _group_marker(expression: str, /) -> str:
    """Use abstract markers rather than any language's expression
    syntax.
    """
    return f"<group>{expression}</group>"


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_grouped_transform_preserves_operand_usage(case: _GroupCase) -> None:
    """An outer transform receives the grouped value and retains zip usage."""
    transform = GroupedCallTransform(
        body=CallTransform(template=case.body),
        suffix=case.suffix,
        outer=CallTransform(template=case.outer),
        group=_group_marker,
    )
    context = CallContext(
        call="call-value", index=0, row=(42,), zipped="zip-value"
    )
    assert transform.uses_zipped is case.uses_zipped
    assert transform(context) == case.expected
