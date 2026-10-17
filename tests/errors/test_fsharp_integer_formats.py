"""F# only admits decimal literals with the bigint suffix."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableIntegerError
from literalizer.languages import FSharp


@pytest.mark.parametrize(
    argnames="value",
    argvalues=[-(2**63) - 1, 2**63, 2**128],
)
@pytest.mark.parametrize(
    argnames="integer_format",
    argvalues=["HEX", "OCTAL", "BINARY"],
)
@pytest.mark.parametrize(
    argnames="dict_format",
    argvalues=["DEFAULT", "ANONYMOUS_RECORD"],
)
def test_nondecimal_bigint(
    value: int,
    integer_format: str,
    dict_format: str,
) -> None:
    """Reject unsupported bigint literals in both native output modes."""
    with pytest.raises(
        expected_exception=UnrepresentableIntegerError,
        match="F# bigint literals require decimal integer_format",
    ):
        _ = literalize(
            source=f"{value}",
            input_format=InputFormat.JSON,
            language=FSharp(
                integer_format=FSharp.integer_formats[integer_format],
                dict_format=FSharp.dict_formats[dict_format],
            ),
        )
