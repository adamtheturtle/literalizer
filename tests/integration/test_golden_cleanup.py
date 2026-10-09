"""Verification and explicit regeneration handle stale fixtures
differently.
"""

from pathlib import Path

import pytest

from .golden_checks import cleanup_stale_golden


@pytest.mark.parametrize(argnames="regenerate", argvalues=[False, True])
@pytest.mark.parametrize(argnames="exists", argvalues=[False, True])
def test_stale_golden_cleanup_modes(
    *, tmp_path: Path, regenerate: bool, exists: bool
) -> None:
    """Only explicit regeneration removes an unsupported golden."""
    config = pytest.Config.fromdictargs(
        option_dict={}, args=["--regen-all"] if regenerate else []
    )
    golden_path = tmp_path / "stale.txt"
    if exists:
        _ = golden_path.write_bytes(data=b"stale\r\n")
    if exists and not regenerate:
        with pytest.raises(
            expected_exception=pytest.fail.Exception,
            match=r"Stale golden file: .*stale\.txt.*--regen-all",
        ):
            cleanup_stale_golden(golden_path=golden_path, config=config)
        assert golden_path.read_bytes() == b"stale\r\n"
    else:
        cleanup_stale_golden(golden_path=golden_path, config=config)
        assert not golden_path.exists()
