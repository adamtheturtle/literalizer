"""Golden coverage for unwrapped :class:`LiteralizeResult` prefixes."""

from pathlib import Path
from typing import Literal

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, NewVariable
from literalizer.languages import (
    Cpp,
    Elm,
    FSharp,
    Go,
    Haskell,
    Java,
    Kotlin,
    PureScript,
    Rust,
    Scala,
)

from .golden_checks import check_golden
from .language_specs import make_golden_path

_GOLDEN_DIR = Path(__file__).parent / "unwrapped_literalize_results"
_LANGUAGES = (Elm, FSharp, Haskell, PureScript)
_RECORD_LANGUAGES = (Cpp, Go, Java, Kotlin, Rust, Scala)


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_LANGUAGES,
    ids=[lang_cls.__name__ for lang_cls in _LANGUAGES],
)
@pytest.mark.parametrize(argnames="attribute", argvalues=["code", "bare_code"])
def test_unwrapped_literalize_result_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    attribute: Literal["code", "bare_code"],
    file_regression: FileRegressionFixture,
) -> None:
    """Pin both prefix-composition views for every producing family."""
    spec = lang_cls()
    result = literalizer.literalize(
        source="# note\n42\n",
        input_format=InputFormat.YAML,
        language=spec,
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=False,
    )
    assert result.body_preamble
    assert result.pre_declaration_comments
    contents = result.code if attribute == "code" else result.bare_code
    check_golden(
        contents=contents + "\n",
        extension=spec.extension,
        golden_path=make_golden_path(
            parent=_GOLDEN_DIR,
            name=f"{lang_cls.__name__}_{attribute}",
            extension=spec.extension,
            lang_cls=lang_cls,
            version=spec.language_version,
        ),
        file_regression=file_regression,
    )


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_RECORD_LANGUAGES,
    ids=[lang_cls.__name__ for lang_cls in _RECORD_LANGUAGES],
)
def test_unwrapped_record_preamble_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    file_regression: FileRegressionFixture,
) -> None:
    """Pin where ``RECORD`` declarations land on unwrapped results.

    Every ``RECORD``-capable language returns its generated record
    declarations via :attr:`~literalizer.LiteralizeResult.preamble`
    and keeps :attr:`~literalizer.LiteralizeResult.code` as just the
    literal, so callers can splice the code into a surrounding
    collection literal they control (issue #3615 pinned Scala, which
    used to prepend ``case class`` lines to the code instead).
    """
    spec = lang_cls(
        heterogeneous_strategy=lang_cls.HeterogeneousStrategies["RECORD"],
    )
    result = literalizer.literalize(
        source='a: 1\nb: "x"\n',
        input_format=InputFormat.YAML,
        language=spec,
        wrap_in_file=False,
    )
    assert result.preamble
    assert not result.body_preamble
    assert not any(entry in result.code for entry in result.preamble)
    check_golden(
        contents="\n".join((*result.preamble, result.code)) + "\n",
        extension=spec.extension,
        golden_path=make_golden_path(
            parent=_GOLDEN_DIR,
            name=f"{lang_cls.__name__}_record_preamble",
            extension=spec.extension,
            lang_cls=lang_cls,
            version=spec.language_version,
        ),
        file_regression=file_regression,
    )
