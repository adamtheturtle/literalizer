"""``literalize_call`` cross-call divergence tests for Mojo VARIANT.

Covers branches in the Mojo cross-call VARIANT machinery that the
golden-file fixtures in :mod:`tests.integration.cases` do not naturally
exercise: a multi-parameter call where only one slot diverges, and a
single-parameter call whose slot contains an unmappable scalar.
"""

from literalizer import InputFormat, literalize_call
from literalizer.languages import Mojo

_VARIANT_STRATEGY = next(
    strategy
    for strategy in Mojo.heterogeneous_strategies
    if strategy.name == "VARIANT"
)


def test_mojo_variant_multi_arg_only_divergent_slot_wraps() -> None:
    """A multi-arg Mojo VARIANT call wraps only divergent slots.

    Slot 0 holds ``String, Int, Bool`` across sibling calls (divergent
    scalars) so each value renders inside ``Value(...)`` and the slot
    is typed ``Value``.  Slot 1 holds ``String, String, String`` so its
    values render unwrapped and the slot is typed ``String``.  This
    exercises the homogeneous-slot short-circuit inside
    ``_mojo_cross_call_scalar_wrap_ids``.
    """
    source = "---\n- - hello\n  - a\n- - 42\n  - b\n- - true\n  - c\n"
    result = literalize_call(
        source=source,
        input_format=InputFormat.YAML,
        language=Mojo(heterogeneous_strategy=_VARIANT_STRATEGY),
        target_function="process",
        parameter_names=["divergent", "uniform"],
        per_element=True,
        wrap_in_file=True,
    )
    assert "def process(divergent: Value, uniform: String):" in result.code
    assert 'process(Value(String("hello")), "a")' in result.code
    assert 'process(Value(42), "b")' in result.code
    assert 'process(Value(True), "c")' in result.code


def test_mojo_variant_call_slot_with_unmappable_scalar_falls_back() -> None:
    """A Mojo VARIANT call slot containing ``None`` falls back to the
    generic stub.

    ``None`` is not in Mojo's call-arg scalar type mapping, so
    ``_value_to_mojo_type`` returns ``None`` for it.  The typed-param
    helper detects the unresolved slot type and bails to the generic
    ``[*Ts: AnyType]`` signature instead of emitting ``Variant[...]``.
    """
    source = "---\n- null\n- hello\n"
    result = literalize_call(
        source=source,
        input_format=InputFormat.YAML,
        language=Mojo(heterogeneous_strategy=_VARIANT_STRATEGY),
        target_function="process",
        parameter_names=["value"],
        per_element=True,
        wrap_in_file=True,
    )
    assert "def process[*Ts: AnyType](*args: *Ts):" in result.code
