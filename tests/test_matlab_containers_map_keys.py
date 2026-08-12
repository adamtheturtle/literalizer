"""MATLAB ``containers.Map`` key rendering coverage."""

import json

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Matlab


def test_containers_map_renders_empty_and_control_character_keys() -> None:
    """Character-array keys safely compose empty and control segments."""
    result = literalize(
        source=json.dumps(obj={"": 1, "a\u0001b": 2}),
        input_format=InputFormat.JSON,
        language=Matlab(
            dict_format=Matlab.dict_formats.CONTAINERS_MAP,
        ),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
    )

    assert "containers.Map({''" in result.code
    assert "['a', char(1), 'b']" in result.code
