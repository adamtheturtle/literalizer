"""Check the Java native runner's fixture coverage contract."""

from pathlib import Path

import click
import pytest

from scripts.run_java_fixtures import verify_coverage

_FIRST = Path("Java@jdk_11.java")
_SECOND = Path("default_module_name.java")
_COMPLETE = tuple(
    f"11\t{stage}\t{fixture}"
    for fixture in (_FIRST, _SECOND)
    for stage in ("compile", "execute")
)


def test_complete_coverage() -> None:
    """Accept both observed stages for each expected fixture."""
    verify_coverage(
        release="11", fixtures=(_FIRST, _SECOND), records=_COMPLETE
    )


@pytest.mark.parametrize(
    argnames=("records", "message"),
    argvalues=[
        pytest.param(_COMPLETE[:2], r"Missing \(2\)", id="omitted-fixture"),
        pytest.param(
            tuple(record.replace("11\t", "16\t") for record in _COMPLETE),
            r"unexpected \(4\)",
            id="wrong-release",
        ),
        pytest.param(_COMPLETE[:-1], r"Missing \(1\)", id="omitted-stage"),
        pytest.param(
            (*_COMPLETE, _COMPLETE[0]), "Duplicate", id="duplicate-stage"
        ),
    ],
)
def test_coverage_mismatch(records: tuple[str, ...], message: str) -> None:
    """Reject missing, incorrect and repeated observations."""
    with pytest.raises(expected_exception=click.ClickException, match=message):
        verify_coverage(
            release="11", fixtures=(_FIRST, _SECOND), records=records
        )


def test_reject_empty_inventory() -> None:
    """A scope with no fixture coverage cannot pass."""
    with pytest.raises(
        expected_exception=click.ClickException, match="No Java 11 fixtures"
    ):
        verify_coverage(release="11", fixtures=(), records=())
