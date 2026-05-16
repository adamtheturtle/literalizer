"""Rejection of non-finite floats for languages with no literal form
for them.

Gleam targets Erlang, which has no expression that evaluates to a
non-finite float, so ``literalize`` raises
:class:`~literalizer.exceptions.UnrepresentableSpecialFloatError` rather
than emitting output that panics at ``gleam run``.  The integration
framework only exercises golden output that runs, so this contract has
no golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableSpecialFloatError
from literalizer.languages import Gleam


@pytest.mark.parametrize(
    argnames="yaml_value",
    argvalues=[".inf", "-.inf", ".nan"],
    ids=["positive_infinity", "negative_infinity", "nan"],
)
def test_gleam_special_floats_raise(yaml_value: str) -> None:
    """Gleam raises ``UnrepresentableSpecialFloatError`` for non-finite
    floats.

    Gleam targets Erlang, which has no expression that evaluates to a
    non-finite float, so the literalizer surfaces this at literalize
    time rather than producing output that panics at ``gleam run``.
    """
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        literalize(
            source=f"- {yaml_value}\n",
            input_format=InputFormat.YAML,
            language=Gleam(),
        )
