"""Rejection of heterogeneous lists nested in a record under ``RECORD``.

The Rust ``RECORD`` strategy's carve-out only covers record-shaped
dicts; a heterogeneous list nested inside a record still fails the
standard heterogeneous-list check because ``vec![]`` cannot represent
mixed scalar types.  The integration framework treats
:class:`~literalizer.exceptions.HeterogeneousCollectionError` as a skip,
so this contract has no golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import HeterogeneousCollectionError
from literalizer.languages import Rust

_HETEROGENEOUS_LIST_YAML = 'items:\n  - 1\n  - "two"\n'


def test_record_strategy_rejects_heterogeneous_list_field() -> None:
    """A heterogeneous list under ``RECORD`` raises rather than
    emitting a ``vec![]`` that fails to compile.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=HeterogeneousCollectionError):
        literalize(
            source=_HETEROGENEOUS_LIST_YAML,
            input_format=InputFormat.YAML,
            language=language,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
            wrap_in_file=True,
        )
