"""Rejection of null elements in collection literals that cannot hold
them.

Java's ``List.of(...)`` throws ``NullPointerException`` on a null
element, so ``literalize`` raises
:class:`~literalizer.exceptions.NullInCollectionError` rather than
emitting a list literal that fails at runtime.  The integration
framework only exercises golden output that runs, so this contract has
no golden-file surface and needs unit coverage.
"""

import json
import re

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import NullInCollectionError
from literalizer.languages import Java, V

_V_NULL_ONLY_MSG = re.escape(
    pattern="V cannot infer an element type for a collection whose "
    "members are all null; remove the nulls or select the INTERFACE "
    "or RECORD heterogeneous strategy."
)


def test_java_list_rejects_null_elements() -> None:
    """Java's ``List.of()`` does not accept null elements."""
    spec = Java(
        sequence_format=Java.sequence_formats.LIST,
    )
    expected_msg = re.escape(
        pattern="Java's List.of() does not accept null elements"
        " (got 3 items, including null). "
        "Use sequence_format=ARRAY instead."
    )
    with pytest.raises(
        expected_exception=NullInCollectionError,
        match=f"^{expected_msg}$",
    ):
        literalize(
            source=json.dumps(obj=[1, None, "hello"]),
            input_format=InputFormat.JSON,
            language=spec,
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


@pytest.mark.parametrize(
    argnames="source",
    argvalues=[
        json.dumps(obj=[None, None]),
        json.dumps(obj={"a": None, "b": None}),
        json.dumps(obj=[[None]]),
        json.dumps(obj={"a": {"b": None}}),
    ],
    ids=["null_list", "null_map", "nested_null_list", "nested_null_map"],
)
def test_v_default_rejects_null_only_container(source: str) -> None:
    """V's default (``ERROR``) strategy has no element type to infer for
    a non-empty all-null list or map, so it refuses the shape instead of
    emitting a ``voidptr`` collection the V/C back end rejects (issues
    #3017 and #3018).
    """
    with pytest.raises(
        expected_exception=NullInCollectionError,
        match=f"^{_V_NULL_ONLY_MSG}$",
    ):
        literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=V(),
            pre_indent_level=0,
            include_delimiters=True,
            variable_form=None,
        )


def test_v_interface_strategy_admits_null_only_container() -> None:
    """The ``INTERFACE`` strategy wraps each null in ``IVal(...)``, so a
    null-only list is representable and is not rejected.
    """
    result = literalize(
        source=json.dumps(obj=[None, None]),
        input_format=InputFormat.JSON,
        language=V(
            heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE,
        ),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    assert result.code == (
        "[\n\tIVal(unsafe { nil }),\n\tIVal(unsafe { nil }),\n]"
    )
