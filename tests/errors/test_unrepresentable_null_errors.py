"""Errors for languages that cannot distinguish null from empty text."""

import pytest

from literalizer import InputFormat, Language, literalize
from literalizer.exceptions import UnrepresentableNullError
from literalizer.languages import Bash, Tcl


@pytest.mark.parametrize(argnames="language", argvalues=[Bash(), Tcl()])
@pytest.mark.parametrize(
    argnames=("source", "input_format"),
    argvalues=[
        ("null", InputFormat.JSON),
        ('{"outer": [null]}', InputFormat.JSON),
        ("? ~\n: 1\n", InputFormat.YAML),
        ("!!set\n? null\n", InputFormat.YAML),
    ],
)
def test_null_is_rejected(
    source: str, input_format: InputFormat, language: Language
) -> None:
    """Null is rejected at any reachable collection depth."""
    with pytest.raises(expected_exception=UnrepresentableNullError):
        literalize(
            source=source,
            input_format=input_format,
            language=language,
        )


@pytest.mark.parametrize(argnames="language", argvalues=[Bash(), Tcl()])
def test_empty_string_remains_representable(language: Language) -> None:
    """Rejecting null does not reject the distinct empty-string value."""
    result = literalize(
        source='""',
        input_format=InputFormat.JSON,
        language=language,
    )

    assert result.code == '""'
