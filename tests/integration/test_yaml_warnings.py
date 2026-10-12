"""Expected fixture warnings must not conceal warning regressions."""

import warnings
from pathlib import Path

import pytest
from ruamel.yaml.error import ReusedAnchorWarning

from .yaml_warnings import expected_yaml_warnings


def _emit_fixture_warnings(
    *, cases_dir: Path, count: int, unrelated: bool
) -> None:
    """Emit controlled warnings through the fixture's warning boundary."""
    with expected_yaml_warnings(
        input_path=cases_dir / "yaml_rebound_anchor_scalar" / "input.yaml",
    ):
        for _ in range(count):
            warnings.warn(
                message=ReusedAnchorWarning("found duplicate anchor 'x'"),
                stacklevel=2,
            )
        if unrelated:
            warnings.warn(message="unexpected warning", stacklevel=2)


def test_extra_anchor_warning_fails(cases_dir: Path) -> None:
    """A second rebound-anchor warning violates the fixture contract."""
    with pytest.raises(
        expected_exception=pytest.fail.Exception,
        match="Expected one reused-anchor warning",
    ):
        _emit_fixture_warnings(cases_dir=cases_dir, count=2, unrelated=False)


def test_unrelated_warning_is_reemitted(cases_dir: Path) -> None:
    """Capturing the deliberate warning leaves unrelated warnings
    visible.
    """
    with pytest.warns(
        expected_warning=UserWarning, match="unexpected warning"
    ):
        _emit_fixture_warnings(cases_dir=cases_dir, count=1, unrelated=True)
