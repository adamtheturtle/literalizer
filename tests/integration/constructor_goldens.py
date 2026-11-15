"""Render and compare constructor-binding golden fixtures."""

import dataclasses

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import NewVariable, literalize, literalize_call

from .constructor_cases import ConstructorRendering
from .constructor_templates import constructor_target_template
from .golden_checks import GoldenSkips, check_golden, format_consumer
from .language_specs import make_spec, with_per_fixture_module_name


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
    if len(config.target_options) > 0:
        language = dataclasses.replace(
            language,
            **{
                key: value.format(
                    target=language.format_constructor_target(
                        config.class_name
                    )
                )
                for key, value in config.target_options.items()
            },
        )
    consumer_template = config.consumer_for_language(
        language_name=case.lang_cls.__name__
    )
    source = manifest.input.path.read_text(encoding="utf-8")
    input_format = manifest.input.input_format
    target_template = constructor_target_template(
        config=config, language_name=case.lang_cls.__name__
    )
    if target_template is not None:
        contents = target_template.format(
            target=language.format_constructor_target(config.class_name)
        )
    elif config.target_source_template is not None or config.target_variable:
        target_source = source
        if config.target_source_template is not None:
            target_source = config.target_source_template.format(
                target=language.format_constructor_target(config.class_name)
            )
        result = literalize(
            source=target_source,
            input_format=input_format,
            language=(
                language
                if config.target_language is None
                else make_spec(lang_cls=config.target_language)
            ),
            variable_form=(
                NewVariable(
                    name=(
                        language.format_constructor_target(config.class_name)
                        if config.target_variable_name is None
                        else config.target_variable_name
                    ),
                    modifiers=frozenset(),
                )
                if config.target_variable
                else None
            ),
            wrap_in_file=config.target_variable,
        )
        contents = result.code + "\n"
    else:
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
                wrap_in_file=consumer_template is None,
                variable_form=dataclasses.replace(
                    case.variable_form, name=config.variable_name
                ),
            )
        contents = result.code + "\n"
        if consumer_template is not None:
            contents = format_consumer(
                template=consumer_template,
                result=result,
                golden_path=golden_path,
            )
    check_golden(
        contents=contents,
        golden_path=golden_path,
        file_regression=file_regression,
    )
