"""Rejection of unusable field-name keys under the Rust ``RECORD``
strategy.

A dict key that collides with a Rust keyword renders as a raw
identifier (``r#type``, issue #2880; golden-file coverage exercises
that path).  Keys that raw-identifier escaping cannot express have no
compiling struct field name at all, so ``literalize`` raises
:class:`~literalizer.exceptions.UnrepresentableInputError` rather than
producing a struct that fails to compile.  The integration framework
only exercises golden output that compiles, so this contract needs
unit coverage.
"""

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.exceptions import UnrepresentableInputError
from literalizer.languages import Rust


@pytest.mark.parametrize(
    argnames="key",
    argvalues=[
        # Keywords ``rustc`` rejects even in raw-identifier form.
        "crate",
        "self",
        "super",
        "Self",
        # The reserved wildcard identifier (``r#_`` is also rejected).
        "_",
        # Keys that are not identifier-shaped text at all.
        "foo-bar",
        "1abc",
        "has space",
    ],
)
def test_record_strategy_rejects_unusable_field_name_key(key: str) -> None:
    """A key with no compiling struct field name raises rather than
    emitting a struct that fails to compile.
    """
    language = Rust(
        heterogeneous_strategy=Rust.heterogeneous_strategies.RECORD,
    )
    source = f'- "{key}": a\n  other: b\n'
    with pytest.raises(
        expected_exception=UnrepresentableInputError,
        match="cannot represent the dict key",
    ):
        literalize(
            source=source,
            input_format=InputFormat.YAML,
            language=language,
            wrap_in_file=True,
            variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        )
