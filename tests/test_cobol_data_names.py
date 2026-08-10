"""COBOL data-name normalization behavior."""

from literalizer import InputFormat, literalize
from literalizer.languages import Cobol


def test_bare_mapping_disambiguates_normalized_and_truncated_names() -> None:
    """Sibling names are unique even when no variable wrapper is requested."""
    result = literalize(
        source=(
            '{"a_b": 1, "a-b": 2, '
            '"averyveryverylongkeynamethatgoesonandonandon": 3, '
            '"averyveryverylongkeynamethatgoesonandmore": 4}'
        ),
        input_format=InputFormat.JSON,
        language=Cobol(),
    )

    assert "05 F-A-B PIC" in result.code
    assert "05 F-A-B-2 PIC" in result.code
    assert "05 F-AVERYVERYVERYLONGKEYNAMETHAT PIC" in result.code
    assert "05 F-AVERYVERYVERYLONGKEYNAMETH-2 PIC" in result.code
