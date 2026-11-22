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
    HeterogeneousCollectionError,
    HeterogeneousScalarCollectionError,
    MixedListValuesError,
    NullInCollectionError,
    UnrepresentableInputError,
)
from literalizer.languages import Bash, Mojo, Scala, V
from tests.integration.call_collection import discover_call_cases
from tests.integration.call_ref_contracts import authored_call_ref_outcome
from tests.integration.case_manifests import case_input
from tests.integration.golden_checks import (
    assert_rejection,
    check_outcome,
    golden_test_parameters,
)
from tests.integration.golden_outcomes import SUCCESS, Exclusion, Rejection
from tests.integration.golden_renderings import compact_render
from tests.integration.golden_scenarios import scenario_renderings
from tests.integration.literal_expectations import (
    literal_rejection,
    literal_source,
)
from tests.integration.literal_rejection_manifest import (
    LITERAL_REJECTION_MANIFEST,
    authored_literal_rejection,
    literal_rejection_rules,
)

pytest_plugins: tuple[str, ...] = ("pytester",)


def test_literal_rejection_rules_are_exercised() -> None:
    """Every fixture and language named by a rule has a matching spec."""
    rules = literal_rejection_rules(manifest_path=LITERAL_REJECTION_MANIFEST)
    remaining = {
        (case_name, lang_cls, index)
        for (case_name, lang_cls), entries in rules.items()
        for index in range(len(entries))
    }
    for (_, lang_cls), renderings in scenario_renderings().items():
        for rendering in renderings:
            key = (rendering.case_dir_name, lang_cls)
            if key not in rules:
                continue
            for spec in rendering.specs:
                for index, (selector, _) in enumerate(iterable=rules[key]):
                    if selector.matches(spec=spec, render=rendering.render):
                        remaining.discard((*key, index))

    assert len(remaining) == 0, [
        (case_name, lang_cls.__name__, rules[case_name, lang_cls][index])
        for case_name, lang_cls, index in remaining
    ]


_LITERAL_REJECTION_RULE = """\
[[rejection]]
error = "UnrepresentableInputError"
match = "cannot represent null"
applies = [{cases = ["null"], languages = ["Bash"]}]
"""


@pytest.mark.parametrize(
    argnames=("manifest", "match"),
    argvalues=[
        (
            _LITERAL_REJECTION_RULE.replace(
                'languages = ["Bash"]',
                'languages = ["Bash"], options = {unknown = "NONE"}',
            ),
            "Unknown literal rejection options.*unknown",
        ),
        (
            _LITERAL_REJECTION_RULE
            + _LITERAL_REJECTION_RULE.replace(
                "UnrepresentableInputError", "UnrepresentableNullError"
            ),
            "Conflicting rejections for fixture null",
        ),
    ],
)
def test_literal_rejection_manifest_rejects_ambiguous_configuration(
    *, tmp_path: Path, manifest: str, match: str
) -> None:
    """Invalid rules fail before the target renderer runs."""
    manifest_path = tmp_path / "literal_rejections.toml"
    _ = manifest_path.write_text(data=manifest, encoding="utf-8")
    with pytest.raises(expected_exception=ValueError, match=match):
        _ = authored_literal_rejection(
            case_name="null",
            lang_cls=Bash,
            spec=Bash(),
            render=compact_render(variable_form=None),
            manifest_path=manifest_path,
        )


def test_exact_rejection_rejects_a_subclass(*, tmp_path: Path) -> None:
    """Matching diagnostic text cannot mask a different exception type."""
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match="got UnrepresentableNullError",
    ):
        assert_rejection(
            outcome=Rejection(
                error=UnrepresentableInputError,
                match="cannot represent null",
            ),
            render=functools.partial(
                literalize,
                source="null",
                input_format=InputFormat.JSON,
                language=Bash(),
            ),
            golden_path=tmp_path / "null.sh",
            exact_type=True,
        )


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


def test_mojo_stub_requires_common_argument_slot_types(
    cases_dir: Path,
) -> None:
    """A generated Mojo target needs a common type for each slot."""
    case = next(
        case
        for case in discover_call_cases()
        if case.config.case_dir_name == "call_scalar_args"
        and case.lang_cls is Mojo
    )
    assert all(
        rendering.outcome
        == Exclusion(
            reason="the synthetic target stub needs a common type "
            "for each argument slot"
        )
        for rendering in case.renderings
    )
    parameters = golden_test_parameters(
        cases=[(case.test_id, case.renderings)]
    )
    assert len(parameters) == 0

    case_source = case_input(case_dir=cases_dir / case.config.case_dir_name)
    render = functools.partial(
        literalize_call,
        source=case_source.path.read_text(encoding="utf-8"),
        input_format=case_source.input_format,
        language=Mojo(),
        target_function=case.config.target_function,
        parameter_names=case.config.parameter_names,
        per_element=case.config.per_element,
    )
    assert render().code.splitlines() == [
        'process("hello")',
        "process(42)",
        "process(True)",
    ]
    with pytest.raises(
        expected_exception=HeterogeneousScalarCollectionError,
        match="call argument types diverge across calls",
    ):
        _ = render(wrap_in_file=True)


@pytest.mark.parametrize(
    argnames=("options", "message"),
    argvalues=[
        ('{ bogus = "NONE" }', "Unknown contract options"),
        ("{}", "Conflicting contracts"),
    ],
)
def test_invalid_call_ref_contract_fails_during_resolution(
    *, tmp_path: Path, options: str, message: str
) -> None:
    """Reject misspelled option selectors and contradictory outcomes."""
    case = next(
        case
        for case in discover_call_cases()
        if case.config.case_dir_name == "call_scalar_args"
        and case.lang_cls is Mojo
    )
    manifest = tmp_path / "contracts.toml"
    _ = manifest.write_text(
        data=f"""\
[[exclusion]]
reason = "synthetic fixture prerequisite"

[[exclusion.applies]]
cases = ["call_scalar_args"]
languages = ["Mojo"]
options = {options}

[[rejection]]
error = "HeterogeneousScalarCollectionError"

[[rejection.applies]]
cases = ["call_scalar_args"]
languages = ["Mojo"]
""",
        encoding="utf-8",
    )
    with pytest.raises(expected_exception=ValueError, match=message):
        _ = authored_call_ref_outcome(
            config=case.config,
            spec=Mojo(),
            lang_cls=Mojo,
            manifest_path=manifest,
        )


def test_strict_rejection_rejects_a_different_subclass(
    *, tmp_path: Path, file_regression: FileRegressionFixture
) -> None:
    """A related collection exception cannot satisfy an exact contract."""
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match="got HeterogeneousScalarCollectionError",
    ):
        check_outcome(
            outcome=Rejection(
                error=HeterogeneousCollectionError, match=None, exact_type=True
            ),
            render=lambda: (
                literalize(
                    source='[1, "hello"]',
                    input_format=InputFormat.JSON,
                    language=Mojo(),
                ).code
            ),
            golden_path=tmp_path / "mixed.mojo",
            file_regression=file_regression,
        )


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
from literalizer.exceptions import (
    NullInCollectionError,
    UnrepresentableInputError,
)
from literalizer.languages import Scala
from tests.integration import test_literalize_golden as runner
from tests.integration.golden_renderings import (
    compact_render,
    unprefixed_rendering,
)


def test_null_sequence(file_regression):
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

    # Keep the list option so the harness still expects success.
    class ScalaListWithArrayOpener(Scala):
        @property
        def sequence_open(self):
            return array_spec.sequence_open

    with pytest.raises(
        NullInCollectionError, match="Array cannot contain null"
    ):
        check(rendering, ScalaListWithArrayOpener())
    assert (case_dir / "Scala@v3.scala").read_bytes() == original

    class ScalaListWithUnrepresentableOpener(Scala):
        @property
        def sequence_open(self):
            raise UnrepresentableInputError("unexpected rejection")

    missing = replace(rendering, golden_name="Scala_second_list")
    with pytest.raises(
        UnrepresentableInputError, match="unexpected rejection"
    ):
        check(missing, ScalaListWithUnrepresentableOpener())
    assert not missing.artifact(version=Scala().language_version).path.exists()
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
    source = literal_source(case_dir=tmp_path)
    assert source.input_info.input_format is InputFormat.JSONC
    outcome = literal_rejection(
        spec=spec,
        lang_cls=lang_cls,
        variable_form=None,
        case_dir=tmp_path,
        substitutions=substitutions,
        wrap_in_file=False,
    )
    render = functools.partial(
        literalize,
        language=spec,
        source=source.source_text,
        input_format=source.input_info.input_format,
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


def test_mojo_mixed_list_takes_precedence_over_null(*, tmp_path: Path) -> None:
    """A scalar wrapper cannot reconcile a scalar and a list."""
    _ = (tmp_path / "case.toml").write_text(
        data='schema_version = 1\nsuites = ["base"]\n',
        encoding="utf-8",
    )
    source = "[null, [1], 2]"
    _ = (tmp_path / "input.yaml").write_text(data=source, encoding="utf-8")
    spec = Mojo(heterogeneous_strategy=Mojo.HeterogeneousStrategies["VARIANT"])
    assert (
        literal_rejection(
            spec=spec,
            lang_cls=Mojo,
            variable_form=None,
            case_dir=tmp_path,
            substitutions=None,
            wrap_in_file=False,
        )
        is None
    )
    with pytest.raises(
        expected_exception=MixedListValuesError, match="mixed type families"
    ):
        _ = literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=spec,
        )
