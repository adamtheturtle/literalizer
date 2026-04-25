"""``literalize_call`` golden-file tests against non-default language
specs.

Covers call inputs that the default spec rejects but a particular
non-default variant (e.g. Rust's ``TAGGED_ENUM`` heterogeneous
strategy) can represent.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .call_cases import run_call_golden_case
from .call_variant_cases import CallVariantCase, build_call_variant_cases


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
) -> None:
    """Test ``literalize_call`` for a non-default language spec.

    Covers call inputs that the language's default
    :attr:`Language.heterogeneous_strategy` rejects, which
    :func:`test_call_golden_file` skips — in particular the
    sibling-widening behavior of Rust's ``TAGGED_ENUM`` across
    per-element call arguments.
    """
    run_call_golden_case(
        config=call_variant_case.config,
        spec=call_variant_case.variant.spec,
        golden_name=f"{call_variant_case.variant.name}_call",
        cases_dir=cases_dir,
        file_regression=file_regression,
    )
