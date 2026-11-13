"""Select native lint jobs for a pull request's tested merge commit.

Only versioned golden files and documentation are eligible for filtering. Any
other change runs every native job: round-trip helpers generate programs
from source, and some read case manifests and inputs. Main, scheduled and
manual runs always run everything, including external compiler updates.
"""

import json
import logging
import os
import shutil
import subprocess
from collections.abc import Sequence
from pathlib import Path

_LOGGER = logging.getLogger(name=__name__)
_CASES_DIR = Path("tests/integration/cases")

# Keep grouped jobs and the shared C/C++ toolchain paired with their fixture
# extensions in the lint workflow. Tests check the actual fixture commands.
JOB_EXTENSIONS: dict[str, frozenset[str]] = {
    "lint-fast": frozenset(
        {
            ".c",
            ".dhall",
            ".f90",
            ".fth",
            ".java",
            ".js",
            ".lua",
            ".nix",
            ".php",
            ".ps1",
            ".rb",
            ".scm",
            ".sh",
            ".tcl",
            ".wren",
        }
    ),
    "lint-odin": frozenset({".odin"}),
    "lint-roc": frozenset({".roc"}),
    "lint-matlab": frozenset({".m"}),
    "lint-perl": frozenset({".pl"}),
    "lint-go-installed": frozenset({".hcl", ".jsonnet"}),
    "lint-npm-installed": frozenset({".json5", ".jsonc", ".norg", ".ts"}),
    "lint-typescript-run": frozenset({".ts"}),
    "lint-elm": frozenset({".elm"}),
    "lint-elm-run": frozenset({".elm"}),
    "lint-uv-scripts": frozenset({".adb", ".occ", ".toml", ".yaml"}),
    "lint-dotnet": frozenset({".cs", ".fs", ".fsi", ".vb"}),
    "lint-sml": frozenset({".sml"}),
    "lint-elixir": frozenset({".ex"}),
    "lint-erlang": frozenset({".erl"}),
    "lint-gleam": frozenset({".gleam"}),
    "lint-jvm-mini": frozenset({".clj", ".groovy"}),
    "lint-haskell-family": frozenset({".hs", ".purs"}),
    "lint-c-tidy": frozenset({".c"}),
    "build-cpp-toolchain": frozenset({".c", ".cpp"}),
    "lint-cpp-tidy": frozenset({".cpp"}),
    "lint-cobol": frozenset({".cob"}),
    "lint-cpp": frozenset({".cpp"}),
    "lint-kotlin": frozenset({".kts"}),
    "lint-swift": frozenset({".swift"}),
    "lint-ocaml": frozenset({".ml"}),
    "lint-commonlisp": frozenset({".lisp"}),
    "lint-scala": frozenset({".scala"}),
    "lint-haxe": frozenset({".hx"}),
    "lint-dart": frozenset({".dart"}),
    "lint-julia": frozenset({".jl"}),
    "lint-go": frozenset({".go"}),
    "lint-rust": frozenset({".rs"}),
    "lint-r": frozenset({".R"}),
    "lint-d": frozenset({".d"}),
    "lint-crystal": frozenset({".cr"}),
    "lint-mojo": frozenset({".mojo"}),
    "lint-nim": frozenset({".nim"}),
    "lint-python": frozenset({".py"}),
    "lint-racket": frozenset({".rkt"}),
    "lint-raku": frozenset({".raku"}),
    "lint-zig": frozenset({".zig"}),
    "lint-systemverilog": frozenset({".sv"}),
    "lint-v": frozenset({".v"}),
    "lint-objectivec": frozenset({".m"}),
    "lint-objectivec-tidy": frozenset({".m"}),
}


def select_jobs(*, paths: Sequence[str]) -> list[str]:
    """Run matching jobs, or everything for any unrecognized input."""
    known_extensions = {
        extension
        for extensions in JOB_EXTENSIONS.values()
        for extension in extensions
    }
    changed_extensions: set[str] = set()
    for name in paths:
        if name.startswith(("docs/", "newsfragments/")) or name in {
            "README.rst",
            "CHANGELOG.md",
            "LICENSE",
        }:
            continue
        path = Path(name)
        if (
            path.parent.parent != _CASES_DIR
            or "@" not in path.stem
            or path.suffix not in known_extensions
        ):
            return list(JOB_EXTENSIONS)
        changed_extensions.add(path.suffix)
    return [
        job
        for job, extensions in JOB_EXTENSIONS.items()
        if len(extensions & changed_extensions) > 0
    ]


def main() -> None:
    """Write selected job IDs as a JSON GitHub Actions output."""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    jobs = list(JOB_EXTENSIONS)
    git = shutil.which(cmd="git")
    if (
        os.environ.get(key="GITHUB_EVENT_NAME") == "pull_request"
        and git is not None
    ):
        # checkout's default PR ref is the tested merge commit; its first
        # parent is the base it was merged into. Disable rename detection
        # so both the deleted and added paths select their native jobs.
        diff = subprocess.run(
            args=[
                git,
                "diff",
                "--name-only",
                "--no-renames",
                "-z",
                "HEAD^1",
                "HEAD",
                "--",
            ],
            check=False,
            capture_output=True,
        )
        if diff.returncode == 0:
            paths = os.fsdecode(filename=diff.stdout).split(sep="\0")
            jobs = select_jobs(paths=[path for path in paths if path != ""])
        else:
            _LOGGER.warning(
                "Cannot compare the PR merge commit; running all native jobs."
            )
    with Path(os.environ["GITHUB_OUTPUT"]).open(
        mode="a", encoding="utf-8"
    ) as output:
        _ = output.write(f"jobs={json.dumps(obj=jobs)}\n")
    _LOGGER.info("Selected %s native jobs: %s", len(jobs), ", ".join(jobs))


if __name__ == "__main__":
    main()
