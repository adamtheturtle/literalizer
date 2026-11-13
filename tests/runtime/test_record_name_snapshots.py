"""Caller-owned record names retain their native golden programs."""

import dataclasses
from collections.abc import Mapping
from pathlib import Path
from typing import Protocol, runtime_checkable

import pytest

from literalizer import Language, literalize_call_with_declarations
from literalizer.languages import ALL_LANGUAGES
from tests.integration.case_manifests import case_input
from tests.integration.golden_renderings import GoldenRendering
from tests.integration.golden_scenarios import GOLDEN_SCENARIOS
from tests.integration.language_specs import with_per_fixture_module_name
from tests.integration.literalize_rendering import literalize_rendering

_CASES_DIR = Path(__file__).parents[1] / "integration" / "cases"


@runtime_checkable
class _HasRecordNames(Protocol):
    """The constructor field promised by the record-name capability."""

    record_shape_names: Mapping[frozenset[str], str]


def _snapshot_renderings() -> list[GoldenRendering]:
    """Reuse named-record programs for every backend offering the
    option.
    """
    languages = {
        cls for cls in ALL_LANGUAGES if cls.supports_record_shape_names
    }
    family = next(
        family
        for family in GOLDEN_SCENARIOS
        if family.name == "format_variant"
    )
    renderings = [
        rendering
        for cls in sorted(languages, key=lambda cls: cls.__name__)
        for rendering in family.build(lang_cls=cls)
        if rendering.case_dir_name == "record_named_nested_record"
        and rendering.golden_name.startswith(
            cls.__name__ + "_record_shape_names_"
        )
    ]
    assert {rendering.lang_cls for rendering in renderings} == languages
    return renderings


def _render_program(*, rendering: GoldenRendering, language: Language) -> str:
    """Keep the actual wrapper and any caller-declared record types."""
    info = case_input(case_dir=_CASES_DIR / rendering.case_dir_name)
    result = literalize_rendering(
        rendering=rendering,
        spec=language,
        input_info=info,
        source_text=info.path.read_text(encoding="utf-8"),
        variable_form=rendering.render.variable_form,
    )
    if len(rendering.extra_preamble) > 0:
        result = dataclasses.replace(
            result, preamble=rendering.extra_preamble + result.preamble
        )
        result = literalize_call_with_declarations(
            language=language, declarations=(), call=result
        )
    return result.code + "\n"


@pytest.mark.parametrize(
    argnames=("rendering", "seed"),
    argvalues=[
        pytest.param(
            rendering,
            spec,
            id=f"{rendering.golden_name}/{spec.language_version.name}",
        )
        for rendering in _snapshot_renderings()
        for spec in rendering.specs
    ],
)
@pytest.mark.parametrize(argnames="warm_cache", argvalues=[False, True])
def test_record_names_are_caller_independent(
    *, rendering: GoldenRendering, seed: Language, warm_cache: bool
) -> None:
    """Mutating caller mappings cannot change cold or cached native output."""
    path = rendering.golden_path(version=seed.language_version)
    configured = with_per_fixture_module_name(spec=seed, golden_path=path)
    assert isinstance(configured, _HasRecordNames)
    caller_names = dict(configured.record_shape_names)
    assert len(caller_names) > 0
    language = dataclasses.replace(configured, record_shape_names=caller_names)
    expected = path.read_text(encoding="utf-8")
    if warm_cache:
        assert (
            _render_program(rendering=rendering, language=language) == expected
        )
    caller_names[next(iter(caller_names))] = "Replacement"
    caller_names[frozenset({"collection", "featured_entry"})] = "Parent"
    assert _render_program(rendering=rendering, language=language) == expected
