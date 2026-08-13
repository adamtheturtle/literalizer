"""Nix special-float representation errors."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableSpecialFloatError
from literalizer.languages import Nix


def test_nix_nan_raises() -> None:
    """Nix division by zero is an evaluation error, not NaN."""
    with pytest.raises(
        expected_exception=UnrepresentableSpecialFloatError,
        match="cannot represent NaN without an evaluation error",
    ):
        literalize(
            source="- .nan\n",
            input_format=InputFormat.YAML,
            language=Nix(),
        )


def test_nix_infinities_remain_representable() -> None:
    """Nix multiplication can still produce positive and negative infinity."""
    result = literalize(
        source="[.inf, -.inf]",
        input_format=InputFormat.YAML,
        language=Nix(),
    )

    assert "1.0e308 * 10.0" in result.code
