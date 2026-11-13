"""Manifest-owned public rendering scenarios remain safe under shared
state.

Native golden fixtures supply the expected rendering results. The runtime
checks exercise concurrent calls (issue #4699).
"""

import dataclasses
from concurrent.futures import ThreadPoolExecutor

import pytest
from pydantic import BaseModel

from literalizer.languages import ALL_LANGUAGES
from tests.integration.golden_scenarios import GOLDEN_SCENARIOS
from tests.integration.language_specs import with_per_fixture_module_name
from tests.integration.manifest_values import ManifestLanguage
from tests.integration.state_goldens import (
    StateGolden,
    read_state_golden,
    render_state_golden,
)
from tests.integration.variant_cases import variants_for_axis


class _ThreadCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """A shared language instance exercised against native golden fixtures."""

    name: str
    scenario_name: str
    language: ManifestLanguage
    golden_name: str
    case_names: tuple[str, ...]


def _variant_thread_cases() -> list[_ThreadCase]:
    """Exercise record and JSON caches through every declared producer.

    Retain the Rust record and C cJSON regressions from issue #4699 while
    selecting their peers by the shared option axes.
    """
    cases: list[_ThreadCase] = []
    for axis, case_names in (
        (
            "heterogeneous_strategy_record",
            (
                "record_pure_scalars",
                "record_nested_record",
                "record_nested_container",
            ),
        ),
        (
            "json_type",
            (
                "json_helper_name_arena",
                "sibling_list_values_same_shape",
                "rectangular_map_sequence_shapes",
            ),
        ),
    ):
        producers = {
            (variant.lang_cls, variant.name)
            for variant in variants_for_axis(axis_key=axis)
        }
        cases.extend(
            _ThreadCase(
                name=name,
                scenario_name="format_variant",
                language=cls,
                golden_name=name,
                case_names=case_names,
            )
            for cls, name in sorted(producers, key=lambda pair: pair[1])
        )
    return cases


@pytest.mark.parametrize(
    argnames="scenario",
    argvalues=[
        *_variant_thread_cases(),
        *(
            _ThreadCase(
                name=f"{cls.language_id}_default",
                scenario_name="base",
                language=cls,
                golden_name=cls.__name__,
                case_names=("scalar_int", "simple_sequence", "simple_dict"),
            )
            for cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
        ),
    ],
    ids=lambda scenario: scenario.name,
)
def test_language_instance_is_thread_safe(scenario: _ThreadCase) -> None:
    """Compare 300 calls on sixteen threads with native golden programs.

    Reuse language instances across scalar, sequence and mapping
    documents, retaining separate instances for fixture-specific modules.
    Expected output comes from checked-in fixtures,
    independently of the cached state exercised by these calls (#4699).
    """
    renderings = [
        rendering
        for family in GOLDEN_SCENARIOS
        if family.name == scenario.scenario_name
        for rendering in family.build(lang_cls=scenario.language)
        if rendering.golden_name == scenario.golden_name
        and rendering.case_dir_name in scenario.case_names
    ]
    assert {rendering.case_dir_name for rendering in renderings} == set(
        scenario.case_names
    )
    cases: list[StateGolden] = []
    versions = dict.fromkeys(
        spec.language_version
        for rendering in renderings
        for spec in rendering.specs
    )
    for version in versions:
        version_renderings = [
            rendering
            for rendering in renderings
            if version in {spec.language_version for spec in rendering.specs}
        ]
        shared_language = dataclasses.replace(
            version_renderings[0].spec_for(version=version)
        )
        version_cases = [
            read_state_golden(
                rendering=rendering,
                language=(
                    with_per_fixture_module_name(
                        spec=shared_language,
                        golden_path=rendering.golden_path(version=version),
                    )
                    if rendering.apply_fixture_module_name
                    else shared_language
                ),
            )
            for rendering in version_renderings
            # The base suite omits shapes a backend cannot represent.
            # Exercise its complete native fixtures without a language list.
            if rendering.golden_path(version=version).is_file()
        ]
        assert len(version_cases) > 0, version.name
        cases.extend(version_cases)

    def render(index: int) -> None:
        """Render one document through the shared language instance."""
        case = cases[index % len(cases)]
        assert render_state_golden(case=case) == case.expected, (
            case.rendering.case_dir_name
        )

    with ThreadPoolExecutor(max_workers=16) as pool:
        _ = tuple(pool.map(render, range(300)))
