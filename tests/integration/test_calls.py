"""``literalize_call`` golden-file tests.

Drives each call-case configuration against every supporting language,
both for default specs and for non-default language variants (e.g.
Rust's ``TAGGED_ENUM`` strategy on inputs the default ``ERROR``
strategy rejects).
"""

import enum
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat
from literalizer.exceptions import (
    InvalidCallParameterNameError,
    InvalidCallTargetError,
)
from literalizer.languages import (
    Ada,
    Bash,
    Crystal,
    Dart,
    Fortran,
    Kotlin,
    Python,
    Scala,
    V,
    Wren,
    Zig,
)

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


def _check_rejected_call(
    *,
    call_case: CallCase,
    spec: literalizer.Language,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
    version: enum.Enum,
    pytest_config: pytest.Config,
) -> None:
    """Assert the declared public rejection before handling stale
    output.
    """
    assert call_case.expected_exception is not None
    lang_cls = call_case.lang_cls
    with pytest.raises(expected_exception=call_case.expected_exception):
        run_call_golden_case(
            config=call_case.config,
            spec=spec,
            lang_cls=lang_cls,
            golden_name=f"{lang_cls.__name__}_call",
            cases_dir=cases_dir,
            file_regression=file_regression,
            version=version,
        )
    cleanup_stale_golden(
        golden_path=make_golden_path(
            parent=cases_dir / call_case.config.case_dir_name,
            name=f"{lang_cls.__name__}_call",
            extension=lang_cls.extension,
            lang_cls=lang_cls,
            version=version,
        ),
        config=pytest_config,
    )


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
@pytest.mark.parametrize(
    argnames=("lang_cls", "case_name", "target", "parameters"),
    argvalues=[
        (V, "call_quoted_atom_target", "DoThing", ("x",)),
        (Ada, "call_elixir_ignored_parameter_collision", "f", ("x", "_x")),
        (Ada, "call_elixir_ignored_parameter_collision", "f", ("x", "x_")),
    ],
)
def test_invalid_wrapped_identifiers_handle_stale_goldens(
    *,
    tmp_path: Path,
    file_regression: FileRegressionFixture,
    lang_cls: literalizer.LanguageCls,
    case_name: str,
    target: str,
    parameters: tuple[str, ...],
    regenerate: bool,
) -> None:
    """Grammar rejections preserve stale output unless regeneration is
    explicit.
    """
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == case_name
    ).model_copy(
        update={"target_function": target, "parameter_names": parameters}
    )
    case_dir = tmp_path / case_name
    case_dir.mkdir()
    source = "[1]" if len(parameters) == 1 else "[[1, 2]]"
    _ = (case_dir / "input.json").write_text(data=source)
    _ = (case_dir / "case.toml").write_text(
        data=(
            Path(__file__).parent / "cases" / case_name / "case.toml"
        ).read_text(encoding="utf-8")
    )
    version = next(iter(lang_cls.VersionFormats))
    path = make_golden_path(
        parent=case_dir,
        name=f"{lang_cls.__name__}_call",
        extension=lang_cls.extension,
        lang_cls=lang_cls,
        version=version,
    )
    _ = path.write_text(data="stale\n")
    case = CallCase(
        config=config,
        lang_cls=lang_cls,
        expected_exception=expected_call_shape_exception(
            lang_cls=lang_cls, config=config
        ),
    )
    pytest_config = pytest.Config.fromdictargs(
        option_dict={}, args=["--regen-all"] if regenerate else []
    )
    if regenerate:
        _check_rejected_call(
            call_case=case,
            spec=make_spec(lang_cls=lang_cls),
            cases_dir=tmp_path,
            file_regression=file_regression,
            version=version,
            pytest_config=pytest_config,
        )
        assert not path.exists()
    else:
        with pytest.raises(
            expected_exception=pytest.fail.Exception, match="Stale golden file"
        ):
            _check_rejected_call(
                call_case=case,
                spec=make_spec(lang_cls=lang_cls),
                cases_dir=tmp_path,
                file_regression=file_regression,
                version=version,
                pytest_config=pytest_config,
            )
        assert path.read_text(encoding="utf-8") == "stale\n"


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
                _check_rejected_call(
                    call_case=call_case,
                    spec=spec,
                    cases_dir=cases_dir,
                    file_regression=file_regression,
                    version=version_format,
                    pytest_config=file_regression.request.config,
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
    with subtests.test(version=version_format.name):
        run_call_golden_case(
            config=call_variant_case.config,
            spec=call_variant_case.variant.spec,
            lang_cls=lang_cls,
            golden_name=f"{call_variant_case.variant.name}_call",
            cases_dir=cases_dir,
            file_regression=file_regression,
            version=version_format,
        )


@pytest.mark.parametrize(
    argnames=("lang_cls", "target", "parameters", "expected"),
    argvalues=[
        (Fortran, "f", ("x" * 64,), InvalidCallParameterNameError),
        (Fortran, "f" * 64, ("x",), InvalidCallTargetError),
        (Python, "f..g", ("x",), InvalidCallTargetError),
        (Python, "", ("x",), InvalidCallTargetError),
        (Zig, "f", ("i32",), InvalidCallParameterNameError),
        (Dart, "f", ("_x",), InvalidCallParameterNameError),
        (Scala, "f", ("using",), InvalidCallParameterNameError),
        (Scala, "f", ("_",), InvalidCallParameterNameError),
        (Crystal, "f", ("_",), InvalidCallParameterNameError),
        (Kotlin, "f", ("_",), InvalidCallParameterNameError),
        (Wren, "f", ("_x",), InvalidCallParameterNameError),
    ],
)
def test_discovery_identifier_rejections_match_public_api(
    *,
    lang_cls: literalizer.LanguageCls,
    target: str,
    parameters: tuple[str, ...],
    expected: type[Exception],
) -> None:
    """Length, grammar, and pattern facts agree with real public
    rejections.
    """
    config = next(
        config
        for config in default_call_case_specs()
        if config.case_dir_name == "call_quoted_atom_target"
    ).model_copy(
        update={"target_function": target, "parameter_names": parameters}
    )
    assert (
        expected_call_shape_exception(lang_cls=lang_cls, config=config)
        is expected
    )
    with pytest.raises(expected_exception=expected):
        _ = literalizer.literalize_call(
            source="[1]",
            input_format=InputFormat.JSON,
            language=make_spec(lang_cls=lang_cls),
            target_function=target,
            parameter_names=parameters,
            per_element=True,
            wrap_in_file=True,
        )
