"""Validate the Java runner's release selection and native failure
path.
"""

import shutil
from pathlib import Path

import pytest
from click.testing import CliRunner

from scripts.run_java_fixtures import main
from tests.integration import list_fixtures


def test_java_fixture_runner(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Both target releases compile and execute; a bad initializer
    fails.
    """
    if shutil.which(cmd="java") is None or (
        shutil.which(cmd="timeout") is None
        and shutil.which(cmd="gtimeout") is None
    ):
        pytest.skip(reason="A JDK and GNU timeout are required")
    monkeypatch.setattr(target=list_fixtures, name="CASES_DIR", value=tmp_path)
    selected = tmp_path / "selected"
    selected.mkdir()
    for release in (11, 16):
        _ = (selected / f"fixture@jdk_{release}.java").write_text(
            data="class Main { public static void main() {} }",
            encoding="utf-8",
        )
    ignored = tmp_path / "ignored"
    ignored.mkdir()
    _ = (ignored / "invalid@jdk_11.java").write_text(
        data="invalid java",
        encoding="utf-8",
    )
    runner = CliRunner()
    arguments = ["--case", "selected", "--batch-size", "1"]
    assert runner.invoke(cli=main, args=arguments).exit_code == 0
    failing = selected / "failing@jdk_11.java"
    _ = failing.write_text(
        data='class Main { int value = Integer.parseInt("bad"); }',
        encoding="utf-8",
    )
    assert runner.invoke(cli=main, args=arguments).exit_code != 0
    # A failure in the old-target population cannot contaminate a selected
    # newer-target run, and no fixture runs for an empty case selection.
    assert (
        runner.invoke(cli=main, args=[*arguments, "--release", "16"]).exit_code
        == 0
    )
    assert runner.invoke(cli=main, args=["--case", "absent"]).exit_code != 0
