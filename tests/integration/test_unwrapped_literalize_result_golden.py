"""Golden coverage for unwrapped :class:`LiteralizeResult` prefixes."""

from pathlib import Path
from textwrap import dedent
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


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_LANGUAGES,
    ids=lambda lang_cls: lang_cls.__name__,
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
    assert len(result.body_preamble) > 0
    assert len(result.pre_declaration_comments) > 0
    contents_by_attribute = {
        "code": result.code,
        "bare_code": result.bare_code,
    }
    contents = contents_by_attribute[attribute]
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
    argnames=("lang_cls", "expected_code"),
    argvalues=[
        pytest.param(
            Cpp,
            dedent(
                text="""\
                Record0{
                    .a = 1,
                    .b = "x",
                }"""
            ),
            id="Cpp",
        ),
        pytest.param(
            Go,
            'Record0{\n\tA: 1,\n\tB: "x",\n}',
            id="Go",
        ),
        pytest.param(
            Java,
            dedent(
                text="""\
                new Record0(
                    1,
                    "x"
                )"""
            ),
            id="Java",
        ),
        pytest.param(
            Kotlin,
            dedent(
                text="""\
                Record0(
                    a = 1,
                    b = "x",
                )"""
            ),
            id="Kotlin",
        ),
        pytest.param(
            Rust,
            dedent(
                text="""\
                Record0 {
                    a: 1,
                    b: "x",
                }"""
            ),
            id="Rust",
        ),
        pytest.param(
            Scala,
            dedent(
                text="""\
                Record0(
                    a = 1,
                    b = "x",
                )"""
            ),
            id="Scala",
        ),
    ],
)
def test_unwrapped_record_preamble_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    expected_code: str,
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
    assert len(result.preamble) > 0
    assert len(result.body_preamble) == 0
    assert result.code == expected_code
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
