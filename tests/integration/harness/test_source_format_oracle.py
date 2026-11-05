"""Failure diagnostics and independence of the formatting CI oracle."""

import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path
from unittest.mock import Mock

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

from literalizer.languages import ALL_LANGUAGES
from tests.integration import golden_checks
from tests.integration import source_format_oracle as oracle


@pytest.fixture(autouse=True)
def fixture_reset_oracle_cache() -> Iterator[None]:
    """Keep each tool-installation scenario independent."""
    oracle.formatter_path.cache_clear()
    yield
    oracle.formatter_path.cache_clear()


def test_missing_formatter(monkeypatch: pytest.MonkeyPatch) -> None:
    """A CI environment missing the pinned tool fails explicitly."""
    monkeypatch.setattr(
        target=shutil, name="which", value=Mock(return_value=None)
    )
    with pytest.raises(
        expected_exception=FileNotFoundError, match="source-format"
    ):
        _ = oracle.formatter_path()


def test_wrong_formatter_version(monkeypatch: pytest.MonkeyPatch) -> None:
    """An arbitrary system installation cannot replace the pinned
    oracle.
    """
    monkeypatch.setattr(
        target=shutil,
        name="which",
        value=Mock(return_value="/tools/clang-format"),
    )
    monkeypatch.setattr(
        target=subprocess,
        name="run",
        value=Mock(
            return_value=subprocess.CompletedProcess(
                args=[], returncode=0, stdout="clang-format version 0.0.1\n"
            )
        ),
    )
    with pytest.raises(
        expected_exception=AssertionError,
        match=r"Expected clang-format 23\.1\.3",
    ):
        _ = oracle.formatter_path()


@pytest.mark.parametrize(argnames="changed", argvalues=[False, True])
def test_compare_fresh_source(
    *, changed: bool, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A mismatch fails with an attributed diff without rewriting
    input.
    """
    source = "int main(void) { return 0; }"
    formatted = (
        "int main(void) {\n  return 0;\n}\n" if changed else source + "\n"
    )
    monkeypatch.setattr(
        target=shutil,
        name="which",
        value=Mock(return_value="/tools/clang-format"),
    )
    run = Mock(
        side_effect=[
            subprocess.CompletedProcess(
                args=[], returncode=0, stdout="clang-format version 23.1.3\n"
            ),
            subprocess.CompletedProcess(
                args=[], returncode=0, stdout=formatted
            ),
        ]
    )
    monkeypatch.setattr(target=subprocess, name="run", value=run)
    if changed:
        with pytest.raises(
            expected_exception=AssertionError, match="fresh canonical request"
        ):
            oracle.check_source_format(
                contents=source, path=Path("owned-request.m")
            )
    else:
        oracle.check_source_format(
            contents=source, path=Path("owned-request.m")
        )
    assert run.call_args.kwargs["input"] == source + "\n"


def test_profile_discovery_uses_capabilities() -> None:
    """Every producer owns exactly its declared canonical artifact
    family.
    """
    for language in ALL_LANGUAGES:
        path = Path(
            f"{language.__name__}_canonical_example@version{language.extension}"
        )
        assert (
            oracle.has_canonical_profile(path=path)
            == language.supports_canonical_source_format
        )
    assert not oracle.has_canonical_profile(path=Path("unowned.m"))


def test_golden_adapter_enables_raw_oracle(
    *,
    file_regression: FileRegressionFixture,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """The opt-in gate sees the original bytes before golden
    comparison.
    """
    language = next(
        language
        for language in ALL_LANGUAGES
        if language.supports_canonical_source_format
    )
    path = (
        tmp_path / f"{language.__name__}_canonical_oracle{language.extension}"
    )
    checked = Mock()
    compared = Mock()
    monkeypatch.setattr(
        target=golden_checks, name="check_source_format", value=checked
    )
    monkeypatch.setattr(target=file_regression, name="check", value=compared)
    monkeypatch.setattr(
        target=file_regression.request.config.option,
        name="check_source_format",
        value=True,
    )
    golden_checks.check_golden(
        contents="original source",
        extension=language.extension,
        golden_path=path,
        file_regression=file_regression,
    )
    checked.assert_called_once_with(contents="original source", path=path)
    assert compared.call_args.kwargs["contents"] == "original source"
