"""Record callbacks enforce types without pytest import
instrumentation.
"""

import subprocess
import sys


def test_record_strategy_checks_normal_imports() -> None:
    """A fresh interpreter checks the constructor and each state
    callback.
    """
    result = subprocess.run(
        args=[
            sys.executable,
            "-c",
            """
import unittest
from beartype.roar import BeartypeCallHintParamViolation
from literalizer._formatters.record_strategy import _RecordStrategyState

checks = unittest.TestCase()
with checks.assertRaises(BeartypeCallHintParamViolation):
    _RecordStrategyState(
        renderer=object(),
        widen_unrecordizable_nested_sibling_maps=False,
        name_by_shape={}, id_to_shape={}, request_by_shape={},
        emit_order=[], preamble_by_value={},
    )
state = object.__new__(_RecordStrategyState)
for callback in (
    state.compute_shapes, state.field_type_request, state.preamble,
):
    with checks.assertRaises(BeartypeCallHintParamViolation):
        callback(object())
with checks.assertRaises(BeartypeCallHintParamViolation):
    state.render_literal(object(), {})
print("checked constructor and four callbacks")
""",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "checked constructor and four callbacks"
