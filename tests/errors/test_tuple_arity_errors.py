"""Rejection of over-long arrays under the Scala ``TUPLE`` strategy.

Scala's tuple sugar ``(a, b, ...)`` expands to ``TupleN``, which the
standard library defines only up to ``Tuple22``.  A tuple-eligible
heterogeneous scalar array longer than 22 elements therefore has no
native tuple type, so the ``TUPLE`` heterogeneous strategy raises
:class:`~literalizer.exceptions.TupleArityNotRepresentableError` at
check time rather than silently downgrading to a homogeneous
collection (which would discard the per-element types) or emitting
code that does not compile.  The integration framework only exercises
golden output that compiles, so this contract has no golden-file
surface and needs unit coverage.
"""

import json

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import TupleArityNotRepresentableError
from literalizer.languages import Scala

# Scala's tuple sugar tops out at ``Tuple22``; an array one element
# longer is the smallest case with no native tuple representation.
_SCALA_TUPLE_ARITY_LIMIT = 22
_OVERSIZED_ARITY = _SCALA_TUPLE_ARITY_LIMIT + 1


def _mixed_scalar_array(length: int) -> list[object]:
    """Return a *length*-element array spanning two scalar buckets.

    Alternating ``int`` and ``str`` keeps every element a scalar while
    spanning more than one bucket, so the array is tuple-eligible.
    """
    return [index if index % 2 else f"s{index}" for index in range(length)]


def test_tuple_strategy_rejects_arity_over_22() -> None:
    """A 23-element heterogeneous array raises the explicit
    not-representable error rather than silently downgrading.
    """
    language = Scala(
        heterogeneous_strategy=Scala.heterogeneous_strategies.TUPLE,
    )
    source = json.dumps(
        obj={"args": _mixed_scalar_array(length=_OVERSIZED_ARITY)},
    )
    with pytest.raises(
        expected_exception=TupleArityNotRepresentableError,
    ) as exc_info:
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data"),
        )
    assert exc_info.value.arity == _OVERSIZED_ARITY
    assert exc_info.value.limit == _SCALA_TUPLE_ARITY_LIMIT


def test_tuple_strategy_rejects_arity_over_22_at_document_root() -> None:
    """The length limit also covers a bare top-level tuple-eligible
    array, not only a record field.
    """
    language = Scala(
        heterogeneous_strategy=Scala.heterogeneous_strategies.TUPLE,
    )
    source = json.dumps(obj=_mixed_scalar_array(length=_OVERSIZED_ARITY))
    with pytest.raises(
        expected_exception=TupleArityNotRepresentableError,
    ) as exc_info:
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data"),
        )
    assert exc_info.value.arity == _OVERSIZED_ARITY
    assert exc_info.value.limit == _SCALA_TUPLE_ARITY_LIMIT
