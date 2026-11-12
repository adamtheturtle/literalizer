"""Complete Python multiline golden programs retain their input values."""

import json
import subprocess
import sys
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

_CHECK_PROGRAM = """\
import json
import sys
from pathlib import Path

path, variable_name, expected_json, assignment_count, sequence_format = (
    sys.argv[1:]
)
expected = json.loads(expected_json)
values = []

class Namespace(dict):
    def __setitem__(self, name, value):
        super().__setitem__(name, value)
        if name == variable_name:
            values.append(value)

namespace = Namespace(__name__="__main__", __file__=path)
source = Path(path).read_text(encoding="utf-8").lstrip()
exec(compile(source, path, "exec"), namespace)
if sequence_format == "LIST":
    assert values == [expected] * int(assignment_count)
else:
    assert json.loads(json.dumps(values)) == [expected] * int(assignment_count)
"""


@pytest.mark.parametrize(
    argnames="case",
    argvalues=[
        case
        for case in build_variant_cases()
        if case.variant.lang_cls is Python
        and case.variant.spec.string_format is Python.string_formats.MULTILINE
    ],
    ids=lambda case: f"{case.case_dir_name}/{case.golden_name}",
)
def test_multiline_string_program_values(
    case: VariantCase,
    cases_dir: Path,
) -> None:
    """Every emitted assignment retains leading, nested and trailing
    whitespace.

    The rendering suite compares public API output with these same files.
    Executing the complete programs also rejects a regenerated golden that
    changes the source value while remaining valid Python.
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
        name=case.golden_name,
        lang_cls=case.variant.lang_cls,
        version=spec.language_version,
    )
    assignment_count = (
        2 if isinstance(case.variable_form, BothVariableForms) else 1
    )
    completed = subprocess.run(  # noqa: S603 - execute complete checked-in programs
        args=[
            sys.executable,
            "-I",
            "-c",
            _CHECK_PROGRAM,
            str(object=golden_path),
            case.variable_form.name,
            json.dumps(obj=expected),
            str(object=assignment_count),
            spec.sequence_format.name,
        ],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
