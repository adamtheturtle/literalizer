"""Error paths for :meth:`~literalizer.LanguageCls.configured`.

``configured`` raises
:class:`~literalizer.exceptions.UnsupportedLanguageOptionError` for an
option whose backing field the target language does not have, and for a
format option whose string value does not name a member of that
language's nested format enum.
"""

import re

import pytest

from literalizer import LanguageOptions
from literalizer.exceptions import UnsupportedLanguageOptionError
from literalizer.languages import Forth, Python


def test_unsupported_field_for_language_raises() -> None:
    """Forth has no ``module_name`` field, so requesting it raises."""
    expected_msg = re.escape(
        pattern="Forth cannot be configured with option 'module_name': "
        "this language has no such field",
    )
    with pytest.raises(
        expected_exception=UnsupportedLanguageOptionError,
        match=f"^{expected_msg}$",
    ):
        Forth.configured(options=LanguageOptions(module_name="Thing"))


def test_unknown_enum_member_name_raises() -> None:
    """A format value that names no enum member raises and lists the
    valid choices.
    """
    expected_msg = re.escape(
        pattern="Python cannot be configured with option 'string_format': "
        "'NOPE' is not a valid choice; valid choices are: "
        "DOUBLE, RAW, SINGLE",
    )
    with pytest.raises(
        expected_exception=UnsupportedLanguageOptionError,
        match=f"^{expected_msg}$",
    ):
        Python.configured(options=LanguageOptions(string_format="NOPE"))
