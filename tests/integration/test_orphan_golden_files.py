"""Detect orphaned golden files that no parameterized test covers."""

import os
from pathlib import Path

from beartype import beartype

import literalizer

from .call_cases import discover_call_cases
from .call_variant_cases import build_call_variant_cases
from .case_discovery import (
    build_heterogeneous_strategy_combined_cases,
    build_indent_cases,
    build_no_variable_form_cases,
    build_pre_indent_cases,
    build_statement_terminator_combined_cases,
    discover_cases,
    discover_combined_cases,
)
from .language_specs import make_golden_path, make_spec
from .literalize_ref_cases import (
    discover_literalize_default_ref_cases,
    discover_literalize_ref_cases,
)
from .variant_cases import build_variant_cases


@beartype
def _paths_for_versions(
    *,
    parent: Path,
    name: str,
    extension: str,
    lang_cls: literalizer.LanguageCls,
) -> set[Path]:
    """Return one ``make_golden_path`` result per language version."""
    return {
        make_golden_path(
            parent=parent,
            name=name,
            extension=extension,
            lang_cls=lang_cls,
            version=version_format,
        )
        for version_format in lang_cls.VersionFormats
    }


@beartype
def _expected_variant_golden_files(cases_dir: Path) -> set[Path]:
    """Return expected paths for variant, statement-terminator, strategy,
    and
    pre-indent golden files.
    """
    expected: set[Path] = set()

    for variant_case in build_variant_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / variant_case.case_dir_name,
                name=variant_case.variant_name,
                extension=variant_case.variant.spec.extension,
                lang_cls=variant_case.variant.lang_cls,
            )
        )

    for case in build_statement_terminator_combined_cases():
        statement_terminator_style_spec = make_spec(
            lang_cls=case.lang_cls,
            statement_terminator_style=case.statement_terminator_style,
        )
        expected.update(
            _paths_for_versions(
                parent=cases_dir / case.case_dir_name,
                name=case.name,
                extension=statement_terminator_style_spec.extension,
                lang_cls=case.lang_cls,
            )
        )

    for strategy_case in build_heterogeneous_strategy_combined_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / strategy_case.case_dir_name,
                name=strategy_case.name,
                extension=strategy_case.lang_cls.extension,
                lang_cls=strategy_case.lang_cls,
            )
        )

    for indent_case in build_indent_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / indent_case.case_dir_name,
                name=indent_case.name,
                extension=indent_case.lang_cls.extension,
                lang_cls=indent_case.lang_cls,
            )
        )

    for pre_indent_case in build_pre_indent_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / pre_indent_case.case_dir_name,
                name=pre_indent_case.name,
                extension=pre_indent_case.lang_cls.extension,
                lang_cls=pre_indent_case.lang_cls,
            )
        )

    for no_variable_form_case in build_no_variable_form_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / no_variable_form_case.case_dir_name,
                name=no_variable_form_case.name,
                extension=no_variable_form_case.lang_cls.extension,
                lang_cls=no_variable_form_case.lang_cls,
            )
        )

    return expected


@beartype
def _expected_golden_files(cases_dir: Path) -> set[Path]:
    """Return the set of all golden files that parameterized tests
    cover.
    """
    expected: set[Path] = set()

    for case_dir in sorted(cases_dir.iterdir()):
        expected.add(case_dir / "input.yaml")

    for case_name, lang_cls in discover_cases(cases_dir=cases_dir):
        expected.update(
            _paths_for_versions(
                parent=cases_dir / case_name,
                name=lang_cls.__name__,
                extension=lang_cls.extension,
                lang_cls=lang_cls,
            )
        )

    for combined_case in discover_combined_cases(cases_dir=cases_dir):
        expected.update(
            _paths_for_versions(
                parent=cases_dir / combined_case.case_name,
                name=combined_case.golden_file_name,
                extension=combined_case.lang_cls.extension,
                lang_cls=combined_case.lang_cls,
            )
        )

    expected.update(_expected_variant_golden_files(cases_dir=cases_dir))

    for call_case in discover_call_cases():
        if call_case.expected_exception is not None:
            continue
        expected.update(
            _paths_for_versions(
                parent=cases_dir / call_case.config.case_dir_name,
                name=f"{call_case.lang_cls.__name__}_call",
                extension=call_case.lang_cls.extension,
                lang_cls=call_case.lang_cls,
            )
        )

    for call_variant_case in build_call_variant_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / call_variant_case.config.case_dir_name,
                name=f"{call_variant_case.variant.name}_call",
                extension=call_variant_case.variant.spec.extension,
                lang_cls=call_variant_case.variant.lang_cls,
            )
        )

    for literalize_ref_case in discover_literalize_ref_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / literalize_ref_case.config.case_dir_name,
                name=f"{literalize_ref_case.lang_cls.__name__}_ref",
                extension=literalize_ref_case.lang_cls.extension,
                lang_cls=literalize_ref_case.lang_cls,
            )
        )

    for default_ref_case in discover_literalize_default_ref_cases():
        expected.update(
            _paths_for_versions(
                parent=cases_dir / default_ref_case.config.case_dir_name,
                name=f"{default_ref_case.lang_cls.__name__}_ref_default",
                extension=default_ref_case.lang_cls.extension,
                lang_cls=default_ref_case.lang_cls,
            )
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
