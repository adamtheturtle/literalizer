"""Keep Dart's fixture consumer aligned with manifest-owned bindings."""

from pathlib import Path

import pytest

from scripts.run_dart_fixtures import (
    dart_fixture_bindings,
    write_dart_driver,
)


def test_driver_uses_manifest_roots(cases_dir: Path, tmp_path: Path) -> None:
    """Custom names and declaration-like string contents stay distinct."""
    fixtures = [
        cases_dir
        / "swift_record_name_without_record_strategy"
        / "Dart@v3.dart",
        cases_dir / "fortran_variable_name_standard_limit" / "Dart@v3.dart",
        cases_dir
        / "dart_fixture_root_multiline"
        / "Dart_string_format_multiline@v3.dart",
        cases_dir
        / "dart_fixture_root_multiline"
        / "Dart_string_format_multiline_private@v3.dart",
        cases_dir
        / "dart_fixture_root_multiline"
        / "Dart_string_format_multiline_accessor_collision@v3.dart",
    ]
    write_dart_driver(fixtures=fixtures, target=tmp_path)

    driver = (tmp_path / "main.dart").read_text(encoding="utf-8")
    assert "f0.literalizerFixtureRoot," in driver
    assert "f2.literalizerFixtureRoot1," in driver
    assert "f2.my_data" not in driver
    copied = [
        (tmp_path / f"fixture_{index}.dart").read_text(encoding="utf-8")
        for index in range(len(fixtures))
    ]
    assert "get literalizerFixtureRoot => Record0;" in copied[0]
    assert "get literalizerFixtureRoot => " + "v" * 63 + ";" in copied[1]
    assert "get literalizerFixtureRoot1 => custom_data;" in copied[2]
    assert "get literalizerFixtureRoot1 => _customRoot;" in copied[3]
    assert (
        "get literalizerFixtureRoot1 => literalizerFixtureRoot;" in copied[4]
    )
    assert (
        (tmp_path / "fixture_2.dart")
        .read_bytes()
        .startswith(fixtures[2].read_bytes())
    )


def test_all_dart_fixtures_have_binding_metadata(cases_dir: Path) -> None:
    """Regular, call and reference golden files all have an owned root."""
    bindings = dart_fixture_bindings()
    actual = {
        fixture.resolve() for fixture in cases_dir.rglob(pattern="*.dart")
    }
    assert actual <= bindings.keys()


def test_unowned_dart_fixture_is_rejected(tmp_path: Path) -> None:
    """A valid declaration cannot substitute for missing ownership."""
    fixture = tmp_path / "unowned.dart"
    _ = fixture.write_text(data="final my_data = 1;\n", encoding="utf-8")
    with pytest.raises(
        expected_exception=ValueError, match="has no golden metadata"
    ):
        write_dart_driver(fixtures=[fixture], target=tmp_path)
