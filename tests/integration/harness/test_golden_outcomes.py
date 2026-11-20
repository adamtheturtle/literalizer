"""A resolved golden expectation governs execution and fixture writes."""

import functools
from collections.abc import Mapping
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer import (
    InputFormat,
    Language,
    LanguageCls,
    ValueInput,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    CallArgNotSupportedError,
    ExistingVariableNotSelfContainedError,
    NullInCollectionError,
)
from literalizer.languages import Bash, Mojo, Scala, V
from tests.integration.golden_checks import check_outcome
from tests.integration.golden_outcomes import SUCCESS, Exclusion, Rejection
from tests.integration.literal_expectations import (
    literal_rejection,
    literal_source,
)

pytest_plugins: tuple[str, ...] = ("pytester",)


def _bash_call(*, source: str) -> str:
    """Render a native call carrying one JSON value."""
    return literalize_call(
        source=source,
        input_format=InputFormat.JSON,
        language=Bash(),
        target_function="emit",
        parameter_names=("value",),
        per_element=False,
    ).code


def test_success_propagates_a_previous_skip_error(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A selected successful call fails if Bash rejects its value."""
    golden_path = tmp_path / "call.sh"
    with pytest.raises(
        expected_exception=CallArgNotSupportedError, match="list values"
    ):
        check_outcome(
            outcome=SUCCESS,
            render=functools.partial(_bash_call, source="[]"),
            golden_path=golden_path,
            file_regression=file_regression,
        )
    assert not golden_path.exists()


def test_rejection_propagates_the_wrong_error(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A collection argument error cannot satisfy a binding rejection."""
    golden_path = tmp_path / "call.sh"
    with pytest.raises(
        expected_exception=CallArgNotSupportedError, match="list values"
    ):
        check_outcome(
            outcome=Rejection(
                error=ExistingVariableNotSelfContainedError,
                match="the assignment has no prior declaration",
            ),
            render=functools.partial(_bash_call, source="[]"),
            golden_path=golden_path,
            file_regression=file_regression,
        )
    assert not golden_path.exists()


def test_exclusion_reaching_execution_fails(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A fixture prerequisite belongs in discovery."""
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match="Discovery exclusion reached execution: missing call syntax",
    ):
        check_outcome(
            outcome=Exclusion(reason="missing call syntax"),
            render=functools.partial(_bash_call, source="[]"),
            golden_path=tmp_path / "call.sh",
            file_regression=file_regression,
        )


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_rejection_preserves_fixture_ownership(
    *, pytester: pytest.Pytester, regenerate: bool
) -> None:
    """Exercise the real verification and regeneration command lines."""
    _ = pytester.makepyfile(
        """\
from pathlib import Path
import pytest
from literalizer.exceptions import CallArgNotSupportedError
from tests.integration.golden_checks import check_outcome
from tests.integration.golden_outcomes import Rejection
from tests.integration.harness.test_golden_outcomes import _bash_call


def test_rejection(file_regression):
    golden_path = Path(__file__).with_name("rejected.sh")
    outcome = Rejection(error=CallArgNotSupportedError, match="list values")
    with pytest.raises(pytest.fail.Exception, match="DID NOT RAISE"):
        check_outcome(
            outcome=outcome,
            render=lambda: _bash_call(source="3"),
            golden_path=golden_path,
            file_regression=file_regression,
        )

    with pytest.raises(
        pytest.fail.Exception, match="Unexpected success fixture"
    ):
        check_outcome(
            outcome=outcome,
            render=lambda: _bash_call(source="[]"),
            golden_path=Path(__file__).with_name("stale.sh"),
            file_regression=file_regression,
        )
""",
    )
    stale_path = pytester.path / "stale.sh"
    original = b"stale\n"
    _ = stale_path.write_bytes(data=original)
    _ = pytester.makeini(source="[pytest]")
    pytester.syspathinsert(path=Path(__file__).resolve().parents[3])
    result = pytester.runpytest_inprocess(
        "--disable-plugin-autoload",
        "-p",
        "pytest_regressions.plugin",
        "-p",
        "pytest_datadir.plugin",
        "-q",
        *(["--regen-all"] if regenerate else []),
    )
    result.assert_outcomes(passed=1)
    assert stale_path.read_bytes() == original
    assert not (pytester.path / "rejected.sh").exists()


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
def test_literal_null_collection_outcomes(
    *, pytester: pytest.Pytester, regenerate: bool
) -> None:
    """Assert the native carrier's limit and preserve a supported
    golden.
    """
    source_case = (
        Path(__file__).resolve().parents[1] / "cases" / "simple_sequence"
    )
    case_dir = pytester.path / source_case.name
    case_dir.mkdir()
    for name in ("case.toml", "input.yaml", "Scala@v3.scala"):
        _ = (case_dir / name).write_bytes(
            data=(source_case / name).read_bytes()
        )
    _ = pytester.makepyfile(
        """\
from dataclasses import replace
from pathlib import Path

import pytest

from literalizer import NewVariable
from literalizer.exceptions import NullInCollectionError
from literalizer.languages import Scala
from tests.integration import test_literalize_golden as runner
from tests.integration.golden_renderings import (
    compact_render,
    unprefixed_rendering,
)
from tests.integration.scenario_skips import VARIANT_SKIPS


def test_null_sequence(file_regression, monkeypatch):
    cases_dir = Path(__file__).parent
    case_dir = cases_dir / "simple_sequence"
    rendering = replace(
        unprefixed_rendering(
            lang_cls=Scala,
            case_dir_name=case_dir.name,
            golden_name="Scala",
            spec_source={},
            render=compact_render(
                variable_form=NewVariable(
                    name="my_data", modifiers=frozenset()
                ),
            ),
            skip=VARIANT_SKIPS,
        ),
        golden_parent=case_dir,
    )
    original = (case_dir / "Scala@v3.scala").read_bytes()

    def check(rendering, spec):
        runner._check_rendering(
            rendering=rendering,
            spec=spec,
            cases_dir=cases_dir,
            file_regression=file_regression,
        )

    rejected = replace(rendering, golden_name="Scala_sequence_format_array")
    array_spec = Scala(sequence_format=Scala.SequenceFormats["ARRAY"])
    check(rejected, array_spec)
    rejected_path = rejected.artifact(version=array_spec.language_version).path
    assert not rejected_path.exists()

    check(rendering, Scala())
    assert (case_dir / "Scala@v3.scala").read_bytes() == original

    def unexpected_null_error(**kwargs):
        raise NullInCollectionError("unexpected failure in a supported list")

    monkeypatch.setattr(runner, "literalize_rendering", unexpected_null_error)
    with pytest.raises(NullInCollectionError, match="unexpected failure"):
        check(rendering, Scala())
    assert (case_dir / "Scala@v3.scala").read_bytes() == original
""",
    )
    root = Path(__file__).resolve().parents[3]
    _ = pytester.makeini(
        source=f'[pytest]\npythonpath = "{root}" "{root / "src"}"'
    )
    result = pytester.runpytest_subprocess(
        "--disable-plugin-autoload",
        "-p",
        "pytest_regressions.plugin",
        "-p",
        "pytest_datadir.plugin",
        "-q",
        *(["--regen-all"] if regenerate else []),
    )
    result.assert_outcomes(passed=1)


@pytest.mark.parametrize(
    argnames=("lang_cls", "spec", "yaml", "substitutions", "rejects"),
    argvalues=[
        (V, V(), "field: null", None, True),
        (V, V(), "field: null", {"field": 42}, False),
        (V, V(), "field: null", {"field": (None,)}, True),
        (
            Scala,
            Scala(
                sequence_format=Scala.SequenceFormats["ARRAY"],
                heterogeneous_strategy=Scala.HeterogeneousStrategies["RECORD"],
            ),
            '[null, [{"field": 1}]]',
            None,
            False,
        ),
        (
            Scala,
            Scala(
                sequence_format=Scala.SequenceFormats["ARRAY"],
                json_type=Scala.JsonTypes["CIRCE"],
            ),
            "[1, null]",
            None,
            False,
        ),
        (
            Mojo,
            Mojo(
                heterogeneous_strategy=Mojo.HeterogeneousStrategies["VARIANT"]
            ),
            "[1, null]",
            None,
            True,
        ),
    ],
)
def test_null_expectations_use_effective_input(
    *,
    tmp_path: Path,
    lang_cls: LanguageCls,
    spec: Language,
    yaml: str,
    substitutions: Mapping[str, ValueInput] | None,
    rejects: bool,
) -> None:
    """Resolve nulls after the declared round trip and substitutions."""
    _ = (tmp_path / "case.toml").write_text(
        data='schema_version = 1\nsuites = ["base"]\n'
        '[input_roundtrip]\nlanguage = "Jsonc"\ninput_format = "jsonc"\n',
        encoding="utf-8",
    )
    _ = (tmp_path / "input.yaml").write_text(data=yaml, encoding="utf-8")
    input_info, source = literal_source(case_dir=tmp_path)
    assert input_info.input_format is InputFormat.JSONC
    outcome = literal_rejection(
        spec=spec,
        lang_cls=lang_cls,
        variable_form=None,
        case_dir=tmp_path,
        substitutions=substitutions,
    )
    render = functools.partial(
        literalize,
        language=spec,
        source=source,
        input_format=input_info.input_format,
        record_null_substitutions=substitutions,
    )
    if rejects:
        assert isinstance(outcome, Rejection)
        assert outcome.error is NullInCollectionError
        with pytest.raises(
            expected_exception=outcome.error, match=outcome.match
        ):
            _ = render()
    else:
        assert outcome is None
        _ = render()
