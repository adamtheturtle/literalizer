"""Tests for typed failures from unsupported language options.

The subject is the structured ``language_name`` and ``option``
attributes rather than the message a rejection manifest keeps in a
golden file, and the second case asserts a bare ``TypeError``, which
is not a name in ``literalizer.exceptions`` for a manifest to spell.
"""

import pytest

from literalizer import LanguageCls
from literalizer.exceptions import UnsupportedOptionError
from literalizer.languages import Cpp, Haxe, Python


@pytest.mark.parametrize(
    argnames=("language_cls", "option", "value"),
    argvalues=[
        (Python, "empty_dict_key", None),
        (Cpp, "annotation_evaluation", None),
        (Python, "multiline_raw_string_delimiter_base", "tag"),
        (Python, "heterogeneous_value_enum_name", "Value"),
        (Haxe, "default_set_element_type", "String"),
        (Haxe, "default_dict_key_type", "Int"),
        (Haxe, "default_dict_value_type", "String"),
    ],
)
def test_known_unsupported_option_raises_typed_error(
    *, language_cls: LanguageCls, option: str, value: object
) -> None:
    """Known options use the public Literalizer error hierarchy."""
    with pytest.raises(expected_exception=UnsupportedOptionError) as caught:
        language_cls(**{option: value})

    assert caught.value.language_name == language_cls.__name__
    assert caught.value.option == option


def test_unknown_option_remains_type_error() -> None:
    """Typos are not misreported as unsupported public options."""
    language_cls: LanguageCls = Cpp
    with pytest.raises(expected_exception=TypeError):
        language_cls(definitely_not_an_option=True)
