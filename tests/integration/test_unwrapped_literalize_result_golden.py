"""Golden coverage for unwrapped :class:`LiteralizeResult` prefixes."""

from pathlib import Path
from typing import Literal

import pytest
from pydantic import BaseModel, TypeAdapter
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer import InputFormat, NewVariable
from tests.toml_cases import load_toml_cases

from .case_manifests import ManifestLanguage, ManifestLanguages
from .golden_checks import check_golden
from .language_specs import make_golden_path

_GOLDEN_DIR = Path(__file__).parent / "unwrapped_literalize_results"


class _PrefixCases(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Declared languages and result views for a commented scalar."""

    languages: ManifestLanguages
    input_case: str
    attributes: tuple[Literal["code", "bare_code"], ...]
    variable_name: str


class _RecordCase(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """One language's unwrapped record literal contract."""

    language: ManifestLanguage
    expected_code: str


class _ResultCases(BaseModel, extra="forbid", frozen=True):
    """TOML-owned inputs and expectations for unwrapped result views."""

    prefix: _PrefixCases
    record_input_case: str
    records: tuple[_RecordCase, ...]


_CASES = TypeAdapter(type=_ResultCases).validate_python(
    load_toml_cases(name="unwrapped_literalize_results"),
)


@pytest.mark.parametrize(
    argnames="lang_cls",
    argvalues=_CASES.prefix.languages,
    ids=lambda lang_cls: lang_cls.__name__,
)
@pytest.mark.parametrize(
    argnames="attribute", argvalues=_CASES.prefix.attributes
)
def test_unwrapped_literalize_result_golden(
    *,
    lang_cls: literalizer.LanguageCls,
    attribute: Literal["code", "bare_code"],
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Pin both prefix-composition views for every producing family."""
    spec = lang_cls()
    result = literalizer.literalize(
        source=(cases_dir / _CASES.prefix.input_case / "input.yaml").read_text(
            encoding="utf-8"
        ),
        input_format=InputFormat.YAML,
        language=spec,
        variable_form=NewVariable(
            name=_CASES.prefix.variable_name, modifiers=frozenset()
        ),
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
    argnames="case",
    argvalues=_CASES.records,
    ids=lambda case: case.language.__name__,
)
def test_unwrapped_record_preamble_golden(
    *,
    case: _RecordCase,
    cases_dir: Path,
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
    lang_cls = case.language
    spec = lang_cls(
        heterogeneous_strategy=lang_cls.HeterogeneousStrategies["RECORD"],
    )
    result = literalizer.literalize(
        source=(cases_dir / _CASES.record_input_case / "input.yaml").read_text(
            encoding="utf-8"
        ),
        input_format=InputFormat.YAML,
        language=spec,
        wrap_in_file=False,
    )
    assert len(result.preamble) > 0
    assert len(result.body_preamble) == 0
    assert result.code == case.expected_code
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
