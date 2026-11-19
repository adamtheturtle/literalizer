"""Execute typed observations of existing Python and Ruby declarations."""

import base64
import datetime as dt
import json
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

from pydantic import JsonValue
from ruamel.yaml import YAML

from scripts.native_value_python import (
    epoch_microseconds,
    is_native_mapping,
    is_native_sequence,
    observe,
)
from scripts.roundtrip_common import verify_observation

CONSUMER_MARKER = "# Independent native value checks."
_INSPECTORS = Path(__file__).resolve().parent
_RECORD = "_heterogeneous_strategy_record@"


def _project_datetime(value: dt.datetime, *, fixture: Path) -> object:
    """Apply native, epoch or ISO datetime semantics."""
    name = fixture.name
    if "_datetime_epoch_" in name:
        return epoch_microseconds(value=value) // 1_000_000
    if "_datetime_iso_" in name:
        return value.isoformat()
    if fixture.suffix == ".rb" and value.utcoffset() is None:
        return value.replace(tzinfo=dt.UTC)
    return value


def _project_bytes(value: bytes, *, fixture: Path) -> bytes | str:
    """Apply the byte encoding selected by the fixture."""
    if "_bytes_format_python@" in fixture.name:
        return value
    if "_bytes_format_base64@" in fixture.name:
        return base64.b64encode(s=value).decode(encoding="ascii")
    return value.hex()


def _project(value: object, *, fixture: Path) -> object:
    """Apply the selected golden's public representation to authored data."""
    match value:
        case dt.datetime():
            return _project_datetime(value=value, fixture=fixture)
        case bytes():
            return _project_bytes(value=value, fixture=fixture)
        case _ if is_native_sequence(value):
            return [_project(value=item, fixture=fixture) for item in value]
        case _ if is_native_mapping(value):
            return {
                _project(value=key, fixture=fixture): _project(
                    value=item, fixture=fixture
                )
                for key, item in value.items()
            }
        case _:
            return value


def expected_observation(
    *,
    fixture: Path,
    input_path: Path,
    substitutions: Mapping[str, object] | None,
) -> JsonValue:
    """Observe the authored input after applying documented conversions."""
    source = input_path.read_text(encoding="utf-8")
    if input_path.suffix == ".yaml":
        yaml = YAML(typ="safe")
        value: object = yaml.load(stream=source)  # pyright: ignore[reportUnknownMemberType]
    else:
        value = json.loads(s=source)
    if substitutions is not None:
        if not is_native_mapping(value):
            msg = f"{input_path}: expected a mapping for native substitutions"
            raise ValueError(msg)
        if any(
            key not in value or value[key] is not None for key in substitutions
        ):
            msg = (
                f"{input_path}: native substitutions require null placeholders"
            )
            raise ValueError(msg)
        value.update(substitutions.items())
    return observe(value=_project(value=value, fixture=fixture))


def run_golden_program(
    *, fixture: Path, command: Sequence[str], program: str, scratch: Path
) -> subprocess.CompletedProcess[str]:
    """Execute an authored golden program with a portable deadline."""
    path = scratch / fixture.name
    _ = path.write_text(data=program, encoding="utf-8")
    try:
        return subprocess.run(
            args=[*command, str(object=path)],
            cwd=scratch,
            check=False,
            capture_output=True,
            encoding="utf-8",
            timeout=30,
        )
    except subprocess.TimeoutExpired as exc:
        msg = f"{fixture}: native execution exceeded its 30-second deadline"
        raise TimeoutError(msg) from exc


def check_golden_observation(
    *,
    fixture: Path,
    declaration: str,
    command: Sequence[str],
    expected: JsonValue,
    scratch: Path,
) -> None:
    """Run a saved declaration and compare the independent inspection."""
    if fixture.suffix == ".py":
        inspector = _INSPECTORS / "native_value_python.py"
        operation = "observe_record" if _RECORD in fixture.name else "observe"
        consumer = (
            "import json as oracle_json\n"
            "import runpy as oracle_runpy\n"
            f"oracle = oracle_runpy.run_path({str(object=inspector)!r})\n"
            f"print(oracle_json.dumps(oracle[{operation!r}](my_data)))\n"
        )
    else:
        inspector = _INSPECTORS / "native_value_ruby.rb"
        consumer = (
            f"require {json.dumps(obj=str(object=inspector))}\n"
            "puts JSON.generate(observe_native(my_data))\n"
        )
    result = run_golden_program(
        fixture=fixture,
        command=command,
        program=f"{declaration}\n{consumer}",
        scratch=scratch,
    )
    if result.returncode != 0:
        msg = (
            f"{fixture}: native observer exited {result.returncode}\n"
            f"{result.stdout}{result.stderr}"
        )
        raise RuntimeError(msg)
    verify_observation(
        label=str(object=fixture),
        produced_json=result.stdout,
        expected_observation=expected,
    )
