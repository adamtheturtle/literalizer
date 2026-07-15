"""Rejection of non-record dict fields under the Rust ``RECORD``
strategy.

A record field whose value is a dict that is not record-eligible
(empty, or an ordered map) is rendered as a map literal but has no
matching struct field type, so the ``RECORD`` heterogeneous strategy
cannot emit a struct for it that compiles.  ``literalize`` therefore
raises :class:`~literalizer.exceptions.UnrepresentableInputError`
rather than producing a struct that fails to compile.  The ordered-map
case additionally drives the walk over a non-record dict that carries
entries.  The integration framework only exercises golden output that
compiles, so this contract has no golden-file surface and needs unit
coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Rust

_EMPTY_DICT_FIELD_JSON = '{"title": "report", "extra": {}}'
_ORDERED_MAP_FIELD_YAML = (
    "title: report\nordered: !!omap\n  - a: 1\n  - b: 2\n"
)


@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        (_EMPTY_DICT_FIELD_JSON, InputFormat.JSON),
        (_ORDERED_MAP_FIELD_YAML, InputFormat.YAML),
    ],
)
def test_record_strategy_rejects_non_record_dict_field(
    source: str,
    input_format: InputFormat,
) -> None:
    """A non-record dict field under ``RECORD`` raises rather than
    emitting a struct that fails to compile.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    with pytest.raises(expected_exception=UnrepresentableInputError):
        literalize(
            source=source,
            input_format=input_format,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
