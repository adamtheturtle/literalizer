"""Caller source must not stall statement comment scanning."""

import threading

import pytest

import literalizer
from literalizer.languages import Dart


@pytest.mark.parametrize(
    argnames="transform",
    argvalues=['"unterminated // comment', '"${1 // comment'],
    ids=["unfinished_string", "unfinished_interpolation"],
)
@pytest.mark.filterwarnings(
    "error::pytest.PytestUnhandledThreadExceptionWarning"
)
def test_incomplete_call_transform_finishes(transform: str) -> None:
    """Comment scanning must finish when callers omit closing
    delimiters.
    """

    def render() -> None:
        """Exercise comment placement through the public call API."""
        _ = literalizer.literalize_call(
            source="42",
            input_format=literalizer.InputFormat.JSON,
            language=Dart(),
            target_function="make_widget",
            parameter_names=("count",),
            per_element=False,
            variable_form=literalizer.ExistingVariable(name="my_data"),
            call_transform=lambda _value: transform,
        )

    # A stalled scanner must fail without blocking the test worker's exit.
    worker = threading.Thread(target=render, daemon=True)
    worker.start()
    worker.join(timeout=30)
    assert not worker.is_alive()
