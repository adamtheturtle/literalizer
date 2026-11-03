"""Golden planning and scheduling preserve every declared contract."""

import dataclasses
from collections import Counter
from typing import Literal, assert_never

import pytest

import literalizer
from literalizer.languages import Cpp, Erlang, Python, Zig
from tests.integration.custom_languages import SkipNullZig
from tests.integration.golden_checks import NO_SKIPS
from tests.integration.golden_scenarios import (
    GOLDEN_BATCH_VERSION_LIMIT,
    GOLDEN_SCENARIOS,
    batch_renderings,
    golden_groups,
    golden_plan,
    overridden_spec_source,
    pinned_spec_source,
    plan_renderings,
)
from tests.integration.language_specs import make_spec, sorted_languages


def test_golden_batches_preserve_every_rendering_in_order() -> None:
    """Batching neither drops nor duplicates scenarios or their
    versions.
    """
    groups = golden_groups()
    assert len({group.test_id for group in groups}) == len(groups)
    for scenario in GOLDEN_SCENARIOS:
        for lang_cls in sorted_languages():
            plan = golden_plan(scenario=scenario, lang_cls=lang_cls)
            actual = tuple(
                rendering
                for group in groups
                if group.scenario_name == scenario.name
                and group.lang_cls is lang_cls
                for rendering in group.renderings
            )
            assert actual == plan.renderings
            original = scenario.build(lang_cls=lang_cls)
            assert Counter(
                original_name.golden_name for original_name in original
            ) == Counter(
                rendering.golden_name for rendering in plan.renderings
            ) + Counter(alias.original.golden_name for alias in plan.aliases)
            assert all(
                alias.witness in plan.renderings for alias in plan.aliases
            )
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


def test_equivalent_default_requests_retain_both_option_labels() -> None:
    """Explicit and omitted defaults share a witness without losing a
    label.
    """
    scenario = GOLDEN_SCENARIOS[0]
    original = scenario.build(lang_cls=Python)[0]
    explicit = dataclasses.replace(
        original,
        golden_name="explicit_default",
        spec_source=overridden_spec_source(overrides={"indent": "    "}),
    )
    plan = plan_renderings(renderings=(original, explicit))
    assert plan.renderings == (original,)
    assert len(plan.aliases) == 1
    assert plan.aliases[0].original == explicit
    assert plan.aliases[0].witness == original


@pytest.mark.parametrize(
    argnames="difference",
    argvalues=[
        "skip",
        "layout",
        "preamble",
        "initialize",
        "module_policy",
        "input",
    ],
)
def test_different_rendering_contracts_keep_independent_requests(
    difference: Literal[
        "skip", "layout", "preamble", "initialize", "module_policy", "input"
    ],
) -> None:
    """Similar output cannot erase caller context or failure
    expectations.
    """
    original = GOLDEN_SCENARIOS[0].build(lang_cls=Python)[0]
    distinct = dataclasses.replace(original, golden_name="distinct_contract")
    match difference:
        case "skip":
            distinct = dataclasses.replace(distinct, skip=NO_SKIPS)
        case "layout":
            distinct = dataclasses.replace(
                distinct,
                render=dataclasses.replace(
                    distinct.render,
                    collection_layout=literalizer.CollectionLayout.MULTILINE,
                ),
            )
        case "preamble":
            distinct = dataclasses.replace(
                distinct, extra_preamble=("# context",)
            )
        case "initialize":
            distinct = dataclasses.replace(distinct, initialize_variable=True)
        case "module_policy":
            distinct = dataclasses.replace(
                distinct, apply_fixture_module_name=False
            )
        case "input":
            distinct = dataclasses.replace(
                distinct, case_dir_name="other_input"
            )
        case _ as unreachable:
            assert_never(unreachable)
    plan = plan_renderings(renderings=(original, distinct))
    assert plan.renderings == (original, distinct)
    assert len(plan.aliases) == 0


def test_module_names_and_versions_keep_independent_requests() -> None:
    """Equal source inputs retain actual modules and compiler versions."""
    for lang_cls in (Erlang, Cpp):
        original = GOLDEN_SCENARIOS[0].build(lang_cls=lang_cls)[0]
        distinct = dataclasses.replace(
            original,
            golden_name="distinct_contract",
            spec_source=pinned_spec_source(
                spec=make_spec(
                    lang_cls=lang_cls,
                    language_version=next(iter(lang_cls.VersionFormats)),
                )
            ),
        )
        plan = plan_renderings(renderings=(original, distinct))
        assert plan.renderings == (original, distinct)
        assert len(plan.aliases) == 0


def test_custom_spec_implementations_keep_independent_requests() -> None:
    """Equal constructor values do not erase an overridden public hook."""
    original = next(
        rendering
        for rendering in GOLDEN_SCENARIOS[0].build(lang_cls=Zig)
        if rendering.case_dir_name == "null_field_policy"
    )
    custom = dataclasses.replace(
        original,
        golden_name="custom_null_policy",
        spec_source=pinned_spec_source(spec=make_spec(lang_cls=SkipNullZig)),
    )
    plan = plan_renderings(renderings=(original, custom))
    assert plan.renderings == (original, custom)
    assert len(plan.aliases) == 0
