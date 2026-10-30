"""Typed scaffold refusals must not leave executable stale fixtures."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import SequenceFormatConfig
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import CSharp, Elm
from tests.integration import literalize_ref_cases
from tests.integration.case_manifests import RefCaseSpec
from tests.integration.language_specs import make_golden_path, make_spec
from tests.integration.literalize_ref_cases import external_assignment_spec


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


@pytest.mark.parametrize(argnames="explicit_choice", argvalues=[False, True])
def test_fixed_length_destination_refuses_different_arity(
    *, monkeypatch: pytest.MonkeyPatch, explicit_choice: bool
) -> None:
    """Neither a forced tuple nor fixed-only formats can change native
    type.
    """
    spec = CSharp()
    config = RefCaseSpec.model_validate(
        obj={
            "variable_form": "existing",
            "external_declarations": {"my_data": "[0]", "shared": "[1, 2]"},
            "sequence_format": "TUPLE" if explicit_choice else None,
        },
        context={"case_dir_name": "external"},
    )
    if not explicit_choice:
        fixed_config = spec.sequence_format_config

        def fixed_only_config(_spec: object, /) -> SequenceFormatConfig:
            """Model a producer with no length-independent sequence option."""
            return fixed_config

        monkeypatch.setattr(
            target=CSharp,
            name="sequence_format_config",
            value=property(fget=fixed_only_config),
        )
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot change length on reassignment",
    ):
        _ = external_assignment_spec(
            spec=spec, config=config, raw_data={"$ref": "shared"}
        )
