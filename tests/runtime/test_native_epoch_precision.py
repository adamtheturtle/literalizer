"""Integer epochs retain exact cancellation of native UTC offsets.

These public API inputs cannot be expressed by YAML/TOML timestamps (#6582).
"""

import datetime as dt
import runpy
from pathlib import Path

import pytest

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames=("wall_microseconds", "offset_microseconds", "seconds"),
    argvalues=[(1, 1, 0), (999999, -1, 1), (123456, 123456, 0)],
)
def test_native_epoch_cancellation(
    wall_microseconds: int,
    offset_microseconds: int,
    seconds: int,
    tmp_path: Path,
) -> None:
    """Execute the generated integer and check its exact value and
    type.
    """
    stamp = dt.datetime(
        year=1970,
        month=1,
        day=1,
        microsecond=wall_microseconds,
        tzinfo=dt.timezone(
            offset=dt.timedelta(microseconds=offset_microseconds)
        ),
    )
    result = literalize(
        source='{"$ref": "stamp"}',
        input_format=InputFormat.JSON,
        language=Python(datetime_format=Python.datetime_formats.EPOCH),
        variable_form=NewVariable(name="result_data", modifiers=frozenset()),
        ref_key="$ref",
        bound_refs={"stamp": stamp},
        wrap_in_file=True,
    )
    evaluation_path = tmp_path / "epoch.py"
    _ = evaluation_path.write_text(data=result.code, encoding="utf-8")
    namespace = runpy.run_path(path_name=str(object=evaluation_path))
    actual = namespace["result_data"]
    assert isinstance(actual, int)
    assert not isinstance(actual, bool)
    assert actual == seconds
