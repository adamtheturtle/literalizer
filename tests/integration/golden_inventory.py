"""Resolved fixture ownership shared by corpus tools and orphan checks."""

import dataclasses
import os
from collections.abc import Iterator
from pathlib import Path

from beartype import beartype

from .call_variant_cases import call_golden_cases
from .case_manifests import load_case_manifests
from .constructor_cases import constructor_binding_cases
from .deep_input_cases import deep_input_cases
from .golden_artifacts import GoldenArtifact
from .golden_outcomes import Success
from .golden_scenarios import scenario_renderings
from .native_invocation_cases import native_invocation_cases
from .record_snapshot_cases import record_snapshot_artifacts
from .reference_cases import reference_golden_cases
from .shared_checked_cases import shared_checked_cases
from .unwrapped_result_cases import result_view_artifacts


def call_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Only successful call renderings can own golden fixtures."""
    return (
        rendering.artifact(cases_dir=cases_dir)
        for case in call_golden_cases(cases_dir=cases_dir)
        for rendering in case.renderings
        if rendering.outcome is None
    )


def literal_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Include ordinary renderings and sibling default-module fixtures."""
    integration_dir = Path(__file__).parent
    for renderings in scenario_renderings().values():
        for rendering in renderings:
            for spec in rendering.specs:
                if rendering.rejection(spec=spec) is not None:
                    continue
                artifact = rendering.artifact(version=spec.language_version)
                yield dataclasses.replace(
                    artifact,
                    path=cases_dir.parent
                    / os.path.relpath(
                        path=artifact.path, start=integration_dir
                    ),
                )


def authored_paths(*, cases_dir: Path) -> Iterator[Path]:
    """Return manifests and source inputs owned by the corpus."""
    for manifest in load_case_manifests(cases_dir=cases_dir):
        yield manifest.path
        yield manifest.input.path


def golden_artifacts(*, cases_dir: Path) -> Iterator[GoldenArtifact]:
    """Combine the artifacts exposed by each golden family."""
    yield from literal_artifacts(cases_dir=cases_dir)
    yield from call_artifacts(cases_dir=cases_dir)
    yield from (
        rendering.artifact(cases_dir=cases_dir)
        for case in reference_golden_cases()
        for rendering in case.renderings
        if rendering.outcome is None or isinstance(rendering.outcome, Success)
    )
    yield from (
        rendering.artifact
        for case in constructor_binding_cases(cases_dir=cases_dir)
        for rendering in case.renderings
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
