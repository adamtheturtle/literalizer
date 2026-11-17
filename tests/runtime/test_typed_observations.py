"""Real native corruption controls for the deterministic typed oracle."""

import dataclasses
import datetime as dt
import shutil
import sys
from pathlib import Path

import pytest
from pydantic import JsonValue

from scripts.bounded_command import bounded_command
from scripts.native_observation import observe, verify_observation
from scripts.roundtrip_common import Step, json_object_from_text, run_program
from scripts.run_typed_roundtrip import (
    BACKENDS,
    build_program,
    check_backend,
    selected_cases,
)

_MINIMUM_RUBY_MAJOR = 3


@pytest.fixture(scope="session", name="ruby_available")
def fixture_ruby_available() -> bool:
    """Require a runtime supported by the Ruby backend, if installed."""
    ruby = shutil.which(cmd="ruby")
    if ruby is None:
        return False
    version = run_program(
        label="Ruby version",
        source_filename="version.rb",
        program="puts RUBY_VERSION.split('.').first.to_i\n",
        steps=[
            Step(
                args=bounded_command(
                    args=[ruby, "version.rb"],
                    fixture="Ruby version",
                    timeout_seconds=10,
                ),
                failure_label="Ruby version check failed",
            )
        ],
        extra_files=None,
    )
    return int(version) >= _MINIMUM_RUBY_MAJOR


@pytest.mark.parametrize(argnames="backend_name", argvalues=["python", "ruby"])
def test_supported_golden_groups(
    *, backend_name: str, ruby_available: bool
) -> None:
    """Correct values and declared record/byte/epoch/ISO conversions
    pass.
    """
    if backend_name == "ruby" and not ruby_available:
        pytest.skip(reason="Ruby 3+ is unavailable")
    result = check_backend(backend=BACKENDS[backend_name])
    assert len(result.observed) > 0
    assert len(result.snapshot_compile_only) > 0
    assert set(result.observed).isdisjoint(result.snapshot_compile_only)


@dataclasses.dataclass(frozen=True, kw_only=True)
class Corruption:
    """A changed native literal, independent of the authored expected
    input.
    """

    case: str
    stem_suffix: str
    python: tuple[str, str]
    ruby: tuple[str, str]


_CORRUPTIONS = (
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        python=("9223372036854775808", "9223372036854775809"),
        ruby=("9223372036854775808", "9223372036854775809"),
    ),
    Corruption(
        case="list_beyond_i64",
        stem_suffix="",
        python=("9223372036854775808", "9223372036854775808.0"),
        ruby=("9223372036854775808", "9223372036854775808.0"),
    ),
    Corruption(
        case="bool_list",
        stem_suffix="",
        python=("True", "1"),
        ruby=("true", "1"),
    ),
    Corruption(
        case="float_negative_zero",
        stem_suffix="",
        python=("-0.0", "0.0"),
        ruby=("-0.0", "0.0"),
    ),
    Corruption(
        case="scientific_float_precision",
        stem_suffix="_float_format_scientific_precision",
        python=("1.2345678901234567", "1.2345678901234565"),
        ruby=("1.2345678901234567", "1.2345678901234565"),
    ),
    Corruption(
        case="float_special_values",
        stem_suffix="",
        python=('float("nan")', 'float("inf")'),
        ruby=("Float::NAN", "Float::INFINITY"),
    ),
    Corruption(
        case="binary_octets",
        stem_suffix="",
        python=("00010203", "01010203"),
        ruby=("00010203", "01010203"),
    ),
    Corruption(
        case="int_key_dict",
        stem_suffix="",
        python=('1: "one"', '"1": "one"'),
        ruby=('1 => "one"', '"1" => "one"'),
    ),
    Corruption(
        case="date_list",
        stem_suffix="",
        python=("day=20", "day=21"),
        ruby=("2, 20,", "2, 21,"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        python=("hour=18", "hour=17"),
        ruby=("15, 18,", "15, 17,"),
    ),
    Corruption(
        case="scalar_datetime_non_utc",
        stem_suffix="",
        python=("minutes=30", "minutes=0"),
        ruby=("+05:30", "+05:00"),
    ),
)


@pytest.mark.parametrize(
    argnames=("backend_name", "corruption"),
    argvalues=[
        (backend_name, corruption)
        for backend_name in ("python", "ruby")
        for corruption in _CORRUPTIONS
    ]
    + [
        (
            "python",
            Corruption(
                case="binary_nonempty_octets",
                stem_suffix="_bytes_format_python",
                python=(r"\x00", r"\x01"),
                ruby=("", ""),
            ),
        ),
        (
            "python",
            Corruption(
                case="binary_nonempty_octets",
                stem_suffix="_bytes_format_python",
                python=("b'", "'"),
                ruby=("", ""),
            ),
        ),
    ],
)
def test_native_corruptions(
    *,
    backend_name: str,
    corruption: Corruption,
    tmp_path: Path,
    ruby_available: bool,
) -> None:
    """Corrupted golden values fail with their case name."""
    if backend_name == "ruby" and not ruby_available:
        pytest.skip(reason="Ruby 3+ is unavailable")
    backend = BACKENDS[backend_name]
    executable = (
        sys.executable
        if backend_name == "python"
        else shutil.which(cmd="ruby")
    )
    if executable is None:
        pytest.skip(reason="Ruby is unavailable")
    cases = selected_cases(backend=backend)
    path = next(
        path
        for path in cases
        if path.parent.name == corruption.case
        and path.name.startswith(backend.name + corruption.stem_suffix + "@")
    )
    old, new = (
        corruption.python if backend_name == "python" else corruption.ruby
    )
    source = path.read_text(encoding="utf-8")
    assert old in source
    mutated = tmp_path / path.name
    _ = mutated.write_text(data=source.replace(old, new), encoding="utf-8")
    filename = f"control.{backend.extension}"
    output = run_program(
        label=corruption.case,
        source_filename=filename,
        program=build_program(
            backend=backend, fixtures=(mutated,), cases_dir=tmp_path
        ),
        steps=[
            Step(
                args=bounded_command(
                    args=[executable, filename],
                    fixture=corruption.case,
                    timeout_seconds=10,
                ),
                failure_label="control execution failed",
            )
        ],
        extra_files=None,
    )
    actual = json_object_from_text(text=output)[path.name]
    with pytest.raises(
        expected_exception=ValueError,
        match=corruption.case + ": typed observation mismatch",
    ):
        verify_observation(
            label=corruption.case, actual=actual, expected=cases[path]
        )


def test_native_bytes_and_naive_datetime() -> None:
    """The wire format retains native bytes and naive/aware
    distinctions.
    """
    assert observe(value=b"\x00\xff") == ["bytes", "00ff"]
    with pytest.raises(
        expected_exception=ValueError,
        match="bytes: typed observation mismatch",
    ):
        verify_observation(
            label="bytes",
            actual=observe(value="00ff"),
            expected=observe(value=b"\x00\xff"),
        )
    # Python datetime equality ignores offsets for equal instants; our contract
    # preserves the authored wall time and offset as separate observations.
    stamp = dt.datetime(year=2024, month=1, day=1, tzinfo=dt.UTC)
    shifted = stamp.astimezone(tz=dt.timezone(offset=dt.timedelta(hours=1)))
    assert stamp == shifted
    with pytest.raises(
        expected_exception=ValueError,
        match="offset: typed observation mismatch",
    ):
        verify_observation(
            label="offset",
            actual=observe(value=shifted),
            expected=observe(value=stamp),
        )


@pytest.mark.parametrize(
    argnames="invalid",
    argvalues=[
        ["bool", 1],
        ["int", 1],
        ["int", "-0"],
        ["float", "7ff0000000000000"],
        ["bytes", "0"],
        ["datetime", "2024-01-01T00:00:00.000000", "86400000000"],
        ["unknown", "1"],
    ],
)
def test_malformed_observations(*, invalid: JsonValue) -> None:
    """Malformed envelopes cannot exploit JSON/Python numeric equality."""
    with pytest.raises(
        expected_exception=ValueError,
        match="malformed: invalid typed observation",
    ):
        verify_observation(
            label="malformed", actual=invalid, expected=["null"]
        )


def test_mapping_order_and_typed_keys() -> None:
    """Ignore entry ordering, retaining distinct integer and string
    keys.
    """
    first = observe(value={1: "integer", "1": "string"})
    second = observe(value={"1": "string", 1: "integer"})
    verify_observation(label="ordered", actual=first, expected=second)
