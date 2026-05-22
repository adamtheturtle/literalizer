"""In-memory golden-file comparison helper."""

from pathlib import Path

from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture


@beartype
def check_golden(
    *,
    file_regression: FileRegressionFixture,
    contents: str,
    golden_path: Path,
    extension: str,
    newline: str | None,
) -> None:
    """Compare ``contents`` against ``golden_path`` in memory.

    ``file_regression.check`` writes an ``.obtained`` file, reads both
    files back from disk, and runs ``difflib`` even on the pass path,
    which dominates this module's runtime (~13k calls per run).  For
    the pass path we can compare the already-in-memory ``contents``
    against the golden file directly; only on miss or regen do we
    delegate to the fixture for its ``.obtained`` + HTML-diff output.
    """
    config = file_regression.request.config
    regen = file_regression.force_regen or bool(
        config.getoption(name="regen_all")
        or config.getoption(name="force_regen"),
    )
    if (
        not regen
        and golden_path.is_file()
        and contents.splitlines()
        == golden_path.read_text(encoding="utf-8").splitlines()
    ):
        return
    file_regression.check(
        contents=contents,
        encoding="utf-8",
        extension=extension,
        newline=newline,
        fullpath=golden_path,
    )
