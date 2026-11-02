"""Declarations and paths for unwrapped result-view golden files."""

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, TypeAdapter

from tests.toml_cases import load_toml_cases

from .case_manifests import ManifestLanguages
from .language_specs import make_golden_path


class _PrefixCases(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """Declared languages and result views for a commented scalar."""

    languages: ManifestLanguages
    input_case: str
    attributes: tuple[Literal["code", "bare_code"], ...]
    variable_name: str


class _ResultCases(
    BaseModel, arbitrary_types_allowed=True, extra="forbid", frozen=True
):
    """TOML-owned inputs and expectations for unwrapped result views."""

    prefix: _PrefixCases
    record_input_case: str
    records: ManifestLanguages


RESULT_CASES = TypeAdapter(type=_ResultCases).validate_python(
    load_toml_cases(name="unwrapped_literalize_results"),
)


def result_view_golden_paths(*, cases_dir: Path) -> set[Path]:
    """Return the compiling paths owned by the result-view runner."""
    return {
        make_golden_path(
            parent=cases_dir / RESULT_CASES.prefix.input_case,
            name=f"{lang_cls.__name__}_unwrapped_{attribute}",
            extension=lang_cls.extension,
            lang_cls=lang_cls,
            version=lang_cls().language_version,
        )
        for lang_cls in RESULT_CASES.prefix.languages
        for attribute in RESULT_CASES.prefix.attributes
    }
