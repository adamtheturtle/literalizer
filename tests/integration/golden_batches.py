"""Bound golden renderings into stable scheduling groups."""

import dataclasses

from beartype import beartype

import literalizer

from .golden_renderings import GoldenRendering

GOLDEN_BATCH_VERSION_LIMIT = 64


@dataclasses.dataclass(frozen=True, kw_only=True)
class GoldenGroup:
    """One bounded batch of a scenario's renderings for one language.

    Bounded groups give workers more scheduling opportunities while
    each rendering remains a sub-test at its original golden path.
    """

    scenario_name: str
    lang_cls: literalizer.LanguageCls
    renderings: tuple[GoldenRendering, ...]
    batch_index: int | None

    @property
    def test_id(self) -> str:
        """Return the pytest ID identifying this group."""
        prefix = f"{self.scenario_name}-{self.lang_cls.__name__}"
        if self.batch_index is None:
            return prefix
        return f"{prefix}-batch{self.batch_index:03d}"


@beartype
def batch_renderings(
    *, renderings: tuple[GoldenRendering, ...], max_versions: int
) -> tuple[tuple[GoldenRendering, ...], ...]:
    """Bound scheduling units without splitting a rendering's versions."""
    batches: list[tuple[GoldenRendering, ...]] = []
    current: list[GoldenRendering] = []
    versions = 0
    for rendering in renderings:
        cost = len(rendering.versions)
        if len(current) > 0 and versions + cost > max_versions:
            batches.append(tuple(current))
            current = []
            versions = 0
        current.append(rendering)
        versions += cost
    if len(current) > 0:
        batches.append(tuple(current))
    return tuple(batches)
