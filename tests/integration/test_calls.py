"""``literalize_call`` golden-file tests.

Drives each call-case configuration against every supporting language,
both for default specs and for non-default language variants (e.g.
Rust's ``TAGGED_ENUM`` strategy on inputs the default ``ERROR``
strategy rejects).
"""

from pathlib import Path
from typing import NoReturn

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer.exceptions import CallArgNotSupportedError
from literalizer.languages import Python

from .call_cases import (
    CALL_CASE_CONFIGS,
    CallCase,
    _run_wrap_in_file_case,  # pyright: ignore[reportPrivateUsage]
    discover_call_cases,
    run_call_golden_case,
)
from .call_variant_cases import CallVariantCase, build_call_variant_cases
from .language_specs import make_spec


def test_wrap_in_file_case_skips_when_call_arg_is_rejected(
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Wrapped call cases drop stale golden files on rejected
    arguments.
    """
    config = next(
        config for config in CALL_CASE_CONFIGS if config.wrap_in_file
    )
    golden_path = tmp_path / "stale.py"
    golden_path.write_text(data="stale\n")

    def reject_call(**_kwargs: object) -> NoReturn:
        """Raise the configured call argument error."""
        raise CallArgNotSupportedError(
            language_name="Python",
            reason="compound argument",
        )

    monkeypatch.setattr(target="literalizer.literalize_call", name=reject_call)

    with pytest.raises(
        expected_exception=pytest.skip.Exception,
        match="Python rejected call arg: compound argument",
    ):
        _run_wrap_in_file_case(
            config=config,
            spec=make_spec(lang_cls=Python),
            yaml_string="[]\n",
            effective_ref_case=None,
            lang_name="Python",
            lang_extension=Python.extension,
            golden_path=golden_path,
            file_regression=file_regression,
        )

    assert not golden_path.exists()


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
