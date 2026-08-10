"""COBOL integer picture range tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import Cobol


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[9223372036854775807, -9223372036854775808],
)
def test_cobol_rejects_values_outside_s9_18(value: int) -> None:
    """A 19-digit value is not emitted into an 18-digit picture."""
    with pytest.raises(expected_exception=UnrepresentableIntegerError):
        literalize(
            source=f"[{value}]",
            input_format=InputFormat.JSON,
            language=Cobol(),
        )


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[999999999999999999, -999999999999999999],
)
def test_cobol_accepts_s9_18_boundaries(value: int) -> None:
    """Both signed endpoints that fit S9(18) remain representable."""
    result = literalize(
        source=f"[{value}]",
        input_format=InputFormat.JSON,
        language=Cobol(),
    )

    assert f"PIC S9(18) COMP-5 VALUE {value}." in result.code
