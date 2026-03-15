"""Integration tests that compare literalize_yaml output against golden
files.

Each subdirectory contains an ``input.yaml`` and one expected-output file
per supported language per supported formatter pair, using the real file
extension for that language.

Golden files contain syntactically valid programs so that pre-commit hooks
can syntax-check them directly without additional wrapping.
"""

from __future__ import annotations

import dataclasses
import datetime
from collections.abc import Callable  # noqa: TC003
from pathlib import Path

import pytest
from pytest_regressions.file_regression import FileRegressionFixture

import literalizer

_CASES_DIR = Path(__file__).parent / "cases"


def _wrap_identity(content: str) -> str:
    """Return content unchanged."""
    return content


def _wrap_python(content: str) -> str:
    """Wrap with a datetime import so date/datetime literals are valid."""
    return f"import datetime\n{content}"


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
import java.time.Instant;
import java.time.LocalDate;
import java.time.ZonedDateTime;
import java.time.ZoneId;
import java.util.Map;
import java.util.Set;
class Check {{
    Object x = {content};
}}"""


def _wrap_kotlin(content: str) -> str:
    """Wrap in a Kotlin variable assignment."""
    return (
        "import java.time.LocalDate\n"
        "import java.time.LocalDateTime\n"
        f"val x: Any? = {content}"
    )


def _wrap_cpp(content: str) -> str:
    """Wrap in a C++ struct and function for type-flexible
    initialization.
    """
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


def _wrap_csharp(content: str) -> str:
    """Wrap in C# using statement and variable assignment."""
    return f"""\
using System.Collections.Generic;
var x = {content};"""


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

_WRAPPERS: dict[str, Callable[[str], str]] = {
    "python": _wrap_python,
    "ruby": _wrap_identity,
    "javascript": _wrap_js,
    "typescript": _wrap_js,
    "go": _wrap_go,
    "java": _wrap_java,
    "kotlin": _wrap_kotlin,
    "cpp": _wrap_cpp,
    "csharp": _wrap_csharp,
}


@dataclasses.dataclass(frozen=True)
class _FormatterPair:
    """A named pair of date and datetime format functions."""

    name: str
    format_date: Callable[[datetime.date], str]
    format_datetime: Callable[[datetime.datetime], str]


_LANGUAGE_FORMATTERS: dict[str, list[_FormatterPair]] = {
    "python": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "python",
            literalizer.format_date_python,
            literalizer.format_datetime_python,
        ),
    ],
    "javascript": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "js",
            literalizer.format_date_js,
            literalizer.format_datetime_js,
        ),
    ],
    "typescript": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "js",
            literalizer.format_date_js,
            literalizer.format_datetime_js,
        ),
    ],
    "ruby": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "ruby",
            literalizer.format_date_ruby,
            literalizer.format_datetime_ruby,
        ),
    ],
    "go": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "go",
            literalizer.format_date_go,
            literalizer.format_datetime_go,
        ),
    ],
    "java": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "java_instant",
            literalizer.format_date_java,
            literalizer.format_datetime_java_instant,
        ),
        _FormatterPair(  # type: ignore[misc]
            "java_zoned",
            literalizer.format_date_java,
            literalizer.format_datetime_java_zoned,
        ),
    ],
    "kotlin": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "kotlin",
            literalizer.format_date_kotlin,
            literalizer.format_datetime_kotlin,
        ),
    ],
    "csharp": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
        _FormatterPair(  # type: ignore[misc]
            "csharp",
            literalizer.format_date_csharp,
            literalizer.format_datetime_csharp,
        ),
    ],
    "cpp": [
        _FormatterPair(  # type: ignore[misc]
            "iso",
            literalizer.format_date_iso,
            literalizer.format_datetime_iso,
        ),
    ],
}


def _yaml_has_dates(input_path: Path) -> bool:
    """Return True if the YAML input contains any date or datetime
    values.
    """
    from ruamel.yaml import YAML  # noqa: PLC0415

    yaml = YAML()
    data = yaml.load(input_path)

    def _contains_date(obj: object) -> bool:
        """Return True if obj or any nested value is a date/datetime."""
        if isinstance(obj, datetime.date):
            return True
        if isinstance(obj, dict):
            return any(_contains_date(v) for v in obj.values())
        if isinstance(obj, list):
            return any(_contains_date(v) for v in obj)
        return False

    return _contains_date(data)


def _discover_cases() -> list[tuple[str, str, str, Path]]:
    """Return ``(case_name, language, formatter_name, input_path)`` tuples.

    For cases with date/datetime values every formatter pair is emitted
    so that each formatter's output is checked.  For date-free cases only
    the ``iso`` pair is emitted, since all formatters produce identical
    output when there are no dates to format.
    """
    cases: list[tuple[str, str, str, Path]] = []
    for case_dir in sorted(_CASES_DIR.iterdir()):
        input_path = case_dir / "input.yaml"
        has_dates = _yaml_has_dates(input_path)
        for lang_name, formatter_pairs in _LANGUAGE_FORMATTERS.items():
            pairs = formatter_pairs if has_dates else formatter_pairs[:1]
            cases.extend(
                (case_dir.name, lang_name, fp.name, input_path) for fp in pairs
            )
    return cases


_CASES = _discover_cases()


@pytest.mark.parametrize(
    argnames=("_case_name", "language", "formatter_name", "input_path"),
    argvalues=_CASES,
    ids=[f"{c[0]}/{c[1]}/{c[2]}" for c in _CASES],
)
def test_golden_file(
    _case_name: str,
    language: str,
    formatter_name: str,
    input_path: Path,
    file_regression: FileRegressionFixture,
) -> None:
    """Test that literalize_yaml output matches expected golden file."""
    base_spec, extension = _LANGUAGES[language]
    formatters = _LANGUAGE_FORMATTERS[language]
    formatter_pair = next(fp for fp in formatters if fp.name == formatter_name)
    spec = dataclasses.replace(
        base_spec,
        format_date=formatter_pair.format_date,
        format_datetime=formatter_pair.format_datetime,
    )
    yaml_string = input_path.read_text()
    result = literalizer.literalize_yaml(
        yaml_string=yaml_string,
        language=spec,
        prefix="",
        wrap=True,
    )
    wrapped = _WRAPPERS[language](result)
    filename = f"{language}_{formatter_name}{extension}"
    file_regression.check(
        contents=wrapped + "\n",
        extension=extension,
        fullpath=input_path.parent / filename,
    )
