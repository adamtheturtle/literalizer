"""Tests for Literalizer's public exception hierarchy.

These make no call and raise nothing, so there is no rejection for a
manifest to declare: the subject is which class inherits from which.
"""

import literalizer.exceptions
from literalizer import LiteralizerError


def test_every_literalizer_exception_has_public_base() -> None:
    """Every exception declared by Literalizer shares one public base."""
    exception_classes = [
        member
        for member in vars(literalizer.exceptions).values()
        if isinstance(member, type)
        and member.__module__ == literalizer.exceptions.__name__
    ]

    assert exception_classes
    assert all(
        issubclass(exception_class, LiteralizerError)
        for exception_class in exception_classes
    )
