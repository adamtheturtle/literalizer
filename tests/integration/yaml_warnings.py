"""Expected warnings for fixtures that deliberately reuse YAML anchors."""

import warnings
from collections.abc import Generator
from contextlib import contextmanager

from beartype import beartype
from ruamel.yaml.error import ReusedAnchorWarning

from .case_inputs import ReusedAnchorWarningSpec


@contextmanager
@beartype
def expected_yaml_warnings(
    *, expectation: ReusedAnchorWarningSpec | None
) -> Generator[None]:
    """Check the declared anchor and count, re-emitting unrelated warnings."""
    if expectation is None:
        yield
        return

    with warnings.catch_warnings(record=True) as recorded:
        warnings.simplefilter(action="always")
        yield

    expected_text = f"found duplicate anchor {expectation.anchor!r}"
    reused_count = 0
    matched = False
    for warning in recorded:
        if isinstance(warning.message, ReusedAnchorWarning):
            reused_count += 1
            if expected_text in str(object=warning.message):
                matched = True
                continue
        warnings.warn_explicit(
            message=warning.message,
            category=warning.category,
            filename=warning.filename,
            lineno=warning.lineno,
            source=warning.source,
        )

    if not matched or reused_count != expectation.count:
        msg = (
            f"Expected {expectation.count} reused-anchor warnings "
            f"for {expectation.anchor!r}, got {reused_count}"
        )
        raise AssertionError(msg)
