"""Execute complete JSON-derived programs against canonical native golden
programs.
"""

import enum
import json
import subprocess
import sys
import tomllib
from collections.abc import Mapping
from pathlib import Path
from typing import Literal

import pytest
from hypothesis import HealthCheck, example, given, settings
from hypothesis import strategies as st
from hypothesis.strategies import dictionaries
from pydantic import BaseModel, TypeAdapter
from ruamel.yaml import YAML

from literalizer import InputFormat, literalize, literalize_call
from literalizer.languages import Python
from tests.integration.case_manifests import case_input
from tests.integration.language_specs import make_golden_path, make_spec
from tests.yaml_support import as_yaml_parser


class _Contract(BaseModel, extra="forbid", frozen=True):
    """A generated JSON shape and its existing complete program
    control.
    """

    name: str
    strategy: Literal["array", "scalar", "object"]
    case_name: str
    golden_name: str
    include_delimiters: bool


_MANIFEST: Mapping[str, object] = tomllib.loads(
    Path(__file__).with_suffix(suffix=".toml").read_text(encoding="utf-8")
)
_CONTRACTS = TypeAdapter(type=tuple[_Contract, ...]).validate_python(
    _MANIFEST["contracts"]
)

type _JSONScalar = str | int | float | bool | None

type _JSONValue = _JSONScalar | list[_JSONValue] | dict[str, _JSONValue]

_JSON_VALUES = TypeAdapter(type=_JSONValue)


# Preserve the original character categories, null exclusion, and bounds.
json_text: st.SearchStrategy[str] = st.text(
    alphabet=st.characters(
        categories=("L", "M", "N", "P", "S", "Z"), exclude_characters="\x00"
    ),
    max_size=20,
)
json_scalars: st.SearchStrategy[_JSONValue] = (
    st.none()
    | st.booleans()
    | st.integers()
    # ``nan`` and ``inf`` are excluded because JSON does not support them.
    | st.floats(allow_nan=False, allow_infinity=False)
    | json_text
)


def _json_collection_values(
    children: st.SearchStrategy[_JSONValue],
) -> st.SearchStrategy[_JSONValue]:
    """Return recursive JSON collection strategies."""
    return st.lists(elements=children, max_size=3) | dictionaries(
        keys=json_text,
        values=children,
        max_size=3,
    )


json_values: st.SearchStrategy[_JSONValue] = st.recursive(
    base=json_scalars,
    extend=_json_collection_values,
    # Preserve the original recursive corpus size and nesting budget.
    max_leaves=15,
)
json_arrays: st.SearchStrategy[list[_JSONValue]] = st.lists(
    elements=json_values, max_size=5
)
json_objects: st.SearchStrategy[dict[str, _JSONValue]] = dictionaries(
    keys=json_text, values=json_values, max_size=5
)


def _check_program(
    *, data: _JSONValue, contract: _Contract, version: enum.Enum
) -> str:
    """Execute both the generated literal and direct call in Python."""
    source = json.dumps(obj=data)
    language = make_spec(
        lang_cls=Python,
        language_version=version,
        date_format=Python.date_formats.PYTHON,
        datetime_format=Python.datetime_formats.PYTHON,
        bytes_format=Python.bytes_formats.HEX,
        sequence_format=Python.sequence_formats.LIST,
        set_format=Python.set_formats.SET,
        variable_type_hints=Python.variable_type_hints_formats.NEVER,
    )
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        pre_indent_level=0,
        include_delimiters=contract.include_delimiters,
        variable_form=None,
        wrap_in_file=False,
    )
    assert result.source_data == data
    call = literalize_call(
        source=source,
        input_format=InputFormat.JSON,
        language=language,
        target_function="check_value",
        parameter_names=("actual",),
        per_element=False,
    )
    # Native equality checks collection kinds; JSON encoding also
    # distinguishes booleans, integers, floats and the sign of zero.
    native_program = f"my_data = {result.code}\n"
    program = (
        "import json\n"
        f"expected = json.loads({source!r})\n"
        "def check_value(actual):\n"
        "    assert actual == expected, (actual, expected)\n"
        "    assert json.dumps(actual, sort_keys=True) == "
        "json.dumps(expected, sort_keys=True), (actual, expected)\n"
        f"{native_program}"
        "check_value(my_data)\n"
        f"{call.code}\n"
    )
    _run_python_program(program=program)
    return native_program


def _run_python_program(*, program: str) -> None:
    """Execute generated code in an isolated, bounded interpreter."""
    completed = subprocess.run(  # noqa: S603 - run generated test code
        args=[sys.executable, "-I", "-c", program],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr


@pytest.mark.parametrize(
    argnames="contract",
    argvalues=_CONTRACTS,
    ids=[case.name for case in _CONTRACTS],
)
@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
def test_json_program_matches_native_golden(
    contract: _Contract, version: enum.Enum, cases_dir: Path
) -> None:
    """Use each canonical document and complete checked-in Python
    program.
    """
    input_info = case_input(case_dir=cases_dir / contract.case_name)
    source = input_info.path.read_text(encoding="utf-8")
    raw_data = (
        as_yaml_parser(parser=YAML(typ="safe")).load(stream=source)
        if input_info.input_format is InputFormat.YAML
        else json.loads(s=source)
    )
    data = _JSON_VALUES.validate_python(raw_data, strict=True)
    path = make_golden_path(
        parent=cases_dir / contract.case_name,
        name=contract.golden_name,
        lang_cls=Python,
        version=version,
    )
    assert _check_program(
        data=data, contract=contract, version=version
    ) == path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    argnames="contract",
    argvalues=_CONTRACTS,
    ids=[case.name for case in _CONTRACTS],
)
@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@settings(deadline=None, suppress_health_check=[HealthCheck.filter_too_much])
@given(draw=st.data())
def test_json_documents_execute_as_complete_programs(
    contract: _Contract, version: enum.Enum, draw: st.DataObject
) -> None:
    """Preserve the original recursive scalar, array, and object
    generators.
    """
    strategies: dict[str, st.SearchStrategy[_JSONValue]] = {
        "array": json_arrays,
        "scalar": json_scalars,
        "object": json_objects,
    }
    value = draw.draw(
        strategy=strategies[contract.strategy], label=contract.name
    )
    _ = _check_program(data=value, contract=contract, version=version)


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.VersionFormats)
)
@settings(max_examples=24, deadline=None)
@given(rows=st.lists(elements=st.tuples(json_values, json_values), max_size=4))
@example(rows=[])
@example(rows=[(True, 1), (1.0, -0.0), ([], {"nested": [None]})])
def test_generated_python_call_rows_preserve_values(
    *, version: enum.Enum, rows: list[tuple[_JSONValue, _JSONValue]]
) -> None:
    """Check argument positions, row order and native value types."""
    source = json.dumps(obj=rows)
    call = literalize_call(
        source=source,
        input_format=InputFormat.JSON,
        language=make_spec(
            lang_cls=Python,
            language_version=version,
            sequence_format=Python.sequence_formats.LIST,
        ),
        target_function="check_row",
        parameter_names=("first", "second"),
        per_element=True,
    )
    _run_python_program(
        program=(
            "import json\n"
            f"expected = json.loads({source!r})\n"
            "collected = []\n"
            "def check_row(first, second):\n"
            "    collected.append([first, second])\n"
            f"{call.code}\n"
            "assert collected == expected, (collected, expected)\n"
            "assert json.dumps(collected, sort_keys=True) == "
            "json.dumps(expected, sort_keys=True), (collected, expected)\n"
        )
    )
