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
import re
from pathlib import Path
from typing import cast

import pytest
from beartype import beartype
from pytest_regressions.file_regression import FileRegressionFixture
from ruamel.yaml import YAML as _YAML

import literalizer
from literalizer.exceptions import (
    CallArgNotSupportedError,
    HeterogeneousCollectionError,
)

from .case_discovery import (
    LITERALIZE_REF_CASE_CONFIGS,
    LiteralizeRefCaseConfig,
)
from .check_golden import check_golden
from .language_specs import sorted_languages, with_per_fixture_module_name
from .variant_cases import wrap_variable_form


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


def _collect_ref_names(data: object) -> list[str]:
    """Recursively collect all ``$ref`` name values from parsed data."""
    if isinstance(data, dict):
        typed_data = cast("dict[object, object]", data)
        if len(typed_data) == 1 and "$ref" in typed_data:
            name = typed_data["$ref"]
            return [name] if isinstance(name, str) else []
        return [
            n for v in typed_data.values() for n in _collect_ref_names(data=v)
        ]
    if isinstance(data, list):
        typed_list = cast("list[object]", data)
        return [
            n for item in typed_list for n in _collect_ref_names(data=item)
        ]
    return []


_STUB_ASSIGN_LINE_RE = re.compile(pattern=r"^\w+\s*=(?!=)")


def _split_stubs(
    stub_codes: list[str],
) -> tuple[list[str], list[str]]:
    """Split each stub code into declaration lines and assignment lines.

    The split point is the first line (after stripping leading whitespace)
    that looks like
    ``identifier =``, indicating the start of an executable assignment.
    Lines before that point are type/signature declarations; from that
    point on are executable statements.
    """
    decl_lines: list[str] = []
    assign_lines: list[str] = []
    for stub_code in stub_codes:
        stub_lines = stub_code.split(sep="\n")
        split_idx = len(stub_lines)
        for j, stub_line in enumerate(iterable=stub_lines):
            if _STUB_ASSIGN_LINE_RE.match(stub_line.lstrip()):
                split_idx = j
                break
        decl_lines.extend(stub_lines[:split_idx])
        assign_lines.extend(stub_lines[split_idx:])
    return decl_lines, assign_lines


def _find_first_occurrence(lines: list[str], lower_name: str) -> int | None:
    """Return the index of the first line containing ``lower_name`` that
    is not immediately preceded by ``[``.
    """
    for i, line in enumerate(iterable=lines):
        idx = line.lower().find(lower_name)
        if idx == -1:
            continue
        if idx > 0 and line[idx - 1] == "[":
            continue
        return i
    return None


def _find_assignment_line(lines: list[str], lower_name: str) -> int | None:
    """Return the index of the first line whose stripped content starts
    with ``lower_name`` followed by a non-identifier character.

    This locates the main-variable assignment (as opposed to a type
    declaration that merely mentions the variable name).
    """
    for i, line in enumerate(iterable=lines):
        lower_stripped = line.lstrip().lower()
        if not lower_stripped.startswith(lower_name):
            continue
        post = len(lower_name)
        if post < len(lower_stripped) and (
            lower_stripped[post].isalnum() or lower_stripped[post] == "_"
        ):
            continue
        raw_idx = line.lower().find(lower_name)
        if raw_idx > 0 and line[raw_idx - 1] == "[":
            continue
        return i
    return None


def inject_stubs_before_variable(
    code: str,
    variable_name: str,
    stub_codes: list[str],
) -> str:
    """Insert stub declarations before ``variable_name`` using a
    case-insensitive match.

    For languages like Fortran where ``declaration_code`` contains both
    a type-declaration statement and an executable assignment, the stubs
    are split at the first assignment line (detected by
    ``identifier =``) and injected in two phases so that all
    declarations precede all executable statements:

    1. Declaration lines of each stub are inserted before the first
       line that contains ``variable_name``.
    2. Assignment lines of each stub are inserted before the first line
       whose content (after stripping leading whitespace) *starts with*
       ``variable_name`` (the main-variable's own assignment).

    For languages where declaration and assignment are on the same line
    (Python, C, JavaScript, …) both injection points coincide and the
    behavior is identical to a single-location insert.

    The case-insensitive search handles languages such as Erlang that
    capitalize variable names in output (e.g. ``my_data`` →
    ``My_data``).  Matches where the variable name is immediately
    preceded by ``[`` are skipped to avoid false positives on
    module-declaration lines in Roc such as ``module [my_data]``.
    """
    if not stub_codes or not variable_name:
        return code

    decl_stub_lines, assign_stub_lines = _split_stubs(stub_codes=stub_codes)
    lines = code.split(sep="\n")
    lower_name = variable_name.lower()

    decl_idx = _find_first_occurrence(lines=lines, lower_name=lower_name)
    if decl_idx is None:
        return code

    assign_idx = _find_assignment_line(lines=lines, lower_name=lower_name)

    indent = len(lines[decl_idx]) - len(lines[decl_idx].lstrip())
    prefix = " " * indent

    def _indented(stub_line_list: list[str]) -> list[str]:
        """Apply the main variable's indentation prefix to stub lines."""
        return [prefix + sl if sl else "" for sl in stub_line_list]

    if assign_idx is None or assign_idx == decl_idx:
        all_stub = decl_stub_lines + assign_stub_lines
        return "\n".join(
            lines[:decl_idx] + _indented(all_stub) + lines[decl_idx:]
        )

    result = list(lines)
    if decl_stub_lines:
        result = (
            result[:decl_idx] + _indented(decl_stub_lines) + result[decl_idx:]
        )
    adjusted_assign = assign_idx + len(decl_stub_lines)
    if assign_stub_lines:
        result = (
            result[:adjusted_assign]
            + _indented(assign_stub_lines)
            + result[adjusted_assign:]
        )
    return "\n".join(result)


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
    identifier is spelled idiomatically for each language.  A stub
    declaration for each referenced identifier is injected before the
    first use so the golden file is a complete unit that can be compiled.
    """
    input_path = cases_dir / config.case_dir_name / "input.yaml"
    yaml_string = input_path.read_text()
    golden_path = input_path.parent / (golden_name + lang_cls.extension)
    spec = with_per_fixture_module_name(spec=spec, golden_path=golden_path)
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
    final_code = result.code
    if wrap_variable_form(lang_cls=lang_cls) is not None:
        ruamel_yaml = _YAML()
        raw_data: object = ruamel_yaml.load(  # pyright: ignore[reportUnknownMemberType]
            stream=yaml_string,
        )
        stub_codes: list[str] = []
        for raw_name in _collect_ref_names(data=raw_data):
            converted_name = ref_case.convert(name=raw_name)
            stub = literalizer.literalize(
                source='{"_": "_"}',
                input_format=literalizer.InputFormat.JSON,
                language=spec,
                variable_form=literalizer.NewVariable(
                    name=converted_name,
                ),
                wrap_in_file=False,
            )
            stub_codes.append(stub.declaration_code)
        variable_form_obj = wrap_variable_form(lang_cls=lang_cls)
        final_code = inject_stubs_before_variable(
            code=result.code,
            variable_name=variable_form_obj.name if variable_form_obj else "",
            stub_codes=stub_codes,
        )
    check_golden(
        file_regression=file_regression,
        contents=final_code + "\n",
        extension=lang_cls.extension,
        newline="",
        golden_path=golden_path,
    )
