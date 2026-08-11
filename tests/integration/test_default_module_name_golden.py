"""Golden coverage for languages' default wrapped-file module names."""

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, NewVariable

from .golden_checks import check_golden
from .language_specs import make_golden_path, sorted_languages

_GOLDEN_DIR = Path(__file__).parent / "default_module_names"
_LANGUAGES = [
    lang_cls
    for lang_cls in sorted_languages()
    if lang_cls.supports_module_name
]


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_LANGUAGES,
    ids=[lang_cls.__name__ for lang_cls in _LANGUAGES],
)
def test_default_module_name_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    file_regression: FileRegressionFixture,
) -> None:
    """Every declared module-name default produces a wrapped source
    file.
    """
    spec = lang_cls()
    result = literalizer.literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=spec,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=True,
    )
    check_golden(
        contents=result.code + "\n",
        extension=spec.extension,
        golden_path=make_golden_path(
            parent=_GOLDEN_DIR,
            name=f"{lang_cls.__name__}_default_module_name",
            extension=spec.extension,
            lang_cls=lang_cls,
            version=spec.language_version,
        ),
        file_regression=file_regression,
    )
