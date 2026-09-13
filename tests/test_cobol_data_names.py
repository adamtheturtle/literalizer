"""Tests for COBOL data-name disambiguation through literalize."""

import json
import re

from literalizer import InputFormat, literalize
from literalizer.languages import Cobol


def test_cobol_collision_suffix_probe_advances() -> None:
    """A thousand distinct keys retain unique consecutive data names."""
    # Keep this generated stress case in Python: a YAML input and COBOL golden
    # would repeat 1,000 entries, obscuring the consecutive-suffix invariant
    # expressed directly below. Small collision cases use golden fixtures.
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
