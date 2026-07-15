"""Rejection of set-valued fields under the Rust ``RECORD`` strategy.

A set-valued record field has no struct field type that agrees with the
set literal rendered for the value, so the ``RECORD`` heterogeneous
strategy cannot emit a struct for it that compiles.  ``literalize``
therefore raises
:class:`~literalizer.exceptions.UnrepresentableInputError` rather than
producing a struct that fails to compile.  The integration framework
only exercises golden output that compiles, so this contract has no
golden-file surface and needs unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Rust

_SET_FIELD_YAML = "title: report\ntags: !!set\n  ? apple\n  ? banana\n"


def test_record_strategy_rejects_set_valued_field() -> None:
    """A set-valued field under ``RECORD`` raises rather than emitting
    a struct that fails to compile.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=_SET_FIELD_YAML,
            input_format=InputFormat.YAML,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
