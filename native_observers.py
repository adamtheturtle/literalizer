"""Bounded typed scalar and sequence discovery for Literalizer #5493."""

import base64
import collections
from decimal import Decimal
import datetime as dt
import json
import math
import os
import random
import struct
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from literalizer import (
    CollectionLayout,
    InputFormat,
    NewVariable,
    literalize,
    literalize_call,
)
from literalizer.exceptions import (
    UnrepresentableEmptyDictError,
    UnrepresentableInputError,
    UnrepresentableIntegerError,
)
from literalizer.languages import JavaScript, Lua, Php, Python, Ruby

UTC = dt.timezone.utc
EPOCH = dt.datetime(1970, 1, 1, tzinfo=UTC)
SEEDS = (5493, 6569, 0)
RUNTIME = {
    "Python": (sys.executable, "sample.py"),
    "JavaScript": ("node", "sample.js"),
    "Lua": ("lua", "sample.lua"),
    "Ruby": ("ruby", "sample.rb"),
    "Php": ("php", "sample.php"),
}
OBSERVERS = {
    "Python": """
import datetime as dt
import struct
def capture(value):
    kind = type(value)
    if kind is list or kind is tuple:
        print(f"{kind.__name__}:{len(value)}")
        for item in value:
            capture(item)
    elif kind is bytes:
        print("bytes:" + value.hex())
    elif kind is dt.datetime:
        print("datetime:" + value.isoformat(timespec="microseconds"))
    elif kind is dt.date:
        print("date:" + value.isoformat())
    elif value is None:
        print("null:")
    elif kind is bool:
        print(f"bool:{int(value)}")
    elif kind is int:
        print(f"int:{value}")
    elif kind is float:
        print("f64:" + struct.pack(">d", value).hex())
    elif kind is str:
        print("text:" + value.encode().hex())
    else:
        raise TypeError(kind)
""",
    "JavaScript": """
function observe(value) {
  if (Array.isArray(value)) {
    console.log("list:" + value.length);
    for (const item of value) observe(item);
  } else if (value instanceof Date) {
    console.log("datejs:" + value.toISOString());
  } else if (value === null) {
    console.log("null:");
  } else if (typeof value === "boolean") {
    console.log("bool:" + Number(value));
  } else if (typeof value === "number") {
    const bytes = Buffer.alloc(8);
    bytes.writeDoubleBE(value);
    console.log("f64:" + bytes.toString("hex"));
  } else if (typeof value === "string") {
    console.log("text:" + Buffer.from(value, "utf8").toString("hex"));
  } else {
    throw new TypeError(typeof value);
  }
}
function capture({value}) { observe(value); }
""",
    "Lua": """
local function hex(value)
  return (value:gsub(".", function(ch) return string.format("%02x", ch:byte()) end))
end
local function capture(value)
  local kind = type(value)
  if kind == "table" then
    local count = 0
    for key in pairs(value) do
      assert(math.type(key) == "integer" and key >= 1 and key <= #value)
      count = count + 1
    end
    assert(count == #value)
    print("list:" .. count)
    for i = 1, count do capture(value[i]) end
  elseif kind == "nil" then
    print("null:")
  elseif kind == "boolean" then
    print("bool:" .. (value and "1" or "0"))
  elseif math.type(value) == "integer" then
    print("int:" .. value)
  elseif kind == "number" then
    print("f64:" .. hex(string.pack(">d", value)))
  elseif kind == "string" then
    print("text:" .. hex(value))
  else
    error(kind)
  end
end
""",
    "Ruby": """
def observe(value)
  case value
  when Array
    puts("list:#{value.length}")
    value.each { |item| observe(item) }
  when Time
    puts("datetime:" + value.strftime("%Y-%m-%dT%H:%M:%S.%6N%:z"))
  when ->(candidate) { defined?(Date) && candidate.is_a?(Date) }
    puts("date:" + value.iso8601)
  when NilClass
    puts("null:")
  when TrueClass, FalseClass
    puts("bool:#{value ? 1 : 0}")
  when Integer
    puts("int:#{value}")
  when Float
    puts("f64:" + [value].pack("G").unpack1("H*"))
  when String
    puts("text:" + value.unpack1("H*"))
  else
    raise TypeError, value.class.to_s
  end
end
def capture(value:)
  observe(value)
end
""",
    "Php": r"""
function capture($value) {
    if (is_array($value)) {
        if (!array_is_list($value)) throw new Exception("expected sequence");
        echo "list:", count($value), "\n";
        foreach ($value as $item) capture($item);
    } elseif ($value instanceof DateTimeInterface) {
        echo "datetime:", $value->format('Y-m-d\TH:i:s.uP'), "\n";
    } elseif ($value === null) {
        echo "null:\n";
    } elseif (is_bool($value)) {
        echo "bool:", (int) $value, "\n";
    } elseif (is_int($value)) {
        echo "int:", $value, "\n";
    } elseif (is_float($value)) {
        echo "f64:", bin2hex(pack("E", $value)), "\n";
    } elseif (is_string($value)) {
        echo "text:", bin2hex($value), "\n";
    } else {
        throw new Exception(gettype($value));
    }
}
""",
}


def yaml_source(value):
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()
    if isinstance(value, bytes):
        return "!!binary " + json.dumps(
            base64.b64encode(value).decode("ascii")
        )
    if isinstance(value, list):
        return "[" + ", ".join(map(yaml_source, value)) + "]"
    return json.dumps(value, ensure_ascii=False)


def expected_lines(value, backend, alternate):
    if isinstance(value, list):
        kind = "tuple" if backend == "Python" and not alternate else "list"
        return [
            f"{kind}:{len(value)}",
            *(
                entry
                for child in value
                for entry in expected_lines(child, backend, alternate)
            ),
        ]
    if isinstance(value, bytes):
        if backend == "Python" and not alternate:
            return ["bytes:" + value.hex()]
        encoding = (
            base64.b64encode(value).decode("ascii")
            if alternate
            else value.hex()
        )
        return ["text:" + encoding.encode().hex()]
    if isinstance(value, dt.date):
        moment = (
            value
            if isinstance(value, dt.datetime)
            else dt.datetime.combine(value, dt.time(), UTC)
        )
        if alternate and backend != "Python":
            return ["text:" + value.isoformat().encode().hex()]
        if backend == "Lua":
            offset = moment - EPOCH
            whole = offset.days * 86400 + offset.seconds
            value = (
                whole
                if not offset.microseconds
                else float(
                    Decimal(whole) + Decimal(offset.microseconds) / 1000000
                )
            )
        elif backend == "JavaScript":
            instant = (
                moment.astimezone(UTC)
                .isoformat(timespec="milliseconds")
                .replace("+00:00", "Z")
            )
            return ["datejs:" + instant]
        elif backend == "Php" or isinstance(value, dt.datetime):
            return ["datetime:" + moment.isoformat(timespec="microseconds")]
        else:
            return ["date:" + value.isoformat()]
    if value is None:
        return ["null:"]
    if isinstance(value, bool):
        return [f"bool:{int(value)}"]
    if isinstance(value, int) and backend != "JavaScript":
        return [f"int:{value}"]
    if isinstance(value, (int, float)):
        return ["f64:" + struct.pack(">d", value).hex()]
    if isinstance(value, str):
        return ["text:" + value.encode().hex()]
    raise TypeError(type(value))


def language_profiles():
    for cls in (Python, JavaScript, Lua, Ruby, Php):
        main_options = {}
        alternate_options = {
            "string_format": cls.string_formats.SINGLE,
            "integer_format": cls.integer_formats.HEX,
            "float_format": cls.float_formats.SCIENTIFIC,
            "bytes_format": cls.bytes_formats.BASE64,
        }
        if cls is Python:
            main_options["bytes_format"] = Python.bytes_formats.PYTHON
            alternate_options["sequence_format"] = Python.sequence_formats.LIST
        else:
            alternate_options.update(
                date_format=cls.date_formats.ISO,
                datetime_format=cls.datetime_formats.ISO,
            )
        yield cls.__name__, False, cls(**main_options)
        yield cls.__name__, True, cls(**alternate_options)


def values_for_seed(seed):
    rng = random.Random(seed)
    day = rng.choice(
        [
            dt.date(9, 2, 28),
            dt.date(1582, 10, 10),
            dt.date(1970, 1, 1),
            dt.date(2024, 2, 29),
        ]
    )
    east = dt.timezone(dt.timedelta(hours=5, minutes=30))
    moment = dt.datetime(
        1969, 12, 31, 23, 59, 59, rng.randrange(1, 999) * 1000, tzinfo=east
    )
    octets = rng.randbytes(rng.randint(1, 9))
    number = rng.randint(-1000000, 1000000)
    small = math.ldexp(rng.random(), rng.choice([-12, -40, -90]))
    text = rng.choice(
        ["é中😀", "alpha\\beta", "e\u0301", "newline\nfollow", "tab\tend"]
    )
    yield from (
        False,
        number,
        -0.0,
        small,
        -5e-324,
        1.7976931348623157e308,
        text,
        None,
        octets,
        day,
        moment,
        [],
        [number, False, -0.0, text],
        [day, moment, octets],
        [[number, octets], [], [text, [small]]],
    )


def program_for(*, backend, language, alternate, source, input_format, api):
    layout = (
        CollectionLayout.MULTILINE if alternate else CollectionLayout.COMPACT
    )
    options = dict(
        source=source,
        input_format=input_format,
        language=language,
        collection_layout=layout,
    )
    if api in ("whole", "rows"):
        result = literalize_call(
            **options,
            input_root_key="sample"
            if input_format is InputFormat.TOML
            else None,
            target_function="capture",
            parameter_names=("value",),
            per_element=api == "rows",
        )
        code = result.code
    elif api == "new":
        result = literalize(
            **options,
            variable_form=NewVariable(name="sample", modifiers=frozenset()),
        )
        code = (
            result.code
            + "\n"
            + {
                "Ruby": "capture(value: sample)",
                "Php": "capture($sample);",
                "JavaScript": "observe(sample);",
            }.get(backend, "capture(sample)")
        )
    else:
        result = literalize(**options)
        operand = result.code
        code = {
            "Ruby": f"capture(value: {operand})",
            "JavaScript": f"observe({operand});",
            "Php": f"capture({operand});",
        }.get(backend, f"capture({operand})")
    return "\n".join(
        (*result.preamble, *result.body_preamble, OBSERVERS[backend], code, "")
    )


def observe(backend, program, deadline):
    command, filename = RUNTIME[backend]
    with tempfile.TemporaryDirectory() as directory:
        (Path(directory) / filename).write_text(program, encoding="utf-8")
        remaining = deadline - time.monotonic()
        assert remaining > 0, "overall discovery deadline reached"
        result = subprocess.run(
            [command, filename],
            cwd=directory,
            env={**os.environ, "TZ": "UTC"},
            capture_output=True,
            text=True,
            timeout=min(8, remaining),
        )
    return result.returncode, result.stdout.splitlines(), result.stderr


def run_controls(deadline):
    mutations = (
        ("boolean-to-integer", True, 1),
        ("signed-zero", -0.0, 0.0),
        ("binary-octet", b"\x00\xff", b"\x00\xfe"),
        ("sequence-width", [1, [2, 3]], [1, [2]]),
    )
    mutation_count = 0
    for backend, alternate, language in language_profiles():
        if alternate:
            continue
        for name, expected, mutated in mutations:
            program = program_for(
                backend=backend,
                language=language,
                alternate=alternate,
                source=yaml_source(mutated),
                input_format=InputFormat.YAML,
                api="whole",
            )
            status, actual, stderr = observe(backend, program, deadline)
            assert status == 0, (backend, name, program, stderr)
            assert actual == expected_lines(mutated, backend, alternate), (
                backend,
                name,
                actual,
            )
            assert actual != expected_lines(expected, backend, alternate), (
                backend,
                name,
            )
            mutation_count += 1
    unsupported = (
        (JavaScript(), "9007199254740993", UnrepresentableIntegerError),
        (
            JavaScript(),
            "1969-12-31T23:59:59.123456Z",
            UnrepresentableInputError,
        ),
        (Lua(), "{}", UnrepresentableEmptyDictError),
        (Lua(), "{null: 1}", UnrepresentableInputError),
        (Php(), "{}", UnrepresentableEmptyDictError),
        (Php(), '{"0": false}', UnrepresentableInputError),
    )
    rejection_count = 0
    for language, source, error in unsupported:
        for api in ("bare", "whole"):
            try:
                program_for(
                    backend=type(language).__name__,
                    language=language,
                    alternate=False,
                    source=source,
                    input_format=InputFormat.YAML,
                    api=api,
                )
            except error as exc:
                print(
                    "Expected rejection:",
                    type(language).__name__,
                    api,
                    source,
                    type(exc).__name__,
                )
                rejection_count += 1
            else:
                raise AssertionError(
                    (type(language).__name__, api, source, error)
                )
    print("Wrong-value mutations detected:", mutation_count)
    print("Expected API rejections:", rejection_count)


def main():
    started = time.monotonic()
    deadline = started + 240
    counts = collections.Counter()
    mismatches = []
    first = set()
    for backend, alternate, language in language_profiles():
        for seed in SEEDS:
            for index, value in enumerate(values_for_seed(seed)):
                yaml = yaml_source(value)
                formats = [(InputFormat.YAML, yaml)]
                if index not in (8, 9, 10, 13, 14):
                    formats.append((InputFormat.JSON, json.dumps(value)))
                if index in (0, 1, 2, 3, 9, 10, 11, 12):
                    formats.append((InputFormat.TOML, yaml))
                for input_format, source in formats:
                    apis = (
                        ("bare", "new", "whole", "rows")
                        if index % 3 == 0
                        else ("bare", "whole")
                    )
                    if input_format is InputFormat.TOML:
                        apis = ("whole", "rows")
                    for api in apis:
                        rendered_source = (
                            f"[[{source}]]" if api == "rows" else source
                        )
                        if input_format is InputFormat.TOML:
                            rendered_source = f"sample = {rendered_source}\n"
                        label = dict(
                            backend=backend,
                            alternate=alternate,
                            seed=seed,
                            source=rendered_source,
                            format=input_format.name,
                            api=api,
                        )
                        try:
                            program = program_for(
                                backend=backend,
                                language=language,
                                alternate=alternate,
                                source=rendered_source,
                                input_format=input_format,
                                api=api,
                            )
                            status, actual, stderr = observe(
                                backend, program, deadline
                            )
                            expected = expected_lines(
                                value, backend, alternate
                            )
                        except Exception as exc:
                            mismatches.append(
                                {
                                    **label,
                                    "exception": str(exc),
                                    "type": type(exc).__name__,
                                }
                            )
                            continue
                        if status or actual != expected:
                            mismatch = {
                                **label,
                                "expected": expected,
                                "actual": actual,
                                "status": status,
                                "stderr": stderr,
                            }
                            key = (
                                backend,
                                input_format.name,
                                api,
                                repr(value),
                            )
                            if key not in first:
                                mismatch["program"] = program
                                first.add(key)
                            mismatches.append(mismatch)
                        else:
                            counts[backend, input_format.name, api] += 1
    for (backend, input_format, api), count in sorted(counts.items()):
        print(backend, input_format, api, count)
    print("Native programs passed:", sum(counts.values()))
    print("Mismatch count:", len(mismatches))
    Path(sys.argv[1]).write_text(
        json.dumps(mismatches, indent=2) + "\n", encoding="utf-8"
    )
    if not mismatches:
        run_controls(deadline)
    print("Elapsed seconds:", round(time.monotonic() - started, 3))
    sys.exit(bool(mismatches))


if __name__ == "__main__":
    main()
