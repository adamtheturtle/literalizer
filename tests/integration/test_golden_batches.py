"""Scheduling batches preserve the complete compiler-owned golden
corpus.
"""

from collections import Counter

from .golden_scenarios import (
    GOLDEN_BATCH_VERSION_LIMIT,
    GOLDEN_SCENARIOS,
    batch_renderings,
    golden_groups,
)
from .language_specs import sorted_languages


def test_golden_batches_preserve_every_rendering_in_order() -> None:
    """Batching neither drops nor duplicates scenarios or their
    versions.
    """
    groups = golden_groups()
    assert len({group.test_id for group in groups}) == len(groups)
    for scenario in GOLDEN_SCENARIOS:
        for lang_cls in sorted_languages():
            original = scenario.build(lang_cls=lang_cls)
            actual = tuple(
                rendering
                for group in groups
                if group.scenario_name == scenario.name
                and group.lang_cls is lang_cls
                for rendering in group.renderings
            )
            assert actual == original
    assert all(
        sum(len(rendering.versions) for rendering in group.renderings)
        <= GOLDEN_BATCH_VERSION_LIMIT
        for group in groups
    )


def test_golden_batches_preserve_single_and_empty_groups() -> None:
    """Small groups retain their IDs and empty inputs collect no items."""
    groups = golden_groups()
    counts = Counter((group.scenario_name, group.lang_cls) for group in groups)
    assert any(count == 1 for count in counts.values())
    assert any(count > 1 for count in counts.values())
    for group in groups:
        if counts[group.scenario_name, group.lang_cls] == 1:
            assert group.batch_index is None
            assert (
                group.test_id
                == f"{group.scenario_name}-{group.lang_cls.__name__}"
            )
        else:
            assert group.batch_index is not None
    assert len(batch_renderings(renderings=(), max_versions=64)) == 0
