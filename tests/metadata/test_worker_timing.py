"""Check Literalizer's JSON summary adapter, leaving capture tests
upstream.
"""

import json
from io import StringIO
from pathlib import Path

import pytest
from _pytest.terminal import TerminalReporter

from scripts.pytest_worker_timing import (
    completion_tail,
    pytest_terminal_summary,
)


def _summarize(
    *,
    path: Path,
    config: pytest.Config,
    monkeypatch: pytest.MonkeyPatch,
) -> str:
    """Run the adapter against a report and capture its terminal
    output.
    """
    monkeypatch.setattr(
        target=config.option,
        name="timing_json_file",
        value=str(object=path),
        raising=False,
    )
    stream = StringIO()
    pytest_terminal_summary(
        terminalreporter=TerminalReporter(config=config, file=stream),
        config=config,
    )
    return stream.getvalue()


def test_no_workers_have_zero_release_tail() -> None:
    """Keep the empty-input contract that serial capture does not call."""
    assert completion_tail(arrivals={}) == 0.0


def test_public_report_preserves_ci_summary(
    tmp_path: Path,
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Preserve the summary schema, worker errors, and aggregate release
    tail.
    """
    path = tmp_path / "timing.json"
    _ = path.write_text(
        data=json.dumps(
            obj={
                "run": {"workers_only": True, "dist": "worksteal"},
                "workers": [
                    {
                        "id": "gw0",
                        "collected": 1.0,
                        "down": 10.0,
                        "error": None,
                    },
                    {
                        "id": "gw1",
                        "collected": 1.0,
                        "down": 25.0,
                        "error": "crashed",
                    },
                    {
                        "id": "gw2",
                        "collected": 1.0,
                        "down": 30.0,
                        "error": None,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    output = _summarize(
        path=path, config=request.config, monkeypatch=monkeypatch
    )
    assert output.splitlines()[-1] == json.dumps(
        obj={
            "collection_finished_seconds": {
                "gw0": 1.0,
                "gw1": 1.0,
                "gw2": 1.0,
            },
            "worker_released_seconds": {"gw0": 10.0, "gw1": 25.0, "gw2": 30.0},
            "released_worker_tail_seconds": 25.0,
            "worker_errors": ["gw1"],
            "observation": "Arrivals include teardown and communication. "
            "the tail is not a measured recoverable speedup.",
        },
        sort_keys=True,
    )


@pytest.mark.parametrize(argnames="contents", argvalues=[None, "not JSON"])
def test_report_read_error_is_nonfatal(
    tmp_path: Path,
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
    contents: str | None,
) -> None:
    """Missing or malformed telemetry must not raise during pytest's
    summary.
    """
    path = tmp_path / "timing.json"
    if contents is not None:
        _ = path.write_text(data=contents, encoding="utf-8")
    output = _summarize(
        path=path, config=request.config, monkeypatch=monkeypatch
    )
    assert "worker timing summary unavailable:" in output
