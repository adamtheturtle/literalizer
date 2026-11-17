"""Canonical fixture ownership shared by corpus tools and orphan
checks.
"""

import os
from pathlib import Path

from beartype import beartype

from .call_variant_cases import call_golden_cases
from .case_manifests import load_case_manifests
from .constructor_cases import constructor_binding_cases
from .deep_input_cases import deep_input_golden_paths
from .golden_scenarios import scenario_renderings
from .native_invocation_cases import native_invocation_cases
from .record_snapshot_cases import record_snapshot_golden_paths
from .reference_cases import reference_golden_cases
from .shared_checked_cases import shared_checked_cases
from .unwrapped_result_cases import result_view_golden_paths


@beartype
def call_owned_paths(*, cases_dir: Path) -> set[Path]:
    """Only successful call renderings can own golden fixtures."""
    return {
        rendering.golden_path(cases_dir=cases_dir)
        for case in call_golden_cases(cases_dir=cases_dir)
        for rendering in case.renderings
        if rendering.expected_exception is None
    }


@beartype
def literal_owned_paths(*, cases_dir: Path) -> set[Path]:
    """Read the fixture inventory directly from the golden runner's cases.

    Place paths under *cases_dir*'s parent so temporary inventory tests
    also cover fixtures in the sibling default_module_names directory.
    """
    integration_dir = Path(__file__).parent
    return {
        cases_dir.parent
        / os.path.relpath(
            path=rendering.golden_path(version=spec.language_version),
            start=integration_dir,
        )
        for renderings in scenario_renderings().values()
        for rendering in renderings
        for spec in rendering.specs
    }


@beartype
def _reference_owned_paths(*, cases_dir: Path) -> set[Path]:
    """Read reference ownership from the renderings executed by pytest."""
    return {
        rendering.golden_path(cases_dir=cases_dir)
        for case in reference_golden_cases()
        for rendering in case.renderings
    }


@beartype
def _constructor_owned_paths(*, cases_dir: Path) -> set[Path]:
    """Read constructor fixture ownership from the runner's renderings."""
    return {
        rendering.golden_path
        for case in constructor_binding_cases(cases_dir=cases_dir)
        for rendering in case.renderings
    }


@beartype
def owned_paths(cases_dir: Path) -> set[Path]:
    """Return the set of all golden files that parameterized tests
    cover.
    """
    expected: set[Path] = set()

    for manifest in load_case_manifests(cases_dir=cases_dir):
        expected.add(manifest.path)
        expected.add(manifest.input.path)

    expected.update(_constructor_owned_paths(cases_dir=cases_dir))

    expected.update(
        case.golden_path
        for case in native_invocation_cases(cases_dir=cases_dir)
    )
    expected.update(literal_owned_paths(cases_dir=cases_dir))
    expected.update(result_view_golden_paths(cases_dir=cases_dir))
    expected.update(record_snapshot_golden_paths(cases_dir=cases_dir))
    expected.update(deep_input_golden_paths(cases_dir=cases_dir))
    expected.update(
        case.golden_path for case in shared_checked_cases(cases_dir=cases_dir)
    )

    expected.update(call_owned_paths(cases_dir=cases_dir))

    expected.update(_reference_owned_paths(cases_dir=cases_dir))

    return expected
