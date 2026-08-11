"""TOML rejects null values instead of silently changing the data."""

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Toml


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        "null",
        '{"a": null}',
        "[null, 1]",
        '{"a": [{"b": null}]}',
    ],
    ids=["scalar", "mapping", "sequence", "nested"],
)
def test_toml_rejects_null(source: str) -> None:
    """TOML has no lossless representation for JSON null."""
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="TOML cannot represent null values",
    ):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=Toml(),
        )
