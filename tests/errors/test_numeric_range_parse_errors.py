"""Numeric parser behavior that cannot share the cached YAML runner."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import ParseError
from literalizer.languages import Python


def test_yaml_finite_float_underflow_raises() -> None:
    """A finite nonzero YAML number must not silently become zero."""
    with pytest.raises(
        expected_exception=ParseError,
        match="outside binary64 range",
    ):
        literalize(
            source="-1e-4000",
            input_format=InputFormat.YAML,
            language=Python(),
        )
