"""Rejection of tuple lengths Kotlin has no native tuple for under
the ``TUPLE`` strategy.

Kotlin only has ``Pair`` (two elements) and ``Triple`` (three
elements); a tuple-eligible heterogeneous scalar array of any other
length has no native fixed-size tuple, so the ``TUPLE`` strategy
raises
:class:`~literalizer.exceptions.TupleArityNotRepresentableError`
rather than degrading to a homogeneous list (which would re-trip the
heterogeneity checks the strategy exists to satisfy).  The
integration framework only exercises golden output that a language
can represent (it skips inputs that raise), so this contract has no
golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import TupleArityNotRepresentableError
from literalizer.languages import Kotlin

_ARITY_4_RECORD_FIELD = (
    "call: send\nargs:\n  - 1\n  - email\n  - a@gmail.com\n  - 100\n"
)
_ARITY_5_TOP_LEVEL = "- 1\n- email\n- a@gmail.com\n- 100\n- x\n"


@pytest.mark.parametrize(
    argnames=("source", "arity"),
    argvalues=[
        (_ARITY_4_RECORD_FIELD, 4),
        (_ARITY_5_TOP_LEVEL, 5),
    ],
)
def test_tuple_strategy_rejects_unrepresentable_arity(
    *,
    source: str,
    arity: int,
) -> None:
    """A tuple-eligible array whose length is outside ``{2, 3}`` raises
    rather than falling back to a homogeneous list.
    """
    language = Kotlin(
        heterogeneous_strategy=Kotlin.heterogeneous_strategies.TUPLE,
    )
    with pytest.raises(
        expected_exception=TupleArityNotRepresentableError,
    ) as exc_info:
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data"),
        )
    assert exc_info.value.arity == arity
