"""Decode native invocation recipes into typed calls."""

from collections.abc import Mapping, Sequence

from beartype import beartype

from literalizer import _native_call_data
from literalizer._types import ValueInput
from literalizer.native_calls import NativeInvocation


@beartype
def native_invocation_from_data(
    *,
    spec: Mapping[str, object],
    values: Sequence[ValueInput],
    zipped: object = _native_call_data.MISSING,
) -> NativeInvocation:
    """Build a native expression from a validated declarative recipe.

    Operands explicitly select ``input`` indexes, ``zipped`` companion
    values, ``literal`` values, typed references, or nested invocations.
    No field is interpreted as executable source text.
    """
    return _native_call_data.invocation_from_data(
        spec=spec, values=values, zipped=zipped
    )
