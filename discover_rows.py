"""Run bounded Python and JavaScript per-row call discovery from a source checkout."""

import argparse
import contextlib
import dataclasses
import io
import json
import math
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

import hypothesis
from hypothesis import Phase, given, seed, settings
from hypothesis import strategies as st
from ruamel.yaml import YAML

from literalizer import CollectionLayout, InputFormat, literalize_call
from literalizer.languages import JavaScript, Python
from scripts.bounded_command import bounded_command
from scripts.roundtrip_common import verify


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


# Native normalization and rendering profiles adapted from the #5493 archive
# at e53380545ca7d7b3f5e9b682cff8f0e3f0764da1.
PYTHON_NORMALIZER = """
import json
import math

def normalize(value):
    if value is None:
        return ["null"]
    if isinstance(value, bool):
        return ["bool", value]
    if isinstance(value, str):
        return ["string", value]
    if isinstance(value, (int, float)):
        if value == 0:
            return ["number", "-zero" if math.copysign(1, value) < 0 else "+zero"]
        return ["number", value]
    if isinstance(value, dict):
        return ["dict", [[key, normalize(value[key])] for key in sorted(value)]]
    if isinstance(value, (list, tuple)):
        return [type(value).__name__, [normalize(item) for item in value]]
    raise TypeError(type(value))
"""

JAVASCRIPT_NORMALIZER = """
function normalize(value) {
    if (value === null) return ["null"];
    if (typeof value === "boolean") return ["bool", value];
    if (typeof value === "string") return ["string", value];
    if (typeof value === "number") {
        return ["number", value === 0 ? (Object.is(value, -0) ? "-zero" : "+zero") : value];
    }
    if (Array.isArray(value)) return ["array", value.map(normalize)];
    if (value instanceof Map) {
        return ["map", [...value.keys()].sort().map(key => [key, normalize(value.get(key))])];
    }
    if (Object.getPrototypeOf(value) === Object.prototype) {
        return ["object", Object.keys(value).sort().map(key => [key, normalize(value[key])])];
    }
    throw Error("unexpected value");
}
"""


@dataclasses.dataclass(frozen=True)
class Profile:
    language: Python | JavaScript
    layout: CollectionLayout
    sequence_kind: str
    mapping_kind: str
    runtime: str


PROFILES = {
    "python-tuple": Profile(
        Python(), CollectionLayout.COMPACT, "tuple", "dict", "python"
    ),
    "python-list": Profile(
        Python(
            sequence_format=Python.sequence_formats.LIST,
            variable_type_hints=Python.variable_type_hints_formats.SAFE,
            string_format=Python.string_formats.SINGLE,
            float_format=Python.float_formats.SCIENTIFIC,
            integer_format=Python.integer_formats.HEX,
        ),
        CollectionLayout.MULTILINE,
        "list",
        "dict",
        "python",
    ),
    "javascript-object": Profile(
        JavaScript(),
        CollectionLayout.COMPACT,
        "array",
        "object",
        "node",
    ),
    "javascript-map": Profile(
        JavaScript(
            dict_format=JavaScript.dict_formats.MAP,
            declaration_style=JavaScript.declaration_styles.LET,
            call_style=JavaScript.call_styles.POSITIONAL,
            string_format=JavaScript.string_formats.MULTILINE,
            float_format=JavaScript.float_formats.FIXED,
            integer_format=JavaScript.integer_formats.HEX,
        ),
        CollectionLayout.MULTILINE,
        "array",
        "map",
        "node",
    ),
}

TEXT = st.text(alphabet="abXYZ09 _-\n\r\t\x00\"'\\${}`é中🙂", max_size=12)
KEYS = st.one_of(
    st.sampled_from(["", "__proto__", "constructor", "value", "a", "z", "${x}", "01"]),
    st.text(alphabet="abcXYZ_-$", min_size=1, max_size=8),
)
SCALARS = st.one_of(
    st.none(),
    st.booleans(),
    st.integers(min_value=-1_000_000, max_value=1_000_000),
    st.floats(
        min_value=-1_000_000, max_value=1_000_000, allow_nan=False, allow_infinity=False
    ),
    st.sampled_from([-0.0, 0.0, 1.0, 0.1, 1e-100]),
    TEXT,
)


def values(depth):
    if depth == 0:
        return SCALARS
    children = values(depth - 1)
    return st.one_of(
        SCALARS,
        st.lists(children, max_size=3),
        st.dictionaries(KEYS, children, max_size=3),
    )


@st.composite
def call_rows(draw):
    arity = draw(st.integers(min_value=2, max_value=4))
    identifiers = draw(
        st.lists(st.integers(0, 99), min_size=2, max_size=4, unique=True)
    )
    arguments = st.lists(values(3), min_size=arity - 1, max_size=arity - 1)
    return [[f"row-{identifier}", *draw(arguments)] for identifier in identifiers]


def expected_argument(value, profile):
    if value is None:
        return ["null"]
    if isinstance(value, bool):
        return ["bool", value]
    if isinstance(value, str):
        return ["string", value]
    if isinstance(value, (int, float)):
        if value == 0:
            return ["number", "-zero" if math.copysign(1, value) < 0 else "+zero"]
        return ["number", value]
    if isinstance(value, list):
        return [
            profile.sequence_kind,
            [expected_argument(item, profile) for item in value],
        ]
    if isinstance(value, dict):
        return [
            profile.mapping_kind,
            [[key, expected_argument(value[key], profile)] for key in sorted(value)],
        ]
    raise TypeError(type(value))


def consumer(profile, parameters):
    arguments = ", ".join(parameters)
    if profile.runtime == "python":
        return (
            PYTHON_NORMALIZER + f"\ncalls = []\ndef consume(*, {arguments}):\n"
            f"    calls.append([normalize(value) for value in ({arguments})])\n",
            'print(json.dumps({"calls": calls}, allow_nan=False))\n',
        )
    if profile.language.call_style is JavaScript.call_styles.OBJECT:
        binding = f"""
function consume(argument) {{
    const keys = {json.dumps(parameters)};
    if (arguments.length !== 1 || Object.keys(argument).length !== keys.length ||
        !keys.every(key => Object.hasOwn(argument, key))) {{
        throw Error("unexpected argument keys");
    }}
    calls.push(keys.map(key => normalize(argument[key])));
}}
"""
    else:
        binding = f"""
function consume(...values) {{
    if (values.length !== {len(parameters)}) throw Error("unexpected argument count");
    calls.push(values.map(normalize));
}}
"""
    return (
        JAVASCRIPT_NORMALIZER + "\nconst calls = [];\n" + binding,
        "process.stdout.write(JSON.stringify({calls}));\n",
    )


def serialize(rows, fmt):
    if fmt is InputFormat.JSON:
        return json.dumps(rows, allow_nan=False)
    stream = io.StringIO()
    YAML(typ="safe", pure=True).dump(rows, stream)
    return stream.getvalue()


def run_case(
    *, case, rows, profile_name, fmt, executable, deadline, timeout, reproduce
):
    case.mkdir()
    write_json(
        case / "input.json", {"profile": profile_name, "format": fmt.name, "rows": rows}
    )
    (case / "replay.sh").write_text(reproduce(case / "input.json") + "\n")
    profile = PROFILES[profile_name]
    source = serialize(rows, fmt)
    (case / "source.txt").write_text(source)
    parameters = [f"arg{index}" for index in range(len(rows[0]))]
    result = literalize_call(
        source=source,
        input_format=fmt,
        language=profile.language,
        target_function="consume",
        parameter_names=parameters,
        collection_layout=profile.layout,
        per_element=True,
    )
    prefix, suffix = consumer(profile, parameters)
    program = case / ("consumer.py" if profile.runtime == "python" else "consumer.js")
    program.write_text(
        "\n".join(
            (*result.preamble, *result.body_preamble, prefix, result.code, suffix)
        )
    )
    expected = {
        "calls": [[expected_argument(value, profile) for value in row] for row in rows]
    }
    write_json(case / "expected.json", expected)
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError(f"overall deadline reached at {case / 'input.json'}")
    command = bounded_command(
        args=[executable, program],
        fixture=str(case / "input.json"),
        timeout_seconds=min(timeout, remaining),
    )
    (case / "execute.sh").write_text(shlex.join(command) + "\n")
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=min(timeout + 1, remaining),
    )
    (case / "stdout.json").write_text(completed.stdout)
    (case / "stderr.txt").write_text(completed.stderr)
    completed.check_returncode()
    expected_json = json.dumps(expected)
    verify(
        label=str(case),
        produced_json=completed.stdout,
        exclude_keys=(),
        expected_json=expected_json,
    )
    got = json.loads(completed.stdout)["calls"]
    first, second, *rest = got
    mutations = {
        "swapped-rows": [second, first, *rest],
        "swapped-arguments": [[first[1], first[0], *first[2:]], second, *rest],
        "dropped-row": [second, *rest],
    }
    for name, changed in mutations.items():
        payload = {"calls": changed}
        write_json(case / f"{name}.json", payload)
        with contextlib.redirect_stderr(io.StringIO()):
            try:
                verify(
                    label=name,
                    produced_json=json.dumps(payload),
                    exclude_keys=(),
                    expected_json=expected_json,
                )
            except SystemExit as exc:
                if exc.code != 1:
                    raise
            else:
                raise AssertionError(f"oracle accepted {name} at {case}")
    return list(mutations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=5493)
    parser.add_argument("--examples", type=int, default=24)
    parser.add_argument("--budget-seconds", type=int, default=120)
    parser.add_argument("--child-seconds", type=int, default=10)
    parser.add_argument("--replay", type=Path)
    args = parser.parse_args()
    if min(args.examples, args.budget_seconds, args.child_seconds) <= 0:
        parser.error("examples and deadlines must be positive")
    started = time.monotonic()
    deadline = started + args.budget_seconds
    output = args.output.resolve()
    output.mkdir(parents=True)
    replay = json.loads(args.replay.read_text()) if args.replay else None
    runtimes = {"python": sys.executable, "node": shutil.which("node")}

    def capture(command):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise TimeoutError("overall deadline reached during setup")
        return subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=min(args.child_seconds, remaining),
        ).stdout.strip()

    selected = [replay["profile"]] if replay else list(PROFILES)
    versions = {}
    for runtime in sorted({PROFILES[name].runtime for name in selected}):
        executable = runtimes[runtime]
        if executable is None:
            raise RuntimeError(f"missing native runtime: {runtime}")
        versions[runtime] = {
            "path": executable,
            "version": capture([executable, "--version"]),
        }

    def reproduce(input_path=None):
        destination = (
            str(input_path.parent) + "-replay" if input_path else str(output) + "-rerun"
        )
        command = [
            sys.executable,
            str(Path(__file__).resolve()),
            "--output",
            destination,
            "--seed",
            str(args.seed),
            "--examples",
            str(args.examples),
            "--budget-seconds",
            str(args.budget_seconds),
            "--child-seconds",
            str(args.child_seconds),
        ]
        if input_path:
            command.extend(["--replay", str(input_path)])
        return "PYTHONPATH=.:src " + shlex.join(
            [
                "scripts/run-bounded.sh",
                "row-discovery",
                "--signal=KILL",
                f"{args.budget_seconds}s",
                *command,
            ]
        )

    write_json(
        output / "metadata.json",
        {
            "source_head": capture(["git", "rev-parse", "HEAD"]),
            "seed": args.seed,
            "examples_per_profile_and_format": args.examples,
            "budget_seconds": args.budget_seconds,
            "child_seconds": args.child_seconds,
            "hypothesis": hypothesis.__version__,
            "controller": sys.version,
            "runtimes": versions,
            "reproduce": reproduce(args.replay.resolve() if args.replay else None),
            "profiles": {
                name: {
                    "layout": PROFILES[name].layout.value,
                    "options": {
                        field.name: str(getattr(PROFILES[name].language, field.name))
                        for field in dataclasses.fields(PROFILES[name].language)
                    },
                }
                for name in selected
            },
        },
    )

    cases = []

    def run(rows, profile, fmt):
        case = output / f"{len(cases):04d}"
        (output / "active.txt").write_text(f"{case / 'input.json'}\n")
        mutations = run_case(
            case=case,
            rows=rows,
            profile_name=profile,
            fmt=fmt,
            executable=runtimes[PROFILES[profile].runtime],
            deadline=deadline,
            timeout=args.child_seconds,
            reproduce=reproduce,
        )
        cases.append(
            {
                "case": case.name,
                "profile": profile,
                "format": fmt.name,
                "calls": len(rows),
                "arity": len(rows[0]),
                "rejected_mutations": mutations,
            }
        )

    def generate(profile, fmt):
        @seed(args.seed)
        @settings(
            max_examples=args.examples,
            database=None,
            deadline=None,
            phases=(Phase.generate,),
        )
        @given(call_rows())
        def probe(rows):
            run(rows, profile, fmt)

        probe()

    try:
        if replay:
            run(replay["rows"], replay["profile"], InputFormat[replay["format"]])
        else:
            for profile in selected:
                for fmt in (InputFormat.JSON, InputFormat.YAML):
                    generate(profile, fmt)
    finally:
        summary = {
            "programs_passed": len(cases),
            "calls_verified": sum(case["calls"] for case in cases),
            "mutations_rejected": sum(
                len(case["rejected_mutations"]) for case in cases
            ),
            "elapsed_seconds": round(time.monotonic() - started, 3),
        }
        write_json(output / "results.json", {"summary": summary, "cases": cases})
        print(json.dumps(summary), flush=True)


if __name__ == "__main__":
    main()
