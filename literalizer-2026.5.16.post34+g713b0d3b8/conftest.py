"""Configuration for pytest."""

from pathlib import Path

import pytest


@pytest.fixture(scope="session", name="lazy_datadir")
def fixture_lazy_datadir(
    tmp_path_factory: pytest.TempPathFactory,
) -> Path:
    """Override pytest-regressions' ``lazy_datadir`` with a shared path.

    All ``file_regression.check()`` calls in this repo pass ``fullpath=``,
    so ``lazy_datadir`` is only used to compute the ``.obtained`` file
    location on failure. Returning a single session-scoped path breaks
    the per-test ``tmp_path`` dependency, which otherwise dominates
    runtime via pytest's O(N^2) ``make_numbered_dir``/``find_prefixed``
    scan.
    """
    return tmp_path_factory.mktemp(
        basename="file_regression_obtained",
        numbered=False,
    )
