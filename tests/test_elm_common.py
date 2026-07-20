"""Tests for shared Elm lint helpers."""

import subprocess
from unittest.mock import Mock

import pytest

from scripts import elm_common


def test_connection_timeout_is_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Retry an Elm package-download timeout."""
    results = iter(
        (
            subprocess.CompletedProcess[str](
                args=["elm", "make"],
                returncode=1,
                stdout="ConnectionTimeout",
                stderr="",
            ),
            subprocess.CompletedProcess[str](
                args=["elm", "make"],
                returncode=0,
                stdout="",
                stderr="",
            ),
        )
    )
    run = Mock(side_effect=results)
    sleep = Mock()

    monkeypatch.setattr(elm_common.subprocess, "run", run)
    monkeypatch.setattr(elm_common.time, "sleep", sleep)

    result = elm_common.run_elm_make(args=["elm", "make"], cwd=".", env={})

    assert result.returncode == 0
    expected_runs = 2
    assert run.call_count == expected_runs


def test_non_transient_elm_error_is_not_retried(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Preserve failures caused by invalid Elm source."""
    result = subprocess.CompletedProcess[str](
        args=["elm", "make"],
        returncode=1,
        stdout="SYNTAX PROBLEM",
        stderr="",
    )
    run = Mock(return_value=result)

    monkeypatch.setattr(elm_common.subprocess, "run", run)

    actual = elm_common.run_elm_make(args=["elm", "make"], cwd=".", env={})

    assert actual is result
    assert run.call_count == 1
