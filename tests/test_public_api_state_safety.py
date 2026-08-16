"""Public rendering boundaries remain safe under hostile shared state."""

from concurrent.futures import ThreadPoolExecutor
from typing import Any

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    BoundRefOutputCollisionError,
    InvalidValueInputError,
)
from literalizer.languages import JavaScript, Python, Rust


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
        match="ref_values",
    ):
        literalize(
            source="1",
            input_format=InputFormat.JSON,
            language=Python(),
            ref_values={"value": deeply_nested_value},
        )


def test_bound_ref_cannot_redeclare_output_variable() -> None:
    """Bound refs and the final output share one declaration name-
    space.
    """
    with pytest.raises(
        expected_exception=BoundRefOutputCollisionError,
        match="'data'",
    ):
        literalize(
            source='{"$ref":"data"}',
            input_format=InputFormat.JSON,
            language=JavaScript(),
            variable_form=NewVariable(name="data", modifiers=frozenset()),
            wrap_in_file=True,
            bound_refs={"data": 1},
            ref_key="$ref",
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
