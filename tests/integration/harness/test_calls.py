"""Regeneration and rejection-policy checks for the call golden
harness.
"""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, LanguageCls, literalize_call
from literalizer.exceptions import InvalidCallTargetError
from literalizer.languages import ALL_LANGUAGES, V
from tests.integration.call_cases import (
    run_call_golden_case,
)
from tests.integration.call_collection import (
    CallRendering,
    default_call_case_specs,
    discover_call_cases,
)
from tests.integration.call_variant_cases import (
    build_call_variant_cases,
)
from tests.integration.case_manifests import CaseManifestError
from tests.integration.language_specs import (
    find_redefinition_styles,
    make_spec,
)


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
            rendering=CallRendering(
                config=config,
                spec=spec,
                lang_cls=V,
                golden_name="V_call",
                expected_exception=None,
            ),
            cases_dir=cases_dir,
            file_regression=file_regression,
        )


def _declares_immutable_call_binding(lang_cls: LanguageCls, /) -> bool:
    """Select assignments that declare a binding with no mutable style."""
    spec = make_spec(lang_cls=lang_cls)
    return (
        len(lang_cls.CallStyles) > 0
        and spec.call_assignment_declares_binding
        and len(find_redefinition_styles(spec=spec)) == 0
    )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=[
        cls
        for cls in sorted(ALL_LANGUAGES, key=lambda cls: cls.__name__)
        if _declares_immutable_call_binding(cls)
    ],
    ids=lambda cls: cls.language_id,
)
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
            rendering=CallRendering(
                config=config,
                spec=spec,
                lang_cls=lang_cls,
                golden_name=f"{lang_cls.__name__}_call",
                expected_exception=None,
            ),
            cases_dir=cases_dir,
            file_regression=file_regression,
        )


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


@pytest.mark.parametrize(argnames="variant", argvalues=[False, True])
def test_call_rejection_handles_stale_fixture(
    *,
    variant: bool,
    tmp_path: Path,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Report the conflicting fixture and preserve its contents."""
    if variant:
        rendering = next(
            case.renderings[0]
            for case in build_call_variant_cases(cases_dir=cases_dir)
            if case.config.case_dir_name == "call_generated_helper_member_zval"
            and case.variant.name == "V_heterogeneous_strategy_record"
        )
    else:
        rendering = next(
            case.renderings[0]
            for case in discover_call_cases()
            if case.config.case_dir_name == "call_generated_helper_member_zkv"
            and case.lang_cls is V
        )
    assert rendering.expected_exception is not None
    case_dir = tmp_path / rendering.config.case_dir_name
    _copy_call_inputs(
        source_dir=cases_dir / rendering.config.case_dir_name,
        target_dir=case_dir,
    )
    golden_path = rendering.golden_path(cases_dir=tmp_path)
    _ = golden_path.write_text(data="stale\n")
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match="Unexpected success fixture",
    ):
        run_call_golden_case(
            rendering=rendering,
            cases_dir=tmp_path,
            file_regression=file_regression,
        )
    assert golden_path.read_text(encoding="utf-8") == "stale\n"


def test_variant_rejection_preserves_unexpected_errors(
    *,
    tmp_path: Path,
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
        run_call_golden_case(
            rendering=case.renderings[0],
            cases_dir=tmp_path,
            file_regression=file_regression,
        )
