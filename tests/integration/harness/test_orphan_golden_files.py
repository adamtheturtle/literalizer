"""Detect orphaned golden files that no parameterized test covers."""

import os
import shutil
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
    load_case_manifest,
    load_case_manifests,
)
from tests.integration.golden_inventory import (
    call_artifacts,
    literal_artifacts,
    owned_paths,
    reference_artifacts,
)
from tests.integration.reference_cases import (
    ref_language_specs,
)


@beartype
def _check_golden_inventory(*, cases_dir: Path, expected: set[Path]) -> None:
    """Reject files outside the exercised golden inventory."""
    actual = {path for path in cases_dir.rglob(pattern="*") if path.is_file()}
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
        expected=owned_paths(cases_dir=cases_dir),
    )


@pytest.mark.parametrize(argnames="variant", argvalues=[False, True])
def test_rejected_call_renderings_do_not_own_goldens(
    *, variant: bool, cases_dir: Path
) -> None:
    """A call that checks an error cannot keep an unverified fixture alive."""
    rejected = {
        rendering.artifact(cases_dir=cases_dir).path
        for case in call_golden_cases(cases_dir=cases_dir)
        if isinstance(case, CallVariantCase) is variant
        for rendering in case.renderings
        if rendering.expected_exception is not None
    }
    assert len(rejected) > 0
    assert rejected.isdisjoint(
        artifact.path for artifact in call_artifacts(cases_dir=cases_dir)
    )


def test_base_cases_own_effective_golden(cases_dir: Path) -> None:
    """A declared success case must not silently skip every target."""
    empty = [
        manifest.case_dir.name
        for manifest in load_case_manifests(cases_dir=cases_dir)
        if "base" in manifest.suites
        and not any(manifest.case_dir.glob(pattern="*@*"))
        and not any(manifest.case_dir.glob(pattern="goldens/*/*/base.*"))
    ]
    assert empty == [], f"Base cases without effective goldens: {empty}"


def _literal_paths_in_temp_case(*, case_dir: Path) -> set[Path]:
    """Copy the repository's expected paths for a single case into a test."""
    corpus = Path(__file__).parents[1] / "cases"
    original = corpus / case_dir.name
    return {
        case_dir / os.path.relpath(path=artifact.path, start=original)
        for artifact in literal_artifacts(cases_dir=corpus)
        if original in artifact.path.parents
    }


def test_effective_language_version_owns_golden(tmp_path: Path) -> None:
    """Pinned Java RECORD covers JDK16; C++ retains all actual
    versions.
    """
    cases_dir = tmp_path / "custom_corpus"
    case_dir = cases_dir / "dict_mixed_scalars"
    case_dir.mkdir(parents=True)
    expected = _literal_paths_in_temp_case(case_dir=case_dir)
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
    cases_dir = tmp_path / "custom_corpus"
    case_dir = cases_dir / "binary"
    case_dir.mkdir(parents=True)
    expected = _literal_paths_in_temp_case(case_dir=case_dir)
    cpp_dir = case_dir / "goldens" / "cpp"
    ordinary = {
        cpp_dir / version / "bytes_format_base64.cpp"
        for version in ("cpp14", "cpp17", "cpp20")
    }
    pinned = cpp_dir / "cpp14" / "version_cpp14.cpp"
    assert {
        path
        for path in expected
        if cpp_dir in path.parents and path.name == "bytes_format_base64.cpp"
    } == ordinary
    assert {
        path
        for path in expected
        if cpp_dir in path.parents and path.name == "version_cpp14.cpp"
    } == {pinned}
    for path in ordinary | {pinned}:
        actual = (
            Path(__file__).parents[1]
            / "cases"
            / os.path.relpath(path=path, start=cases_dir)
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        _ = path.write_bytes(data=actual.read_bytes())
    _check_golden_inventory(cases_dir=cases_dir, expected=expected)

    phantom = cpp_dir / "cpp20" / "version_cpp14.cpp"
    _ = phantom.write_bytes(data=pinned.read_bytes())
    with pytest.raises(
        expected_exception=AssertionError,
        match=r"cpp20[/\\]+version_cpp14\.cpp",
    ):
        _check_golden_inventory(cases_dir=cases_dir, expected=expected)


def test_literal_inventory_reads_selected_corpus(
    tmp_path: Path, cases_dir: Path
) -> None:
    """Select inputs, scenarios, and fixture layout from the same root."""
    # Seed the alternate corpus with the inputs owned by singleton
    # scenarios. Their authored declarations remain required.
    for name in (
        "bool_list",
        "comment_scalar_before_and_inline",
        "dict_mixed_scalars",
        "dict_with_list_value",
        "multiline_string_scalar",
        "new_variable_kebab_name",
        "new_variable_prime_suffix",
        "scalar_int",
        "simple_dict",
        "tuple_record_field",
    ):
        manifest = load_case_manifest(case_dir=cases_dir / name)
        target = tmp_path / name
        target.mkdir()
        for authored in (manifest.path, manifest.input.path):
            _ = shutil.copyfile(src=authored, dst=target / authored.name)
    selected = tmp_path / "selected_only"
    selected.mkdir()
    _ = (selected / "case.toml").write_text(
        data=(
            'schema_version = 1\ngolden_layout = "nested"\n'
            'suites = ["base", "combined"]\n'
            '[[variants]]\naxis = "collection_layout"\n'
        ),
        encoding="utf-8",
    )
    _ = (selected / "input.json").write_text(data="[2, 3]\n", encoding="utf-8")
    artifacts = tuple(literal_artifacts(cases_dir=tmp_path))
    assert {
        Path(os.path.relpath(path=artifact.path, start=tmp_path)).parts[0]
        for artifact in artifacts
    } <= {case.name for case in tmp_path.iterdir()}
    python_paths = {
        artifact.path.name
        for artifact in artifacts
        if selected in artifact.path.parents
        and artifact.language.language_id == "python"
        and artifact.path.parent.parent == selected / "goldens" / "python"
    }
    assert {
        "base.py",
        "combined.py",
        "collection_layout_multiline.py",
    } <= python_paths


def test_reference_versions_follow_selected_options() -> None:
    """Java records own JDK16 once; C++ keeps each supported standard."""
    config = RefCaseSpec.model_validate(
        obj={"heterogeneous_strategy": "RECORD"},
        context={"case_dir_name": "record_reference"},
    )
    assert tuple(
        spec.language_version
        for spec in ref_language_specs(config=config, lang_cls=Java)
    ) == (enum_member_by_name(enum_cls=Java.VersionFormats, name="JDK_16"),)
    assert tuple(
        spec.language_version
        for spec in ref_language_specs(config=config, lang_cls=Cpp)
    ) == tuple(Cpp.VersionFormats)


def test_reference_inventory_reads_selected_corpus(tmp_path: Path) -> None:
    """Resolve reference outcomes and paths from the same manifests."""
    cases_dir = tmp_path / "custom_corpus"
    case_dir = cases_dir / "custom_references"
    case_dir.mkdir(parents=True)
    _ = (case_dir / "case.toml").write_text(
        data=(
            'schema_version = 1\ngolden_layout = "nested"\n'
            'owner = "literalize-ref"\n[ref]\n'
            '[[ref.variants]]\naxis = "collection_layout"\n'
        ),
        encoding="utf-8",
    )
    _ = (case_dir / "input.json").write_text(
        data='{"a": {"$ref": "shared_values"}}\n', encoding="utf-8"
    )
    artifacts = tuple(reference_artifacts(cases_dir=cases_dir))
    assert all(case_dir in artifact.path.parents for artifact in artifacts)
    python_cases = {
        artifact.path.name
        for artifact in artifacts
        if artifact.language.language_id == "python"
    }
    assert python_cases == {
        "ref.py",
        "collection_layout_compact_ref.py",
        "collection_layout_multiline_ref.py",
    }
