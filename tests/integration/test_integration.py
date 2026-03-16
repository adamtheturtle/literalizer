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
    import datetime
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
class _DateVariant:
    """A date/datetime formatting variant for a language."""

    name: str
    format_date: Callable[[datetime.date], str] | None
    format_datetime: Callable[[datetime.datetime], str]
    wrap: Callable[[str], str]


@dataclasses.dataclass
class _LanguageConfig:
    """Language configuration with spec, file extension, and wrapper."""

    spec: literalizer.LanguageSpec
    extension: str
    wrap: Callable[[str], str]
    date_variants: tuple[_DateVariant, ...] = ()


_LANGUAGES: dict[str, _LanguageConfig] = {
    "python": _LanguageConfig(
        spec=literalizer.PYTHON,
        extension=".py",
        wrap=_wrap_identity,
        date_variants=(
            _DateVariant(
                name="python_native",
                format_date=literalizer.format_date_python,
                format_datetime=literalizer.format_datetime_python,
                wrap=_wrap_python_datetime,
            ),
            _DateVariant(
                name="python_epoch",
                format_date=None,
                format_datetime=literalizer.format_datetime_epoch,
                wrap=_wrap_identity,
            ),
        ),
    ),
    "javascript": _LanguageConfig(
        spec=literalizer.JAVASCRIPT,
        extension=".js",
        wrap=_wrap_js,
        date_variants=(
            _DateVariant(
                name="js_native",
                format_date=literalizer.format_date_js,
                format_datetime=literalizer.format_datetime_js,
                wrap=_wrap_js,
            ),
        ),
    ),
    "typescript": _LanguageConfig(
        spec=literalizer.TYPESCRIPT,
        extension=".ts",
        wrap=_wrap_js,
        date_variants=(
            _DateVariant(
                name="ts_native",
                format_date=literalizer.format_date_js,
                format_datetime=literalizer.format_datetime_js,
                wrap=_wrap_js,
            ),
        ),
    ),
    "kotlin": _LanguageConfig(
        spec=literalizer.KOTLIN,
        extension=".kts",
        wrap=_wrap_kotlin,
        date_variants=(
            _DateVariant(
                name="kotlin_native",
                format_date=literalizer.format_date_kotlin,
                format_datetime=literalizer.format_datetime_kotlin,
                wrap=_wrap_kotlin_time,
            ),
        ),
    ),
    "ruby": _LanguageConfig(
        spec=literalizer.RUBY,
        extension=".rb",
        wrap=_wrap_identity,
        date_variants=(
            _DateVariant(
                name="ruby_native",
                format_date=literalizer.format_date_ruby,
                format_datetime=literalizer.format_datetime_ruby,
                wrap=_wrap_ruby_date,
            ),
        ),
    ),
    "go": _LanguageConfig(
        spec=literalizer.GO,
        extension=".go",
        wrap=_wrap_go,
        date_variants=(
            _DateVariant(
                name="go_native",
                format_date=literalizer.format_date_go,
                format_datetime=literalizer.format_datetime_go,
                wrap=_wrap_go_time,
            ),
        ),
    ),
    "java": _LanguageConfig(
        spec=literalizer.JAVA,
        extension=".java",
        wrap=_wrap_java,
        date_variants=(
            _DateVariant(
                name="java_instant",
                format_date=literalizer.format_date_java,
                format_datetime=literalizer.format_datetime_java_instant,
                wrap=_wrap_java_time,
            ),
            _DateVariant(
                name="java_zoned",
                format_date=literalizer.format_date_java,
                format_datetime=literalizer.format_datetime_java_zoned,
                wrap=_wrap_java_time,
            ),
        ),
    ),
    "csharp": _LanguageConfig(
        spec=literalizer.CSHARP,
        extension=".cs",
        wrap=_wrap_csharp,
        date_variants=(
            _DateVariant(
                name="csharp_native",
                format_date=literalizer.format_date_csharp,
                format_datetime=literalizer.format_datetime_csharp,
                wrap=_wrap_csharp_date,
            ),
        ),
    ),
    "cpp": _LanguageConfig(
        spec=literalizer.CPP,
        extension=".cpp",
        wrap=_wrap_cpp,
        date_variants=(
            _DateVariant(
                name="cpp_native",
                format_date=literalizer.format_date_cpp,
                format_datetime=literalizer.format_datetime_cpp,
                wrap=_wrap_cpp_chrono,
            ),
        ),
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


_DATES_CASE_DIR = _CASES_DIR / "dates"

_DATE_VARIANT_CASES: list[tuple[str, _LanguageConfig, _DateVariant]] = [
    (variant.name, lang_config, variant)
    for lang_config in _LANGUAGES.values()
    for variant in lang_config.date_variants
]


@pytest.mark.parametrize(
    argnames=("variant_name", "lang_config", "variant"),
    argvalues=_DATE_VARIANT_CASES,
    ids=[c[0] for c in _DATE_VARIANT_CASES],
)
def test_date_format_golden_file(
    variant_name: str,
    lang_config: _LanguageConfig,
    variant: _DateVariant,
    file_regression: FileRegressionFixture,
) -> None:
    """Test native date format variants against golden files."""
    if variant.format_date is not None:
        spec = dataclasses.replace(
            lang_config.spec,
            format_date=variant.format_date,
            format_datetime=variant.format_datetime,
        )
    else:
        spec = dataclasses.replace(
            lang_config.spec,
            format_datetime=variant.format_datetime,
        )
    yaml_string = (_DATES_CASE_DIR / "input.yaml").read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        prefix="",
        wrap=True,
    )
    wrapped = variant.wrap(result)
    file_regression.check(
        contents=wrapped + "\n",
        extension=lang_config.extension,
        fullpath=_DATES_CASE_DIR / (variant_name + lang_config.extension),
    )
