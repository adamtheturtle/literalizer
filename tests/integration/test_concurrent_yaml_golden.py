"""Concurrent YAML renders retain their compiling golden-file results."""

import dataclasses
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from literalizer import InputFormat, Language
from literalizer.languages import ALL_LANGUAGES

from .case_inputs import CaseInput
from .case_manifests import (
    CONCURRENT_YAML_ROLE,
    case_input,
)
from .golden_renderings import GoldenRendering
from .golden_scenarios import GOLDEN_SCENARIOS
from .language_specs import with_per_fixture_module_name
from .literalize_rendering import literalize_rendering
from .manifest_queries import (
    case_dir_names_for_role,
)


@dataclasses.dataclass(frozen=True)
class _ConcurrentGolden:
    """A source document and its independently checked native result."""

    rendering: GoldenRendering
    spec: Language
    input_info: CaseInput
    source: str
    expected: str


def test_concurrent_yaml_golden_files(cases_dir: Path) -> None:
    """Preserve values and comments across shared and fresh threads.

    Compare each result with the existing golden file for ordinary
    rendering to detect crossed values or comment streams (issue #4699).
    """
    names = set(
        case_dir_names_for_role(cases_dir=cases_dir, role=CONCURRENT_YAML_ROLE)
    )
    languages = {
        cls for cls in ALL_LANGUAGES if cls().supports_collection_comments
    }
    base = next(family for family in GOLDEN_SCENARIOS if family.name == "base")
    renderings = [
        rendering
        for cls in sorted(languages, key=lambda cls: cls.__name__)
        for rendering in base.build(lang_cls=cls)
        if rendering.case_dir_name in names
    ]
    assert {rendering.case_dir_name for rendering in renderings} == names
    cases: list[_ConcurrentGolden] = []
    for rendering in renderings:
        input_info = case_input(case_dir=cases_dir / rendering.case_dir_name)
        assert input_info.input_format is InputFormat.YAML
        for spec in rendering.specs:
            path = rendering.golden_path(version=spec.language_version)
            # The base suite omits input shapes a backend cannot represent.
            if not path.is_file():
                continue
            effective_spec = (
                with_per_fixture_module_name(spec=spec, golden_path=path)
                if rendering.apply_fixture_module_name
                else spec
            )
            cases.append(
                _ConcurrentGolden(
                    rendering=rendering,
                    spec=effective_spec,
                    input_info=input_info,
                    source=input_info.path.read_text(encoding="utf-8"),
                    expected=path.read_text(encoding="utf-8"),
                )
            )

    assert {case.rendering.lang_cls for case in cases} == languages

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
            variable_form=(
                case.rendering.render.variable_form
                if case.spec.supports_variable_names
                else None
            ),
        )
        assert result.code + "\n" == case.expected, (
            case.rendering.case_dir_name
        )

    with ThreadPoolExecutor(max_workers=16) as pool:
        _ = tuple(pool.map(render, range(max(200, len(cases)))))

    # Repeated thread lifetimes must not accumulate global constructors.
    for index in range(1024):
        with ThreadPoolExecutor(max_workers=1) as pool:
            pool.submit(render, index).result()
