"""Golden-file tests that drive :func:`literalizer.literalize`.

Every scenario declared in :mod:`golden_scenarios` -- single
declaration form, combined declaration + assignment, format-variant
kwargs, statement-terminator option, heterogeneous-scalar strategy,
``pre_indent_level`` -- shares the one runner below: render a case
input to a language and compare against a checked-in golden file.

Each rendering covers every member of its language's
``VersionFormats``, bar a spec that pins its own version, so adding a
second member to a language's enum automatically produces a parallel
set of golden files.
"""

import dataclasses
import functools
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

from .case_manifests import load_case_manifest
from .golden_batches import GoldenGroup, golden_groups
from .golden_checks import (
    GoldenSkips,
    assert_rejection,
    check_golden,
    fixture_contents,
    format_consumer,
)
from .golden_renderings import GoldenRendering
from .language_metadata import language_metadata
from .language_specs import with_per_fixture_module_name
from .literalize_rendering import literalize_rendering
from .yaml_warnings import expected_yaml_warnings


@beartype
def _check_rendering(
    *,
    rendering: GoldenRendering,
    spec: literalizer.Language,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Render one golden file and compare it against its fixture."""
    manifest = load_case_manifest(case_dir=cases_dir / rendering.case_dir_name)
    input_info = manifest.input
    source_text = input_info.path.read_text(encoding="utf-8")
    roundtrip = manifest.input_roundtrip
    if roundtrip is not None:
        with expected_yaml_warnings(
            expectation=input_info.expected_reused_anchor_warning,
        ):
            source_text = literalizer.literalize(
                source=source_text,
                input_format=input_info.input_format,
                language=roundtrip.language(),
            ).code
        input_info = dataclasses.replace(
            input_info,
            input_format=roundtrip.input_format,
            expected_reused_anchor_warning=None,
        )
    golden_path = rendering.artifact(version=spec.language_version).path
    if rendering.apply_fixture_module_name:
        spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    variable_form = (
        rendering.render.variable_form
        if spec.supports_variable_names
        else None
    )
    rejection = rendering.rejection(spec=spec)
    if rejection is not None:
        assert_rejection(
            outcome=rejection,
            golden_path=golden_path,
            render=functools.partial(
                literalize_rendering,
                rendering=rendering,
                spec=spec,
                input_info=input_info,
                source_text=source_text,
                variable_form=variable_form,
            ),
        )
        return
    with GoldenSkips(
        policy=rendering.skip,
        golden_path=golden_path,
        prefix=rendering.lang_cls.__name__,
    ):
        result = literalize_rendering(
            rendering=rendering,
            spec=spec,
            input_info=input_info,
            source_text=source_text,
            variable_form=variable_form,
        )
    if rendering.initialize_variable or len(rendering.extra_preamble) > 0:
        declarations: list[literalizer.LiteralizeResult] = []
        if rendering.initialize_variable:
            assert isinstance(
                rendering.render.variable_form, literalizer.ExistingVariable
            )
            declarations.append(
                literalize_rendering(
                    rendering=rendering,
                    spec=spec,
                    input_info=input_info,
                    source_text=source_text,
                    variable_form=literalizer.NewVariable(
                        name=rendering.render.variable_form.name,
                        modifiers=frozenset(),
                    ),
                )
            )
        # External types must be available before generated record definitions.
        result = dataclasses.replace(
            result, preamble=rendering.extra_preamble + result.preamble
        )
        result = literalizer.literalize_call_with_declarations(
            language=spec,
            declarations=declarations,
            call=result,
        )
    metadata = language_metadata(language_id=spec.language_id)
    contents = fixture_contents(
        code=result.code,
        language_id=spec.language_id,
        intentional_identifier=(
            variable_form is not None
            and variable_form.name != variable_form.name.lower()
            and variable_form.name
            != metadata.variants.declaration_style_variable_names.get(
                spec.declaration_style.name, "my_data"
            )
        ),
    )
    if rendering.consumer_template is not None:
        contents = format_consumer(
            template=rendering.consumer_template,
            result=result,
            golden_path=golden_path,
            spec=spec,
        )
    check_golden(
        contents=contents,
        golden_path=golden_path,
        file_regression=file_regression,
    )


@pytest.mark.parametrize(
    argnames="group",
    argvalues=golden_groups(),
    ids=lambda group: group.test_id,
)
def test_golden_file(
    group: GoldenGroup,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Every declared rendering matches its checked-in golden file."""
    for rendering in group.renderings:
        for spec in rendering.specs:
            with subtests.test(
                golden_name=rendering.golden_name,
                case_dir_name=rendering.case_dir_name,
                version=spec.language_version.name,
            ):
                _check_rendering(
                    rendering=rendering,
                    spec=spec,
                    cases_dir=cases_dir,
                    file_regression=file_regression,
                )
