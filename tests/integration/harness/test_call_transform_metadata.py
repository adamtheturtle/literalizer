"""Operand metadata for fixture transforms without native-language
syntax.
"""

import pytest
from pydantic import BaseModel, TypeAdapter

from tests.integration.call_cases import (
    GroupedCallTransform,
    LiteralArgumentsTransform,
)
from tests.integration.case_manifests import CallTransform
from tests.toml_cases import load_toml_cases


class _GroupCase(BaseModel, extra="forbid", frozen=True):
    """One abstract grouping pipeline and its operand contract."""

    name: str
    body: str
    outer: str
    suffix: str
    uses_zipped: bool


class _GroupCases(BaseModel, extra="forbid", frozen=True):
    """The manifest-owned metadata corpus."""

    cases: tuple[_GroupCase, ...]


_CASES = TypeAdapter(type=_GroupCases).validate_python(
    load_toml_cases(name="grouped_call_transforms")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_grouped_transform_preserves_operand_usage(case: _GroupCase) -> None:
    """Pin operand metadata; native expression order has compiling
    coverage.
    """
    transform = GroupedCallTransform(
        body=CallTransform(template=case.body),
        suffix=case.suffix,
        outer=CallTransform(template=case.outer),
        group=str,
    )
    assert transform.uses_zipped is case.uses_zipped


class _ArgumentCase(BaseModel, extra="forbid", frozen=True):
    """An abstract native operand expression and optional outer
    transform.
    """

    name: str
    outer: str
    suffix: str
    uses_zipped: bool


class _ArgumentCases(BaseModel, extra="forbid", frozen=True):
    """The declarative native operand metadata corpus."""

    cases: tuple[_ArgumentCase, ...]


_ARGUMENT_CASES = TypeAdapter(type=_ArgumentCases).validate_python(
    load_toml_cases(name="literal_argument_transforms")
)


@pytest.mark.parametrize(
    argnames="case",
    argvalues=_ARGUMENT_CASES.cases,
    ids=lambda case: case.name,
)
def test_literal_arguments_preserve_outer_operand_usage(
    case: _ArgumentCase,
) -> None:
    """Native operands retain an outer transform's operand contract."""
    transform = LiteralArgumentsTransform(
        call="native-value",
        suffix=case.suffix,
        outer=None if case.outer == "" else CallTransform(template=case.outer),
    )
    assert transform.uses_zipped is case.uses_zipped
