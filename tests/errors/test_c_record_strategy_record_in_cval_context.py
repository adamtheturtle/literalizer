"""Rejection of a record nested in a ``CVal`` context under the C
``RECORD`` strategy.

Under C's ``RECORD`` strategy a record-shaped dict renders as a
``(struct RecordN){...}`` literal and a list whose every element is one
as a ``struct RecordN[]`` array.  A ``struct`` is not a member of the
tagged ``CVal`` union, so either is representable only as a
record-field value, an element of such a field's struct array, or the
document root.  Reached only through a non-record container (a
non-all-record list, a non-record dict, an ordered map, or a set) it
would have to occupy a ``CVal`` slot, so ``literalize`` raises
:class:`~literalizer.exceptions.UnrepresentableInputError` rather than
emitting C that fails to compile.  The integration framework only
exercises golden output that compiles, so this contract has no
golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import C

# A record-shaped dict reached as an ordered-map value: the ordered map
# renders as a tagged-union key/value map, so its value cannot be a
# ``struct``.
_RECORD_IN_ORDERED_MAP_YAML = "--- !!omap\n- rec:\n    a: 1\n"

# A record-field value that is a list of lists of record-shaped dicts:
# the outer list is not all-record (its elements are lists), so it is a
# ``CVal`` array and the inner all-record list cannot be a ``struct``
# array there.
_RECORD_LIST_NESTED_IN_LIST_YAML = "field:\n- - a: 1\n"

# A top-level list whose single element is a list of record-shaped
# dicts: the root list is not all-record, so the inner all-record list
# is reached in a ``CVal`` context.
_RECORD_LIST_NESTED_AT_ROOT_YAML = "- - a: 1\n"


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        _RECORD_IN_ORDERED_MAP_YAML,
        _RECORD_LIST_NESTED_IN_LIST_YAML,
        _RECORD_LIST_NESTED_AT_ROOT_YAML,
    ],
)
def test_c_record_strategy_rejects_record_in_cval_context(
    source: str,
) -> None:
    """A record reachable only through a non-record container raises
    rather than emitting C that fails to compile.
    """
    language = C(heterogeneous_strategy=C.heterogeneous_strategies.RECORD)
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data"),
        )
