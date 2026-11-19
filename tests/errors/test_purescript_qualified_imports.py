"""Validation of PureScript qualified import names."""

import pytest

from literalizer.languages import PureScript


@pytest.mark.parametrize(
    argnames=("module", "alias"),
    argvalues=[("bad.Module", "Numbers"), ("Prelude", "badAlias")],
)
def test_invalid_qualified_import(module: str, alias: str) -> None:
    """Reject invalid module paths and aliases at construction."""
    with pytest.raises(
        expected_exception=ValueError, match="Invalid qualified import"
    ):
        _ = PureScript(qualified_imports=((module, alias),))
