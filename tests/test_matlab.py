"""Focused tests for MATLAB rendering."""

import json

from literalizer import InputFormat, literalize
from literalizer.languages import Matlab


def test_matlab_map_char_keys() -> None:
    """Escape empty, quoted, and control-character map keys."""
    result = literalize(
        source=json.dumps(obj={"": 1, "'": 2, "a\x01b": 3}),
        input_format=InputFormat.JSON,
        language=Matlab(dict_format=Matlab.dict_formats.CONTAINERS_MAP),
    )

    assert "{'', '''', ['a', char(1), 'b']}" in result.code
