"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

_CASES_DIR = Path(__file__).parent / "cases"

_LANGUAGES: dict[str, tuple[literalizer.LanguageSpec, str]] = {
    "python": (literalizer.PYTHON, ".py"),
    "javascript": (literalizer.JAVASCRIPT, ".js"),
    "typescript": (literalizer.TYPESCRIPT, ".ts"),
    "kotlin": (literalizer.KOTLIN, ".kt"),
    "ruby": (literalizer.RUBY, ".rb"),
    "go": (literalizer.GO, ".go"),
    "java": (literalizer.JAVA, ".java"),
    "csharp": (literalizer.CSHARP, ".cs"),
    "cpp": (literalizer.CPP, ".cpp"),
}


def _discover_cases() -> list[tuple[str, str, Path]]:
    """Return ``(case_name, language, input_path)`` tuples."""
    cases: list[tuple[str, str, Path]] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        cases.extend(
            (case_dir.name, lang_name, case_dir / "input.yaml")
            for lang_name in _LANGUAGES
        )
    return cases


_CASES = _discover_cases()


@pytest.mark.parametrize(
    argnames=("_case_name", "language", "input_path"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}" for c in _CASES],
)
def test_golden_file(
    _case_name: str,
    language: str,
    input_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    spec, extension = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        prefix="",
        wrap=True,
    )
    file_regression.check(
        contents=result + "\n",
        extension=extension,
        fullpath=input_path.parent / language,
    )
