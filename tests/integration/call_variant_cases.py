"""``literalize_call`` golden-file cases driven by language variants.

Covers call inputs that need a non-default language spec, such as
inputs that a default heterogeneous strategy rejects or calls rendered
with a non-default statement terminator.  Sibling to :mod:`call_cases`.

Which variants drive a case is declared by the case itself, in the
``[[call.variants]]`` tables of its ``case.toml``, so a call case is
described in one place.
"""

import dataclasses
import functools
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer._enums import enum_payload

from .call_cases import expected_call_shape_exception, run_call_golden_case
from .case_manifests import CallCaseSpec, call_case_specs
from .golden_checks import cleanup_stale_golden
from .language_specs import make_golden_path
from .variant_cases import Variant, variants_for_axis
from .variant_context import config_with_variant_layout


@dataclasses.dataclass(frozen=True)
class CallVariantCase:
    """A ``literalize_call`` golden-file case run with a non-default
    language spec (e.g. a ``TAGGED_ENUM`` strategy).
    """

    config: CallCaseSpec
    variant: Variant


@functools.cache
@beartype
def build_call_variant_cases(*, cases_dir: Path) -> list[CallVariantCase]:
    """Return call-test cases for the variant axes cases declare.

    A case names an axis when the default spec cannot represent its
    input -- which makes :func:`test_call_golden_file` skip -- or when
    the call is only interesting under a non-default option, such as a
    statement terminator or a JSON-aware result binding.
    """
    return [
        CallVariantCase(
            config=config_with_variant_layout(
                config=config, layout=variant.collection_layout
            ),
            variant=variant,
        )
        for config in call_case_specs(cases_dir=cases_dir)
        for manifest_variant in config.variants
        for variant in variants_for_axis(axis_key=manifest_variant.axis)
        if config.admits_language(lang_cls=variant.lang_cls)
        if config.call_style_type is None
        or any(
            isinstance(
                enum_payload(member=style, payload_type=object),
                config.call_style_type,
            )
            for style in variant.lang_cls.CallStyles
        )
    ]


@beartype
def run_call_variant_golden_case(
    *,
    call_variant_case: CallVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    pytest_config: pytest.Config,
) -> None:
    """Run a variant with an explicit stale-file policy."""
    lang_cls = call_variant_case.variant.lang_cls
    # The plan already expands supported versions and resolves explicit
    # pins and syntax floors. Render each effective spec once.
    version_format = call_variant_case.variant.spec.language_version
    expected_exception = expected_call_shape_exception(
        lang_cls=lang_cls,
        config=call_variant_case.config,
        spec=call_variant_case.variant.spec,
    )
    if expected_exception is not None:
        with pytest.raises(expected_exception=expected_exception):
            run_call_golden_case(
                config=call_variant_case.config,
                spec=call_variant_case.variant.spec,
                lang_cls=lang_cls,
                golden_name=f"{call_variant_case.variant.name}_call",
                cases_dir=cases_dir,
                file_regression=file_regression,
                version=version_format,
            )
        cleanup_stale_golden(
            golden_path=make_golden_path(
                parent=cases_dir / call_variant_case.config.case_dir_name,
                name=call_variant_case.config.golden_name(
                    name=f"{call_variant_case.variant.name}_call"
                ),
                extension=lang_cls.extension,
                lang_cls=lang_cls,
                version=version_format,
            ),
            config=pytest_config,
        )
        return
    run_call_golden_case(
        config=call_variant_case.config,
        spec=call_variant_case.variant.spec,
        lang_cls=lang_cls,
        golden_name=f"{call_variant_case.variant.name}_call",
        cases_dir=cases_dir,
        file_regression=file_regression,
        version=version_format,
    )
