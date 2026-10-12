"""Expected warnings for fixtures that deliberately reuse YAML anchors."""

from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pytest
from beartype import beartype
from ruamel.yaml.error import ReusedAnchorWarning

_REBOUND_ANCHOR_CASES = frozenset(
    {
        "yaml_rebound_anchor_scalar",
        "yaml_rebound_anchor_collection",
        "yaml_rebound_anchor_nested",
    }
)


@contextmanager
@beartype
def expected_yaml_warnings(*, input_path: Path) -> Generator[None, None, None]:
    """Assert the deliberate duplicate-anchor warning for its owning cases.

    ``pytest.warns`` re-emits warnings that do not match, so unrelated
    warnings remain visible even while loading these three fixtures.
    """
    if input_path.parent.name in _REBOUND_ANCHOR_CASES:
        with pytest.warns(
            expected_warning=ReusedAnchorWarning,
            match="found duplicate anchor 'x'",
        ) as recorded:
            yield
        anchor_warnings = [
            warning
            for warning in recorded
            if isinstance(warning.message, ReusedAnchorWarning)
        ]
        if len(anchor_warnings) != 1:
            pytest.fail(reason="Expected one reused-anchor warning")
    else:
        yield
