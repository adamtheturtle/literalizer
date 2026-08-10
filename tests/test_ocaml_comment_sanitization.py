"""Tests for OCaml comment lexical safety."""

from literalizer import InputFormat, literalize
from literalizer.languages import OCaml


def test_ocaml_comments_strip_quote_tokens() -> None:
    """Quotes cannot start unterminated literals inside OCaml comments."""
    result = literalize(
        source="a: 1  # don't leave \" open or close *) early\nb: 2\n",
        input_format=InputFormat.YAML,
        language=OCaml(),
    )

    assert "(* dont leave  open or close * ) early *)" in result.code
