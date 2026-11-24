"""Resolved fixture ownership shared by corpus tools and orphan checks."""

from collections.abc import Iterator
from pathlib import Path

from beartype import beartype

from .call_variant_cases import call_golden_cases
from .case_manifests import (
    ComposedCallFixture,
    call_case_specs,
    load_case_manifests,
)
from .constructor_cases import constructor_binding_cases
from .deep_input_cases import deep_input_cases
from .golden_artifacts import GoldenArtifact
from .golden_outcomes import Exclusion, Rejection, Success
from .golden_scenarios import scenario_renderings
from .native_invocation_cases import native_invocation_cases
from .record_snapshot_cases import record_snapshot_artifacts
from .reference_cases import reference_golden_cases
from .shared_checked_cases import shared_checked_cases
from .unwrapped_result_cases import result_view_artifacts


def call_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Omit calls with declared rejections or exclusions."""
    return (
        rendering.artifact(cases_dir=cases_dir)
        for case in call_golden_cases(cases_dir=cases_dir)
        for rendering in case.renderings
        if not isinstance(rendering.outcome, (Rejection, Exclusion))
    )


def reference_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Include successful references declared by the selected corpus."""
    return (
        rendering.artifact(cases_dir=cases_dir)
        for case in reference_golden_cases(cases_dir=cases_dir)
        for rendering in case.renderings
        if not isinstance(rendering.outcome, (Rejection, Exclusion))
    )


def literal_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Include ordinary and default-module renderings."""
    for renderings in scenario_renderings(cases_dir=cases_dir).values():
        for rendering in renderings:
            for spec in rendering.specs:
                if isinstance(rendering.outcome(spec=spec), Success):
                    yield rendering.artifact(version=spec.language_version)


def authored_paths(*, cases_dir: Path) -> Iterator[Path]:
    """Return manifests, source inputs and native checker definitions."""
    for manifest in load_case_manifests(cases_dir=cases_dir):
        yield manifest.path
        yield manifest.input.path
        for variant in manifest.variants:
            for filename in variant.consumer_calls.values():
                yield manifest.case_dir / filename
    for config in call_case_specs(cases_dir=cases_dir):
        fixture = config.fixture
        if (
            isinstance(fixture, ComposedCallFixture)
            and fixture.target_source is not None
        ):
            yield cases_dir / config.case_dir_name / fixture.target_source


def golden_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Combine the artifacts exposed by each golden family."""
    yield from literal_artifacts(cases_dir=cases_dir)
    yield from call_artifacts(cases_dir=cases_dir)
    yield from reference_artifacts(cases_dir=cases_dir)
    yield from (
        rendering.artifact
        for case in constructor_binding_cases(cases_dir=cases_dir)
        for rendering in case.participating_renderings
        if isinstance(rendering.outcome, Success)
    )
    yield from (
        case.artifact for case in native_invocation_cases(cases_dir=cases_dir)
    )
    yield from (
        case.artifact for case in deep_input_cases(cases_dir=cases_dir)
    )
    yield from (
        case.artifact for case in shared_checked_cases(cases_dir=cases_dir)
    )
    yield from result_view_artifacts(cases_dir=cases_dir)
    yield from record_snapshot_artifacts(cases_dir=cases_dir)


@beartype
def owned_paths(cases_dir: Path) -> set[Path]:
    """Project generated artifacts and authored files onto owned paths."""
    return {
        *authored_paths(cases_dir=cases_dir),
        *(artifact.path for artifact in golden_artifacts(cases_dir=cases_dir)),
    }
