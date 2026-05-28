"""Rejection of empty mappings on Ada/Lua/PHP/R (#2712, #2747).

Lua tables, PHP arrays, R lists, and the Ada literalizer's unified
``A_Val`` aggregate are all runtime representations that cannot
distinguish an empty mapping from an empty sequence; the matching
encoders serialize an empty mapping the same way they serialize an
empty sequence, so the mapping/sequence distinction is lost on
round-trip.  ``literalize`` raises
:class:`~literalizer.exceptions.UnrepresentableEmptyDictError` at
literalize time rather than emit a literal that silently degrades.
"""

import json

import pytest

from literalizer import InputFormat, Language, NewVariable, literalize
from literalizer.exceptions import UnrepresentableEmptyDictError
from literalizer.languages import Ada, Lua, Php, R


def _literalize(language: Language, value: object) -> None:
    """Literalize *value* under *language*, discarding the result."""
    literalize(
        source=json.dumps(obj=value),
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="x"),
    )


@pytest.mark.parametrize(
    argnames=("language", "language_name"),
    argvalues=[
        (Ada(), "Ada"),
        (Lua(), "Lua"),
        (Php(), "PHP"),
        (R(), "R"),
    ],
)
def test_top_level_empty_dict_rejected(
    language: Language, language_name: str
) -> None:
    """A bare empty dict is rejected at the top level."""
    with pytest.raises(
        expected_exception=UnrepresentableEmptyDictError,
        match=rf"^{language_name} cannot represent an empty dict ",
    ):
        _literalize(language=language, value={})


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Ada(), Lua(), Php(), R()],
)
def test_nested_empty_dict_rejected(language: Language) -> None:
    """An empty dict nested inside a populated dict is rejected."""
    with pytest.raises(expected_exception=UnrepresentableEmptyDictError):
        _literalize(language=language, value={"outer": {}})


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Ada(), Lua(), Php(), R()],
)
def test_empty_dict_inside_list_rejected(language: Language) -> None:
    """An empty dict nested inside a list element is rejected."""
    with pytest.raises(expected_exception=UnrepresentableEmptyDictError):
        _literalize(language=language, value=[{"k": 1}, {}])


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Ada(), Lua(), Php(), R()],
)
def test_empty_list_not_rejected(language: Language) -> None:
    """An empty list is unambiguous and must not be rejected."""
    _literalize(language=language, value=[])


@pytest.mark.parametrize(
    argnames="language",
    argvalues=[Ada(), Lua(), Php(), R()],
)
def test_populated_dict_not_rejected(language: Language) -> None:
    """A non-empty dict is unambiguous and must not be rejected."""
    _literalize(language=language, value={"k": 1})
