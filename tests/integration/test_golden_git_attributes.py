"""Git preserves intentional CRLF bytes in string-format goldens."""

import os
import shutil
import subprocess
from pathlib import Path

import pytest


def _git(
    *, repo: Path, args: list[str], check: bool
) -> subprocess.CompletedProcess[bytes]:
    """Use a temporary index with a known ordinary whitespace policy."""
    git = shutil.which(cmd="git")
    assert git is not None
    return subprocess.run(
        args=[
            git,
            "-C",
            str(object=repo),
            "-c",
            "core.autocrlf=true",
            "-c",
            "core.whitespace=blank-at-eol,blank-at-eof,space-before-tab",
            *args,
        ],
        check=check,
        capture_output=True,
        timeout=30,
    )


@pytest.mark.parametrize(
    argnames="case_name",
    argvalues=["string_carriage_return_line_feed", "crlf_string_formats"],
)
def test_staged_crlf_goldens_preserve_bytes(
    case_name: str, cases_dir: Path, tmp_path: Path
) -> None:
    """Stage real goldens without normalization or a whitespace error."""
    project = cases_dir.parents[2]
    _ = _git(repo=tmp_path, args=["init", "--quiet"], check=True)
    _ = (tmp_path / ".gitattributes").write_bytes(
        data=(project / ".gitattributes").read_bytes()
    )
    goldens = {
        Path(os.path.relpath(path=path, start=project)).as_posix(): (
            path.read_bytes()
        )
        for path in (cases_dir / case_name).glob(pattern="*@*")
        if b"\r\n" in path.read_bytes()
    }
    assert len(goldens) > 0
    for name, contents in goldens.items():
        destination = tmp_path / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        _ = destination.write_bytes(data=contents)
    _ = _git(repo=tmp_path, args=["add", "."], check=True)
    for name, contents in goldens.items():
        staged = _git(repo=tmp_path, args=["show", f":{name}"], check=True)
        assert staged.stdout == contents
    _ = _git(repo=tmp_path, args=["diff", "--cached", "--check"], check=True)

    # The case attributes must not relax checks on ordinary files.
    _ = (tmp_path / "control.txt").write_bytes(data=b"trailing space \n")
    _ = _git(repo=tmp_path, args=["add", "control.txt"], check=True)
    invalid = _git(
        repo=tmp_path, args=["diff", "--cached", "--check"], check=False
    )
    assert invalid.returncode != 0
    assert b"control.txt" in invalid.stdout
