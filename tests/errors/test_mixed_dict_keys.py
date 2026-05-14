"""Heterogeneity check for dict keys.

The check runs inside :func:`literalizer._checks.check_data` and rejects
dicts whose keys span multiple type families when the target language
sets ``dict_supports_heterogeneous_values = False``.  Today the surface
parsers coerce non-string keys to strings, so the check is wired but
unreachable through :func:`literalizer.literalize`; the tests here
invoke ``check_data`` directly to exercise the contract.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

import pytest

from literalizer._checks import check_data
from literalizer.exceptions import MixedDictKeysError
from literalizer.languages import Mojo

if TYPE_CHECKING:
    from literalizer._types import Scalar, Value


def test_mixed_int_str_keys_raise_on_homogeneous_target() -> None:
    """Mojo rejects a dict mixing ``int`` and ``str`` keys."""
    data: dict[Scalar, Value] = {}
    data[1] = "a"
    data["x"] = "b"
    expected_msg = re.escape(
        pattern="Dict contains keys of mixed types that cannot be "
        "represented in the target language "
        "(found types: int, str)",
    )
    with pytest.raises(
        expected_exception=MixedDictKeysError,
        match=f"^{expected_msg}$",
    ):
        check_data(data=data, spec=Mojo())


def test_mixed_bool_int_keys_raise_on_homogeneous_target() -> None:
    """``bool`` and ``int`` are distinct type families for key
    checking.
    """
    data: dict[Scalar, Value] = {}
    data[True] = "a"
    data[2] = "b"
    with pytest.raises(expected_exception=MixedDictKeysError):
        check_data(data=data, spec=Mojo())


def test_nested_mixed_keys_raise() -> None:
    """Mixed-key dicts nested in a list raise."""
    inner: dict[Scalar, Value] = {}
    inner[1] = "a"
    inner["x"] = "b"
    data: list[Value] = [inner]
    with pytest.raises(expected_exception=MixedDictKeysError):
        check_data(data=data, spec=Mojo())


def test_mixed_keys_inside_dict_value_raise() -> None:
    """Mixed-key dicts found by descending through outer dict values
    raise.
    """
    inner: dict[Scalar, Value] = {}
    inner[1] = "a"
    inner["x"] = "b"
    data: dict[Scalar, Value] = {}
    data["outer"] = inner
    with pytest.raises(expected_exception=MixedDictKeysError):
        check_data(data=data, spec=Mojo())


def test_mixed_keys_in_second_list_element_raise() -> None:
    """Mixed-key dicts found past a homogeneous first list element
    raise.
    """
    inner: dict[Scalar, Value] = {}
    inner[1] = "a"
    inner["x"] = "b"
    sibling: dict[Scalar, Value] = {"only": "string"}
    data: list[Value] = [sibling, inner]
    with pytest.raises(expected_exception=MixedDictKeysError):
        check_data(data=data, spec=Mojo())


def test_mixed_keys_past_set_sibling_raise() -> None:
    """Recursion skips past a set sibling before finding the mixed
    dict.
    """
    inner: dict[Scalar, Value] = {}
    inner[1] = "a"
    inner["x"] = "b"
    sibling: set[Scalar] = {1, 2}
    data: list[Value] = [sibling, inner]
    with pytest.raises(expected_exception=MixedDictKeysError):
        check_data(data=data, spec=Mojo())
