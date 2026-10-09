"""Exercise Kotlin fixture deadlines with actual compiler/evaluation
work.
"""

import os
import shutil
import subprocess
from pathlib import Path

import pytest

_TIMEOUT_EXIT_STATUS = 124

_requires_pinned_kotlin = pytest.mark.skipif(
    condition=os.environ.get(key="LITERALIZER_KOTLIN_DEADLINE_TESTS") != "1",
    reason="native Kotlin deadline tests run in the pinned Kotlin lint job",
)


def _run_kotlin(
    *, tmp_path: Path, sources: list[str]
) -> subprocess.CompletedProcess[str]:
    """Run the real Kotlin host with an isolated output directory."""
    kotlin = shutil.which(cmd="kotlin")
    assert kotlin is not None, "the Kotlin lint job must supply its compiler"
    files: list[str] = []
    for index, source in enumerate(iterable=sources):
        path = tmp_path / f"fixture {index}.kts"
        _ = path.write_text(data=source, encoding="utf-8")
        files.append(str(object=path))
    temp_root = tmp_path / "jvm-temp"
    temp_root.mkdir()
    environment = dict(os.environ)
    environment["LITERALIZER_KOTLIN_TIMEOUT_SECONDS"] = "15"
    result = subprocess.run(
        args=[
            kotlin,
            f"-J-Djava.io.tmpdir={temp_root}",
            "scripts/lint-kotlin.main.kts",
        ],
        input="\0".join(files) + "\0",
        capture_output=True,
        text=True,
        check=False,
        env=environment,
        timeout=90,
    )
    assert not any(temp_root.glob(pattern="kotlin-lint-*"))
    return result


@_requires_pinned_kotlin
def test_completed_fixture_cancels_deadline(tmp_path: Path) -> None:
    """Cancel each timer before a later fixture runs past its deadline."""
    result = _run_kotlin(
        tmp_path=tmp_path,
        sources=[
            'Thread.sleep(8000); println("first")',
            'Thread.sleep(8000); println("second")',
        ],
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == "first\nsecond\n"
    assert "deadline" not in result.stderr


@_requires_pinned_kotlin
def test_compilation_error_preserves_remaining_checks(tmp_path: Path) -> None:
    """Keep compilation failures and continue with subsequent fixtures."""
    result = _run_kotlin(
        tmp_path=tmp_path,
        sources=["val broken =", 'println("checked")'],
    )
    assert result.returncode == 1, result.stderr
    assert result.stdout == "checked\n"
    assert f"Failed: {tmp_path / 'fixture 0.kts'}" in result.stderr
    assert "deadline" not in result.stderr


@_requires_pinned_kotlin
def test_stalled_evaluation_reports_fixture(tmp_path: Path) -> None:
    """Stop an infinite evaluation and name its file and elapsed
    budget.
    """
    result = _run_kotlin(
        tmp_path=tmp_path,
        sources=['println("started"); while (true) {}'],
    )
    assert result.returncode == _TIMEOUT_EXIT_STATUS, result.stderr
    assert result.stdout == "started\n"
    assert (
        f"{tmp_path / 'fixture 0.kts'}: compiler/evaluation deadline (15s) "
        "exceeded after "
    ) in result.stderr
