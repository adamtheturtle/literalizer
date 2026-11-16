"""Exercise native runner selection and real syntax/runtime failures."""

import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from scripts import run_interpreted_fixtures


def _require_runtime(*, backend: str) -> None:
    """Keep optional native controls portable across Python test hosts."""
    executable = "node" if backend == "javascript" else backend
    if shutil.which(cmd=executable) is None or (
        shutil.which(cmd="timeout") is None
        and shutil.which(cmd="gtimeout") is None
    ):
        pytest.skip(reason=f"{backend} and GNU timeout are required")
    if backend == "bash":
        result = subprocess.run(  # noqa: S603 - selected installed interpreter
            args=[
                executable,
                "-c",
                (
                    "(( BASH_VERSINFO[0] > 5 || "
                    "(BASH_VERSINFO[0] == 5 && BASH_VERSINFO[1] >= 1) ))"
                ),
            ],
            timeout=5,
            check=False,
        )
        if result.returncode != 0:
            pytest.skip(reason="Bash 5.1+ is required")


@pytest.mark.parametrize(
    argnames=("backend", "extension", "valid", "invalid", "runtime_error"),
    argvalues=[
        ("bash", ".sh", "true", "if", "exit 3"),
        ("ruby", ".rb", "1", "def", 'raise "native failure"'),
        (
            "javascript",
            ".js",
            "const value = 1;",
            "const = ;",
            'throw new Error("native failure");',
        ),
    ],
)
def test_native_runner_failures(
    *,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    backend: str,
    extension: str,
    valid: str,
    invalid: str,
    runtime_error: str,
) -> None:
    """Select one case and distinguish native syntax and execution
    checks.
    """
    _require_runtime(backend=backend)
    monkeypatch.setattr(
        target=run_interpreted_fixtures, name="_CASES_DIR", value=tmp_path
    )
    selected = tmp_path / "selected"
    selected.mkdir()
    fixture = selected / f"fixture@version{extension}"
    ignored = tmp_path / "ignored"
    ignored.mkdir()
    _ = (ignored / f"invalid@version{extension}").write_text(
        data=invalid, encoding="utf-8"
    )
    runner = CliRunner()
    arguments = [backend, "--case", "selected", "--jobs", "1"]
    _ = fixture.write_text(data=valid, encoding="utf-8")
    assert (
        runner.invoke(
            cli=run_interpreted_fixtures.main, args=arguments
        ).exit_code
        == 0
    )
    _ = fixture.write_text(data=invalid, encoding="utf-8")
    assert (
        runner.invoke(
            cli=run_interpreted_fixtures.main, args=arguments
        ).exit_code
        != 0
    )
    _ = fixture.write_text(data=runtime_error, encoding="utf-8")
    assert (
        runner.invoke(
            cli=run_interpreted_fixtures.main,
            args=[*arguments, "--check", "syntax"],
        ).exit_code
        == 0
    )
    assert (
        runner.invoke(
            cli=run_interpreted_fixtures.main,
            args=[*arguments, "--check", "execution"],
        ).exit_code
        != 0
    )
    assert (
        runner.invoke(
            cli=run_interpreted_fixtures.main,
            args=[backend, "--case", "absent"],
        ).exit_code
        != 0
    )


def test_native_runner_deadline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """An infinite native consumer terminates at its own deadline."""
    _require_runtime(backend="javascript")
    monkeypatch.setattr(
        target=run_interpreted_fixtures, name="_CASES_DIR", value=tmp_path
    )
    _ = (tmp_path / "loop@es2015.js").write_text(
        data="while (true) {}", encoding="utf-8"
    )
    result = CliRunner().invoke(
        cli=run_interpreted_fixtures.main,
        args=["javascript", "--check", "execution", "--timeout", "0.1"],
    )
    assert isinstance(result.exception, subprocess.CalledProcessError)
    assert result.exception.returncode in (124, 137)
