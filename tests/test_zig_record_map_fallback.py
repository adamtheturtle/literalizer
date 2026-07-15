"""Regression coverage for Zig record-map fallback values."""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Zig


def test_zig_record_map_fallback_wraps_null_as_zval_nil() -> None:
    """A widened map stores a null scalar in the ``ZVal.nil`` variant."""
    result = literalize(
        source="""\
- input:
    kind: add
    missing: null
  expected:
    done: true
- input:
    kind: remove
  expected:
    error: absent
""",
        input_format=InputFormat.YAML,
        language=Zig(
            heterogeneous_strategy=Zig.heterogeneous_strategies.RECORD,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert '.{ .key = "missing", .val = .nil }' in result.code
