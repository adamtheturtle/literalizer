"""Unsupported call backends retain direct shared-recipe rejection
checks.
"""

import pytest

from literalizer import (
    InputFormat,
    LanguageCls,
    literalize_invocations,
)
from literalizer._language import CallSupport
from literalizer.exceptions import (
    CallsNotSupportedByLanguageError,
    CallsNotSupportedByToolError,
)
from literalizer.languages import ALL_LANGUAGES

_UNSUPPORTED: list[LanguageCls] = sorted(
    (
        cls
        for cls in ALL_LANGUAGES
        if isinstance(cls().call_style_config, CallSupport)
    ),
    key=lambda cls: cls.__name__,
)


@pytest.mark.parametrize(argnames="language_cls", argvalues=_UNSUPPORTED)
def test_shared_recipe_rejects_unsupported_calls(
    language_cls: LanguageCls,
) -> None:
    """Call-language and call-tool failures keep their original types."""
    language = language_cls()
    error = (
        CallsNotSupportedByLanguageError
        if language.call_style_config is CallSupport.NOT_IN_LANGUAGE
        else CallsNotSupportedByToolError
    )
    with pytest.raises(expected_exception=error):
        _ = literalize_invocations(
            source="[[1]]",
            input_format=InputFormat.JSON,
            language=language,
            invocation={
                "default": {
                    "target-function": "consume",
                    "parameter-names": ["value"],
                },
            },
        )
