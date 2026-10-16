"""JSONC input accepts comments while keeping JSON syntax rules."""

import ast

from literalizer import InputFormat, literalize
from literalizer.languages import Jsonc, Python


def test_jsonc_output_can_be_read_as_jsonc_input() -> None:
    """Rendered comments and values survive a public API round trip."""
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

    assert ast.literal_eval(node_or_string=result.code) == {"count": 2}
