"""Expected fixture warnings must not conceal warning regressions."""

import warnings
from pathlib import Path

import pytest
from ruamel.yaml.error import ReusedAnchorWarning

from .case_inputs import ReusedAnchorWarningSpec
from .case_manifests import case_input
from .yaml_warnings import expected_yaml_warnings


def _emit_fixture_warnings(
    *, cases_dir: Path, count: int, unrelated: bool
) -> None:
    """Emit controlled warnings through the fixture's warning boundary."""
    with expected_yaml_warnings(
        expectation=case_input(
            case_dir=cases_dir / "yaml_rebound_anchor_scalar",
        ).expected_reused_anchor_warning,
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
        match="Expected 1 reused-anchor warnings",
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


def test_warning_contract_follows_a_renamed_case(tmp_path: Path) -> None:
    """The manifest supplies the anchor and count without a directory
    registry.
    """
    case_dir = tmp_path / "renamed_case"
    case_dir.mkdir()
    _ = (case_dir / "input.yaml").write_text(
        data="value: 1\n", encoding="utf-8"
    )
    _ = (case_dir / "case.toml").write_text(
        data=(
            'schema_version = 1\nsuites = ["base"]\n'
            '[expected_reused_anchor_warning]\nanchor = "other+"\ncount = 2\n'
        ),
        encoding="utf-8",
    )
    with expected_yaml_warnings(
        expectation=case_input(
            case_dir=case_dir
        ).expected_reused_anchor_warning,
    ):
        for _ in range(2):
            warnings.warn(
                message=ReusedAnchorWarning("found duplicate anchor 'other+'"),
                stacklevel=2,
            )


def test_missing_declared_warning_fails() -> None:
    """Declaring a warning requires the parser to actually emit it."""
    with (
        pytest.raises(
            expected_exception=pytest.fail.Exception, match="DID NOT WARN"
        ),
        expected_yaml_warnings(
            expectation=ReusedAnchorWarningSpec(anchor="missing", count=1),
        ),
    ):
        pass
