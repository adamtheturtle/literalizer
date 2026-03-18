"""OCaml language specification."""

from __future__ import annotations

from typing import TYPE_CHECKING

from literalizer._formatters import (
    format_bytes_hex,
    format_date_iso,
    format_datetime_iso,
)

if TYPE_CHECKING:
    from literalizer._language import Language


def _to_val(value: str) -> str:
    """Convert a value to an OCaml union type expression."""
    _val_prefixes = (
        "ONull",
        "OBool",
        "OList",
        "OMap",
        "OSet",
        "OStr",
        "OInt",
        "OFloat",
    )
    if any(value.startswith(p) for p in _val_prefixes):
        return value
    if value.startswith('"') and value.endswith('"'):
        return f"OStr {value}"
    negative = value.startswith("-")
    rest = value[1:] if negative else value
    int_result = None
    try:
        int(rest)
        int_result = f"OInt ({value})" if negative else f"OInt {value}"
    except ValueError:
        pass
    if int_result is not None:
        return int_result
    float_result = None
    try:
        float(rest)
        float_result = f"OFloat ({value})" if negative else f"OFloat {value}"
    except ValueError:  # pragma: no cover
        pass
    if float_result is not None:
        return float_result
    return value  # pragma: no cover


def _format_ocaml_dict_entry(key: str, value: str) -> str:
    """Format an OCaml dict entry as a ``(key, OXxx value)`` tuple."""
    return f"({key}, {_to_val(value=value)})"


def _format_ocaml_omap_entry(key: str, value: str) -> str:
    """Format an OCaml ordered-map entry as a ``(key, OXxx value)``
    tuple.
    """
    return f"({key}, {_to_val(value=value)})"


def _format_ocaml_set_entry(item: str) -> str:
    """Format an OCaml set entry with the appropriate ``val_t``
    constructor.
    """
    return _to_val(value=item)


def _format_ocaml_sequence_entry(item: str) -> str:
    """Format an OCaml list entry with the appropriate ``val_t``
    constructor.
    """
    return _to_val(value=item)


def _format_variable_declaration(name: str, value: str) -> str:
    """Format an OCaml variable declaration."""
    return f"let {name} : val_t = {_to_val(value=value)}"


def _format_variable_assignment(name: str, value: str) -> str:
    """Format an OCaml variable assignment."""
    return _format_variable_declaration(name=name, value=value)


class OCaml:
    """OCaml language specification."""

    def __init__(self) -> None:
        """Initialize OCaml language specification."""
        self.null_literal = "ONull"
        self.true_literal = "OBool true"
        self.false_literal = "OBool false"
        self.sequence_open = "OList ["
        self.sequence_close = "]"
        self.dict_open = "OMap ["
        self.dict_close = "]"
        self.format_dict_entry = _format_ocaml_dict_entry
        self.multiline_trailing_comma = False
        self.single_element_trailing_comma = False
        self.format_bytes = format_bytes_hex
        self.format_date = format_date_iso
        self.format_datetime = format_datetime_iso
        self.empty_sequence: str | None = None
        self.empty_dict: str | None = None
        self.set_open = "OSet ["
        self.set_close = "]"
        self.empty_set: str | None = None
        self.format_set_entry = _format_ocaml_set_entry
        self.comment_prefix = "(*"
        self.comment_suffix = " *)"
        self.omap_open = "OMap ["
        self.omap_close = "]"
        self.format_omap_entry = _format_ocaml_omap_entry
        self.multiline_close_indent = ""
        self.skip_null_dict_values = False
        self.format_variable_declaration = _format_variable_declaration
        self.format_variable_assignment = _format_variable_assignment
        self.element_separator = "; "
        self.format_sequence_entry = _format_ocaml_sequence_entry


OCAML: Language = OCaml()
