"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

if TYPE_CHECKING:
    from collections.abc import Callable

_CASES_DIR = Path(__file__).parent / "cases"


def _wrap_identity(content: str) -> str:
    """Return content unchanged."""
    return content


def _wrap_js(content: str) -> str:
    """Wrap in ``void(...)`` so bare object/array literals parse as
    expressions in JavaScript and TypeScript.
    """
    return f"void (\n{content}\n)"


def _wrap_go(content: str) -> str:
    """Wrap in a Go package-level variable declaration."""
    return f"package main\n\nvar _ = {content}"


def _wrap_java(content: str) -> str:
    """Wrap in a Java class with necessary imports."""
    return f"""\
import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


def _wrap_kotlin(content: str) -> str:
    """Wrap in a Kotlin variable assignment."""
    return f"val x: Any? = {content}"


def _wrap_cpp(content: str) -> str:
    """Wrap in a C++ struct and function for type-flexible
    initialization.
    """
    return (
        "#include <initializer_list>\n"
        "#include <cstddef>\n"
        "struct _Any {\n"
        "    template<class T> _Any(T&&) noexcept {}\n"
        "    _Any(std::initializer_list<_Any>) noexcept {}\n"
        "};\n"
        "void _check() {\n"
        f"    [[maybe_unused]] _Any _v = {content};\n"
        "}"
    )


def _wrap_csharp(content: str) -> str:
    """Wrap in C# using statement and variable assignment."""
    return f"""\
using System.Collections.Generic;
var x = {content};"""


_LANGUAGES: dict[str, tuple[literalizer.LanguageSpec, str]] = {
    "python": (literalizer.PYTHON, ".py"),
    "javascript": (literalizer.JAVASCRIPT, ".js"),
    "typescript": (literalizer.TYPESCRIPT, ".ts"),
    "kotlin": (literalizer.KOTLIN, ".kts"),
    "ruby": (literalizer.RUBY, ".rb"),
    "go": (literalizer.GO, ".go"),
    "java": (literalizer.JAVA, ".java"),
    "csharp": (literalizer.CSHARP, ".cs"),
    "cpp": (literalizer.CPP, ".cpp"),
}

_WRAPPERS: dict[str, Callable[[str], str]] = {
    "python": _wrap_identity,
    "ruby": _wrap_identity,
    "javascript": _wrap_js,
    "typescript": _wrap_js,
    "go": _wrap_go,
    "java": _wrap_java,
    "kotlin": _wrap_kotlin,
    "cpp": _wrap_cpp,
    "csharp": _wrap_csharp,
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
    wrapped = _WRAPPERS[language](result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=extension,
        fullpath=input_path.parent / (language + extension),
    )
