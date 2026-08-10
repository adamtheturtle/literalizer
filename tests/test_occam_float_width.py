"""Occam float-width regression tests."""

from literalizer import InputFormat, literalize
from literalizer.languages import Occam


def test_occam_json_floats_use_real64() -> None:
    """JSON binary64 extremes retain a compatible Occam width."""
    result = literalize(
        source="[1e-320, 1.7976931348623157e308]",
        input_format=InputFormat.JSON,
        language=Occam(),
    )

    assert "1.0e-320(REAL64)" in result.code
    assert "1.7976931348623157e+308(REAL64)" in result.code
    assert "REAL32" not in result.code
