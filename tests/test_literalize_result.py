"""Focused tests for :class:`literalizer.LiteralizeResult`."""

from literalizer import LiteralizeResult


def test_code_prepends_body_preamble_and_comments() -> None:
    """Prefix lines appear before the rendered declaration."""
    result = LiteralizeResult(
        declaration_code="my_data = HInt 42",
        preamble=(),
        body_preamble=("data Val = HInt Integer",),
        pre_declaration_comments=("-- source comment",),
        types_present=frozenset({int}),
        contains_standalone_comments=True,
        source_data=42,
        sections=(),
        data_dependent_preamble=(),
    )

    assert result.code == (
        "data Val = HInt Integer\n-- source comment\nmy_data = HInt 42"
    )
