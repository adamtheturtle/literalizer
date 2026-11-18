"""Check that nested golden paths preserve native fixture behavior."""

from pathlib import Path

from scripts.fixture_staging import stage_fixture_modules
from tests.integration.fixture_names import fixture_module_name
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
