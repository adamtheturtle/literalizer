"""Expected warnings for fixtures that deliberately reuse YAML anchors."""

import re
from collections.abc import Generator
from contextlib import contextmanager

import pytest
from beartype import beartype
from ruamel.yaml.error import ReusedAnchorWarning

from .case_inputs import ReusedAnchorWarningSpec


@contextmanager
@beartype
def expected_yaml_warnings(
    *, expectation: ReusedAnchorWarningSpec | None
) -> Generator[None]:
    """Assert the duplicate-anchor warning declared by a fixture's
    manifest.

    ``pytest.warns`` re-emits warnings that do not match, so unrelated
    warnings remain visible while loading a fixture with an expectation.
    """
    if expectation is not None:
        with pytest.warns(
            expected_warning=ReusedAnchorWarning,
            match=re.escape(
                pattern=f"found duplicate anchor {expectation.anchor!r}",
            ),
        ) as recorded:
            yield
        anchor_warnings = [
            warning
            for warning in recorded
            if isinstance(warning.message, ReusedAnchorWarning)
        ]
        if len(anchor_warnings) != expectation.count:
            pytest.fail(
                reason=(
                    f"Expected {expectation.count} reused-anchor warnings "
                    f"for {expectation.anchor!r}, got {len(anchor_warnings)}"
                ),
            )
    else:
        yield
