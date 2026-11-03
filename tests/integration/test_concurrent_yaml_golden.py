"""Concurrent YAML renders retain their compiling golden-file results."""

import dataclasses
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from literalizer import InputFormat, Language
from literalizer.languages import Python

from .case_inputs import CaseInput
from .case_manifests import (
    CONCURRENT_YAML_ROLE,
    case_dir_names_for_role,
    case_input,
)
from .golden_scenarios import GoldenRendering, golden_groups
from .language_specs import make_golden_path
from .literalize_rendering import literalize_rendering


@dataclasses.dataclass(frozen=True)
class _ConcurrentGolden:
    """A source document and its independently checked native result."""

    rendering: GoldenRendering
    spec: Language
    input_info: CaseInput
    source: str
    expected: str


def test_concurrent_yaml_golden_files(cases_dir: Path) -> None:
    """Preserve values and comments across 200 parses on sixteen threads.

    Compare each result with the existing golden file for ordinary
    rendering to detect crossed values or comment streams (issue #4699).
    """
    names = set(
        case_dir_names_for_role(cases_dir=cases_dir, role=CONCURRENT_YAML_ROLE)
    )
    renderings = [
        rendering
        for group in golden_groups()
        if group.scenario_name == "base" and group.lang_cls is Python
        for rendering in group.renderings
        if rendering.case_dir_name in names
    ]
    assert {rendering.case_dir_name for rendering in renderings} == names
    cases: list[_ConcurrentGolden] = []
    for rendering in renderings:
        input_info = case_input(case_dir=cases_dir / rendering.case_dir_name)
        assert input_info.input_format is InputFormat.YAML
        for version in rendering.versions:
            spec = rendering.spec_for(version=version)
            path = make_golden_path(
                parent=rendering.golden_parent,
                name=rendering.golden_name,
                extension=rendering.lang_cls.extension,
                lang_cls=rendering.lang_cls,
                version=version,
            )
            cases.append(
                _ConcurrentGolden(
                    rendering=rendering,
                    spec=spec,
                    input_info=input_info,
                    source=input_info.path.read_text(encoding="utf-8"),
                    expected=path.read_text(encoding="utf-8"),
                )
            )

    def render(index: int) -> None:
        """Check one fresh language instance against its existing
        golden.
        """
        case = cases[index % len(cases)]
        result = literalize_rendering(
            rendering=case.rendering,
            spec=dataclasses.replace(case.spec),
            input_info=case.input_info,
            source_text=case.source,
            variable_form=case.rendering.render.variable_form,
        )
        assert result.code + "\n" == case.expected, (
            case.rendering.case_dir_name
        )

    with ThreadPoolExecutor(max_workers=16) as pool:
        _ = tuple(pool.map(render, range(200)))
