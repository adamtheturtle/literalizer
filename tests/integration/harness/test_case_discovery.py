"""Direct discovery must not parse or resolve unrelated work."""

import json
from pathlib import Path

import pytest

from literalizer.languages import Dart
from tests.integration import case_discovery


def test_discovery_selects_before_parsing(
    tmp_path: Path,
) -> None:
    """A narrow suite ignores invalid source owned by another suite."""
    for name, suite, source in (
        ("selected", "base", '{"value": 1}'),
        ("unrelated", "combined", "deliberately invalid JSON"),
    ):
        directory = tmp_path / name
        directory.mkdir()
        _ = (directory / "case.toml").write_text(
            data=f'schema_version = 1\nsuites = ["{suite}"]\n',
            encoding="utf-8",
        )
        _ = (directory / "input.json").write_text(
            data=source, encoding="utf-8"
        )
    assert case_discovery.discover_cases(
        cases_dir=tmp_path,
        suite="base",
        lang_cls=Dart,
    ) == ("selected",)
    # Laziness does not conceal errors when that input is actually selected.
    with pytest.raises(expected_exception=json.JSONDecodeError):
        _ = case_discovery.discover_cases(
            cases_dir=tmp_path,
            suite="combined",
            lang_cls=Dart,
        )
