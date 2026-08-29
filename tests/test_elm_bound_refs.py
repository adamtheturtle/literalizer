"""Elm rendering for values supplied through reference bindings.

The golden harness reads a case's bound-reference values with
``json.loads``, and JSON has no time, so the value here cannot be
declared in a case file (issue #4699).
"""

import datetime

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Elm


def test_bare_time_bound_ref_uses_string_constructor() -> None:
    """A bare time still gives the generated Elm value type a
    constructor.
    """
    result = literalize(
        source='{"x": {"$ref": "value"}}',
        input_format=InputFormat.JSON,
        language=Elm(),
        ref_key="$ref",
        bound_refs={"value": datetime.time(hour=1, minute=2, second=3)},
        variable_form=NewVariable(name="out", modifiers=frozenset()),
        wrap_in_file=True,
    )

    assert "type Val\n    = EStr String" in result.code
    assert 'value = EStr "01:02:03"' in result.code
