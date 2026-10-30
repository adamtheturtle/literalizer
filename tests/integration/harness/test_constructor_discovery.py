"""Constructor ownership remains exhaustive when selections overlap."""

from pathlib import Path

import pytest

from tests.integration import constructor_cases


@pytest.mark.parametrize(argnames="owner_count", argvalues=[0, 2])
def test_every_matching_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, owner_count: int
) -> None:
    """Every binding variant retains all owners or its legacy fallback."""
    baseline = constructor_cases.constructor_binding_cases()
    expected = {case.name for case in baseline}
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
    monkeypatch.setattr(
        target=constructor_cases, name="CASES_DIR", value=tmp_path
    )
    actual = constructor_cases.constructor_binding_cases()
    owners = {
        case.manifest.case_dir.name
        for case in actual
        if case.manifest is not None
    }
    assert owners == {f"wrapper_{index}" for index in range(owner_count)}
    for name in expected:
        matching = [case for case in actual if case.name == name]
        assert len(matching) == max(1, owner_count)
        if owner_count == 0:
            assert matching[0].manifest is None
