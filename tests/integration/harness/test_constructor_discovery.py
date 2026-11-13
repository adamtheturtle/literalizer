"""Constructor ownership remains exhaustive when selections overlap."""

from pathlib import Path

import pytest

from tests.integration import constructor_cases
from tests.integration.case_manifests import CaseManifestError


@pytest.mark.parametrize(argnames="owner_count", argvalues=[0, 2])
def test_every_matching_owner(
    tmp_path: Path, cases_dir: Path, owner_count: int
) -> None:
    """Keep every native owner and reject missing fixture ownership."""
    baseline = constructor_cases.constructor_binding_cases(cases_dir=cases_dir)
    expected = {
        case.name
        for case in baseline
        if case.manifest.constructor is not None
        and case.manifest.constructor.target_template is None
        and len(case.manifest.constructor.target_templates) == 0
    }
    for index in range(owner_count):
        case_dir = tmp_path / f"wrapper_{index}"
        case_dir.mkdir()
        _ = (case_dir / "input.json").write_text(
            data="[[]]\n", encoding="utf-8"
        )
        _ = (case_dir / "case.toml").write_text(
            data=(
                "schema_version = 1\n"
                'owner = "constructor-binding"\n[constructor]\n'
            ),
            encoding="utf-8",
        )
    if owner_count == 0:
        with pytest.raises(
            expected_exception=CaseManifestError,
            match="has no native fixture owner",
        ):
            _ = constructor_cases.constructor_binding_cases(cases_dir=tmp_path)
        return
    actual = constructor_cases.constructor_binding_cases(cases_dir=tmp_path)
    owners = {case.manifest.case_dir.name for case in actual}
    assert owners == {f"wrapper_{index}" for index in range(owner_count)}
    for name in expected:
        matching = [case for case in actual if case.name == name]
        assert len(matching) == owner_count
