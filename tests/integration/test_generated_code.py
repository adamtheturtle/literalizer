"""Exercise generated-project execution with real programs and
assertions.
"""

import sys
from pathlib import Path

import pytest

from scripts.generated_code import Step, run_project


def test_compile_batch_and_isolation() -> None:
    """Compile a batch without executing, then verify project
    isolation.
    """
    results = run_project(
        label="compile only",
        files={
            "generated.py": "raise RuntimeError('must not execute')\n",
            "support.py": "raise RuntimeError('must not execute')\n",
        },
        steps=[
            Step(
                args=[
                    sys.executable,
                    "-m",
                    "py_compile",
                    "generated.py",
                    "support.py",
                ],
                failure_label="compile",
            ),
            Step(
                args=[
                    sys.executable,
                    "-c",
                    (
                        "from importlib.util import cache_from_source\n"
                        "from pathlib import Path\n"
                        "for name in ('generated.py', 'support.py'):\n"
                        "    assert Path(cache_from_source(name)).is_file()\n"
                        "print(Path.cwd())\n"
                    ),
                ],
                failure_label="locate project",
            ),
        ],
    )
    assert results[0].stdout == ""
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
                        "assert not any(Path.cwd().iterdir())"
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
