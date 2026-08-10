"""COBOL special-float rejection tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableSpecialFloatError
from literalizer.languages import Cobol


@pytest.mark.parametrize(argnames="value", argvalues=[".nan", ".inf", "-.inf"])
def test_cobol_rejects_special_floats(value: str) -> None:
    """COBOL never substitutes a finite value for a special float."""
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        literalize(
            source=f"value: {value}",
            input_format=InputFormat.YAML,
            language=Cobol(),
        )
