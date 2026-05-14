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
    CallCase,
    discover_call_cases,
    run_call_golden_case,
)
from .call_variant_cases import CallVariantCase, build_call_variant_cases
from .language_specs import make_spec, spec_with_version


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=discover_call_cases(),
    ids=[
        f"{c.config.case_dir_name}/{c.lang_cls.__name__}"
        for c in discover_call_cases()
    ],
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
            kwargs: dict[str, object] = {"language_version": version_format}
            if config.call_style_type is not None:
                style = next(
                    s
                    for s in lang_cls.CallStyles
                    if isinstance(s.value, config.call_style_type)
                )
                kwargs["call_style"] = style
            spec = make_spec(lang_cls=lang_cls, **kwargs)
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
    ids=[
        f"{c.config.case_dir_name}/{c.variant.name}"
        for c in build_call_variant_cases()
    ],
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
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            versioned_spec = spec_with_version(
                spec=call_variant_case.variant.spec,
                version=version_format,
            )
            run_call_golden_case(
                config=call_variant_case.config,
                spec=versioned_spec,
                lang_cls=lang_cls,
                golden_name=f"{call_variant_case.variant.name}_call",
                cases_dir=cases_dir,
                file_regression=file_regression,
                version=version_format,
            )
