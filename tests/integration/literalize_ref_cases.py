"""``literalize`` golden-file case configuration and runner for ``$ref``
support.

The configurations describe how each ``cases/literalize_ref_*`` directory is
driven through :func:`literalizer.literalize` with a ``ref_case`` set to the
language's default identifier case.  The runner
(``run_literalize_ref_golden_case``) is shared by
``test_literalize_ref_golden_file``.
"""

import dataclasses
import functools
from pathlib import Path

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
)

from .check_golden import check_golden
from .language_specs import sorted_languages, with_per_fixture_module_name
from .variant_cases import wrap_variable_form


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCaseConfig:
    """Configuration for a ``literalize`` ``$ref`` golden-file test
    case.
    """

    case_dir_name: str


LITERALIZE_REF_CASE_CONFIGS: list[LiteralizeRefCaseConfig] = [
    LiteralizeRefCaseConfig(case_dir_name="literalize_ref_whole"),
    LiteralizeRefCaseConfig(case_dir_name="literalize_ref_in_dict"),
    LiteralizeRefCaseConfig(case_dir_name="literalize_ref_in_list"),
]


@dataclasses.dataclass(frozen=True)
class LiteralizeRefCase:
    """A parameterized literalize-ref golden-file test case."""

    config: LiteralizeRefCaseConfig
    lang_cls: literalizer.LanguageCls


@functools.cache
@beartype
def discover_literalize_ref_cases() -> list[LiteralizeRefCase]:
    """Return literalize-ref test cases for all languages."""
    return [
        LiteralizeRefCase(config=config, lang_cls=lang_cls)
        for config in LITERALIZE_REF_CASE_CONFIGS
        for lang_cls in sorted_languages()
    ]


@beartype
def run_literalize_ref_golden_case(
    *,
    config: LiteralizeRefCaseConfig,
    lang_cls: literalizer.LanguageCls,
    spec: literalizer.Language,
    golden_name: str,
    cases_dir: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Run a literalize ``$ref`` golden-file case against *golden_name*.

    Uses the language's first (default) identifier case so the ref
    identifier is spelled idiomatically for each language.
    """
    input_path = cases_dir / config.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    golden_path = input_path.parent / (golden_name + lang_cls.extension)
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
    if not spec.identifier_cases:
        golden_path.unlink(missing_ok=True)
        pytest.skip(f"{lang_cls.__name__} has no identifier cases")
    ref_case = spec.identifier_cases[0]
    try:
        result = literalizer.literalize(
            source=yaml_string,
            input_format=literalizer.InputFormat.YAML,
            language=spec,
            variable_form=wrap_variable_form(lang_cls=lang_cls),
            wrap_in_file=True,
            ref_case=ref_case,
        )
    except HeterogeneousCollectionError:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} cannot represent this heterogeneous input",
        )
    except CallArgNotSupportedError as exc:
        golden_path.unlink(missing_ok=True)
        pytest.skip(
            f"{lang_cls.__name__} rejected ref identifier: {exc.reason}"
        )
    check_golden(
        file_regression=file_regression,
        contents=result.code + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=golden_path,
    )
