"""Jsonnet errors for unsupported non-finite floats."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableSpecialFloatError
from literalizer.languages import Jsonnet


@pytest.mark.parametrize(
    argnames="yaml_value",
    argvalues=[".inf", "-.inf", ".nan"],
    ids=["positive_infinity", "negative_infinity", "nan"],
)
def test_jsonnet_special_floats_raise(yaml_value: str) -> None:
    """Jsonnet rejects string substitutions for numeric special values."""
    with pytest.raises(expected_exception=UnrepresentableSpecialFloatError):
        literalize(
            source=f"- {yaml_value}\n",
            input_format=InputFormat.YAML,
            language=Jsonnet(),
        )
