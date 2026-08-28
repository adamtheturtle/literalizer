"""Tests for YAML aliases whose anchor name was bound more than once.

An alias takes the most recent binding of its name, so a name rebound
further in does not make the alias a self-reference even while the node
that first claimed the name is still open.  These documents cannot live
in the golden corpus: the safe loader the case harness parses inputs
with refuses a duplicate anchor outright, while the round-trip loader
the library uses warns and resolves it.
"""

import warnings

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("source", "expected"),
    argvalues=[
        pytest.param(
            "a: &x [1, &x 2, *x]",
            'v = {\n    "a": (1, 2, 2),\n}',
            id="rebound-to-scalar",
        ),
        pytest.param(
            "a: &x [1, &x [2], *x]",
            'v = {\n    "a": (1, (2,), (2,)),\n}',
            id="rebound-to-collection",
        ),
        pytest.param(
            "a: &x [1, [&x 2], *x]",
            'v = {\n    "a": (1, (2,), 2),\n}',
            id="rebound-inside-nested-collection",
        ),
    ],
)
def test_rebound_anchor_is_not_a_cycle(source: str, expected: str) -> None:
    """An alias taking a newer binding is not a self-reference."""
    with warnings.catch_warnings():
        warnings.simplefilter(action="ignore")
        result = literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=Python(),
            variable_form=NewVariable(name="v", modifiers=frozenset()),
        )
    assert result.code == expected
