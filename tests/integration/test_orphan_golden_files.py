"""Detect orphaned golden files that no parameterized test covers."""

import os
from pathlib import Path

from .call_cases import discover_call_cases
from .call_variant_cases import build_call_variant_cases
from .case_discovery import (
    build_heterogeneous_strategy_combined_cases,
    build_pre_indent_cases,
    build_statement_terminator_combined_cases,
    discover_cases,
    discover_combined_cases,
)
from .language_specs import make_spec
from .literalize_ref_cases import (
    discover_literalize_default_ref_cases,
    discover_literalize_ref_cases,
)
from .variant_cases import build_variant_cases


def _expected_variant_golden_files(cases_dir: Path) -> set[Path]:
    """Return expected paths for variant, statement-terminator, strategy,
    and
    pre-indent golden files.
    """
    expected: set[Path] = set()

    for variant_case in build_variant_cases():
        ext = variant_case.variant.spec.extension
        expected.add(
            cases_dir
            / variant_case.case_dir_name
            / (variant_case.variant_name + ext)
        )

    for case in build_statement_terminator_combined_cases():
        statement_terminator_style_spec = make_spec(
            lang_cls=case.lang_cls,
            statement_terminator_style=case.statement_terminator_style,
        )
        expected.add(
            cases_dir
            / case.case_dir_name
            / (case.name + statement_terminator_style_spec.extension)
        )

    for strategy_case in build_heterogeneous_strategy_combined_cases():
        ext = strategy_case.lang_cls.extension
        expected.add(
            cases_dir
            / strategy_case.case_dir_name
            / (strategy_case.name + ext)
        )

    for pre_indent_case in build_pre_indent_cases():
        ext = pre_indent_case.lang_cls.extension
        expected.add(
            cases_dir
            / pre_indent_case.case_dir_name
            / (pre_indent_case.name + ext)
        )

    return expected


def _expected_golden_files(cases_dir: Path) -> set[Path]:
    """Return the set of all golden files that parameterized tests
    cover.
    """
    expected: set[Path] = set()

    for case_dir in sorted(cases_dir.iterdir()):
        expected.add(case_dir / "input.yaml")

    for case_name, lang_cls in discover_cases(cases_dir=cases_dir):
        ext = lang_cls.extension
        expected.add(cases_dir / case_name / (lang_cls.__name__ + ext))

    for combined_case in discover_combined_cases(cases_dir=cases_dir):
        ext = combined_case.lang_cls.extension
        expected.add(
            cases_dir
            / combined_case.case_name
            / (combined_case.golden_file_name + ext)
        )

    expected.update(_expected_variant_golden_files(cases_dir=cases_dir))

    for call_case in discover_call_cases():
        if call_case.expected_exception is not None:
            continue
        ext = call_case.lang_cls.extension
        golden_name = f"{call_case.lang_cls.__name__}_call"
        expected.add(
            cases_dir / call_case.config.case_dir_name / (golden_name + ext)
        )

    for call_variant_case in build_call_variant_cases():
        variant_spec = call_variant_case.variant.spec
        golden_name = f"{call_variant_case.variant.name}_call"
        expected.add(
            cases_dir
            / call_variant_case.config.case_dir_name
            / (golden_name + variant_spec.extension)
        )

    for literalize_ref_case in discover_literalize_ref_cases():
        ext = literalize_ref_case.lang_cls.extension
        golden_name = f"{literalize_ref_case.lang_cls.__name__}_ref"
        expected.add(
            cases_dir
            / literalize_ref_case.config.case_dir_name
            / (golden_name + ext)
        )

    for default_ref_case in discover_literalize_default_ref_cases():
        ext = default_ref_case.lang_cls.extension
        golden_name = f"{default_ref_case.lang_cls.__name__}_ref_default"
        expected.add(
            cases_dir
            / default_ref_case.config.case_dir_name
            / (golden_name + ext)
        )

    return expected


def test_no_dead_golden_files(cases_dir: Path) -> None:
    """Every file under ``cases/`` must be referenced by a parameterized
    test.  Orphaned golden files silently rot and waste repository space.
    """
    expected = _expected_golden_files(cases_dir=cases_dir)
    actual = {path for path in cases_dir.rglob(pattern="*") if path.is_file()}
    dead_files = sorted(
        os.path.relpath(path=path, start=cases_dir)
        for path in actual - expected
    )
    assert not dead_files
