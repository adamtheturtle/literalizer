"""Rejection of same-shape records with a differing-length all-record
list field under the C ``RECORD`` strategy.

Under C's ``RECORD`` strategy a record field whose value is a list of
one-shape record dicts becomes a fixed-size ``struct RecordN [len]``
member, sized from the shape's first-seen instance.  A later record of
the same shape whose list has a different length would overflow that
fixed array (excess initializers fail to compile) or silently
under-fill it, so neither faithfully represents the input.
``literalize`` raises
:class:`~literalizer.exceptions.UnrepresentableInputError` rather than
emitting C that fails to compile or misrepresents the data.  The
integration framework only exercises golden output that compiles, so
this contract has no golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import C

# A record field that is a list of same-shape record dicts whose own
# all-record-list field (``sub``) has length 1 in the first instance
# and length 2 in the second: the generated ``struct`` array member is
# sized from the first instance, so the second overflows it.
_RECORD_FIELD_LIST_LENGTH_MISMATCH_YAML = (
    "items:\n- sub:\n  - x: 1\n- sub:\n  - x: 2\n  - x: 3\n"
)

# A top-level all-record list whose two same-shape elements carry an
# all-record-list field (``group``) of differing length: the shape's
# fixed-size ``struct`` array member is sized from the first element.
_RECORD_ROOT_LIST_LENGTH_MISMATCH_YAML = (
    "- group:\n  - x: 1\n- group:\n  - x: 1\n  - x: 2\n"
)


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        _RECORD_FIELD_LIST_LENGTH_MISMATCH_YAML,
        _RECORD_ROOT_LIST_LENGTH_MISMATCH_YAML,
    ],
)
def test_c_record_strategy_rejects_array_field_length_mismatch(
    source: str,
) -> None:
    """Same-shape records whose shared all-record-list field has
    differing lengths raise rather than emitting C that fails to
    compile or misrepresents the data.
    """
    language = C(heterogeneous_strategy=C.heterogeneous_strategies.RECORD)
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
