"""Error contracts for languages that cannot wrap combined variable
forms.
"""

import pytest

from literalizer import FileWrapperContext, LanguageCls
from literalizer._language import redefinition_config
from literalizer.exceptions import WrapCombinedInFileNotSupportedError
from literalizer.languages import ALL_LANGUAGES


def _language_class_name(language_cls: LanguageCls, /) -> str:
    """Return the language class name."""
    return language_cls.__name__


@pytest.mark.parametrize(
    argnames="language_cls",
    argvalues=[
        cls
        for cls in sorted(ALL_LANGUAGES, key=_language_class_name)
        if not any(
            redefinition_config(style).supports_redefinition
            for style in cls.DeclarationStyles
        )
    ],
    ids=_language_class_name,
)
def test_wrap_combined_in_file_unsupported_raises(
    *,
    language_cls: LanguageCls,
) -> None:
    """Check wrap_combined_in_file raises when redefinition is unsupported."""
    with pytest.raises(expected_exception=WrapCombinedInFileNotSupportedError):
        _ = language_cls().wrap_combined_in_file(
            declaration="x = 1",
            assignment="x = 2",
            context=FileWrapperContext(
                bound_variable_names=(),
                variable_name="x",
                modifiers=frozenset(),
                body_preamble=(),
                class_preamble=(),
                has_literal_declarations=True,
                generated_body_preamble=(),
                call_stub_names=frozenset(),
                root_is_object_literal=False,
                root_mapping_entries=None,
            ),
        )
