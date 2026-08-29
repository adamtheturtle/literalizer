"""Rejection of declaration styles and formats reached without
``literalize``.

The contracts that a caller reaches through ``literalize`` or a
language constructor are declared in ``tests/errors/rejections`` and
run by ``test_rejections.py``.  What is left here is the pair that no
manifest can express, because neither goes through the public entry
points: both call an option member's own callable directly.
"""

import pytest

from literalizer.exceptions import (
    IncompatibleFormatsError,
)
from literalizer.languages import Rust


def test_rust_tuple_format_type_annotation_raises() -> None:
    """TUPLE.format_type_annotation raises for incompatible format."""
    with pytest.raises(expected_exception=IncompatibleFormatsError):
        Rust.sequence_formats.TUPLE.format_type_annotation(
            element_type="i32",
            length=2,
        )


def test_rust_lazy_static_config_formatter_raises_if_called_directly() -> None:
    """The LAZY_STATIC ``DeclarationStyleConfig`` formatter is a
    placeholder.

    The real formatter is built by
    :meth:`Rust.DeclarationStyles.build_formatter`; calling the
    stored one directly would silently emit invalid Rust, so it
    raises instead.
    """
    style = Rust.declaration_styles.LAZY_STATIC
    with pytest.raises(expected_exception=NotImplementedError):
        style.value.formatter("x", "v", None, frozenset())
