"""TOML-driven public API tests for incomplete literal fragments.

These fragments omit delimiters or reference externally declared names,
so they cannot use the compiling whole-file golden suite. The manifest
owns their sources, API arguments, and exact result expectations.
"""

import dataclasses
from typing import Literal

import pytest
from pydantic import BaseModel, Field, TypeAdapter

from literalizer import (
    ExistingVariable,
    Language,
    LiteralizeResult,
    NewVariable,
    ValueInput,
    VariableForm,
    literalize,
    literalize_call,
)
from tests.enum_members import enum_member_by_name
from tests.integration.case_manifests import CallInputFormat, ManifestLanguage
from tests.toml_cases import load_toml_cases

type _ResultView = Literal["code", "bare_code"]


# Omitted TOML keys leave optional reference values and preamble checks unset.
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
    expected_preamble: tuple[str, ...] | None = None
    json_type: str | None = None
    variable_form: Literal["new", "existing"] | None = None

    def resolved_variable_form(self) -> VariableForm | None:
        """Select the caller-owned binding used by this fragment."""
        if self.variable_form == "new":
            return NewVariable(name="my_data", modifiers=frozenset())
        if self.variable_form == "existing":
            return ExistingVariable(name="my_data")
        return None


class _LiteralCase(_FragmentCase, frozen=True):
    """One delimiter and indentation configuration for a literal."""

    pre_indent_level: int
    include_delimiters: bool


class _CallCase(_FragmentCase, frozen=True):
    """One externally defined call target and its argument
    configuration.
    """

    target_function: str
    parameter_names: tuple[str, ...]
    per_element: bool


class _FragmentCases(BaseModel, extra="forbid", frozen=True):
    """All declarative literal and call fragment cases."""

    literals: tuple[_LiteralCase, ...]
    calls: tuple[_CallCase, ...]


_CASES = TypeAdapter(type=_FragmentCases).validate_python(
    load_toml_cases(name="literalize_fragments"),
)


def _fragment_language(*, case: _FragmentCase) -> Language:
    """Apply the JSON value mode explicitly selected by a fragment."""
    language = case.language()
    if case.json_type is not None:
        language = dataclasses.replace(
            language,
            json_type=enum_member_by_name(
                enum_cls=case.language.JsonTypes, name=case.json_type
            ),
        )
    return language


def _check_result(*, case: _FragmentCase, result: LiteralizeResult) -> None:
    """Compare the declared result views and optional preamble
    contract.
    """
    views = {"code": result.code, "bare_code": result.bare_code}
    assert {name: views[name] for name in case.expected} == case.expected
    if case.expected_preamble is not None:
        assert result.preamble == case.expected_preamble


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.literals, ids=lambda case: case.name
)
def test_literal_fragment(case: _LiteralCase) -> None:
    """Each literal fragment preserves its manifest-owned expectations."""
    result = literalize(
        source=case.source,
        input_format=case.input_format,
        language=_fragment_language(case=case),
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
        language=_fragment_language(case=case),
        target_function=case.target_function,
        parameter_names=case.parameter_names,
        per_element=case.per_element,
        variable_form=case.resolved_variable_form(),
        ref_key="$ref",
        ref_values=case.ref_values,
    )
    _check_result(case=case, result=result)
