"""``literalize_call`` golden-file tests.

Drives each call-case configuration against every supporting language,
both for default specs and for non-default language variants (e.g.
Rust's ``TAGGED_ENUM`` strategy on inputs the default ``ERROR``
strategy rejects).
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat
from literalizer.languages import Bash

from .call_cases import (
    CallCase,
    default_call_case_specs,
    discover_call_cases,
    run_call_golden_case,
    run_wrap_in_file_case,
)
from .call_variant_cases import CallVariantCase, build_call_variant_cases
from .case_inputs import CaseInput
from .golden_checks import cleanup_stale_golden
from .language_specs import make_golden_path, make_spec


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_wrap_in_file_case_handles_stale_rejected_call_arg(
    *,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    regenerate: bool,
) -> None:
    """A rejected Bash collection preserves or explicitly removes its
    stale fixture.
    """
    pytest_config = pytest.Config.fromdictargs(
        option_dict={}, args=["--regen-all"] if regenerate else []
    )
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_multiline_list_argument"
    ).model_copy(update={"per_element": False})
    golden_path = tmp_path / "stale.sh"
    _ = golden_path.write_text(data="stale\n")

    expected_exception: type[BaseException] = pytest.fail.Exception
    expected_message = r"Stale golden file: .*stale\.sh.*--regen-all"
    if regenerate:
        expected_exception = pytest.skip.Exception
        expected_message = "Bash rejected call arg: list values"
    with pytest.raises(
        expected_exception=expected_exception, match=expected_message
    ):
        run_wrap_in_file_case(
            config=config,
            spec=make_spec(lang_cls=Bash),
            source="[]\n",
            input_info=CaseInput(
                path=tmp_path / "input.yaml",
                input_format=InputFormat.YAML,
            ),
            effective_ref_case=None,
            lang_name="Bash",
            lang_extension=Bash.extension,
            golden_path=golden_path,
            file_regression=file_regression,
            pytest_config=pytest_config,
        )

    if regenerate:
        assert not golden_path.exists()
    else:
        assert golden_path.read_text(encoding="utf-8") == "stale\n"


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=discover_call_cases(),
    ids=lambda case: f"{case.config.case_dir_name}/{case.lang_cls.__name__}",
)
def test_call_golden_file(
    call_case: CallCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize_call output matches expected golden file."""
    config = call_case.config
    lang_cls = call_case.lang_cls
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            if call_case.expected_exception is not None:
                with pytest.raises(
                    expected_exception=call_case.expected_exception,
                ):
                    run_call_golden_case(
                        config=config,
                        spec=spec,
                        lang_cls=lang_cls,
                        golden_name=f"{lang_cls.__name__}_call",
                        cases_dir=cases_dir,
                        file_regression=file_regression,
                        version=version_format,
                    )
                cleanup_stale_golden(
                    golden_path=make_golden_path(
                        parent=cases_dir / config.case_dir_name,
                        name=f"{lang_cls.__name__}_call",
                        extension=lang_cls.extension,
                        lang_cls=lang_cls,
                        version=version_format,
                    ),
                    config=file_regression.request.config,
                )
                continue
            run_call_golden_case(
                config=config,
                spec=spec,
                lang_cls=lang_cls,
                golden_name=f"{lang_cls.__name__}_call",
                cases_dir=cases_dir,
                file_regression=file_regression,
                version=version_format,
            )


@pytest.mark.parametrize(
    argnames="call_variant_case",
    argvalues=build_call_variant_cases(),
    ids=lambda case: f"{case.config.case_dir_name}/{case.variant.name}",
)
def test_call_variant_golden_file(
    call_variant_case: CallVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test ``literalize_call`` for a non-default language spec.

    Covers call inputs that need a non-default language option, such as
    statement terminators or heterogeneous strategies.
    """
    lang_cls = call_variant_case.variant.lang_cls
    # Each variant pins a specific ``language_version``, so render only
    # that one version.  ``lang_cls.VersionFormats`` is iterated by other
    # tests where the spec is rebuilt per version.
    version_format = call_variant_case.variant.spec.language_version
    with subtests.test(version=version_format.name):
        run_call_golden_case(
            config=call_variant_case.config,
            spec=call_variant_case.variant.spec,
            lang_cls=lang_cls,
            golden_name=f"{call_variant_case.variant.name}_call",
            cases_dir=cases_dir,
            file_regression=file_regression,
            version=version_format,
        )
