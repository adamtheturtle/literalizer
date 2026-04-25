"""Meta-test for the in-memory golden-file assertion helper."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from .golden_assertions import check_golden


def test_check_golden_mismatch_delegates(
    tmp_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """``check_golden`` delegates to ``file_regression.check`` on miss.

    Every golden file matches in CI, so nothing else reaches the
    fallback branch.
    """
    golden = tmp_path / "golden.txt"
    golden.write_text(data="expected\n")
    with pytest.raises(
        expected_exception=AssertionError,
        match="FILES DIFFER",
    ):
        check_golden(
            file_regression=file_regression,
            contents="different\n",
            golden_path=golden,
            extension=".txt",
            newline="",
        )
