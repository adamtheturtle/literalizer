"""Rejection of tuple lengths Scala has no native tuple for under
the ``TUPLE`` strategy.

Scala's tuple sugar ``(a, b, ...)`` expands to ``TupleN``, which the
standard library defines only as ``Tuple2`` through ``Tuple22``; a
tuple-eligible heterogeneous scalar array longer than 22 elements has
no native fixed-size tuple, so the ``TUPLE`` strategy raises
:class:`~literalizer.exceptions.TupleArityNotRepresentableError`
rather than degrading to a homogeneous list (which would re-trip the
heterogeneity checks the strategy exists to satisfy).  The
integration framework only exercises golden output that a language
can represent (it skips inputs that raise), so this contract has no
golden-file surface and needs unit coverage.
"""

import json

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import TupleArityNotRepresentableError
from literalizer.languages import Scala

# Scala ships ``Tuple2`` .. ``Tuple22``; an array one element longer
# is the smallest case with no native fixed-size tuple.
_OVERSIZED_ARITY = 23


def _mixed_scalar_array(length: int) -> list[object]:
    """Return a *length*-element array spanning two scalar buckets.

    Alternating ``int`` and ``str`` keeps every element a scalar while
    spanning more than one bucket, so the array is tuple-eligible.
    """
    return [index if index % 2 else f"s{index}" for index in range(length)]


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        json.dumps(obj={"args": _mixed_scalar_array(length=_OVERSIZED_ARITY)}),
        json.dumps(obj=_mixed_scalar_array(length=_OVERSIZED_ARITY)),
    ],
    ids=["record_field", "document_root"],
)
def test_tuple_strategy_rejects_unrepresentable_arity(*, source: str) -> None:
    """A tuple-eligible array longer than ``Tuple22`` raises rather
    than falling back to a homogeneous list, whether it is a record
    field or the bare document root.
    """
    language = Scala(
        heterogeneous_strategy=Scala.heterogeneous_strategies.TUPLE,
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
