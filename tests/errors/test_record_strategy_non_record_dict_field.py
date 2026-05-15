"""Rejection of non-record dict fields under the Rust ``RECORD``
strategy.

A record field whose value is a dict that is not record-eligible
(here, empty) is rendered as a ``HashMap`` literal but has no matching
struct field type, so the ``RECORD`` heterogeneous strategy cannot emit
a struct for it that compiles.  ``literalize`` therefore raises
:class:`~literalizer.exceptions.UnrepresentableInputError` rather than
producing a struct that fails to compile.  The integration framework
only exercises golden output that compiles, so this contract has no
golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Rust

_EMPTY_DICT_FIELD_JSON = '{"title": "report", "extra": {}}'


def test_record_strategy_rejects_non_record_dict_field() -> None:
    """A non-record dict field under ``RECORD`` raises rather than
    emitting a struct that fails to compile.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=_EMPTY_DICT_FIELD_JSON,
            input_format=InputFormat.JSON,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data"),
        )
