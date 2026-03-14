"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one ``<language>.txt`` file
per supported language.  The test reads the YAML, literalizes it for each
language, and asserts that the result matches the golden file.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import literalizer

_INTEGRATION_DIR = Path(__file__).parent

_LANGUAGES: dict[str, literalizer.LanguageSpec] = {
    "python": literalizer.PYTHON,
    "javascript": literalizer.JAVASCRIPT,
    "typescript": literalizer.TYPESCRIPT,
    "kotlin": literalizer.KOTLIN,
    "ruby": literalizer.RUBY,
    "go": literalizer.GO,
    "java": literalizer.JAVA,
    "csharp": literalizer.CSHARP,
    "cpp": literalizer.CPP,
}


def _discover_cases() -> list[tuple[str, str, Path, Path]]:
    """Return ``(case_name, language, input_path, expected_path)``
    tuples.
    """
    cases: list[tuple[str, str, Path, Path]] = []
    for case_dir in sorted(_INTEGRATION_DIR.iterdir()):
        input_path = case_dir / "input.yaml"
        if not input_path.is_file():
            continue
        for lang_name in _LANGUAGES:
            expected_path = case_dir / f"{lang_name}.txt"
            if expected_path.is_file():
                cases.append(
                    (case_dir.name, lang_name, input_path, expected_path)
                )
    return cases


@pytest.mark.parametrize(  # type: ignore[misc]
    ("case_name", "language", "input_path", "expected_path"),
    _discover_cases(),
    ids=[f"{c[0]}/{c[1]}" for c in _discover_cases()],
)
def test_golden_file(
    case_name: str,
    language: str,
    input_path: Path,
    expected_path: Path,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    yaml_string = input_path.read_text()
    expected = expected_path.read_text().rstrip("\n")
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=_LANGUAGES[language],
        prefix="",
        wrap=False,
    )
    if result != expected:
        msg = (
            f"Mismatch for {case_name}/{language}:\n"
            f"Expected:\n{expected}\n\nGot:\n{result}"
        )
        raise AssertionError(msg)
