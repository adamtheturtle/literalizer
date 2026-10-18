"""Typed scaffold refusals must not leave executable stale fixtures."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer.languages import Elm

from . import literalize_ref_cases
from .case_manifests import RefCaseSpec
from .language_specs import make_golden_path, make_spec


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_refused_scaffold_handles_stale_fixture(
    *,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    file_regression: FileRegressionFixture,
    regenerate: bool,
) -> None:
    """Verification reports stale output; regeneration removes it."""
    case_dir = tmp_path / "external"
    case_dir.mkdir()
    _ = (case_dir / "input.json").write_text(
        data='{"$ref": "shared"}\n', encoding="utf-8"
    )
    _ = (case_dir / "case.toml").write_text(
        data='schema_version = 1\nowner = "literalize-ref-default"\n[ref]\n',
        encoding="utf-8",
    )
    config = RefCaseSpec.model_validate(
        obj={
            "variable_form": "existing",
            "external_declarations": {"my_data": "1", "shared": "1"},
            "explicit_ref_value_sources": {"shared": "1"},
        },
        context={"case_dir_name": "external"},
    )
    version = Elm.VersionFormats["V0_19"]
    golden_path = make_golden_path(
        parent=case_dir,
        name="Elm_ref_default",
        extension=Elm.extension,
        lang_cls=Elm,
        version=version,
    )
    _ = golden_path.write_text(data="stale fixture\n", encoding="utf-8")

    monkeypatch.setattr(
        target=file_regression.request.config.option,
        name="regen_all",
        value=regenerate,
    )
    outcome = pytest.skip.Exception if regenerate else pytest.fail.Exception
    with pytest.raises(expected_exception=outcome):
        literalize_ref_cases.run_literalize_ref_golden_case(
            config=config,
            lang_cls=Elm,
            spec=make_spec(lang_cls=Elm, language_version=version),
            golden_name="Elm_ref_default",
            cases_dir=tmp_path,
            file_regression=file_regression,
            ref_case=None,
            version=version,
        )
    assert golden_path.exists() is not regenerate
