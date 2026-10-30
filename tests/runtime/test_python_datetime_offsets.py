"""Native reference datetimes retain offsets finer than serialized inputs.

YAML and TOML timestamps cannot express offsets finer than a minute, so these
public API regressions construct the native bindings directly (#6573).
"""

import datetime as dt
import enum
import runpy
from pathlib import Path

import pytest

from literalizer import InputFormat, LanguageCls, NewVariable, literalize
from literalizer.languages import Python


@pytest.mark.parametrize(
    argnames="version",
    argvalues=list(Python.version_formats),
)
@pytest.mark.parametrize(
    argnames="offset",
    argvalues=[
        dt.timedelta(),
        dt.timedelta(hours=5, minutes=30),
        dt.timedelta(hours=-5, minutes=-30),
        dt.timedelta(seconds=1),
        dt.timedelta(seconds=-1),
        dt.timedelta(microseconds=1),
        dt.timedelta(microseconds=-1),
        dt.timedelta(hours=5, minutes=30, seconds=15, microseconds=123456),
        -dt.timedelta(hours=5, minutes=30, seconds=15, microseconds=123456),
        dt.timedelta(hours=24) - dt.timedelta(microseconds=1),
        -dt.timedelta(hours=24) + dt.timedelta(microseconds=1),
    ],
)
def test_native_datetime_reference_offset_roundtrip(
    version: enum.Enum,
    offset: dt.timedelta,
    tmp_path: Path,
) -> None:
    """Values and mapping keys preserve the exact instant and UTC
    offset.
    """
    stamp = dt.datetime(
        year=2001,
        month=2,
        day=3,
        hour=4,
        minute=5,
        second=6,
        microsecond=123456,
        tzinfo=dt.timezone(offset=offset),
    )
    language_cls: LanguageCls = Python
    result = literalize(
        source='{"$ref": "binding"}',
        input_format=InputFormat.JSON,
        language=language_cls(language_version=version),
        variable_form=NewVariable(name="result_data", modifiers=frozenset()),
        ref_key="$ref",
        bound_refs={"binding": {"stamp": stamp, stamp: "key"}},
        wrap_in_file=True,
    )
    evaluation_path = tmp_path / "roundtrip.py"
    _ = evaluation_path.write_text(data=result.code, encoding="utf-8")
    namespace = runpy.run_path(path_name=str(object=evaluation_path))
    actual = namespace["result_data"]
    assert actual == {"stamp": stamp, stamp: "key"}
    reconstructed = actual["stamp"]
    assert isinstance(reconstructed, dt.datetime)
    assert reconstructed.isoformat() == stamp.isoformat()
    assert reconstructed.utcoffset() == offset
