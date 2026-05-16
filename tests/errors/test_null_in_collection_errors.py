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
from literalizer.languages import Java


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
