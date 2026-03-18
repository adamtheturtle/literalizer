"""Haskell language specification."""

from __future__ import annotations

import datetime  # noqa: TC003
from typing import TYPE_CHECKING

from beartype import beartype

from literalizer._formatters import (
    fixed_sequence_open,
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
    format_string_backslash,
    passthrough_sequence_entry,
    passthrough_set_entry,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@beartype
def _format_haskell_dict_entry(key: str, value: str) -> str:
    """Format a Haskell dict entry as a tuple pair."""
    return f"({key}, {value})"


@beartype
def _format_haskell_omap_entry(key: str, value: str) -> str:
    """Format a Haskell ordered-map entry as a tuple pair."""
    return f"({key}, {value})"


@beartype
def _format_variable_declaration(name: str, value: str) -> str:
    """Format a Haskell variable declaration."""
    return f"{name} = {value}"


@beartype
def _format_variable_assignment(name: str, value: str) -> str:
    """Format a Haskell variable assignment."""
    return f"{name} = {value}"


_bytes_format: Callable[[bytes], str] = format_bytes_hex
_date_format: Callable[[datetime.date], str] = format_date_iso
_datetime_format: Callable[[datetime.datetime], str] = format_datetime_iso
_string_format: Callable[[str], str] = format_string_backslash


class Haskell:
    """Haskell language specification.

    The generated output uses custom constructors (``HNull``, ``HBool``,
    ``HList``, ``HMap``, ``HSet``) that are **not** built-in Haskell types.
    To compile the generated code, define a ``Val`` ADT and typeclass
    instances in the consuming module:

    .. code-block:: haskell

       {-# LANGUAGE OverloadedStrings #-}

       import Data.String (IsString(fromString))

       data Val
         = HNull
         | HBool Bool
         | HInt Integer
         | HFloat Double
         | HStr String
         | HList [Val]
         | HMap [(String, Val)]
         | HSet [Val]

       instance IsString Val where
           fromString = HStr

       instance Num Val where
           fromInteger = HInt
           negate (HInt n)   = HInt (negate n)
           negate (HFloat f) = HFloat (negate f)
           ...

       instance Fractional Val where
           fromRational r = HFloat (realToFrac r)
           ...

    ``OverloadedStrings`` lets bare string literals like ``"hi"`` resolve to
    ``HStr "hi"`` via ``IsString``, and the ``Num`` / ``Fractional`` instances
    let numeric literals resolve to ``HInt`` / ``HFloat``.
    """

    @beartype
    def __init__(self) -> None:
        """Initialize Haskell language specification."""
        self.null_literal = "HNull"
        self.true_literal = "HBool True"
        self.false_literal = "HBool False"
        self.sequence_open = fixed_sequence_open(delimiter="HList [")
        self.sequence_close = "]"
        self.dict_open = "HMap ["
        self.dict_close = "]"
        self.format_dict_entry: Callable[[str, str], str] = (
            _format_haskell_dict_entry
        )
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes: Callable[[bytes], str] = _bytes_format
        self.format_date: Callable[[datetime.date], str] = _date_format
        self.format_datetime: Callable[[datetime.datetime], str] = (
            _datetime_format
        )
        self.format_string: Callable[[str], str] = _string_format
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "HSet ["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_sequence_entry: Callable[[str], str] = (
            passthrough_sequence_entry
        )
        self.format_set_entry: Callable[[str], str] = passthrough_set_entry
        self.comment_prefix = "--"
        self.comment_suffix = ""
        self.omap_open = "HMap ["
        self.omap_close = "]"
        self.format_omap_entry: Callable[[str, str], str] = (
            _format_haskell_omap_entry
        )
        self.multiline_close_indent = "    "
        self.element_separator = ", "
        self.skip_null_dict_values = False
        self.format_variable_declaration: Callable[[str, str], str] = (
            _format_variable_declaration
        )
        self.format_variable_assignment: Callable[[str, str], str] = (
            _format_variable_assignment
        )
