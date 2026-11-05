"""Manifest-owned public rendering scenarios remain safe under shared
state.

Native golden fixtures supply the expected rendering results. The runtime
checks exercise concurrent calls and caller-owned mutations (issue #4699).
"""

import dataclasses
from concurrent.futures import ThreadPoolExecutor

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer import literalize
from literalizer.languages import Rust
from tests.integration.case_manifests import CallInputFormat, ManifestLanguage
from tests.integration.golden_scenarios import golden_groups
from tests.integration.state_goldens import (
    StateGolden,
    read_state_golden,
    render_state_golden,
)
from tests.toml_cases import load_toml_cases


class _ThreadCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """A shared language instance exercised against native golden fixtures."""

    name: str
    language: ManifestLanguage
    golden_name: str
    case_names: tuple[str, ...]


class _SnapshotCase(BaseModel, extra="forbid", frozen=True):
    """A native record golden and caller-owned name mutations."""

    name: str
    case_name: str
    golden_name: str
    parent_fields: frozenset[str]
    parent_name: str
    child_name: str


class _UnusedReferenceCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """A rendering input and its independent caller-state expectation."""

    name: str
    source: str
    input_format: CallInputFormat
    language: ManifestLanguage
    ref_key: str
    ref_values: dict[str, list[int]]
    expected: dict[str, list[int]]


class _Cases(BaseModel, extra="forbid", frozen=True):
    """Manifest-owned public state-safety scenarios."""

    threads: tuple[_ThreadCase, ...]
    snapshots: tuple[_SnapshotCase, ...]
    unused_references: tuple[_UnusedReferenceCase, ...]


_CASES = TypeAdapter(type=_Cases).validate_python(
    load_toml_cases(name="public_api_state_safety")
)


@pytest.mark.parametrize(
    argnames="scenario",
    argvalues=_CASES.threads,
    ids=lambda scenario: scenario.name,
)
def test_language_instance_is_thread_safe(scenario: _ThreadCase) -> None:
    """Compare 300 calls on sixteen threads with native golden programs.

    Reuse one language instance across scalar, sequence and nested
    mapping documents. Expected output comes from checked-in fixtures,
    independently of the cached state exercised by these calls (#4699).
    """
    renderings = [
        rendering
        for group in golden_groups()
        if group.scenario_name == "format_variant"
        and group.lang_cls is scenario.language
        for rendering in group.renderings
        if rendering.golden_name == scenario.golden_name
        and rendering.case_dir_name in scenario.case_names
    ]
    assert {rendering.case_dir_name for rendering in renderings} == set(
        scenario.case_names
    )
    cases: list[StateGolden] = []
    for version in renderings[0].versions:
        shared_language = dataclasses.replace(
            renderings[0].spec_for(version=version)
        )
        cases.extend(
            read_state_golden(
                rendering=rendering,
                language=shared_language,
            )
            for rendering in renderings
        )

    def render(index: int) -> None:
        """Render one document through the shared language instance."""
        case = cases[index % len(cases)]
        assert render_state_golden(case=case) == case.expected, (
            case.rendering.case_dir_name
        )

    with ThreadPoolExecutor(max_workers=16) as pool:
        _ = tuple(pool.map(render, range(300)))


@pytest.mark.parametrize(
    argnames="scenario",
    argvalues=_CASES.snapshots,
    ids=lambda scenario: scenario.name,
)
def test_record_shape_names_are_snapshotted(scenario: _SnapshotCase) -> None:
    """Caller mutation cannot change either nested or parent record
    names.
    """
    rendering = next(
        rendering
        for group in golden_groups()
        if group.scenario_name == "format_variant" and group.lang_cls is Rust
        for rendering in group.renderings
        if rendering.case_dir_name == scenario.case_name
        and rendering.golden_name == scenario.golden_name
    )
    for version in rendering.versions:
        spec = rendering.spec_for(version=version)
        rust_spec = spec
        assert isinstance(rust_spec, Rust)
        caller_names = dict(rust_spec.record_shape_names)
        language = dataclasses.replace(spec, record_shape_names=caller_names)
        case = read_state_golden(rendering=rendering, language=language)
        assert render_state_golden(case=case) == case.expected

        caller_names[scenario.parent_fields] = scenario.parent_name
        caller_names[next(iter(caller_names))] = scenario.child_name
        assert render_state_golden(case=case) == case.expected


@pytest.mark.parametrize(
    argnames="scenario",
    argvalues=_CASES.unused_references,
    ids=lambda scenario: scenario.name,
)
def test_unrelated_reference_values_are_not_mutated(
    scenario: _UnusedReferenceCase,
) -> None:
    """Rendering a set leaves unused caller-owned bindings unchanged."""
    _ = literalize(
        source=scenario.source,
        input_format=scenario.input_format,
        language=scenario.language(),
        ref_key=scenario.ref_key,
        ref_values=scenario.ref_values,
    )
    assert scenario.ref_values == scenario.expected
