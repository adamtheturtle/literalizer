"""The empty string a null-refusing language still represents.

The refusals are declared in ``tests/errors/rejections`` and run by
``test_rejections.py``.  What is left here is the value they must not
take with them: Bash and Tcl refuse a null because they cannot tell it
from empty text, so the empty text itself has to keep working.
"""

import pytest

from literalizer import InputFormat, Language, literalize
from literalizer.languages import Bash, Tcl


@pytest.mark.parametrize(argnames="language", argvalues=[Bash(), Tcl()])
def test_empty_string_remains_representable(language: Language) -> None:
    """Rejecting null does not reject the distinct empty-string value."""
    result = literalize(
        source='""',
        input_format=InputFormat.JSON,
        language=language,
    )

    assert result.code == '""'
