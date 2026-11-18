"""Direct discovery must not parse or resolve unrelated work."""

import json
from pathlib import Path

import pytest

from literalizer.languages import Dart, Jsonc, Python
from tests.integration import case_discovery
from tests.integration.golden_outcomes import SUCCESS, Exclusion


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


def test_excluded_control_key_lists_its_reason(tmp_path: Path) -> None:
    """The authored key contract excludes Python and admits JSONC."""
    case_dir = tmp_path / "control_key"
    case_dir.mkdir()
    _ = (case_dir / "case.toml").write_text(
        data='schema_version = 1\nsuites = ["base"]\n',
        encoding="utf-8",
    )
    _ = (case_dir / "input.json").write_text(
        data=r'{"a\u0001b": 1}',
        encoding="utf-8",
    )
    (entry,) = case_discovery.discover_case_admissions(
        cases_dir=tmp_path, suite="base", lang_cls=Python
    )
    assert entry.case_name == "control_key"
    assert isinstance(entry.outcome, Exclusion)
    assert "documented control-key rejection" in entry.outcome.reason

    (accepted,) = case_discovery.discover_case_admissions(
        cases_dir=tmp_path, suite="base", lang_cls=Jsonc
    )
    assert accepted.outcome is SUCCESS
