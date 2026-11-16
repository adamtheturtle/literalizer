"""Verify the complete Roc JSON corpus and recursive inspection.

The pinned compiler and command-line platform execute a generated value through
an explicit JSON walker. The shared semantic comparison covers the entire
capability-selected input without exclusions. A second program checks the
shared recursive value from issue 5433 through the public API and Str.inspect.
"""

import json
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Roc
from scripts import roundtrip_common
from scripts.bounded_command import bounded_command

# Keep this platform paired with ROC_NIGHTLY_BUILD in the lint workflow.
_BASIC_CLI_URL = (
    "https://github.com/roc-lang/basic-cli/releases/download/0.28.1/"
    "7brgwR8YUqfeGrkdfF1V4GPPN7DnP7ftqub9KcrTEZtr.tar.zst"
)
_VAR_NAME = "my_data"
_LABEL = "Roc"
_SOURCE_FILENAME = "main.roc"


_WALKER = r"""
val_to_json : Val -> Str
val_to_json = |v| match v {
    RBool(b) => if b "true" else "false"
    RInt(n) => n.to_str()
    RFloat(f) => f.to_str()
    RStr(s) => escape_str(s)
    RList(items) => {
        parts = items.map(|x| val_to_json(x))
        joined = Str.join_with(parts, ",")
        "[${joined}]"
    }
    RDict(entries) => {
        parts = entries.map(|entry| {
            (k, value) = entry
            key = escape_str(k)
            encoded = val_to_json(value)
            "${key}:${encoded}"
        })
        joined = Str.join_with(parts, ",")
        "{${joined}}"
    }
}

escape_str : Str -> Str
escape_str = |s| {
    escaped = s.to_utf8().fold([], |acc, b| acc.concat(escape_byte(b)))
    inner = Str.from_utf8(escaped) ?? ""
    "\"${inner}\""
}

escape_byte : U8 -> List(U8)
escape_byte = |b| match b {
    0x22 => [0x5c, 0x22]
    0x5c => [0x5c, 0x5c]
    0x08 => [0x5c, 0x62]
    0x0c => [0x5c, 0x66]
    0x0a => [0x5c, 0x6e]
    0x0d => [0x5c, 0x72]
    0x09 => [0x5c, 0x74]
    _ => [b]
}
"""


def _build_program(*, json_text: str) -> str:
    """Build a new-compiler app with the same explicit value walker."""
    result = roundtrip_common.literalize_new_variable(
        language=Roc(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    return (
        f'app [main!] {{ pf: platform "{_BASIC_CLI_URL}" }}\n'
        f"import pf.Stdout\n\n{result.code}\n{_WALKER}\n"
        "main! = |_args| {\n"
        f"    Stdout.line!(val_to_json({_VAR_NAME}))?\n"
        "    Ok({})\n}\n"
    )


def _check_recursive_inspection(*, roc: str) -> None:
    """Execute the public shared-reference regression from issue 5433."""
    result = literalize(
        source='{"a":{"$ref":"shared"}}',
        input_format=InputFormat.JSON,
        language=Roc(),
        variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        ref_key="$ref",
        bound_refs={"shared": [1, 2]},
        wrap_in_file=True,
    )
    expected = 'RDict([("a", RList([RInt(1), RInt(2)]))])'
    program = (
        f"{result.code}\n\n"
        f"expect Str.inspect({_VAR_NAME}) == {json.dumps(obj=expected)}\n"
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "inspection.roc"
        _ = path.write_text(data=program, encoding="utf-8")
        for command in ("check", "test"):
            _ = subprocess.run(
                args=bounded_command(
                    args=[roc, command, "--no-color", str(object=path)],
                    fixture=str(object=path),
                    timeout_seconds=60,
                ),
                check=True,
            )


def _log_progress(*, message: str) -> None:
    """Flush a diagnostic before any potentially stalled work."""
    _ = sys.stderr.write(f"{message}\n")
    _ = sys.stderr.flush()


def main() -> None:
    """Round-trip the shared document and verify recursive inspection."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Roc.variant_metadata.round_trip_capabilities,
    )
    _log_progress(message=f"{_LABEL}: generating {_SOURCE_FILENAME}")
    program = _build_program(json_text=json_text)
    _log_progress(
        message=f"{_LABEL}: generated {_SOURCE_FILENAME} "
        f"({len(program.encode(encoding='utf-8'))} bytes)",
    )
    roc = shutil.which(cmd="roc")
    if roc is None or roc == "":
        roc = "roc"
    args = [roc, "run", _SOURCE_FILENAME]
    _log_progress(
        message=f"{_LABEL}: launching {shlex.join(split_command=args)} "
        f"(source: {_SOURCE_FILENAME})",
    )
    roundtrip_common.execute(
        label=_LABEL,
        source_filename=_SOURCE_FILENAME,
        program=program,
        steps=[
            roundtrip_common.Step(args=args, failure_label="roc run error")
        ],
        excluded_keys=(),
        expected_json=json_text,
        extra_files=None,
    )
    _check_recursive_inspection(roc=roc)


if __name__ == "__main__":
    main()
