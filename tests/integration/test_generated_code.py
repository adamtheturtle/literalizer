"""Exercise the extraction boundary with real programs and assertions."""

import json
import sys
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from scripts.generated_code import Step, run_project


def test_independent_generator(
    file_regression: FileRegressionFixture,
) -> None:
    """Snapshot, compile and consume a tiny schema generator's output."""
    fields = {"quantity": "int", "enabled": "bool", "balance": "float"}
    source = (
        "from dataclasses import dataclass\n\n"
        "@dataclass\nclass Invoice:\n"
        + "".join(f"    {name}: {kind}\n" for name, kind in fields.items())
    )
    # Snapshot comparison is usable without invoking a compiler or runner.
    file_regression.check(
        contents=source,
        fullpath=Path(__file__).with_suffix(suffix="")
        / "test_independent_generator.txt",
    )
    results = run_project(
        label="schema generator / Invoice",
        files={
            "models/invoice.py": source,
            "consumer.py": (
                "import json\nfrom models.invoice import Invoice\n"
                "item = Invoice(quantity=1, enabled=True, balance=-0.0)\n"
                "print(json.dumps(item.__dict__))\n"
            ),
        },
        steps=[
            Step(
                args=[sys.executable, "-m", "py_compile", "models/invoice.py"],
                failure_label="Python compile",
            ),
            Step(
                args=[sys.executable, "consumer.py"],
                failure_label="Python consumer",
            ),
        ],
    )
    # This caller ignores key order while retaining JSON's type and sign
    # distinctions: 1 differs from true, and 0.0 differs from -0.0.
    actual = json.dumps(obj=json.loads(s=results[-1].stdout), sort_keys=True)
    assert actual == '{"balance": -0.0, "enabled": true, "quantity": 1}'


def test_standalone_runner() -> None:
    """Use the module with no installed packages or repository imports."""
    source = Path("scripts/generated_code.py").read_text(encoding="utf-8")
    results = run_project(
        label="standalone runner",
        files={
            "generated_code.py": source,
            "generator.py": (
                "import sys\nfrom generated_code import Step, run_project\n"
                "source = 'answer = ' + repr(42) + '\\n'\n"
                "result = run_project(label='independent', "
                "files={'generated.py': source, "
                "'consumer.py': 'from generated import answer; "
                "print(answer)'}, "
                "steps=[Step(args=[sys.executable, 'consumer.py'], "
                "failure_label='consume')])\n"
                "assert not any(name == 'literalizer' or "
                "name.startswith(('literalizer.', 'tests.')) "
                "for name in sys.modules)\n"
                "print(result[-1].stdout, end='')\n"
            ),
        },
        steps=[
            Step(
                args=[sys.executable, "-S", "generator.py"],
                failure_label="standalone generator",
            ),
        ],
    )
    assert results[-1].stdout == "42\n"


def test_compile_only_and_isolation() -> None:
    """Compile without executing, then verify project isolation."""
    results = run_project(
        label="compile only",
        files={"generated.py": "raise RuntimeError('must not execute')\n"},
        steps=[
            Step(
                args=[sys.executable, "-m", "py_compile", "generated.py"],
                failure_label="compile",
            ),
            Step(
                args=[
                    sys.executable,
                    "-c",
                    "from pathlib import Path; print(Path.cwd())",
                ],
                failure_label="locate project",
            ),
        ],
    )
    assert not Path(results[-1].stdout.strip()).exists()
    isolated = run_project(
        label="fresh project",
        files={},
        steps=[
            Step(
                args=[
                    sys.executable,
                    "-c",
                    (
                        "from pathlib import Path; "
                        "assert not Path('generated.py').exists()"
                    ),
                ],
                failure_label="isolation",
            ),
        ],
    )
    assert isolated[-1].returncode == 0


def test_failure_diagnostics_and_cleanup() -> None:
    """A failure reports sources and streams, stops the chain and cleans
    up.
    """
    with pytest.raises(
        expected_exception=AssertionError, match="broken fixture"
    ) as exc:
        _ = run_project(
            label="broken fixture",
            files={
                "generated.py": (
                    "import sys\nfrom pathlib import Path\n"
                    "print(Path.cwd())\nprint('compiler stdout')\n"
                    "print('compiler stderr', file=sys.stderr)\n"
                    "sys.exit(7)\n"
                ),
                "support/config.txt": "support content",
            },
            steps=[
                Step(
                    args=[sys.executable, "generated.py"],
                    failure_label="compile",
                ),
                Step(args=["must-not-run"], failure_label="later step"),
            ],
        )
    diagnostic = str(object=exc.value)
    assert "status 7" in diagnostic
    assert "compiler stdout" in diagnostic
    assert "compiler stderr" in diagnostic
    assert "support/config.txt:\nsupport content" in diagnostic
    assert "generated.py:\nimport sys" in diagnostic
    assert "later step" not in diagnostic
    project = diagnostic.split(sep="\n")[2]
    assert not Path(project).exists()


@pytest.mark.parametrize(
    argnames="name", argvalues=["/absolute.py", "../escape.py", "."]
)
def test_project_relative_paths(name: str) -> None:
    """Reject files that cannot live inside the temporary project."""
    with pytest.raises(
        expected_exception=ValueError, match="project-relative"
    ):
        _ = run_project(label="invalid path", files={name: ""}, steps=[])


def test_missing_compiler() -> None:
    """An unavailable tool reports the fixture and selected command."""
    with pytest.raises(
        expected_exception=AssertionError, match="missing compiler: compile"
    ):
        _ = run_project(
            label="missing compiler",
            files={"main.py": ""},
            steps=[Step(args=["./does-not-exist"], failure_label="compile")],
        )


def test_compiler_batch() -> None:
    """Keep multiple generated modules in one caller-selected compiler
    step.
    """
    results = run_project(
        label="Python batch",
        files={"first.py": "value = 1\n", "second.py": "value = 2\n"},
        steps=[
            Step(
                args=[
                    sys.executable,
                    "-m",
                    "py_compile",
                    "first.py",
                    "second.py",
                ],
                failure_label="batch compile",
            ),
        ],
    )
    assert len(results) == 1
