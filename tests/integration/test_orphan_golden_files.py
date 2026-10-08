"""Detect orphaned golden files that no parameterized test covers."""

import os
from pathlib import Path

import pytest
from beartype import beartype

import literalizer

from .call_cases import discover_call_cases
from .call_variant_cases import build_call_variant_cases
from .case_discovery import (
    build_indent_cases,
    build_no_variable_form_cases,
    build_pre_indent_cases,
    build_statement_terminator_combined_cases,
    discover_cases,
    discover_combined_cases,
    kebab_new_variable_languages,
    primed_new_variable_languages,
)
from .case_manifests import (
    KEBAB_NEW_VARIABLE_OWNER,
    PRIMED_NEW_VARIABLE_OWNER,
    case_dir_name_for_owner,
    load_case_manifests,
)
from .golden_scenarios import golden_groups
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
def _expected_strategy_golden_files(*, cases_dir: Path) -> set[Path]:
    """Follow the strategy runner's effective language versions."""
    expected: set[Path] = set()
    for group in golden_groups():
        if group.scenario_name != "heterogeneous_strategy":
            continue
        for rendering in group.renderings:
            for version in rendering.versions:
                spec = rendering.spec_for(version=version)
                if spec.language_version is not version:
                    continue
                expected.add(
                    make_golden_path(
                        parent=cases_dir / rendering.case_dir_name,
                        name=rendering.golden_name,
                        extension=spec.extension,
                        lang_cls=rendering.lang_cls,
                        version=version,
                    )
                )
    return expected


@beartype
def _expected_variant_golden_files(cases_dir: Path) -> set[Path]:
    """Return expected paths for variant, statement-terminator, strategy,
    and
    pre-indent golden files.
    """
    expected = _expected_strategy_golden_files(cases_dir=cases_dir)

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
def _expected_specialized_new_variable_golden_files(
    cases_dir: Path,
) -> set[Path]:
    """Return expected paths for specialized NewVariable fixtures."""
    expected: set[Path] = set()
    for owner, languages in (
        (KEBAB_NEW_VARIABLE_OWNER, kebab_new_variable_languages()),
        (PRIMED_NEW_VARIABLE_OWNER, primed_new_variable_languages()),
    ):
        case_dir_name = case_dir_name_for_owner(
            cases_dir=cases_dir,
            owner=owner,
        )
        for lang_cls in languages:
            expected.update(
                _paths_for_versions(
                    parent=cases_dir / case_dir_name,
                    name=lang_cls.__name__,
                    extension=lang_cls.extension,
                    lang_cls=lang_cls,
                )
            )
    return expected


@beartype
def _expected_default_module_name_golden_files() -> set[Path]:
    """Return the default-name paths declared by the shared runner."""
    expected: set[Path] = set()
    for group in golden_groups():
        if group.scenario_name != "default_module_name":
            continue
        for rendering in group.renderings:
            for version in rendering.versions:
                expected.add(
                    make_golden_path(
                        parent=rendering.golden_parent,
                        name=rendering.golden_name,
                        extension=rendering.lang_cls.extension,
                        lang_cls=rendering.lang_cls,
                        version=version,
                    )
                )

    return expected


@beartype
def _expected_golden_files(cases_dir: Path) -> set[Path]:
    """Return the set of all golden files that parameterized tests
    cover.
    """
    expected: set[Path] = set()

    for manifest in load_case_manifests(cases_dir=cases_dir):
        expected.add(manifest.path)
        expected.add(manifest.input.path)

    expected.update(_expected_default_module_name_golden_files())

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

    expected.update(
        _expected_specialized_new_variable_golden_files(cases_dir=cases_dir),
    )

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


@beartype
def _check_golden_inventory(*, cases_dir: Path, expected: set[Path]) -> None:
    """Reject files outside the exercised golden inventory."""
    actual = {
        path
        for parent in (cases_dir, cases_dir.parent / "default_module_names")
        for path in parent.rglob(pattern="*")
        if path.is_file()
    }
    dead_files = sorted(
        os.path.relpath(path=path, start=cases_dir)
        for path in actual - expected
    )
    assert dead_files == []


def test_no_dead_golden_files(cases_dir: Path) -> None:
    """Every file under ``cases/`` must be referenced by a parameterized
    test.  Orphaned golden files silently rot and waste repository space.
    """
    _check_golden_inventory(
        cases_dir=cases_dir,
        expected=_expected_golden_files(cases_dir=cases_dir),
    )


def test_effective_language_version_owns_golden(tmp_path: Path) -> None:
    """Pinned Java RECORD covers JDK16; C++ retains all actual
    versions.
    """
    cases_dir = tmp_path / "cases"
    case_dir = cases_dir / "dict_mixed_scalars"
    case_dir.mkdir(parents=True)
    expected = _expected_variant_golden_files(cases_dir=cases_dir)
    java_prefix = "Java_heterogeneous_strategy_record_combined@"
    cpp_prefix = "Cpp_heterogeneous_strategy_record_combined@"
    java_golden = case_dir / f"{java_prefix}jdk_16.java"
    assert {
        path for path in expected if path.name.startswith(java_prefix)
    } == {
        java_golden,
    }
    assert {path for path in expected if path.name.startswith(cpp_prefix)} == {
        case_dir / f"{cpp_prefix}cpp14.cpp",
        case_dir / f"{cpp_prefix}cpp17.cpp",
        case_dir / f"{cpp_prefix}cpp20.cpp",
    }
    contents = (
        Path(__file__).parent
        / "cases"
        / "dict_mixed_scalars"
        / java_golden.name
    ).read_bytes()
    _ = java_golden.write_bytes(data=contents)
    _check_golden_inventory(cases_dir=cases_dir, expected=expected)

    phantom_golden = case_dir / f"{java_prefix}jdk_11.java"
    _ = phantom_golden.write_bytes(data=contents)
    with pytest.raises(
        expected_exception=AssertionError,
        match="Java_heterogeneous_strategy_record_combined@jdk_11",
    ):
        _check_golden_inventory(cases_dir=cases_dir, expected=expected)
