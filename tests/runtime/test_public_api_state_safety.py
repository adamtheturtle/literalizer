"""Public rendering boundaries remain safe under hostile shared state.

These mutate caller-owned configuration or render from several threads
at once, which a case file cannot declare
(issue #4699).
"""

import dataclasses
from concurrent.futures import ThreadPoolExecutor

import pytest

from literalizer import InputFormat, LanguageCls, literalize
from literalizer.languages import C, Python, Rust
from tests.integration.golden_scenarios import golden_groups
from tests.integration.state_goldens import (
    StateGolden,
    read_state_golden,
    render_state_golden,
)


def test_yaml_parsing_is_thread_safe() -> None:
    """Concurrent comment-preserving parses do not share parser state."""
    render_count = 200

    def render(index: int) -> str:
        """Render one YAML document."""
        return literalize(
            source=f"value: {index}\n# comment {index}\n",
            input_format=InputFormat.YAML,
            language=Python(),
        ).code

    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(render, range(render_count)))

    assert len(results) == render_count


@pytest.mark.parametrize(
    argnames=("language_cls", "golden_name", "case_names"),
    argvalues=[
        (
            Rust,
            "Rust_heterogeneous_strategy_record",
            (
                "record_pure_scalars",
                "record_nested_record",
                "record_nested_container",
            ),
        ),
        (
            C,
            "C_json_type_cjson",
            (
                "json_helper_name_arena",
                "sibling_list_values_same_shape",
                "rectangular_map_sequence_shapes",
            ),
        ),
    ],
    ids=["rust-record", "c-cjson"],
)
def test_language_instance_is_thread_safe(
    language_cls: LanguageCls,
    golden_name: str,
    case_names: tuple[str, ...],
) -> None:
    """Compare 300 calls on sixteen threads with native golden programs.

    Reuse one language instance across scalar, sequence and nested
    mapping documents. Expected output comes from checked-in fixtures,
    independently of the cached state exercised by these calls (#4699).
    """
    renderings = [
        rendering
        for group in golden_groups()
        if group.scenario_name == "format_variant"
        and group.lang_cls is language_cls
        for rendering in group.renderings
        if rendering.golden_name == golden_name
        and rendering.case_dir_name in case_names
    ]
    assert {rendering.case_dir_name for rendering in renderings} == set(
        case_names
    )
    cases: list[StateGolden] = []
    for version in renderings[0].versions:
        shared_language = dataclasses.replace(
            renderings[0].spec_for(version=version)
        )
        cases.extend(
            read_state_golden(
                rendering=rendering,
                language=shared_language,
            )
            for rendering in renderings
        )

    def render(index: int) -> None:
        """Render one document through the shared language instance."""
        case = cases[index % len(cases)]
        assert render_state_golden(case=case) == case.expected, (
            case.rendering.case_dir_name
        )

    with ThreadPoolExecutor(max_workers=16) as pool:
        _ = tuple(pool.map(render, range(300)))


def test_record_shape_names_are_snapshotted() -> None:
    """Caller mutation cannot change either nested or parent record
    names.
    """
    rendering = next(
        rendering
        for group in golden_groups()
        if group.scenario_name == "format_variant" and group.lang_cls is Rust
        for rendering in group.renderings
        if rendering.case_dir_name == "record_named_nested_record"
        and rendering.golden_name == "Rust_record_shape_names_NamedType"
    )
    for version in rendering.versions:
        spec = rendering.spec_for(version=version)
        rust_spec = spec
        assert isinstance(rust_spec, Rust)
        caller_names = dict(rust_spec.record_shape_names)
        language = dataclasses.replace(spec, record_shape_names=caller_names)
        case = read_state_golden(rendering=rendering, language=language)
        assert render_state_golden(case=case) == case.expected

        caller_names[frozenset({"collection", "featured_entry"})] = "Parent"
        caller_names[next(iter(caller_names))] = "Replacement"
        assert render_state_golden(case=case) == case.expected


def test_unrelated_reference_values_are_not_mutated() -> None:
    """Rendering a set leaves unused caller-owned bindings unchanged."""
    ref_values = {"unused": [3]}
    _ = literalize(
        source="!!set\n1:\n2:\n",
        input_format=InputFormat.YAML,
        language=Python(),
        ref_key="$ref",
        ref_values=ref_values,
    )

    assert ref_values == {"unused": [3]}
