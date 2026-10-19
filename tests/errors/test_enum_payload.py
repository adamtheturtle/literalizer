"""Reject enum payloads that do not meet their consumer's contract."""

import enum
from collections.abc import Callable

import pytest

from literalizer._enums import enum_payload
from literalizer._language import redefinition_config, scalar_format_config


class _WrongPayload(enum.Enum):
    """An option whose payload cannot be consumed as text."""

    INTEGER = 1


def test_enum_payload_rejects_wrong_type() -> None:
    """Reject a payload that does not match the required type."""
    with pytest.raises(
        expected_exception=TypeError,
        match=r"_WrongPayload\.INTEGER requires a str payload; got int",
    ):
        _ = enum_payload(member=_WrongPayload.INTEGER, payload_type=str)


@pytest.mark.parametrize(
    argnames=("reader", "message"),
    argvalues=[
        (scalar_format_config, "requires scalar format metadata"),
        (redefinition_config, "requires declaration redefinition metadata"),
    ],
)
def test_enum_payload_rejects_missing_metadata(
    *, reader: Callable[[enum.Enum], object], message: str
) -> None:
    """Require the structural metadata consumed by scalar and binding code."""
    with pytest.raises(expected_exception=TypeError, match=message):
        _ = reader(_WrongPayload.INTEGER)
