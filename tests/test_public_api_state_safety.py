"""Public rendering boundaries remain safe under hostile shared state.

These build a cyclic Python value, or render from several threads at
once, neither of which a case file can declare (issue #4699).
"""

import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import InvalidValueInputError
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

    assert "datetime.time(hour=1, minute=2, second=3): 1" in result.bare_code


def test_cyclic_supplemental_values_raise_typed_error() -> None:
    """Cyclic Python-value arguments never leak ``RecursionError``."""
    cycle: list[object] = []
    cycle.append(cycle)
    cyclic_value: Any = cycle

    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match="ref_values",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            ref_values={"value": cyclic_value},
        )
    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match="bound_refs",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            bound_refs={"value": cyclic_value},
        )
    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match="record_null_substitutions",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            record_null_substitutions={"value": cyclic_value},
        )


def test_deep_supplemental_value_raises_typed_error() -> None:
    """Deep cycle-free Python values avoid leaking recursion errors."""
    value: object = 0
    for _ in range(2_000):
        value = [value]
    deeply_nested_value: Any = value

    with pytest.raises(
        expected_exception=InvalidValueInputError,
        match=(
            "ref_values must contain an acyclic value within the supported "
            "nesting depth"
        ),
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            ref_values={"value": deeply_nested_value},
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
