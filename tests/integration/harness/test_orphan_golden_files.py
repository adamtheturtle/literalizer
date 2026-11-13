"""Detect orphaned golden files that no parameterized test covers."""

import os
from pathlib import Path

import pytest
from beartype import beartype

from literalizer.languages import Cpp, Java
from tests.enum_members import enum_member_by_name
from tests.integration.call_variant_cases import (
    CallVariantCase,
    call_golden_cases,
)
from tests.integration.case_manifests import (
    RefCaseSpec,
    load_case_manifests,
)
from tests.integration.constructor_cases import (
    constructor_binding_cases,
)
from tests.integration.deep_input_cases import deep_input_golden_paths
from tests.integration.golden_scenarios import golden_groups
from tests.integration.native_invocation_cases import native_invocation_cases
from tests.integration.record_snapshot_cases import (
    record_snapshot_golden_paths,
)
from tests.integration.reference_cases import (
    ref_language_versions,
    reference_golden_cases,
)
from tests.integration.shared_checked_cases import shared_checked_cases
from tests.integration.unwrapped_result_cases import result_view_golden_paths


@beartype
def _expected_call_golden_files(*, cases_dir: Path) -> set[Path]:
    """Only successful call renderings can own golden fixtures."""
    return {
        rendering.golden_path(cases_dir=cases_dir)
        for case in call_golden_cases(cases_dir=cases_dir)
        for rendering in case.renderings
        if rendering.expected_exception is None
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
def _expected_reference_golden_files(*, cases_dir: Path) -> set[Path]:
    """Read reference ownership from the renderings executed by pytest."""
    return {
        rendering.golden_path(cases_dir=cases_dir)
        for case in reference_golden_cases()
        for rendering in case.renderings
    }


@beartype
def _expected_constructor_golden_files(*, cases_dir: Path) -> set[Path]:
    """Read constructor fixture ownership from the runner's renderings."""
    return {
        rendering.golden_path
        for case in constructor_binding_cases(cases_dir=cases_dir)
        for rendering in case.renderings
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

    expected.update(_expected_constructor_golden_files(cases_dir=cases_dir))

    expected.update(
        case.golden_path
        for case in native_invocation_cases(cases_dir=cases_dir)
    )
    expected.update(_expected_literalize_golden_files(cases_dir=cases_dir))
    expected.update(result_view_golden_paths(cases_dir=cases_dir))
    expected.update(record_snapshot_golden_paths(cases_dir=cases_dir))
    expected.update(deep_input_golden_paths(cases_dir=cases_dir))
    expected.update(
        case.golden_path for case in shared_checked_cases(cases_dir=cases_dir)
    )

    expected.update(_expected_call_golden_files(cases_dir=cases_dir))

    expected.update(_expected_reference_golden_files(cases_dir=cases_dir))

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


@pytest.mark.parametrize(argnames="variant", argvalues=[False, True])
def test_rejected_call_renderings_do_not_own_goldens(
    *, variant: bool, cases_dir: Path
) -> None:
    """A call that checks an error cannot keep an unverified fixture alive."""
    rejected = {
        rendering.golden_path(cases_dir=cases_dir)
        for case in call_golden_cases(cases_dir=cases_dir)
        if isinstance(case, CallVariantCase) is variant
        for rendering in case.renderings
        if rendering.expected_exception is not None
    }
    assert len(rejected) > 0
    assert rejected.isdisjoint(
        _expected_call_golden_files(cases_dir=cases_dir)
    )


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
