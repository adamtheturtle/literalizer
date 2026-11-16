"""Direct discovery must not parse or resolve unrelated work."""

import json
from pathlib import Path
from unittest.mock import Mock

import pytest

from literalizer.languages import Dart
from tests.integration import case_discovery
from tests.integration.language_specs import make_spec


def test_discovery_selects_before_parsing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
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
    specs = Mock(wraps=make_spec)
    monkeypatch.setattr(target=case_discovery, name="make_spec", value=specs)
    assert case_discovery.discover_cases(
        cases_dir=tmp_path,
        suite="base",
        lang_cls=Dart,
    ) == ("selected",)
    assert [call.kwargs["lang_cls"] for call in specs.call_args_list] == [Dart]
    # Laziness does not conceal errors when that input is actually selected.
    with pytest.raises(expected_exception=json.JSONDecodeError):
        _ = case_discovery.discover_cases(
            cases_dir=tmp_path,
            suite="combined",
            lang_cls=Dart,
        )
