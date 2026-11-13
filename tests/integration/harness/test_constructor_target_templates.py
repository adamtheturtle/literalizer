"""Native template availability must not change participation."""

from pathlib import Path

import pytest

from tests.integration import constructor_cases
from tests.integration.case_manifests import CaseManifestError


def test_missing_target_template_is_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An incomplete template table cannot silently skip a backend."""
    monkeypatch.setattr(
        target=constructor_cases,
        name="constructor_binding_specs",
        value=list,
    )
    case_dir = tmp_path / "native_target"
    case_dir.mkdir()
    _ = (case_dir / "input.json").write_text(data="[[]]\n", encoding="utf-8")
    _ = (case_dir / "case.toml").write_text(
        data=(
            'schema_version = 1\nowner = "constructor-binding"\n'
            '[constructor.target_templates]\nAda = "{target}"\n'
        ),
        encoding="utf-8",
    )
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="no constructor target template",
    ):
        _ = constructor_cases.constructor_binding_cases(cases_dir=tmp_path)
