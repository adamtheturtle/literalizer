"""Haskell ``json_type`` rejection paths."""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import (
    UnrepresentableInputError,
)
from literalizer.languages import Haskell


def test_haskell_json_type_rejects_aeson_qq_terminator_in_string() -> None:
    """Reject string values that close the ``aesonQQ`` bracket early."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match=r"aesonQQ terminator",
    ):
        literalize(
            source='{"note": "ends with |] here"}',
            input_format=InputFormat.JSON,
            language=Haskell(json_type=Haskell.json_types.AESON_VALUE),
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
