"""Composed declarations retain helpers absent from the call's hints.

The consumer validates the actual record, beyond a no-op golden stub (#6581).
"""

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
    argnames="version",
    argvalues=list(Python.version_formats),
)
@pytest.mark.parametrize(argnames="known_reference", argvalues=[False, True])
def test_record_declaration_consumed_without_call_hint(
    *,
    version: enum.Enum,
    known_reference: bool,
    tmp_path: Path,
) -> None:
    """A real consumer observes the field from the earlier declaration."""
    language_cls: LanguageCls = Python
    language = language_cls(
        language_version=version,
        heterogeneous_strategy=Python.heterogeneous_strategies.RECORD,
    )
    declaration = literalize(
        source='{"a": 1}',
        input_format=InputFormat.JSON,
        language=language,
        variable_form=NewVariable(name="item", modifiers=frozenset()),
    )
    call = literalize_call(
        source='{"$ref": "item"}',
        input_format=InputFormat.JSON,
        language=language,
        target_function="consume",
        parameter_names=("value",),
        per_element=False,
        ref_key="$ref",
        ref_values={"item": {"a": 1}} if known_reference else None,
    )
    result = literalize_call_with_declarations(
        language=language,
        declarations=[declaration],
        call=call,
        extra_body_preamble=(
            (
                "def consume(*, value: object) -> None:\n"
                "    assert value.a == 1\n"
                "    assert type(value.a) is int\n"
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
