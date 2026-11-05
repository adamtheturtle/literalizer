"""Detect orphaned golden files that no parameterized test covers."""

import os
from pathlib import Path

import pytest
from beartype import beartype

import literalizer
from literalizer.languages import Cpp, Java
from tests.enum_members import enum_member_by_name
from tests.integration.call_cases import discover_call_cases
from tests.integration.call_variant_cases import build_call_variant_cases
from tests.integration.case_manifests import RefCaseSpec, load_case_manifests
from tests.integration.constructor_cases import (
    constructor_binding_cases,
    constructor_golden_path,
)
from tests.integration.golden_scenarios import GOLDEN_SCENARIOS, golden_groups
from tests.integration.language_specs import make_golden_path
from tests.integration.literalize_ref_cases import (
    build_literalize_ref_variant_cases,
    discover_literalize_default_ref_cases,
    discover_literalize_ref_cases,
    ref_language_versions,
)
from tests.integration.native_invocation_cases import native_invocation_cases
from tests.integration.unwrapped_result_cases import result_view_golden_paths


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
def _expected_literalize_golden_files(*, cases_dir: Path) -> set[Path]:
    """Read the fixture inventory directly from the golden runner's cases.

    Place paths under *cases_dir*'s parent so temporary inventory tests
    also cover fixtures in the sibling default_module_names directory.
    """
    integration_dir = Path(__file__).parents[1]
    return {
        cases_dir.parent
        / os.path.relpath(
            path=rendering.golden_path(version=spec.language_version),
            start=integration_dir,
        )
        for group in golden_groups()
        for rendering in group.renderings
        for spec in rendering.specs
    }


@beartype
def _expected_golden_files(cases_dir: Path) -> set[Path]:
    """Return the set of all golden files that parameterized tests
    cover.
    """
    expected: set[Path] = set()

    for manifest in load_case_manifests(cases_dir=cases_dir):
        expected.add(manifest.path)
        expected.add(manifest.input.path)

    expected.update(
        constructor_golden_path(
            case=case,
            version=version,
        )
        for case in constructor_binding_cases(cases_dir=cases_dir)
        for version in case.lang_cls.VersionFormats
    )

    expected.update(
        path for _, _, _, path in native_invocation_cases(cases_dir=cases_dir)
    )
    expected.update(_expected_literalize_golden_files(cases_dir=cases_dir))
    expected.update(result_view_golden_paths(cases_dir=cases_dir))

    for call_case in discover_call_cases():
        if call_case.expected_exception is not None:
            continue
        expected.update(
            _paths_for_versions(
                parent=cases_dir / call_case.config.case_dir_name,
                name=call_case.config.golden_name(
                    name=f"{call_case.lang_cls.__name__}_call"
                ),
                extension=call_case.lang_cls.extension,
                lang_cls=call_case.lang_cls,
            )
        )

    for call_variant_case in build_call_variant_cases(cases_dir=cases_dir):
        expected.add(
            make_golden_path(
                parent=cases_dir / call_variant_case.config.case_dir_name,
                name=call_variant_case.config.golden_name(
                    name=f"{call_variant_case.variant.name}_call"
                ),
                extension=call_variant_case.variant.spec.extension,
                lang_cls=call_variant_case.variant.lang_cls,
                version=call_variant_case.variant.spec.language_version,
            )
        )

    for literalize_ref_case in discover_literalize_ref_cases():
        expected.update(
            make_golden_path(
                parent=cases_dir / literalize_ref_case.config.case_dir_name,
                name=literalize_ref_case.config.golden_name(
                    name=f"{literalize_ref_case.lang_cls.__name__}_ref"
                ),
                extension=literalize_ref_case.lang_cls.extension,
                lang_cls=literalize_ref_case.lang_cls,
                version=version,
            )
            for version in ref_language_versions(
                config=literalize_ref_case.config,
                lang_cls=literalize_ref_case.lang_cls,
            )
        )

    for variant_case in build_literalize_ref_variant_cases():
        expected.add(
            make_golden_path(
                parent=cases_dir / variant_case.config.case_dir_name,
                name=variant_case.config.golden_name(
                    name=variant_case.golden_name
                ),
                extension=variant_case.variant.spec.extension,
                lang_cls=variant_case.variant.lang_cls,
                version=variant_case.variant.spec.language_version,
            )
        )

    for default_ref_case in discover_literalize_default_ref_cases():
        expected.update(
            make_golden_path(
                parent=cases_dir / default_ref_case.config.case_dir_name,
                name=default_ref_case.config.golden_name(
                    name=f"{default_ref_case.lang_cls.__name__}_ref_default"
                ),
                extension=default_ref_case.lang_cls.extension,
                lang_cls=default_ref_case.lang_cls,
                version=version,
            )
            for version in ref_language_versions(
                config=default_ref_case.config,
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


@pytest.mark.parametrize(
    argnames="scenario_name",
    argvalues=[scenario.name for scenario in GOLDEN_SCENARIOS],
)
def test_removed_scenario_leaves_orphan(
    scenario_name: str,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Removing any runner scenario must orphan its existing fixtures."""
    groups = golden_groups()
    original = next(
        path
        for group in groups
        if group.scenario_name == scenario_name
        for rendering in group.renderings
        for spec in rendering.specs
        if (
            path := rendering.golden_path(version=spec.language_version)
        ).is_file()
    )
    cases_dir = tmp_path / "cases"
    orphan = tmp_path / os.path.relpath(
        path=original, start=Path(__file__).parents[1]
    )
    orphan.parent.mkdir(parents=True)
    _ = orphan.write_bytes(data=original.read_bytes())
    monkeypatch.setattr(
        target=f"{__name__}.golden_groups",
        name=lambda: tuple(
            group for group in groups if group.scenario_name != scenario_name
        ),
    )
    expected = _expected_literalize_golden_files(cases_dir=cases_dir)
    with pytest.raises(
        expected_exception=AssertionError,
        match=orphan.name,
    ):
        _check_golden_inventory(cases_dir=cases_dir, expected=expected)


def test_base_cases_own_effective_golden(cases_dir: Path) -> None:
    """A declared success case must not silently skip every target."""
    empty = [
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if "base" in manifest.suites
        and not any(manifest.case_dir.glob(pattern="*@*"))
    ]
    assert empty == [], f"Base cases without effective goldens: {empty}"


def test_effective_language_version_owns_golden(tmp_path: Path) -> None:
    """Pinned Java RECORD covers JDK16; C++ retains all actual
    versions.
    """
    cases_dir = tmp_path / "cases"
    case_dir = cases_dir / "dict_mixed_scalars"
    case_dir.mkdir(parents=True)
    expected = _expected_literalize_golden_files(cases_dir=cases_dir)
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
        Path(__file__).parents[1]
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


def test_variant_version_inventory_preserves_coverage_and_rejects_phantoms(
    tmp_path: Path,
) -> None:
    """Multi-version options own real files; a version selection owns
    one.
    """
    cases_dir = tmp_path / "cases"
    case_dir = cases_dir / "binary"
    case_dir.mkdir(parents=True)
    expected = _expected_literalize_golden_files(cases_dir=cases_dir)
    ordinary_name = "Cpp_bytes_format_base64@"
    pinned_name = "Cpp_version_cpp14@"
    ordinary = {
        case_dir / f"{ordinary_name}{version}.cpp"
        for version in ("cpp14", "cpp17", "cpp20")
    }
    pinned = case_dir / f"{pinned_name}cpp14.cpp"
    assert {
        path
        for path in expected
        if path.parent == case_dir and path.name.startswith(ordinary_name)
    } == ordinary
    assert {
        path
        for path in expected
        if path.parent == case_dir and path.name.startswith(pinned_name)
    } == {pinned}
    for path in ordinary | {pinned}:
        actual = Path(__file__).parents[1] / "cases" / "binary" / path.name
        _ = path.write_bytes(data=actual.read_bytes())
    _check_golden_inventory(cases_dir=cases_dir, expected=expected)

    phantom = case_dir / f"{pinned_name}cpp20.cpp"
    _ = phantom.write_bytes(data=pinned.read_bytes())
    with pytest.raises(
        expected_exception=AssertionError,
        match="Cpp_version_cpp14@cpp20",
    ):
        _check_golden_inventory(cases_dir=cases_dir, expected=expected)


def test_reference_versions_follow_selected_options() -> None:
    """Java records own JDK16 once; C++ keeps each supported standard."""
    config = RefCaseSpec.model_validate(
        obj={"heterogeneous_strategy": "RECORD"},
        context={"case_dir_name": "record_reference"},
    )
    assert ref_language_versions(config=config, lang_cls=Java) == (
        enum_member_by_name(enum_cls=Java.VersionFormats, name="JDK_16"),
    )
    assert ref_language_versions(config=config, lang_cls=Cpp) == tuple(
        Cpp.VersionFormats
    )
