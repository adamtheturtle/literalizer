"""Tests for COBOL data-name disambiguation through literalize."""

import json
import re

import pytest

from literalizer import InputFormat, literalize
from literalizer.languages import Cobol


def test_cobol_collision_suffix_probe_advances() -> None:
    """A thousand distinct keys retain unique consecutive data names."""
    collision_count = 1_000
    data = {
        f"a{index:010b}b".replace("0", "-").replace("1", "_"): index
        for index in range(collision_count)
    }
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=Cobol(),
    )
    names = re.findall(pattern=r"05 (F-A-B(?:-\d+)?) ", string=result.code)

    assert names == [
        "F-A-B",
        *(f"F-A-B-{suffix}" for suffix in range(2, collision_count + 1)),
    ]


@pytest.mark.parametrize(
    argnames=("data", "expected_names"),
    argvalues=[
        (
            {"a-b": 1, "a-b-2": 2, "a b": 3},
            ["F-A-B", "F-A-B-2", "F-A-B-3"],
        ),
        (
            {"a-b": 1, "a b": 2, "a-b-2": 3},
            ["F-A-B", "F-A-B-2", "F-A-B-2-2"],
        ),
    ],
)
def test_cobol_collision_suffix_skips_preexisting_name(
    *,
    data: dict[str, int],
    expected_names: list[str],
) -> None:
    """Source names and generated suffixes cannot shadow each other."""
    result = literalize(
        source=json.dumps(obj=data),
        input_format=InputFormat.JSON,
        language=Cobol(),
    )
    names = re.findall(pattern=r"05 ([A-Z0-9-]+) ", string=result.code)

    assert names == expected_names
