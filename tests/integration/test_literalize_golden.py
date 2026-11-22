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

from .golden_batches import GoldenGroup, golden_groups
from .golden_checks import (
    assert_rejection,
    check_golden,
    fixture_contents,
    format_consumer,
)
from .golden_outcomes import Rejection
from .golden_renderings import GoldenRendering
from .language_metadata import language_metadata
from .language_specs import with_per_fixture_module_name
from .literal_expectations import literal_source
from .literalize_rendering import compose_rendering, literalize_rendering
from .manifest_values import ComposedConsumer


@beartype
def _check_rendering(
    *,
    rendering: GoldenRendering,
    spec: literalizer.Language,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Render one golden file and compare it against its fixture."""
    source = literal_source(case_dir=cases_dir / rendering.case_dir_name)
    golden_path = rendering.artifact(version=spec.language_version).path
    if rendering.apply_fixture_module_name:
        spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    variable_form = (
        rendering.render.variable_form
        if spec.supports_variable_names
        else None
    )
    outcome = rendering.outcome(spec=spec)
    if isinstance(outcome, Rejection):
        assert_rejection(
            outcome=outcome,
            golden_path=golden_path,
            exact_type=True,
            render=functools.partial(
                literalize_rendering,
                rendering=rendering,
                spec=spec,
                input_info=source.input_info,
                source_text=source.source_text,
                variable_form=variable_form,
            ),
        )
        return
    result = literalize_rendering(
        rendering=rendering,
        spec=spec,
        input_info=source.input_info,
        source_text=source.source_text,
        variable_form=variable_form,
    )
    consumer = rendering.consumer_template
    if isinstance(consumer, ComposedConsumer):
        statements = consumer.statements.rstrip("\n")
        result = dataclasses.replace(
            result,
            declaration_code=f"{result.declaration_code}\n{statements}",
        )
    if (
        rendering.initialize_variable
        or len(rendering.extra_preamble) > 0
        or isinstance(consumer, ComposedConsumer)
    ):
        declarations: list[literalizer.LiteralizeResult] = []
        if rendering.initialize_variable:
            assert isinstance(
                rendering.render.variable_form, literalizer.ExistingVariable
            )
            declarations.append(
                literalize_rendering(
                    rendering=rendering,
                    spec=spec,
                    input_info=source.input_info,
                    source_text=source.source_text,
                    variable_form=literalizer.NewVariable(
                        name=rendering.render.variable_form.name,
                        modifiers=frozenset(),
                    ),
                )
            )
        result = compose_rendering(
            rendering=rendering,
            spec=spec,
            declarations=declarations,
            result=result,
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
    if isinstance(consumer, str):
        contents = format_consumer(
            template=consumer,
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
