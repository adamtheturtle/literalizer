"""Tests for Literalizer's public exception hierarchy.

These make no call and raise nothing, so there is no rejection for a
manifest to declare: the subject is which class inherits from which.
"""

from typing import TYPE_CHECKING

import literalizer.exceptions
from literalizer import LiteralizerError

if TYPE_CHECKING:
    from collections.abc import Mapping


def test_every_literalizer_exception_has_public_base() -> None:
    """Every exception declared by Literalizer shares one public base."""
    members: Mapping[str, object] = vars(literalizer.exceptions)
    exception_classes = [
        member
        for member in members.values()
        if isinstance(member, type)
        and member.__module__ == literalizer.exceptions.__name__
    ]

    assert len(exception_classes) > 0
    assert all(
        issubclass(exception_class, LiteralizerError)
        for exception_class in exception_classes
    )
