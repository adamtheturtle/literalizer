"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language, using the real file extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.
"""

from __future__ import annotations

import dataclasses
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


def _wrap_php(content: str) -> str:
    """Wrap in a PHP script variable assignment."""
    return f"<?php\n$x = {content};"


def _wrap_python_datetime(content: str) -> str:
    """Wrap with a datetime import for native Python date literals."""
    return f"import datetime\n{content}"


def _wrap_java_time(content: str) -> str:
    """Wrap in a Java class with java.time.* imports."""
    return f"""\
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


def _wrap_kotlin_time(content: str) -> str:
    """Wrap in a Kotlin variable assignment with java.time imports."""
    return (
        f"import java.time.LocalDate\n"
        f"import java.time.LocalDateTime\n"
        f"val x: Any? = {content}"
    )


def _wrap_go_time(content: str) -> str:
    """Wrap in a Go package with the time package imported."""
    return f'package main\n\nimport "time"\n\nvar _ = {content}'


def _wrap_cpp_chrono(content: str) -> str:
    """Wrap in C++ with the chrono header included."""
    return (
        "#include <chrono>\n"
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


def _wrap_csharp_date(content: str) -> str:
    """Wrap in C# with System and Collections.Generic namespaces."""
    return (
        f"using System;\nusing System.Collections.Generic;\nvar x = {content};"
    )


def _wrap_ruby_date(content: str) -> str:
    """Wrap with require 'date' for Ruby Date literals."""
    return f"require 'date'\n{content}"


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with spec, file extension, and wrapper."""

    spec: literalizer.LanguageSpec
    extension: str
    wrap: Callable[[str], str]


_LANGUAGES: dict[str, _LanguageConfig] = {
    "python": _LanguageConfig(
        spec=literalizer.PYTHON,
        extension=".py",
        wrap=_wrap_identity,
    ),
    "javascript": _LanguageConfig(
        spec=literalizer.JAVASCRIPT,
        extension=".js",
        wrap=_wrap_js,
    ),
    "typescript": _LanguageConfig(
        spec=literalizer.TYPESCRIPT,
        extension=".ts",
        wrap=_wrap_js,
    ),
    "kotlin": _LanguageConfig(
        spec=literalizer.KOTLIN,
        extension=".kts",
        wrap=_wrap_kotlin,
    ),
    "ruby": _LanguageConfig(
        spec=literalizer.RUBY,
        extension=".rb",
        wrap=_wrap_identity,
    ),
    "go": _LanguageConfig(
        spec=literalizer.GO,
        extension=".go",
        wrap=_wrap_go,
    ),
    "java": _LanguageConfig(
        spec=literalizer.JAVA,
        extension=".java",
        wrap=_wrap_java,
    ),
    "csharp": _LanguageConfig(
        spec=literalizer.CSHARP,
        extension=".cs",
        wrap=_wrap_csharp,
    ),
    "cpp": _LanguageConfig(
        spec=literalizer.CPP,
        extension=".cpp",
        wrap=_wrap_cpp,
    ),
    "php": _LanguageConfig(
        spec=literalizer.PHP,
        extension=".php",
        wrap=_wrap_php,
    ),
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
    lang_config = _LANGUAGES[language]
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        prefix="",
        wrap=True,
    )
    wrapped = lang_config.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=input_path.parent / (language + lang_config.extension),
    )


_DATE_FORMAT_LANGUAGES: dict[str, _LanguageConfig] = {
    "python_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.PYTHON,
            format_date=literalizer.format_date_python,
            format_datetime=literalizer.format_datetime_python,
        ),
        extension=".py",
        wrap=_wrap_python_datetime,
    ),
    "python_epoch": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.PYTHON,
            format_datetime=literalizer.format_datetime_epoch,
        ),
        extension=".py",
        wrap=_wrap_identity,
    ),
    "java_instant": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.JAVA,
            format_date=literalizer.format_date_java,
            format_datetime=literalizer.format_datetime_java_instant,
        ),
        extension=".java",
        wrap=_wrap_java_time,
    ),
    "java_zoned": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.JAVA,
            format_date=literalizer.format_date_java,
            format_datetime=literalizer.format_datetime_java_zoned,
        ),
        extension=".java",
        wrap=_wrap_java_time,
    ),
    "kotlin_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.KOTLIN,
            format_date=literalizer.format_date_kotlin,
            format_datetime=literalizer.format_datetime_kotlin,
        ),
        extension=".kts",
        wrap=_wrap_kotlin_time,
    ),
    "ruby_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.RUBY,
            format_date=literalizer.format_date_ruby,
            format_datetime=literalizer.format_datetime_ruby,
        ),
        extension=".rb",
        wrap=_wrap_ruby_date,
    ),
    "js_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.JAVASCRIPT,
            format_date=literalizer.format_date_js,
            format_datetime=literalizer.format_datetime_js,
        ),
        extension=".js",
        wrap=_wrap_js,
    ),
    "ts_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.TYPESCRIPT,
            format_date=literalizer.format_date_js,
            format_datetime=literalizer.format_datetime_js,
        ),
        extension=".ts",
        wrap=_wrap_js,
    ),
    "csharp_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.CSHARP,
            format_date=literalizer.format_date_csharp,
            format_datetime=literalizer.format_datetime_csharp,
        ),
        extension=".cs",
        wrap=_wrap_csharp_date,
    ),
    "go_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.GO,
            format_date=literalizer.format_date_go,
            format_datetime=literalizer.format_datetime_go,
        ),
        extension=".go",
        wrap=_wrap_go_time,
    ),
    "cpp_native": _LanguageConfig(
        spec=dataclasses.replace(
            literalizer.CPP,
            format_date=literalizer.format_date_cpp,
            format_datetime=literalizer.format_datetime_cpp,
        ),
        extension=".cpp",
        wrap=_wrap_cpp_chrono,
    ),
}

_DATE_FORMAT_CASES = list(_DATE_FORMAT_LANGUAGES.keys())
_DATES_CASE_DIR = _CASES_DIR / "dates"


@pytest.mark.parametrize(
    argnames="language",
    argvalues=_DATE_FORMAT_CASES,
    ids=_DATE_FORMAT_CASES,
)
def test_date_format_golden_file(
    language: str,
    file_regression: FileRegressionFixture,
) -> None:
    """Test native date format variants against golden files."""
    lang_config = _DATE_FORMAT_LANGUAGES[language]
    yaml_string = (_DATES_CASE_DIR / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=lang_config.spec,
        prefix="",
        wrap=True,
    )
    wrapped = lang_config.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=_DATES_CASE_DIR / (language + lang_config.extension),
    )
