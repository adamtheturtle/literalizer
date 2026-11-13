"""Render and compare constructor-binding golden fixtures."""

import dataclasses

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import literalize_call

from .constructor_cases import ConstructorRendering
from .constructor_templates import constructor_target_template
from .golden_checks import GoldenSkips, check_golden, format_consumer
from .language_specs import with_per_fixture_module_name


@beartype
def run_constructor_binding_golden_case(
    *,
    rendering: ConstructorRendering,
    file_regression: FileRegressionFixture,
) -> None:
    """Check one constructor binding golden file."""
    case = rendering.case
    golden_path = rendering.golden_path
    manifest = case.manifest
    language = with_per_fixture_module_name(
        spec=rendering.spec, golden_path=golden_path
    )
    config = manifest.constructor
    assert config is not None  # noqa: S101
    source = manifest.input.path.read_text(encoding="utf-8")
    input_format = manifest.input.input_format
    target_template = constructor_target_template(
        config=config, language_name=case.lang_cls.__name__
    )
    if target_template is not None:
        check_golden(
            contents=target_template.format(
                target=language.format_constructor_target(config.class_name)
            ),
            golden_path=golden_path,
            file_regression=file_regression,
        )
        return
    with GoldenSkips(
        policy=case.skip,
        golden_path=golden_path,
        prefix=case.lang_cls.__name__,
        config=file_regression.request.config,
    ):
        result = literalize_call(
            source=source,
            input_format=input_format,
            language=language,
            target_function=language.format_constructor_target(
                config.class_name,
            ),
            parameter_names=config.parameter_names,
            wrap_in_file=config.consumer_template is None,
            variable_form=dataclasses.replace(
                case.variable_form, name=config.variable_name
            ),
        )
    contents = result.code + "\n"
    if config.consumer_template is not None:
        contents = format_consumer(
            template=config.consumer_template,
            result=result,
            golden_path=golden_path,
        )
    check_golden(
        contents=contents,
        golden_path=golden_path,
        file_regression=file_regression,
    )
