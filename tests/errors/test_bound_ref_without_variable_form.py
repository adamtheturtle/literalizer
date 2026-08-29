"""Errors for a bound reference no declaration is emitted for.

A binding is emitted for a bound reference only where the result binds
a variable of its own.  Without one, a complete file still names the
reference and declares nothing.  The rejection manifests give every
language that supports variable names a ``NewVariable`` when a case
declares no variable form, so they cannot express this one; it stays an
ordinary test.
"""

import re

import pytest

from literalizer import InputFormat, literalize
from literalizer.exceptions import RefNotSelfContainedError
from literalizer.languages import Python


def test_bound_ref_without_variable_form_rejected() -> None:
    """A file binding no variable of its own declares no reference."""
    with pytest.raises(
        expected_exception=RefNotSelfContainedError,
        match=re.escape(pattern="unbound reference shared"),
    ):
        literalize(
            source='{"a": {"$ref": "shared"}}',
            input_format=InputFormat.JSON,
            language=Python(),
            wrap_in_file=True,
            ref_key="$ref",
            bound_refs={"shared": [1, 2]},
        )
