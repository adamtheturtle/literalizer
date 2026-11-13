"""Bare result views reproduce existing complete native programs."""

from pathlib import Path

import pytest

from literalizer import FileWrapperContext, Language, NewVariable, literalize
from literalizer.languages import ALL_LANGUAGES
from tests.integration.case_manifests import case_input
from tests.integration.golden_renderings import GoldenRendering
from tests.integration.golden_scenarios import GOLDEN_SCENARIOS
from tests.integration.language_specs import with_per_fixture_module_name

_CASES_DIR = Path(__file__).parents[1] / "integration" / "cases"
_BASE = next(family for family in GOLDEN_SCENARIOS if family.name == "base")


@pytest.mark.parametrize(
    argnames=("rendering", "seed"),
    argvalues=[
        pytest.param(
            rendering,
            spec,
            id=f"{cls.__name__}/{spec.language_version.name}",
        )
        for cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
        if cls.supports_variable_names
        for rendering in _BASE.build(lang_cls=cls)
        if rendering.case_dir_name == "comment_scalar"
        for spec in rendering.specs
    ],
)
def test_bare_result_view_retains_complete_program(
    rendering: GoldenRendering,
    seed: Language,
) -> None:
    """Wrapping bare_code preserves source comments and caller-supplied
    preambles.
    """
    path = rendering.golden_path(version=seed.language_version)
    language = with_per_fixture_module_name(spec=seed, golden_path=path)
    info = case_input(case_dir=_CASES_DIR / rendering.case_dir_name)
    variable = rendering.render.variable_form
    assert isinstance(variable, NewVariable)
    result = literalize(
        source=info.path.read_text(encoding="utf-8"),
        input_format=info.input_format,
        language=language,
        variable_form=variable,
        wrap_in_file=False,
    )
    program = language.wrap_in_file(
        content=result.bare_code,
        context=FileWrapperContext(
            line_prefix="",
            bound_variable_names=(),
            variable_name=variable.name,
            modifiers=variable.modifiers,
            body_preamble=result.body_preamble,
            class_preamble=(),
            has_literal_declarations=True,
            generated_body_preamble=result.body_preamble,
            call_stub_names=frozenset(),
            root_is_object_literal=False,
            root_mapping_entries=None,
            has_existing_bindings=False,
        ),
    )
    assert "\n".join((*result.preamble, program)) + "\n" == path.read_text(
        encoding="utf-8"
    )
