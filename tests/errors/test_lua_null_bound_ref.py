"""Lua errors for invalid table keys supplied through refs.

A manifest spells ``bound_refs`` as a TOML inline table, which has no
null, so the ``None`` these bind cannot be written in one.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Lua

if TYPE_CHECKING:
    from literalizer._types import Scalar


def test_lua_rejects_null_set_member_supplied_by_bound_ref() -> None:
    """Validate the materialized ref value, not just parsed input."""
    items: set[Scalar] = {None}
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="Lua cannot use null as a set member table key",
    ):
        literalize(
            source='[{"$ref": "items"}]',
            input_format=InputFormat.JSON,
            language=Lua(),
            variable_form=NewVariable(name="value", modifiers=frozenset()),
            wrap_in_file=True,
            ref_key="$ref",
            bound_refs={"items": items},
        )
