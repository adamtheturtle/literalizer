"""COBOL integer picture range tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Cobol


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
