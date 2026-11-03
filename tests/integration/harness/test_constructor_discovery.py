"""Constructor ownership remains exhaustive when selections overlap."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from tests.integration import constructor_cases
from tests.integration import test_constructor_targets as constructor_goldens


@pytest.mark.parametrize(argnames="owner_count", argvalues=[0, 2])
def test_every_matching_owner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, owner_count: int
) -> None:
    """Every binding variant retains all owners or its legacy fallback."""
    baseline = constructor_cases.constructor_binding_cases()
    expected = {
        case.name
        for case in baseline
        if case.manifest is None
        or (
            case.manifest.constructor is not None
            and case.manifest.constructor.target_template is None
        )
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


def test_legacy_constructor_binding_uses_fragment_file(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Keep the fragment fallback usable during independent migrations."""
    cases_dir = tmp_path / "cases"
    cases_dir.mkdir()
    monkeypatch.setattr(
        target=constructor_cases, name="CASES_DIR", value=cases_dir
    )
    monkeypatch.setattr(
        target=constructor_cases,
        name="__file__",
        value=str(object=tmp_path / "constructor_cases.py"),
    )
    case = next(
        case
        for case in constructor_cases.constructor_binding_cases()
        if case.name == "OCaml_constructor_call"
    )
    path = constructor_cases.constructor_golden_path(
        case=case, version=next(iter(case.lang_cls.VersionFormats))
    )
    assert path.parent == tmp_path / "constructor_targets"
    assert path.suffix == ".txt"
    path.parent.mkdir()
    _ = path.write_text(
        data="type val_t =\n  | OList of val_t list\nlet p = Playlist()\n",
        encoding="utf-8",
    )
    constructor_goldens.test_constructor_binding_golden_file(
        case=case, file_regression=file_regression, subtests=subtests
    )
