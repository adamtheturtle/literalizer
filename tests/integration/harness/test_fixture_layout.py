"""Check that nested golden paths preserve native fixture behavior."""

from pathlib import Path

from scripts.fixture_staging import stage_fixture_modules
from tests.integration.case_manifests import load_case_manifest
from tests.integration.fixture_names import (
    fixture_module_name,
    nested_golden_path,
)
from tests.integration.list_fixtures import CASES_DIR, fixture_paths


def test_nested_fixture_module_names(tmp_path: Path) -> None:
    """Stage a unique module and a public default from nested paths."""
    ordinary = CASES_DIR / "binary/goldens/haskell/ghc2021/base.hs"
    default = (
        CASES_DIR
        / "default_module_name/goldens/haskell/ghc2021/default_module_name.hs"
    )
    assert stage_fixture_modules(
        fixtures=(ordinary, default),
        workspace=tmp_path,
        default_module_name="Check",
    ) == ["Fixture_binary_Haskell", "Check"]
    assert (tmp_path / "Fixture_binary_Haskell.hs").read_bytes() == (
        ordinary.read_bytes()
    )
    assert (tmp_path / "Check.hs").read_bytes() == default.read_bytes()
    assert (
        fixture_module_name(
            golden_path=CASES_DIR / "binary/goldens/gleam/v1/combined.gleam"
        )
        == "Fixture_binary_gleam_combined"
    )


def test_nested_default_fixture_selection() -> None:
    """Include default-module fixtures only when requested."""
    ordinary = fixture_paths(extension=".java", version="jdk_16")
    complete = fixture_paths(
        extension=".java", version="jdk_16", include_default_module_names=True
    )
    assert set(complete) - set(ordinary) == {
        CASES_DIR
        / "default_module_name/goldens/java/jdk_16/default_module_name.java"
    }


def test_nested_version_and_variant_fixture_selection() -> None:
    """Select a pinned version and a variant-only case for native runs."""
    pinned = CASES_DIR / "empty_list/goldens/cpp/cpp14/version_cpp14.cpp"
    assert pinned in fixture_paths(extension=".cpp", version="cpp14")
    assert pinned not in fixture_paths(extension=".cpp", version="cpp17")

    multiline = (
        CASES_DIR
        / "multiline_string/goldens/haskell/ghc2021"
        / "string_format_double.hs"
    )
    assert multiline in fixture_paths(
        extension=".hs", version="ghc2021", language="Haskell"
    )
    assert (
        fixture_module_name(golden_path=multiline)
        == "Fixture_multiline_string_Haskell_string_format_double"
    )


def test_nested_reference_fixture_selection() -> None:
    """Select a fixture owned by the reference runner for native runs."""
    reference = (
        CASES_DIR / "literalize_ref_both_forms/goldens/gleam/v1/ref.gleam"
    )
    assert reference in fixture_paths(extension=".gleam", version="v1")
    assert (
        fixture_module_name(golden_path=reference)
        == "Fixture_literalize_ref_both_forms_gleam_ref"
    )


def test_nested_call_variant_fixture_selection() -> None:
    """Keep variant call fixtures visible with their original module names."""
    fixture = (
        CASES_DIR
        / "call_json_nested_ref_array/goldens/gleam/v1"
        / "json_type_gleam_json_json_call.gleam"
    )
    assert fixture in fixture_paths(extension=".gleam", version="v1")
    prefix = "Fixture_call_json_nested_ref_array"
    expected = f"{prefix}_gleam_json_type_gleam_json_json_call"
    assert fixture_module_name(golden_path=fixture) == expected


def test_nested_layout_uses_manifest_before_generation(tmp_path: Path) -> None:
    """A new case can choose nested paths before any golden exists."""
    case_dir = tmp_path / "new_case"
    case_dir.mkdir()
    _ = (case_dir / "case.toml").write_text(
        data=(
            'schema_version = 1\ngolden_layout = "nested"\nsuites = ["base"]\n'
        ),
        encoding="utf-8",
    )
    _ = (case_dir / "input.json").write_text(data="42", encoding="utf-8")
    assert load_case_manifest(case_dir=case_dir).golden_layout == "nested"
    assert (
        nested_golden_path(
            case_dir=case_dir,
            stem="Go",
            language_name="Go",
            language_id="go",
            version="v1_18",
            extension=".go",
        )
        == case_dir / "goldens/go/v1_18/base.go"
    )
