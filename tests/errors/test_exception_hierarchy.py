"""Tests for Literalizer's public exception hierarchy."""

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
