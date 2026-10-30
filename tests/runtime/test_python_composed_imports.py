"""Mixed YAML/JSON declarations retain legal Python import order (#6583).

The shared call manifest's reference declarations only accept JSON sources.
"""

import datetime as dt
import enum
import runpy
from pathlib import Path

import pytest

from literalizer import (
    InputFormat,
    LanguageCls,
    NewVariable,
    literalize,
    literalize_call,
    literalize_call_with_declarations,
)
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames="version", argvalues=list(Python.version_formats)
)
@pytest.mark.parametrize(argnames="reverse", argvalues=[False, True])
def test_composed_future_import_order(
    *,
    version: enum.Enum,
    reverse: bool,
    tmp_path: Path,
) -> None:
    """Both declaration orders execute and pass the original record."""
    language_cls: LanguageCls = Python
    language = language_cls(
        language_version=version,
        heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
    )
    declarations = [
        literalize(
            source="2001-02-03",
            input_format=InputFormat.YAML,
            language=language,
            variable_form=NewVariable(name="stamp", modifiers=frozenset()),
        ),
        literalize(
            source='{"a": 1}',
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name="item", modifiers=frozenset()),
        ),
    ]
    if reverse:
        declarations.reverse()
    call = literalize_call(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("value",),
        per_element=False,
        ref_key="$ref",
        ref_values={"item": {"a": 1}},
    )
    result = literalize_call_with_declarations(
        language=language,
        declarations=declarations,
        call=call,
        extra_body_preamble=(
            (
                "def consume(*, value: object) -> None:\n"
                "    assert dataclasses.is_dataclass(value)\n"
                "    observed.append(value.a)"
            ),
        ),
        extra_class_preamble=(),
        extra_preamble=("observed = []",),
    )
    path = tmp_path / "composition.py"
    _ = path.write_text(data=result.code, encoding="utf-8")
    namespace = runpy.run_path(path_name=str(object=path))
    assert namespace["observed"] == [1]
    assert namespace["stamp"] == dt.date(year=2001, month=2, day=3)
