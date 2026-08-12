"""Bash JSON round-trip check (issue #2640).

Literalize the shared ``roundtrip_input.json`` document to a Bash
``declare -A myData=(...)`` binding, wrap it in a script that re-emits
JSON on standard output, run it under ``bash``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Bash roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the pinned ``bash`` interpreter lints and executes the ``.sh``
fixtures.  It shares the same input and comparison logic as the other
per-language round-trip helpers.

Bash has no standard JSON library, and its associative arrays cannot
nest: the backend stores every nested array or object as an *escaped
string* whose text is itself a single-level Bash array literal (see
``_to_bash_value`` in ``src/literalizer/languages/bash.py``).  A generic
encoder therefore cannot walk ``$myData`` blindly -- it cannot tell a
nested-collection string from an ordinary string, nor a literalized
boolean (``true``/``false``) from a string of the same text.  This
script instead drives the re-emission along the *known* JSON shape, the
same strategy the Tcl helper uses: Python walks the parsed input and
generates Bash statements that read each leaf out of ``$myData`` and,
for each nested collection, ``eval`` its stored string back into a fresh
array before descending.  Bash keeps the textual form of un-shimmered
numeric scalars, so wide integers and large exponents round-trip without
the precision-loss exclusions the typed-language scripts need.
"""

import json
import shutil

from literalizer.languages import Bash
from scripts import roundtrip_common

# `json.loads` returns this recursive shape; typing the walker against
# it lets `isinstance` narrow cleanly under pyright, pyrefly, and ty
# without `cast`.
type JsonValue = (
    bool
    | int
    | float
    | str
    | list["JsonValue"]
    | dict[str, "JsonValue"]
    | None
)

_VAR_NAME = "myData"
_LABEL = "Bash"

# A minimal JSON string escaper: the round-trip must serialize the
# *runtime* value, so escaping happens in Bash rather than being baked in
# at code-generation time.  Backslash is replaced first so the escapes
# added afterwards are not doubled.  The shared input carries no control
# characters beyond these, and UTF-8 string bytes pass straight through.
_JSON_STR_FN = """\
_json_str() {
    local s=$1
    s=${s//\\\\/\\\\\\\\}
    s=${s//\\"/\\\\\\"}
    s=${s//$'\\n'/\\\\n}
    s=${s//$'\\r'/\\\\r}
    s=${s//$'\\t'/\\\\t}
    printf '"%s"' "$s"
}
"""


def _emit_value(
    *,
    value: JsonValue,
    ref: str,
    lines: list[str],
    counter: list[int],
) -> None:
    """Append Bash statements that emit the JSON encoding of *value*.

    *ref* is the Bash subscript expression (e.g. ``myData[int]`` or
    ``_c1[0]``) that, expanded as ``${ref}``, yields this node's raw
    stored value.  Generated statements append to the ``out`` variable.
    """
    if isinstance(value, bool):
        lines.append(f'out+="${{{ref}}}"')
    elif isinstance(value, (int, float)):
        # The stored textual form is already a valid JSON number.
        lines.append(f'out+="${{{ref}}}"')
    elif isinstance(value, str):
        lines.append(f'out+="$(_json_str "${{{ref}}}")"')
    elif isinstance(value, list):
        var = _next_var(counter=counter)
        lines.append(f'eval "{var}=${{{ref}}}"')
        _emit_array(items=value, var=var, lines=lines, counter=counter)
    elif isinstance(value, dict):
        var = _next_var(counter=counter)
        lines.append(f'eval "declare -A {var}=${{{ref}}}"')
        _emit_object(entries=value, var=var, lines=lines, counter=counter)
    else:
        # The shared document is null-free; this arm keeps the walker
        # total for the type checker.
        lines.append("out+=null")


def _emit_array(
    *,
    items: list[JsonValue],
    var: str,
    lines: list[str],
    counter: list[int],
) -> None:
    """Append Bash statements emitting a JSON array from indexed *var*."""
    lines.append("out+='['")
    for index, item in enumerate(iterable=items):
        if index:
            lines.append("out+=','")
        _emit_value(
            value=item,
            ref=f"{var}[{index}]",
            lines=lines,
            counter=counter,
        )
    lines.append("out+=']'")


def _emit_object(
    *,
    entries: dict[str, JsonValue],
    var: str,
    lines: list[str],
    counter: list[int],
) -> None:
    """Append Bash statements emitting a JSON object from assoc *var*.

    The shared ``roundtrip_input.json`` only has ASCII-identifier keys,
    so each key is a literal Bash subscript and embeds cleanly in the
    single-quoted JSON key fragment.
    """
    lines.append("out+='{'")
    for index, (key, sub_value) in enumerate(iterable=entries.items()):
        if index:
            lines.append("out+=','")
        lines.append(f"out+='{json.dumps(obj=key)}:'")
        _emit_value(
            value=sub_value,
            ref=f"{var}[{key}]",
            lines=lines,
            counter=counter,
        )
    lines.append("out+='}'")


def _next_var(*, counter: list[int]) -> str:
    """Return a fresh unique Bash variable name for an eval'd child."""
    counter[0] += 1
    return f"_c{counter[0]}"


def _build_program(json_text: str) -> str:
    """Return a runnable Bash script literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Bash(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    # The shared document is a top-level JSON object, so the parsed value
    # is always a `dict`.
    parsed: dict[str, JsonValue] = json.loads(s=json_text)
    lines: list[str] = ['out=""']
    # The top-level value is always a JSON object, declared by
    # `result.code` as the associative array `$myData`; descend into it
    # directly without an `eval` round-trip.
    _emit_object(
        entries=parsed,
        var=_VAR_NAME,
        lines=lines,
        counter=[0],
    )
    lines.append('printf %s "$out"')
    body = "\n".join(lines)
    return f"{preamble}\n{result.code}\n{_JSON_STR_FN}\n{body}\n"


def main() -> None:
    """Round-trip the shared document through the Bash backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    bash = shutil.which(cmd="bash") or "bash"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.sh",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[bash, "main.sh"],
                failure_label="bash runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
