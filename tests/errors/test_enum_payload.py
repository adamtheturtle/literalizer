"""TOML-driven errors for enum payload consumer contracts."""

import enum
from typing import Literal, assert_never

import pytest
from pydantic import BaseModel, TypeAdapter

from literalizer._enums import enum_payload
from literalizer._language import redefinition_config, scalar_format_config
from tests.toml_cases import load_toml_cases


class _PayloadCase(BaseModel, extra="forbid", frozen=True):
    """One invalid payload and the exact error its consumer raises."""

    name: str
    consumer: Literal["text", "scalar_format", "redefinition"]
    payload: int
    message: str

    def read(self, *, member: enum.Enum) -> object:
        """Apply the consumer named by this case."""
        match self.consumer:
            case "text":
                return enum_payload(member=member, payload_type=str)
            case "scalar_format":
                return scalar_format_config(member)
            case "redefinition":
                return redefinition_config(member)
            case _ as unreachable:
                assert_never(unreachable)


class _PayloadCases(BaseModel, extra="forbid", frozen=True):
    """The manifest-owned enum payload rejection corpus."""

    cases: tuple[_PayloadCase, ...]


_CASES = TypeAdapter(type=_PayloadCases).validate_python(
    load_toml_cases(name="enum_payload_errors")
)


@pytest.mark.parametrize(
    argnames="case", argvalues=_CASES.cases, ids=lambda case: case.name
)
def test_enum_payload_error(case: _PayloadCase) -> None:
    """Each consumer rejects the manifest's invalid enum payload."""

    class _WrongPayload(enum.Enum):
        """An option carrying the manifest's invalid payload."""

        VALUE = case.payload

    with pytest.raises(expected_exception=TypeError) as error:
        _ = case.read(member=_WrongPayload.VALUE)
    assert str(object=error.value) == case.message
