"""Render and compare constructor-binding golden fixtures."""

import dataclasses
import enum
from pathlib import Path

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import literalize_call

from .case_manifests import ConstructorCaseSpec
from .constructor_cases import ConstructorBindingCase
from .golden_checks import GoldenSkips, check_golden
from .language_specs import make_spec, with_per_fixture_module_name


@beartype
def run_constructor_binding_golden_case(
    *,
    case: ConstructorBindingCase,
    version: enum.Enum,
    golden_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Check one constructor binding golden file."""
    language = make_spec(
        lang_cls=case.lang_cls,
        language_version=version,
        **case.spec_overrides,
    )
    manifest = case.manifest
    language = with_per_fixture_module_name(
        spec=language, golden_path=golden_path
    )
    config = ConstructorCaseSpec.model_validate(obj=manifest.constructor)
    source = manifest.input.path.read_text(encoding="utf-8")
    input_format = manifest.input.input_format
    if config.target_template is not None:
        check_golden(
            contents=config.target_template.format(
                target=language.format_constructor_target(config.class_name)
            ),
            extension=golden_path.suffix,
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
        contents = config.consumer_template.format(
            preamble="\n".join(result.preamble),
            code=result.code,
            bare_code=result.bare_code,
            body_preamble="\n".join(result.body_preamble),
            module_name=(
                f"Fixture_{golden_path.parent.name}_"
                f"{golden_path.stem.rsplit(sep='@', maxsplit=1)[0]}"
            ),
        )
    check_golden(
        contents=contents,
        extension=golden_path.suffix,
        golden_path=golden_path,
        file_regression=file_regression,
    )
