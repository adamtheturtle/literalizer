"""Python multiline golden fixtures preserve their declared input
values.
"""

import ast
import json
import runpy
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from literalizer import BothVariableForms, InputFormat
from literalizer.languages import Python
from tests.yaml_support import as_yaml_parser

from .case_manifests import case_input
from .language_specs import make_golden_path
from .variant_cases import build_variant_cases
from .variant_types import VariantCase


def _assignment_values(
    *, tree: ast.Module, evaluation_path: Path, variable_name: str
) -> list[object]:
    """Execute each assignment with the imports and bindings preceding
    it.
    """
    values: list[object] = []
    for index, node in enumerate(iterable=tree.body):
        if isinstance(node, ast.Assign):
            prefix = ast.Module(body=tree.body[: index + 1], type_ignores=[])
            _ = evaluation_path.write_text(
                data=ast.unparse(ast_obj=prefix), encoding="utf-8"
            )
            namespace = runpy.run_path(path_name=str(object=evaluation_path))
            values.append(namespace[variable_name])
    return values


@pytest.mark.parametrize(
    argnames="case",
    argvalues=[
        case
        for case in build_variant_cases()
        if case.variant.lang_cls is Python
        and case.variant.spec.string_format is Python.string_formats.MULTILINE
    ],
    ids=lambda case: f"{case.case_dir_name}/{case.variant_name}",
)
def test_multiline_string_golden_roundtrip(
    case: VariantCase,
    cases_dir: Path,
    tmp_path: Path,
) -> None:
    """Every emitted assignment retains leading, nested and trailing
    whitespace.

    The rendering suite compares public API output with these same files.
    Executing their assignments also prevents accepting a regenerated golden
    that changes the source value while remaining valid Python.
    """
    input_info = case_input(case_dir=cases_dir / case.case_dir_name)
    source = input_info.path.read_text(encoding="utf-8")
    if input_info.input_format is InputFormat.JSON:
        expected = json.loads(s=source)
    else:
        assert input_info.input_format is InputFormat.YAML
        expected = as_yaml_parser(parser=YAML(typ="safe")).load(stream=source)
    spec = case.variant.spec
    golden_path = make_golden_path(
        parent=input_info.path.parent,
        name=case.variant_name,
        extension=spec.extension,
        lang_cls=case.variant.lang_cls,
        version=spec.language_version,
    )
    tree = ast.parse(source=golden_path.read_text(encoding="utf-8"))
    values = _assignment_values(
        tree=tree,
        evaluation_path=tmp_path / "roundtrip.py",
        variable_name=case.variable_form.name,
    )
    assignment_count = (
        2 if isinstance(case.variable_form, BothVariableForms) else 1
    )
    if spec.sequence_format is Python.sequence_formats.LIST:
        assert values == [expected] * assignment_count
    else:
        # Default tuple output preserves the source's JSON/YAML array shape.
        assert (
            json.loads(s=json.dumps(obj=values))
            == [expected] * assignment_count
        )
