"""Heterogeneity check for dict keys, exercised through the public API.

The check rejects dicts whose keys span multiple type families when
the target language sets ``dict_supports_heterogeneous_values = False``.
The YAML parser preserves non-string keys natively, so the check is
reachable through :func:`literalizer.literalize`; these tests drive it
that way (rather than calling the internal helper) so the recursion
into nested lists and dict values is covered end to end.
"""

import re

import pytest

import literalizer
from literalizer.exceptions import MixedDictKeysError
from literalizer.languages import Mojo


def test_mixed_int_str_keys_raise_on_homogeneous_target() -> None:
    """Mojo rejects a dict mixing ``int`` and ``str`` keys."""
    expected_msg = re.escape(
        pattern="Dict contains keys of mixed types that cannot be "
        "represented in the target language "
        "(found types: int, str)",
    )
    with pytest.raises(
        expected_exception=MixedDictKeysError,
        match=f"^{expected_msg}$",
    ):
        literalizer.literalize(
            source="1: a\nx: b\n",
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(name="my_data"),
        )


def test_mixed_bool_int_keys_raise_on_homogeneous_target() -> None:
    """``bool`` and ``int`` are distinct type families for key
    checking.
    """
    with pytest.raises(expected_exception=MixedDictKeysError):
        literalizer.literalize(
            source="true: a\n2: b\n",
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(name="my_data"),
        )


def test_nested_mixed_keys_raise() -> None:
    """Mixed-key dicts nested in a list raise."""
    with pytest.raises(expected_exception=MixedDictKeysError):
        literalizer.literalize(
            source="- 1: a\n  x: b\n",
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(name="my_data"),
        )


def test_mixed_keys_inside_dict_value_raise() -> None:
    """Mixed-key dicts found by descending through outer dict values
    raise.
    """
    with pytest.raises(expected_exception=MixedDictKeysError):
        literalizer.literalize(
            source="outer:\n  1: a\n  x: b\n",
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(name="my_data"),
        )


def test_mixed_keys_in_second_list_element_raise() -> None:
    """Mixed-key dicts found past a homogeneous first list element
    raise.
    """
    with pytest.raises(expected_exception=MixedDictKeysError):
        literalizer.literalize(
            source="- foo: string\n- 1: a\n  x: b\n",
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(name="my_data"),
        )


def test_mixed_keys_past_set_sibling_raise() -> None:
    """Recursion skips past a set sibling before finding the mixed
    dict.
    """
    with pytest.raises(expected_exception=MixedDictKeysError):
        literalizer.literalize(
            source="- !!set\n  ? 1\n  ? 2\n- 1: a\n  x: b\n",
            input_format=literalizer.InputFormat.YAML,
            language=Mojo(),
            variable_form=literalizer.NewVariable(name="my_data"),
        )
