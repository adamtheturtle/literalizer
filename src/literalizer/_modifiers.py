"""Declaration modifier enum shared by core and language modules."""

import enum


class DeclarationModifier(enum.Enum):
    """Declaration modifiers (visibility, storage) for a new variable.

    Each language maps these to its own syntax and silently ignores
    modifiers it cannot express.  For example, :attr:`FINAL` becomes
    ``final`` in Java and is a no-op in Python.
    """

    PUBLIC = enum.auto()
    """Visibility: publicly accessible."""

    PRIVATE = enum.auto()
    """Visibility: private to the enclosing scope."""

    PROTECTED = enum.auto()
    """Visibility: protected (accessible from subclasses)."""

    STATIC = enum.auto()
    """Storage: associated with the enclosing type rather than an
    instance.
    """

    FINAL = enum.auto()
    """Immutability: cannot be reassigned.  Java's ``final``."""

    READONLY = enum.auto()
    """Immutability: cannot be reassigned after initialization.
    C#'s ``readonly``.
    """

    CONST = enum.auto()
    """Immutability: compile-time constant.  C++'s ``const``,
    JavaScript/TypeScript's ``const``, Rust's ``const``.
    """
