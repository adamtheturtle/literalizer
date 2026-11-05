"""Native golden expectations for public API state-safety tests."""

import dataclasses
from pathlib import Path

from literalizer import InputFormat, Language, literalize

from .case_manifests import case_input
from .golden_scenarios import GoldenRendering

_CASES_DIR = Path(__file__).with_name(name="cases")


@dataclasses.dataclass(frozen=True)
class StateGolden:
    """One source document and its existing complete native program."""

    rendering: GoldenRendering
    language: Language
    source: str
    input_format: InputFormat
    expected: str


def read_state_golden(
    *, rendering: GoldenRendering, language: Language
) -> StateGolden:
    """Load input and expected native output before state is exercised."""
    input_info = case_input(case_dir=_CASES_DIR / rendering.case_dir_name)
    path = rendering.golden_path(version=language.language_version)
    return StateGolden(
        rendering=rendering,
        language=language,
        source=input_info.path.read_text(encoding="utf-8"),
        input_format=input_info.input_format,
        expected=path.read_text(encoding="utf-8"),
    )


def render_state_golden(*, case: StateGolden) -> str:
    """Render the complete native program for one state-safety case."""
    render_args = case.rendering.render
    result = literalize(
        source=case.source,
        input_format=case.input_format,
        language=case.language,
        variable_form=render_args.variable_form,
        wrap_in_file=render_args.wrap_in_file,
        pre_indent_level=render_args.pre_indent_level,
        collection_layout=render_args.collection_layout,
        record_null_substitutions=render_args.record_null_substitutions,
    )
    return result.code + "\n"
