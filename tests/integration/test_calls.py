"""``literalize_call`` golden-file tests.

Drives each call-case configuration against every supporting language,
both for default specs and for non-default language variants (e.g.
Rust's ``TAGGED_ENUM`` strategy on inputs the default ``ERROR``
strategy rejects).
"""

from contextlib import nullcontext
from pathlib import Path
from typing import NoReturn

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import InputFormat, LanguageCls, literalize_call
from literalizer.exceptions import InvalidCallTargetError
from literalizer.languages import Bash, Cpp, Elm, Hcl, PureScript, Sml, V

from .call_cases import (
    CallCase,
    default_call_case_specs,
    discover_call_cases,
    expected_call_shape_exception,
    run_call_golden_case,
    run_wrap_in_file_case,
)
from .call_variant_cases import CallVariantCase, build_call_variant_cases
from .case_inputs import CaseInput
from .golden_checks import cleanup_stale_golden
from .language_specs import make_golden_path, make_spec


def test_manual_scaffold_rejects_declaration_only_target_error(
    *,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """A valid V fragment must not become an invalid method scaffold."""
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_zig_helper_member_zkv"
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
) -> None:
    """A rejected Bash collection preserves or explicitly removes its
    stale fixture.
    """
    pytest_config = pytest.Config.fromdictargs(
        option_dict={}, args=["--regen-all"] if regenerate else []
    )
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
            pytest_config=pytest_config,
        )

    if regenerate:
        assert not golden_path.exists()
    else:
        assert golden_path.read_text(encoding="utf-8") == "stale\n"


@pytest.mark.parametrize(
    argnames="call_case",
    argvalues=discover_call_cases(),
    ids=lambda case: f"{case.config.case_dir_name}/{case.lang_cls.__name__}",
)
def test_call_golden_file(
    call_case: CallCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test that literalize_call output matches expected golden file."""
    config = call_case.config
    lang_cls = call_case.lang_cls
    for version_format in lang_cls.VersionFormats:
        with subtests.test(version=version_format.name):
            spec = make_spec(
                lang_cls=lang_cls,
                language_version=version_format,
            )
            if call_case.expected_exception is not None:
                with pytest.raises(
                    expected_exception=call_case.expected_exception,
                ):
                    run_call_golden_case(
                        config=config,
                        spec=spec,
                        lang_cls=lang_cls,
                        golden_name=f"{lang_cls.__name__}_call",
                        cases_dir=cases_dir,
                        file_regression=file_regression,
                        version=version_format,
                    )
                cleanup_stale_golden(
                    golden_path=make_golden_path(
                        parent=cases_dir / config.case_dir_name,
                        name=f"{lang_cls.__name__}_call",
                        extension=lang_cls.extension,
                        lang_cls=lang_cls,
                        version=version_format,
                    ),
                    config=file_regression.request.config,
                )
                continue
            run_call_golden_case(
                config=config,
                spec=spec,
                lang_cls=lang_cls,
                golden_name=f"{lang_cls.__name__}_call",
                cases_dir=cases_dir,
                file_regression=file_regression,
                version=version_format,
            )


@pytest.mark.parametrize(
    argnames="call_variant_case",
    argvalues=build_call_variant_cases(),
    ids=lambda case: f"{case.config.case_dir_name}/{case.variant.name}",
)
def test_call_variant_golden_file(
    call_variant_case: CallVariantCase,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
) -> None:
    """Test ``literalize_call`` for a non-default language spec.

    Covers call inputs that need a non-default language option, such as
    statement terminators or heterogeneous strategies.
    """
    lang_cls = call_variant_case.variant.lang_cls
    # The plan already expands supported versions and resolves explicit
    # pins and syntax floors. Render each effective spec once.
    version_format = call_variant_case.variant.spec.language_version
    expected_exception = expected_call_shape_exception(
        lang_cls=lang_cls,
        config=call_variant_case.config,
        spec=call_variant_case.variant.spec,
    )
    with subtests.test(version=version_format.name):
        if expected_exception is not None:
            with pytest.raises(expected_exception=expected_exception):
                run_call_golden_case(
                    config=call_variant_case.config,
                    spec=call_variant_case.variant.spec,
                    lang_cls=lang_cls,
                    golden_name=f"{call_variant_case.variant.name}_call",
                    cases_dir=cases_dir,
                    file_regression=file_regression,
                    version=version_format,
                )
            cleanup_stale_golden(
                golden_path=make_golden_path(
                    parent=cases_dir / call_variant_case.config.case_dir_name,
                    name=f"{call_variant_case.variant.name}_call",
                    extension=lang_cls.extension,
                    lang_cls=lang_cls,
                    version=version_format,
                ),
                config=file_regression.request.config,
            )
            return
        run_call_golden_case(
            config=call_variant_case.config,
            spec=call_variant_case.variant.spec,
            lang_cls=lang_cls,
            golden_name=f"{call_variant_case.variant.name}_call",
            cases_dir=cases_dir,
            file_regression=file_regression,
            version=version_format,
        )


def _uncaptured_subtest(**_kwargs: object) -> nullcontext[None]:
    """Let an outer raises assertion observe an inner test failure."""
    return nullcontext()


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_variant_rejection_handles_stale_fixture(
    *,
    tmp_path: Path,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
    monkeypatch: pytest.MonkeyPatch,
    regenerate: bool,
) -> None:
    """Expected variant refusals use the regeneration-only cleanup
    policy.
    """
    case = next(
        case
        for case in build_call_variant_cases()
        if case.config.case_dir_name == "call_zig_helper_member_zval"
        and case.variant.name == "V_heterogeneous_strategy_record"
    )
    case_dir = tmp_path / case.config.case_dir_name
    case_dir.mkdir()
    for source in (cases_dir / case.config.case_dir_name).glob(pattern="*"):
        if source.name == "case.toml" or source.name.startswith("input."):
            _ = (case_dir / source.name).write_bytes(data=source.read_bytes())
    golden_path = make_golden_path(
        parent=case_dir,
        name=f"{case.variant.name}_call",
        extension=V.extension,
        lang_cls=V,
        version=case.variant.spec.language_version,
    )
    _ = golden_path.write_text(data="stale\n")
    monkeypatch.setattr(
        target=file_regression.request.config.option,
        name="regen_all",
        value=regenerate,
    )
    if regenerate:
        test_call_variant_golden_file(
            call_variant_case=case,
            cases_dir=tmp_path,
            file_regression=file_regression,
            subtests=subtests,
        )
        assert not golden_path.exists()
    else:
        monkeypatch.setattr(
            target=subtests, name="test", value=_uncaptured_subtest
        )
        with pytest.raises(
            expected_exception=pytest.fail.Exception, match="Stale golden file"
        ):
            test_call_variant_golden_file(
                call_variant_case=case,
                cases_dir=tmp_path,
                file_regression=file_regression,
                subtests=subtests,
            )
        assert golden_path.read_text(encoding="utf-8") == "stale\n"


def test_variant_rejection_preserves_unexpected_errors(
    *,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    subtests: pytest.Subtests,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A different error must never be treated as an expected refusal."""
    case = next(
        case
        for case in build_call_variant_cases()
        if case.config.case_dir_name == "call_zig_helper_member_zval"
        and case.variant.name == "V_heterogeneous_strategy_record"
    )

    def fail_unexpectedly(**_kwargs: object) -> NoReturn:
        """Simulate an unrelated harness failure."""
        msg = "unexpected failure"
        raise ValueError(msg)

    monkeypatch.setattr(
        target="tests.integration.test_calls.run_call_golden_case",
        name=fail_unexpectedly,
    )
    monkeypatch.setattr(
        target=subtests, name="test", value=_uncaptured_subtest
    )
    with pytest.raises(
        expected_exception=ValueError, match="unexpected failure"
    ):
        test_call_variant_golden_file(
            call_variant_case=case,
            cases_dir=cases_dir,
            file_regression=file_regression,
            subtests=subtests,
        )


def test_variant_discovery_omits_unavailable_call_styles(
    *, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
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
    monkeypatch.setattr(
        target="tests.integration.call_variant_cases.CASES_DIR",
        name=tmp_path,
    )
    cases = build_call_variant_cases.__wrapped__()
    languages = {case.variant.lang_cls for case in cases}
    assert {PureScript, Sml} <= languages
    assert Cpp not in languages
