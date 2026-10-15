"""Opt-in, bounded boundary propagation discovery for issue #5492.

Run with ``python -m scripts.boundary_containers --help``. This corpus is
deliberately outside normal pytest and compiler CI. Runtime observers tag
integers and binary64 bits before JSON serialization can erase their types.
"""

import argparse
import datetime as dt
import json
import math
import struct
import subprocess
import sys
import tempfile
import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, TypeAdapter

from literalizer import (
    InputFormat,
    Language,
    NewVariable,
    RoundTripCapability,
    literalize,
)
from literalizer.exceptions import (
    LiteralizerError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
    UnrepresentableStringError,
)
from literalizer.languages import CSharp, Go, JavaScript, Python
from scripts.bounded_command import bounded_command
from scripts.roundtrip_common import JsonValue, input_for_capabilities

type BoundaryValue = (
    bool
    | int
    | float
    | str
    | dt.datetime
    | list[BoundaryValue]
    | dict[str, BoundaryValue]
    | None
)

_ROOT = Path(__file__).resolve().parent
_SHAPES = ("list", "map", "record", "nested", "empty", "widen")
_MAX_CASES = 400
_MAX_DEPTH = 6
_CASE_SECONDS = 60
_EPOCH = dt.datetime(year=1970, month=1, day=1, tzinfo=dt.UTC)


@dataclass(frozen=True)
class Target:
    """A deliberately selected runtime/format contract."""

    language: Language
    runtime: Literal["python", "javascript", "go", "csharp"]
    integer_min: int
    integer_max: int
    native_records: bool


def targets() -> dict[str, Target]:
    """Return explicit audited format variants."""
    return {
        "python": Target(
            language=Python(
                sequence_format=Python.sequence_formats.LIST,
                datetime_format=Python.datetime_formats.EPOCH,
            ),
            runtime="python",
            integer_min=-(2**100),
            integer_max=2**100,
            native_records=False,
        ),
        "javascript": Target(
            language=JavaScript(
                datetime_format=JavaScript.datetime_formats.EPOCH
            ),
            runtime="javascript",
            integer_min=-(2**53 - 1),
            integer_max=2**53 - 1,
            native_records=False,
        ),
        "go": Target(
            language=Go(datetime_format=Go.datetime_formats.EPOCH),
            runtime="go",
            integer_min=-(2**63),
            integer_max=2**64 - 1,
            native_records=False,
        ),
        "go-record": Target(
            language=Go(
                datetime_format=Go.datetime_formats.EPOCH,
                heterogeneous_strategy=Go.heterogeneous_strategies.RECORD,
            ),
            runtime="go",
            integer_min=-(2**63),
            integer_max=2**64 - 1,
            native_records=True,
        ),
        "csharp": Target(
            language=CSharp(
                datetime_format=CSharp.datetime_formats.EPOCH,
                sequence_format=CSharp.sequence_formats.ARRAY,
            ),
            runtime="csharp",
            integer_min=-(2**63),
            integer_max=2**64 - 1,
            native_records=False,
        ),
        "csharp-record": Target(
            language=CSharp(
                datetime_format=CSharp.datetime_formats.EPOCH,
                heterogeneous_strategy=CSharp.heterogeneous_strategies.RECORD,
            ),
            runtime="csharp",
            integer_min=-(2**63),
            integer_max=2**64 - 1,
            native_records=True,
        ),
    }


def boundaries() -> dict[str, list[BoundaryValue]]:
    """Enumerate endpoints and immediate neighbors, without randomness."""
    return {
        "signed32": [
            -(2**31) - 1,
            -(2**31),
            -(2**31) + 1,
            2**31 - 2,
            2**31 - 1,
            2**31,
        ],
        "signed64": [-(2**63), -(2**63) + 1, 2**63 - 2, 2**63 - 1],
        "unsigned32": [2**32 - 2, 2**32 - 1, 2**32],
        "unsigned64": [2**63, 2**64 - 2, 2**64 - 1],
        "safeinteger": [-(2**53) + 1, 2**53 - 2, 2**53 - 1],
        "float": [
            -0.0,
            0.0,
            math.nextafter(0.0, 1.0),
            sys.float_info.min,
            math.nextafter(1.0, 0.0),
            1.0,
            math.nextafter(1.0, 2.0),
            float(2**53),
            math.nextafter(float(2**53), math.inf),
            sys.float_info.max,
        ],
        "unicode": [
            "",
            "é",
            "e\u0301",
            "\U0001f600",
            "\u2028\u2029",
            '"\\\n',
            "${x}#{x}`@",
        ],
        "controls": ["\x00", "\x01\x1f", "\x7f\x85"],
        "epoch": [
            _EPOCH + dt.timedelta(seconds=seconds)
            for seconds in (
                -(2**31) - 1,
                -(2**31),
                -(2**31) + 1,
                -1,
                0,
                1,
                2**31 - 2,
                2**31 - 1,
                2**31,
            )
        ],
        "collection": [
            [],
            {},
            [None],
            [None, None],
            {"item": None},
            [1],
            {"item": 1},
        ],
    }


def shape(value: BoundaryValue, *, name: str) -> BoundaryValue:
    """Place a value in a bounded container, preserving every leaf."""
    match name:
        case "list":
            return [value]
        case "map":
            return {"item": value}
        case "record":
            return [{"value": value, "label": "x"}]
        case "nested":
            return [{"item": [value]}]
        case "empty":
            empty: list[BoundaryValue] = []
            return [empty, [value]]
        case "widen":
            return [value, "sentinel"]
        case _:
            msg = f"unknown shape: {name}"
            raise ValueError(msg)


def cases(target: Target) -> Iterator[tuple[str, BoundaryValue]]:
    """Yield only supported values, named independently of their order."""
    for family, values in boundaries().items():
        for index, value in enumerate(iterable=values):
            if (
                family == "controls"
                and index == 1
                and RoundTripCapability.CONTROL_STRINGS
                not in target.language.variant_metadata.round_trip_capabilities
            ):
                continue
            if (
                isinstance(value, int)
                and not target.integer_min <= value <= target.integer_max
            ):
                continue
            for name in _SHAPES:
                if (
                    target.runtime == "go"
                    and target.native_records
                    and name == "empty"
                    and isinstance(value, dict)
                ):
                    continue
                yield f"{family}{index}{name}", shape(value=value, name=name)
            if family in {"signed32", "unsigned32", "safeinteger"}:
                yield (
                    f"{family}{index}numeric",
                    [value, min(2**63 - 1, target.integer_max)],
                )


def observe(value: BoundaryValue, *, javascript: bool) -> JsonValue:
    """Build typed expectations independently of the renderer."""
    if isinstance(value, dt.datetime):
        value = (value - _EPOCH) // dt.timedelta(seconds=1)
    if isinstance(value, dict):
        return {
            str(object=key).lower(): observe(
                value=child, javascript=javascript
            )
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [observe(value=child, javascript=javascript) for child in value]
    if isinstance(value, (bool, str)) or value is None:
        return value
    if isinstance(value, int) and not javascript:
        return ["int", str(object=value)]
    return ["float", struct.pack(">d", float(value)).hex()]


def depth(value: BoundaryValue) -> int:
    """Count container nesting before rendering or running a command."""
    if isinstance(value, dict):
        return 1 + max(
            (depth(value=child) for child in value.values()), default=0
        )
    if isinstance(value, list):
        return 1 + max((depth(value=child) for child in value), default=0)
    return 0


def program(*, target: Target, document: dict[str, BoundaryValue]) -> str:
    """Render native declarations and attach a runtime type observer."""
    result = literalize(
        source=yaml.safe_dump(data=document, allow_unicode=True),
        input_format=InputFormat.YAML,
        language=target.language,
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name="data", modifiers=frozenset()),
        wrap_in_file=False,
    )
    observer = (
        _ROOT / "boundary_runtime" / f"{target.runtime}.txt"
    ).read_text()
    preamble = "\n".join(result.preamble)
    declarations = "\n".join(result.body_preamble)
    match target.runtime:
        case "python" | "javascript":
            return f"{preamble}\n{declarations}\n{result.code}\n{observer}"
        case "go":
            package, *entries = result.preamble
            # Merge the observer's imports with renderer-owned imports such
            # as math (negative zero); Go rejects duplicate import paths.
            generated_imports = "\n".join(
                entry for entry in entries if entry.startswith("import ")
            )
            declarations = "\n".join(
                (
                    *[
                        entry
                        for entry in entries
                        if not entry.startswith("import ")
                    ],
                    *result.body_preamble,
                ),
            )
            needed = [
                name
                for name in (
                    "encoding/json",
                    "fmt",
                    "math",
                    "reflect",
                    "strconv",
                    "strings",
                )
                if f'"{name}"' not in generated_imports
            ]
            added = "\n".join(f'import "{name}"' for name in needed)
            return (
                f"{package}\n{generated_imports}\n{added}\n{declarations}\n"
                f"{observer}\nfunc main() {{\n{result.code}\n"
                "out, err := json.Marshal(observe(reflect.ValueOf(data)))\n"
                "if err != nil { panic(err) }; fmt.Print(string(out))\n}\n"
            )
        case "csharp":
            return (
                f"using System;\n{preamble}\n{declarations}\n{observer}\n"
                "static class Program { public static void Main() {\n"
                f"{result.code}\n"
                "Console.Write(System.Text.Json.JsonSerializer.Serialize(Observer.Observe(data)));\n"
                "} }\n"
            )


def execute(
    *, target: Target, source: str, directory: Path
) -> subprocess.CompletedProcess[str]:
    """Compile and run one bounded native program."""
    match target.runtime:
        case "python":
            filename, command = "main.py", [sys.executable, "main.py"]
        case "javascript":
            filename, command = "main.js", ["node", "main.js"]
        case "go":
            filename, command = "main.go", ["go", "run", "main.go"]
        case "csharp":
            _ = (directory / "global.json").write_text(
                data=json.dumps(
                    obj={
                        "sdk": {"version": "8.0.426", "rollForward": "disable"}
                    }
                ),
            )
            filename, command = (
                "Program.cs",
                [
                    "dotnet",
                    "run",
                    "--project",
                    "fixture.csproj",
                    "--verbosity",
                    "quiet",
                ],
            )
            _ = (directory / "fixture.csproj").write_text(
                data='<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
                "<OutputType>Exe</OutputType><TargetFramework>net8.0</TargetFramework>"
                "<RollForward>LatestMajor</RollForward><LangVersion>10</LangVersion>"
                "<Nullable>enable</Nullable><TreatWarningsAsErrors>true</TreatWarningsAsErrors>"
                "</PropertyGroup></Project>",
            )
    _ = (directory / filename).write_text(data=source, encoding="utf-8")
    return subprocess.run(
        args=bounded_command(
            args=command,
            fixture=target.runtime,
            timeout_seconds=_CASE_SECONDS,
        ),
        cwd=directory,
        capture_output=True,
        text=True,
        check=False,
    )


def rejection_audit(target: Target) -> None:
    """Verify documented integer errors in each shape."""
    integers = (
        ()
        if target.runtime == "python"
        else (
            target.integer_min - 1,
            target.integer_max + 1,
        )
    )
    for value in integers:
        for container in (
            value,
            *(shape(value=value, name=name) for name in _SHAPES),
        ):
            try:
                _ = literalize(
                    source=yaml.safe_dump(data=container),
                    input_format=InputFormat.YAML,
                    language=target.language,
                    pre_indent_level=0,
                    include_delimiters=True,
                )
            except UnrepresentableIntegerError:
                continue
            msg = f"missing UnrepresentableIntegerError for {container!r}"
            raise ValueError(msg)


def control_rejection_audit(target: Target) -> None:
    """Verify unsupported raw C0 controls fail in every shape."""
    if (
        RoundTripCapability.CONTROL_STRINGS
        not in target.language.variant_metadata.round_trip_capabilities
    ):
        for container in (
            "\x01\x1f",
            *(shape(value="\x01\x1f", name=name) for name in _SHAPES),
        ):
            try:
                _ = literalize(
                    source=yaml.safe_dump(data=container),
                    input_format=InputFormat.YAML,
                    language=target.language,
                    pre_indent_level=0,
                    include_delimiters=True,
                )
            except UnrepresentableStringError:
                continue
            msg = f"missing UnrepresentableStringError for {container!r}"
            raise ValueError(msg)


def record_rejection_audit(target: Target) -> None:
    """Verify Go RECORD's documented empty-sibling limitation."""
    if target.runtime == "go" and target.native_records:
        mappings: tuple[dict[str, BoundaryValue], ...] = (
            {},
            {"item": None},
            {"item": 1},
        )
        for mapping in mappings:
            try:
                _ = literalize(
                    source=yaml.safe_dump(
                        data=shape(value=mapping, name="empty")
                    ),
                    input_format=InputFormat.YAML,
                    language=target.language,
                    pre_indent_level=0,
                    include_delimiters=True,
                )
            except UnrepresentableInputError as error:
                if "nested record list and its empty sibling" not in str(
                    object=error
                ):
                    raise
                continue
            msg = "missing documented Go RECORD empty-sibling error"
            raise ValueError(msg)


class Options(BaseModel, extra="forbid", frozen=True):
    """Validate dynamically typed command arguments at the boundary."""

    target: str
    mode: Literal["baseline", "expanded"]
    output: Path
    case: str | None


def options() -> Options:
    """Parse and validate the discovery command's arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    _ = parser.add_argument("--target", choices=targets(), required=True)
    _ = parser.add_argument(
        "--mode", choices=("baseline", "expanded"), required=True
    )
    _ = parser.add_argument("--output", type=Path, required=True)
    _ = parser.add_argument("--case", type=str, default=None)
    return Options.model_validate(obj=parser.parse_args().__dict__)


def selected_document(
    *, target: Target, args: Options
) -> dict[str, BoundaryValue]:
    """Select the existing corpus or the capability-aware expansion."""
    if args.mode == "baseline":
        document = TypeAdapter[dict[str, BoundaryValue]](
            type=dict[str, BoundaryValue],
        ).validate_json(
            input_for_capabilities(
                capabilities=target.language.variant_metadata.round_trip_capabilities,
            )
        )
        # Corpus identifiers deliberately use only lowercase letters/digits.
        # This avoids testing RECORD field-case conversion as value corruption.
        document = {
            key.replace("_", ""): value for key, value in document.items()
        }
        # The existing non-Python harnesses document this same exclusion.
        if target.runtime != "python":
            _ = document.pop("biginteger")
    else:
        document = dict(cases(target=target))
        if args.case is not None:
            document = {args.case: document[args.case]}
    return document


def main() -> None:
    """Write inputs, generated source, diagnostics and timing."""
    args = options()
    target = targets()[args.target]
    output: Path = args.output
    output.mkdir(parents=True, exist_ok=True)
    document = selected_document(target=target, args=args)
    if len(document) > _MAX_CASES or depth(value=document) > _MAX_DEPTH:
        msg = "corpus exceeds its documented size/depth budget"
        raise ValueError(msg)
    _ = (output / "input.yaml").write_text(data=yaml.safe_dump(data=document))
    started = time.monotonic()
    status = "pass"
    try:
        if args.mode == "expanded":
            rejection_audit(target=target)
            control_rejection_audit(target=target)
            record_rejection_audit(target=target)
        source = program(target=target, document=document)
        _ = (output / "source.txt").write_text(data=source)
        with tempfile.TemporaryDirectory() as temporary:
            result = execute(
                target=target, source=source, directory=Path(temporary)
            )
        _ = (output / "stdout.txt").write_text(data=result.stdout)
        _ = (output / "stderr.txt").write_text(data=result.stderr)
        if result.returncode != 0:
            status = "compile/runtime failure"
        else:
            actual = TypeAdapter[JsonValue](type=JsonValue).validate_json(
                result.stdout
            )
            wanted = observe(
                value=document, javascript=target.runtime == "javascript"
            )
            if actual != wanted:
                status = "semantic mismatch"
                _ = (output / "expected.json").write_text(
                    data=json.dumps(obj=wanted)
                )
    except (ValueError, TypeError, LiteralizerError) as error:
        status = "render/rejection failure"
        _ = (output / "stderr.txt").write_text(data=str(object=error))
    report = {
        "target": args.target,
        "mode": args.mode,
        "cases": len(document),
        "depth": depth(value=document),
        "seconds": time.monotonic() - started,
        "status": status,
    }
    text = json.dumps(obj=report)
    _ = (output / "report.json").write_text(data=text)
    _ = sys.stdout.write(f"{text}\n")
    if status != "pass":
        sys.exit(1)


if __name__ == "__main__":
    main()
