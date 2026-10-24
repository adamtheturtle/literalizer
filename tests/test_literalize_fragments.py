"""TOML-driven public API tests for incomplete literal fragments.

These fragments omit delimiters or reference externally declared names,
so they cannot use the compiling whole-file golden suite. The manifest
owns their sources, API arguments, and exact result expectations.
"""

from pathlib import Path
from typing import Literal

import pytest
from pydantic import BaseModel, Field, TypeAdapter

from literalizer import (
    ExistingVariable,
    LiteralizeResult,
    NewVariable,
    ValueInput,
    VariableForm,
    literalize,
    literalize_call,
)
from tests.integration.case_manifests import (
    CallInputFormat,
    CallTransformTemplate,
    ManifestLanguage,
)
from tests.toml_cases import load_toml_cases

type _ResultView = Literal["code", "bare_code"]


# Omitted TOML keys leave optional reference values and binding forms unset.
class _FragmentCase(  # noqa: NOD001
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Shared source, language, reference values, and result
    expectations.
    """

    name: str
    language: ManifestLanguage
    source: str
    input_format: CallInputFormat
    expected: dict[_ResultView, str] = Field(min_length=1)
    ref_values: dict[str, ValueInput] | None = None
    variable_form: Literal["new", "existing"] | None = None

    def resolved_variable_form(self) -> VariableForm | None:
        """Select the declared binding form used by this fragment."""
        if self.variable_form == "new":
            return NewVariable(name="my_data", modifiers=frozenset())
        if self.variable_form == "existing":
            return ExistingVariable(name="my_data")
        return None


class _LiteralCase(_FragmentCase, frozen=True):
    """One delimiter and indentation configuration for a literal."""

    pre_indent_level: int
    include_delimiters: bool


class _CallCase(_FragmentCase, frozen=True):  # noqa: NOD001
    """One externally defined call target and its argument
    configuration.
    """

    target_function: str
    parameter_names: tuple[str, ...]
    per_element: bool
    call_transform: CallTransformTemplate | None = None


class _FragmentCases(BaseModel, extra="forbid", frozen=True):
    """All declarative literal and call fragment cases."""

    literals: tuple[_LiteralCase, ...]
    calls: tuple[_CallCase, ...]


_CASE_DOCUMENTS = tuple(
    TypeAdapter(type=_FragmentCases).validate_python(
        load_toml_cases(name=path.stem)
    )
    for path in sorted(
        (Path(__file__).parent / "unit_cases").glob(
            pattern="literalize_fragments*.toml"
        )
    )
)
_CASES = _FragmentCases(
    literals=tuple(
        case for document in _CASE_DOCUMENTS for case in document.literals
    ),
    calls=tuple(
        case for document in _CASE_DOCUMENTS for case in document.calls
    ),
)


def _check_result(*, case: _FragmentCase, result: LiteralizeResult) -> None:
    """Compare the declared result views."""
    views = {"code": result.code, "bare_code": result.bare_code}
    assert {name: views[name] for name in case.expected} == case.expected


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.literals, ids=lambda case: case.name
)
def test_literal_fragment(case: _LiteralCase) -> None:
    """Each literal fragment preserves its manifest-owned expectations."""
    result = literalize(
        source=case.source,
        input_format=case.input_format,
        language=case.language(),
        pre_indent_level=case.pre_indent_level,
        include_delimiters=case.include_delimiters,
        variable_form=case.resolved_variable_form(),
        ref_key="$ref",
        ref_values=case.ref_values,
    )
    _check_result(case=case, result=result)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.calls, ids=lambda case: case.name
)
def test_call_fragment(case: _CallCase) -> None:
    """Each call fragment preserves its manifest-owned expectations."""
    result = literalize_call(
        source=case.source,
        input_format=case.input_format,
        language=case.language(),
        target_function=case.target_function,
        parameter_names=case.parameter_names,
        per_element=case.per_element,
        call_transform=case.call_transform,
        variable_form=case.resolved_variable_form(),
        ref_key="$ref",
        ref_values=case.ref_values,
    )
    _check_result(case=case, result=result)
