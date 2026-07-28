"""Tests for eager Python annotations."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python


def test_eager_record_union_imports_union() -> None:
    """Record fields using ``typing.Union`` import it at runtime."""
    language = Python(
        annotation_evaluation=Python.annotation_evaluations.EAGER,
        heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
    )

    result = literalize(
        source='vals = [09:30:00, "hello"]\n',
        input_format=InputFormat.TOML,
        language=language,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "from typing import Union" in result.code
    assert "tuple[Union[datetime.time, str], ...]" in result.code
