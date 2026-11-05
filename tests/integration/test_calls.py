"""``literalize_call`` golden-file tests.

Drives each call-case configuration against every supporting language,
both for default specs and for non-default language variants (e.g.
Rust's ``TAGGED_ENUM`` strategy on inputs the default ``ERROR``
strategy rejects).
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .call_cases import (
    CASES_DIR,
    CallCase,
    discover_call_cases,
    run_call_golden_case,
)
from .call_variant_cases import (
    CallVariantCase,
    build_call_variant_cases,
    run_call_variant_golden_case,
)
from .golden_checks import cleanup_stale_golden
from .language_specs import make_golden_path, make_spec
from .source_profiles import source_format_marks


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=[
        pytest.param(case, marks=source_format_marks(lang_cls=case.lang_cls))
        for case in discover_call_cases()
    ],
    ids=lambda case: f"{case.config.coverage_id}/{case.lang_cls.__name__}",
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
                        name=config.golden_name(
                            name=f"{lang_cls.__name__}_call"
                        ),
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
    argvalues=[
        pytest.param(
            case, marks=source_format_marks(lang_cls=case.variant.lang_cls)
        )
        for case in build_call_variant_cases(cases_dir=CASES_DIR)
    ],
    ids=lambda case: f"{case.config.coverage_id}/{case.variant.name}",
)
def test_call_variant_golden_file(
    pytestconfig: pytest.Config,
    call_variant_case: CallVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test ``literalize_call`` for a non-default language spec.

    Covers call inputs that need a non-default language option, such as
    statement terminators or heterogeneous strategies.
    """
    with subtests.test(
        version=call_variant_case.variant.spec.language_version.name
    ):
        run_call_variant_golden_case(
            call_variant_case=call_variant_case,
            cases_dir=cases_dir,
            file_regression=file_regression,
            pytest_config=pytestconfig,
        )
