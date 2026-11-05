"""Execute complete JSON-derived programs against canonical native golden
programs.
"""

import enum
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Literal

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from pydantic import BaseModel, TypeAdapter
from ruamel.yaml import YAML

from literalizer import InputFormat, literalize
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


_CONTRACTS = TypeAdapter(type=tuple[_Contract, ...]).validate_python(
    tomllib.loads(
        Path(__file__).with_suffix(suffix=".toml").read_text(encoding="utf-8")
    )["contracts"]
)

type _JSONScalar = str | int | float | bool | None

type _JSONValue = _JSONScalar | list[_JSONValue] | dict[str, _JSONValue]

_JSON_VALUES = TypeAdapter(type=_JSONValue)


# Preserve the original character categories, null exclusion, and bounds.
json_text = st.text(
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
    return st.lists(elements=children, max_size=3) | st.dictionaries(
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
json_arrays = st.lists(elements=json_values, max_size=5)
json_objects = st.dictionaries(keys=json_text, values=json_values, max_size=5)


def _check_program(
    *, data: _JSONValue, contract: _Contract, version: enum.Enum
) -> str:
    """Compile and execute the actual wrapper, retaining exact JSON
    containers.
    """
    source = json.dumps(obj=data)
    result = literalize(
        source=source,
        input_format=InputFormat.JSON,
        language=make_spec(
            lang_cls=Python,
            language_version=version,
            date_format=Python.date_formats.PYTHON,
            datetime_format=Python.datetime_formats.PYTHON,
            bytes_format=Python.bytes_formats.HEX,
            sequence_format=Python.sequence_formats.LIST,
            set_format=Python.set_formats.SET,
            variable_type_hints=Python.variable_type_hints_formats.NEVER,
        ),
        pre_indent_level=0,
        include_delimiters=contract.include_delimiters,
        variable_form=None,
        wrap_in_file=False,
    )
    assert result.source_data == data
    # Compare inside Python: serializing the actual value first would hide
    # an accidental tuple where the LIST option promises a JSON list.
    native_program = f"my_data = {result.code}\n"
    program = (
        native_program
        + f"\nimport json\nassert my_data == json.loads({source!r})\n"
    )
    completed = subprocess.run(  # noqa: S603 - run generated test code
        args=[sys.executable, "-I", "-c", program],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    return native_program


@pytest.mark.parametrize(
    argnames="contract", argvalues=_CONTRACTS, ids=lambda case: case.name
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
        extension=Python.extension,
        lang_cls=Python,
        version=version,
    )
    assert _check_program(
        data=data, contract=contract, version=version
    ) == path.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    argnames="contract", argvalues=_CONTRACTS, ids=lambda case: case.name
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
