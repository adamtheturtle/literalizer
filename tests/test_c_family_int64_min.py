"""C-family minimum signed 64-bit literal tests."""

import pytest

from literalizer import InputFormat, literalize
from literalizer._language import Language
from literalizer.languages import C, Cpp, ObjectiveC


@pytest.mark.parametrize(
    argnames="language", argvalues=[C(), Cpp(), ObjectiveC()]
)
def test_c_family_int64_min_avoids_unsigned_operand(
    language: Language,
) -> None:
    """INT64_MIN is expressed using an individually valid LL literal."""
    result = literalize(
        source="[-9223372036854775808]",
        input_format=InputFormat.JSON,
        language=language,
    )

    assert "(-9223372036854775807LL - 1)" in result.code
    assert "-9223372036854775808" not in result.code
