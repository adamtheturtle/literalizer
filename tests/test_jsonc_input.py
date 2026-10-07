"""JSONC input accepts comments while keeping JSON syntax rules."""

from literalizer import InputFormat, literalize
from literalizer.languages import Jsonc, Python


def test_jsonc_output_can_be_read_as_jsonc_input() -> None:
    """Rendered comments are accepted by the public input path."""
    output = literalize(
        source="# heading\ncount: 2\n",
        input_format=InputFormat.YAML,
        language=Jsonc(),
    )
    result = literalize(
        source=output.code,
        input_format=InputFormat.JSONC,
        language=Python(),
    )

    assert result.code == '{\n    "count": 2,\n}'
