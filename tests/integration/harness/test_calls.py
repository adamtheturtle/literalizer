"""Regeneration and rejection-policy checks for the call golden
harness.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, LanguageCls, literalize_call
from literalizer.exceptions import InvalidCallTargetError
from literalizer.languages import Bash, Cpp, Elm, Hcl, PureScript, Sml, V
from tests.integration.call_cases import (
    default_call_case_specs,
    run_call_golden_case,
    run_wrap_in_file_case,
)
from tests.integration.call_variant_cases import (
    build_call_variant_cases,
    run_call_variant_golden_case,
)
from tests.integration.case_inputs import CaseInput
from tests.integration.case_manifests import CaseManifestError
from tests.integration.language_specs import make_golden_path, make_spec


def test_manual_scaffold_rejects_declaration_only_target_error(
    *,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """A valid V fragment must not become an invalid method scaffold."""
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_generated_helper_member_zkv"
    )
    spec = make_spec(lang_cls=V)
    fragment = literalize_call(
        source="1",
        input_format=InputFormat.JSON,
        language=spec,
        target_function=config.target_function,
        parameter_names=config.parameter_names,
        per_element=False,
    )
    assert fragment.code == "obj.ZKV(1);"
    with pytest.raises(expected_exception=InvalidCallTargetError):
        run_call_golden_case(
            config=config,
            spec=spec,
            lang_cls=V,
            golden_name="V_call",
            cases_dir=cases_dir,
            file_regression=file_regression,
            version=spec.language_version,
        )


@pytest.mark.parametrize(argnames="lang_cls", argvalues=[Elm, Hcl])
def test_seeded_scaffold_rejects_immutable_binding(
    *,
    lang_cls: LanguageCls,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """A synthetic seed cannot precede a second immutable binding."""
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_binding_existing_seeded"
    )
    spec = make_spec(lang_cls=lang_cls)
    with pytest.raises(
        expected_exception=pytest.skip.Exception,
        match="cannot redefine the seeded binding",
    ):
        run_call_golden_case(
            config=config,
            spec=spec,
            lang_cls=lang_cls,
            golden_name=f"{lang_cls.__name__}_call",
            cases_dir=cases_dir,
            file_regression=file_regression,
            version=spec.language_version,
        )


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_wrap_in_file_case_handles_stale_rejected_call_arg(
    *,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    regenerate: bool,
    regeneration_config: pytest.Config,
) -> None:
    """A rejected Bash collection preserves or explicitly removes its
    stale fixture.
    """
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_multiline_list_argument"
    ).model_copy(update={"per_element": False})
    golden_path = tmp_path / "stale.sh"
    _ = golden_path.write_text(data="stale\n")

    expected_exception: type[BaseException] = pytest.fail.Exception
    expected_message = r"Stale golden file: .*stale\.sh.*--regen-all"
    if regenerate:
        expected_exception = pytest.skip.Exception
        expected_message = "Bash rejected call arg: list values"
    with pytest.raises(
        expected_exception=expected_exception, match=expected_message
    ):
        run_wrap_in_file_case(
            config=config,
            spec=make_spec(lang_cls=Bash),
            source="[]\n",
            input_info=CaseInput(
                path=tmp_path / "input.yaml",
                input_format=InputFormat.YAML,
                expected_reused_anchor_warning=None,
            ),
            effective_ref_case=None,
            lang_name="Bash",
            lang_extension=Bash.extension,
            golden_path=golden_path,
            file_regression=file_regression,
            pytest_config=regeneration_config,
        )

    if regenerate:
        assert not golden_path.exists()
    else:
        assert golden_path.read_text(encoding="utf-8") == "stale\n"


def _copy_call_inputs(*, source_dir: Path, target_dir: Path) -> None:
    """Copy a case manifest and its inputs into an isolated fixture
    root.
    """
    target_dir.mkdir()
    for source in source_dir.glob(pattern="*"):
        if source.name == "case.toml" or source.name.startswith("input."):
            _ = (target_dir / source.name).write_bytes(
                data=source.read_bytes()
            )


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_variant_rejection_handles_stale_fixture(
    *,
    tmp_path: Path,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    regenerate: bool,
    regeneration_config: pytest.Config,
) -> None:
    """Expected variant refusals use the regeneration-only cleanup
    policy.
    """
    case = next(
        case
        for case in build_call_variant_cases(cases_dir=cases_dir)
        if case.config.case_dir_name == "call_generated_helper_member_zval"
        and case.variant.name == "V_heterogeneous_strategy_record"
    )
    case_dir = tmp_path / case.config.case_dir_name
    _copy_call_inputs(
        source_dir=cases_dir / case.config.case_dir_name, target_dir=case_dir
    )
    golden_path = make_golden_path(
        parent=case_dir,
        name=f"{case.variant.name}_call",
        extension=V.extension,
        lang_cls=V,
        version=case.variant.spec.language_version,
    )
    _ = golden_path.write_text(data="stale\n")
    if regenerate:
        run_call_variant_golden_case(
            call_variant_case=case,
            cases_dir=tmp_path,
            file_regression=file_regression,
            pytest_config=regeneration_config,
        )
        assert not golden_path.exists()
    else:
        with pytest.raises(
            expected_exception=pytest.fail.Exception, match="Stale golden file"
        ):
            run_call_variant_golden_case(
                call_variant_case=case,
                cases_dir=tmp_path,
                file_regression=file_regression,
                pytest_config=regeneration_config,
            )
        assert golden_path.read_text(encoding="utf-8") == "stale\n"


def test_variant_rejection_preserves_unexpected_errors(
    *,
    tmp_path: Path,
    pytestconfig: pytest.Config,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """A different error must never be treated as an expected refusal."""
    case = next(
        case
        for case in build_call_variant_cases(cases_dir=cases_dir)
        if case.config.case_dir_name == "call_generated_helper_member_zval"
        and case.variant.name == "V_heterogeneous_strategy_record"
    )

    case_dir = tmp_path / case.config.case_dir_name
    _copy_call_inputs(
        source_dir=cases_dir / case.config.case_dir_name, target_dir=case_dir
    )
    (case_dir / "input.json").unlink()
    with pytest.raises(
        expected_exception=CaseManifestError,
        match="exactly one inferable input",
    ):
        run_call_variant_golden_case(
            call_variant_case=case,
            cases_dir=tmp_path,
            file_regression=file_regression,
            pytest_config=pytestconfig,
        )


def test_variant_discovery_omits_unavailable_call_styles(
    *, tmp_path: Path
) -> None:
    """A shared curried case excludes specs without curried call
    syntax.
    """
    case_dir = tmp_path / "curried_record"
    case_dir.mkdir()
    _ = (case_dir / "input.json").write_text(data='[{"name":"Ada"}]\n')
    _ = (case_dir / "case.toml").write_text(
        data=(
            'schema_version = 1\nowner = "literalize-call"\n'
            '[call]\ntarget_function = "consume"\n'
            'parameter_names = ["item"]\nper_element = true\n'
            'call_style = "command"\nvariant_only = true\n'
            '[[call.variants]]\naxis = "native_record"\n'
        )
    )
    cases = build_call_variant_cases(cases_dir=tmp_path)
    languages = {case.variant.lang_cls for case in cases}
    assert {PureScript, Sml} <= languages
    assert Cpp not in languages
