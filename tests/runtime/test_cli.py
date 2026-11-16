"""Command-line parsing and output contracts for project helpers."""

from pathlib import Path

import click
import pytest
from click.testing import CliRunner

from scripts import (
    build_cpp_toolchain,
    check_jsonc_syntax,
    check_occam_syntax,
    run_dart_fixtures,
    run_go_roundtrip,
    run_mojo_roundtrip,
    run_rust_roundtrip,
)
from tests.integration import list_fixtures


@pytest.mark.parametrize(
    argnames="command",
    argvalues=[
        build_cpp_toolchain.main,
        check_jsonc_syntax.main,
        check_occam_syntax.main,
        list_fixtures.main,
        run_dart_fixtures.main,
        run_go_roundtrip.main,
        run_mojo_roundtrip.main,
        run_rust_roundtrip.main,
    ],
)
def test_help_without_running_tools(command: click.Command) -> None:
    """Help exits successfully before reading files or running a toolchain."""
    result = CliRunner().invoke(cli=command, args=["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.stdout
    assert "--help" in result.stdout
    assert result.stderr == ""


@pytest.mark.parametrize(
    argnames=("command", "arguments", "missing"),
    argvalues=[
        (check_occam_syntax.main, [], "FILENAME"),
        (list_fixtures.main, [".py"], "VERSION"),
        (run_rust_roundtrip.main, ["deps"], "SERDE_JSON_RLIB"),
        (build_cpp_toolchain.main, [], "--work-directory"),
        (
            build_cpp_toolchain.main,
            ["--work-directory", "work"],
            "--output-directory",
        ),
    ],
)
def test_missing_arguments(
    command: click.Command,
    arguments: list[str],
    missing: str,
) -> None:
    """Missing inputs produce usage errors before starting external
    work.
    """
    result = CliRunner().invoke(cli=command, args=arguments)
    assert result.exit_code == click.UsageError.exit_code
    assert missing in result.stderr
    assert "Missing" in result.stderr
    assert result.stdout == ""


def test_unknown_option() -> None:
    """No-argument runners reject unexpected options before running
    tools.
    """
    result = CliRunner().invoke(
        cli=run_go_roundtrip.main,
        args=["--unknown"],
    )
    assert result.exit_code == click.UsageError.exit_code
    assert "No such option" in result.stderr
    assert "--unknown" in result.stderr


def test_jsonc_files(tmp_path: Path) -> None:
    """Variadic filenames preserve spaces, diagnostics and failure
    status.
    """
    valid = tmp_path / "valid document.jsonc"
    invalid = tmp_path / "invalid document.jsonc"
    _ = valid.write_text(data='{"key": true /* comment */}', encoding="utf-8")
    _ = invalid.write_text(data="{", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(
        cli=check_jsonc_syntax.main, args=[str(object=valid)]
    )
    assert result.exit_code == 0
    assert result.output == ""
    result = runner.invoke(
        cli=check_jsonc_syntax.main,
        args=[str(object=invalid), str(object=valid)],
    )
    assert result.exit_code == 1
    assert str(object=invalid) in result.stderr
    assert str(object=valid) not in result.stderr


def test_jsonc_no_files() -> None:
    """An empty file batch remains a successful no-op."""
    result = CliRunner().invoke(cli=check_jsonc_syntax.main, args=[])
    assert result.exit_code == 0
    assert result.output == ""


def test_fixture_listing(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keep version selection, ordering and null delimiters byte-for-
    byte.
    """
    monkeypatch.setattr(target=list_fixtures, name="CASES_DIR", value=tmp_path)
    names = ["b space@v1.py", "a@v1.py", "other@v2.py", "other@v1.rb"]
    for name in names:
        (tmp_path / name).touch()
    runner = CliRunner()
    result = runner.invoke(cli=list_fixtures.main, args=[".py", "v1"])
    assert result.exit_code == 0
    assert result.stdout_bytes == (
        f"{tmp_path / names[1]}\0{tmp_path / names[0]}\0".encode()
    )
    assert result.stderr == ""
    result = runner.invoke(cli=list_fixtures.main, args=[".py", "missing"])
    assert result.exit_code == 0
    assert result.stdout_bytes == b""


def test_toolchain_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Options supply resolved Path objects and create the work
    directory.
    """
    calls: list[tuple[Path, Path]] = []

    def build(work: Path, output: Path, /) -> None:
        """Record build inputs without downloading or compiling LLVM."""
        assert work.is_dir()
        calls.append((work, output))

    monkeypatch.setattr(target=build_cpp_toolchain, name="build", value=build)
    work = tmp_path / "work directory"
    output = tmp_path / "output directory"
    result = CliRunner().invoke(
        cli=build_cpp_toolchain.main,
        args=[
            "--work-directory",
            str(object=work),
            "--output-directory",
            str(object=output),
        ],
    )
    assert result.exit_code == 0
    assert calls == [(work.resolve(), output.resolve())]
