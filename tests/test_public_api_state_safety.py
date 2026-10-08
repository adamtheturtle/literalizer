"""Public rendering boundaries remain safe under hostile shared state.

These use time-only keys, mutate caller-owned configuration, or render
from several threads at once, which a case file cannot declare
(issue #4699).
"""

import datetime
from concurrent.futures import ThreadPoolExecutor
from textwrap import dedent

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python, Rust


def test_time_key_in_public_substitution_uses_time_formatter() -> None:
    """Supplemental mappings preserve time-only scalar keys."""
    result = literalize(
        source='{"value": null}',
        input_format=InputFormat.JSON,
        language=Python(),
        record_null_substitutions={
            "value": {datetime.time(hour=1, minute=2, second=3): 1}
        },
    )

    assert result.bare_code == dedent(
        text="""\
        {
            "value": {datetime.time(hour=1, minute=2, second=3): 1},
        }"""
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


def test_record_language_instance_is_thread_safe() -> None:
    """Each public call gets independent RECORD inference state."""
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD
    )
    sources = (
        '{"a":1,"b":"x"}',
        '{"x":true,"y":[1,2]}',
        '{"q":1.5,"z":{"n":1,"s":"v"}}',
    )

    def render(index: int) -> str:
        """Render one document through the shared language instance."""
        return literalize(
            source=sources[index % len(sources)],
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="data", modifiers=frozenset()),
        ).code

    expected = tuple(render(index=index) for index in range(len(sources)))
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = list(pool.map(render, range(300)))

    assert all(
        result == expected[index % len(expected)]
        for index, result in enumerate(iterable=results)
    )


def test_record_shape_names_are_snapshotted() -> None:
    """Caller mutation cannot change an existing language instance."""
    names = {frozenset({"a", "b"}): "AlphaBeta"}
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
        record_shape_names=names,
    )
    source = '{"r":[{"a":1,"b":2}],"s":[{"d":3,"e":4}]}'

    def render() -> str:
        """Render through the existing language instance."""
        return literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(
                name="value",
                modifiers=frozenset(),
            ),
        ).code

    before_mutation = render()
    names[frozenset({"d", "e"})] = "DeltaEcho"

    assert render() == before_mutation


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
