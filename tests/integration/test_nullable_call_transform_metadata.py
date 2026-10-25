"""Operand contracts and invocation errors for conditional transforms."""

from typing import Literal

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import CallContext
from literalizer.languages import Cpp, Go, Python
from tests.toml_cases import load_toml_cases

from .call_cases import (
    ConditionalCallTransform,
    call_transform_for_case,
    default_call_case_specs,
)
from .case_manifests import CallTransform


class _UsageCase(BaseModel, extra="forbid", frozen=True):
    """An abstract expression pipeline and its operand contract."""

    name: str
    outer: str
    uses_zipped: bool
    expected: str


class _ErrorCase(BaseModel, extra="forbid", frozen=True):
    """An unsupported direct use of the conditional recipe."""

    name: str
    language: Literal["Python", "Cpp", "Go"]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The internal operand and invocation-error corpus."""

    cases: tuple[_UsageCase, ...]
    errors: tuple[_ErrorCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="nullable_call_transforms")
)
_LANGUAGES = {"Python": Python, "Cpp": Cpp, "Go": Go}


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_conditional_transform_preserves_operand_usage(
    case: _UsageCase,
) -> None:
    """The outer callback retains the same call and zipped operands."""
    transform = ConditionalCallTransform(
        template="select<{call}>{inner_comment}|{null}{trailing_comment}",
        null_value="null-value",
        comment_prefix="#",
        indent="    ",
        outer=CallTransform(template=case.outer)
        if len(case.outer) > 0
        else None,
    )
    context = CallContext(
        call="call-value", index=0, row=(42,), zipped="zip-value"
    )
    assert transform.uses_zipped is case.uses_zipped
    assert transform(context) == case.expected


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.errors, ids=lambda case: case.name
)
def test_conditional_transform_requires_native_result(
    case: _ErrorCase,
) -> None:
    """A direct invocation cannot invent a nullable type or grammar."""
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_nullable_object_conditional_comments"
    )
    with pytest.raises(
        expected_exception=ValueError,
        match=(
            "call_transform_nullable_conditional requires a nullable "
            "object result and a native conditional expression"
        ),
    ):
        _ = call_transform_for_case(
            spec=_LANGUAGES[case.language](), config=config
        )
