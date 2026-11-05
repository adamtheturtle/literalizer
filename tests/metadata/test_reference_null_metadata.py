"""Public contracts for null reference knowledge and optional hints."""

import pytest
from pydantic import BaseModel, Json, TypeAdapter

from literalizer import ValueInput, literalize_call
from literalizer.languages import Cpp
from tests.integration.case_manifests import CallInputFormat
from tests.toml_cases import load_toml_cases


class _HintCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Native bindings, separate source knowledge, and expected
    metadata.
    """

    name: str
    source: str
    input_format: CallInputFormat
    target_function: str
    parameter_names: tuple[str, ...]
    per_element: bool
    ref_key: str
    bound_refs: Json[dict[str, ValueInput]]
    ref_values: Json[dict[str, ValueInput]]
    consumable_refs: frozenset[str]
    expected_source_data: Json[ValueInput]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """The declarative source-hint controls."""

    cases: tuple[_HintCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="reference_source_hints")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_cpp_bound_consumption_preserves_source_hint(case: _HintCase) -> None:
    """Actual bindings do not replace caller-supplied source metadata.

    Rendering and ownership are covered by compiling golden cases.
    """
    result = literalize_call(
        source=case.source,
        input_format=case.input_format,
        language=Cpp(),
        target_function=case.target_function,
        parameter_names=case.parameter_names,
        per_element=case.per_element,
        ref_key=case.ref_key,
        bound_refs=case.bound_refs,
        ref_values=case.ref_values,
        consumable_refs=case.consumable_refs,
    )
    assert result.source_data == case.expected_source_data
