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
from pathlib import Path

import click
from pydantic import JsonValue

from literalizer import (
    CollectionLayout,
    InputFormat,
    Language,
    NewVariable,
    literalize,
)
from literalizer.languages import Bash
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Bash"
_JSON_HELPER_PATH = Path(__file__).with_name(name="bash_roundtrip_json.sh")


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
        if index != 0:
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

    A key is carried through a shell variable rather than written into
    the subscript itself, so a key containing a quote, a backtick or a
    ``]`` indexes the array it names instead of breaking the script
    (issue #4545).
    """
    lines.append("out+='{'")
    for index, (key, sub_value) in enumerate(iterable=entries.items()):
        if index != 0:
            lines.append("out+=','")
        key_var = _next_var(counter=counter)
        lines.append(f"{key_var}={_ansi_c_quoted(text=key)}")
        lines.append(f"out+={_single_quoted(text=json.dumps(obj=key))}':'")
        _emit_value(
            value=sub_value,
            ref=f"{var}[${key_var}]",
            lines=lines,
            counter=counter,
        )
    lines.append("out+='}'")


def _single_quoted(*, text: str) -> str:
    """Return *text* as one single-quoted Bash word."""
    escaped = text.replace("'", "'\\''")
    return f"'{escaped}'"


def _ansi_c_quoted(*, text: str) -> str:
    """Return *text* as a Bash ``$'...'`` word.

    ANSI-C quoting spells every byte as an escape, so a key holding a
    quote, a backslash or a control character survives verbatim.
    """
    escaped = "".join(
        f"\\x{byte:02x}" for byte in text.encode(encoding="utf-8")
    )
    return f"$'{escaped}'"


def _next_var(*, counter: list[int]) -> str:
    """Return a fresh unique Bash variable name for an eval'd child."""
    counter[0] += 1
    return f"_c{counter[0]}"


def _build_program(
    *,
    json_text: str,
    language: Language,
    layout: CollectionLayout,
) -> str:
    """Return a runnable Bash script literalized from *json_text*."""
    result = literalize(
        language=language,
        source=json_text,
        input_format=InputFormat.JSON,
        variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        collection_layout=layout,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    # The shared document is a top-level JSON object, so the parsed value
    # is always a `dict`.
    parsed = roundtrip_common.json_object_from_text(text=json_text)
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
    return (
        f"{preamble}\n{result.code}\n"
        f"source ./{_JSON_HELPER_PATH.name}\n{body}\n"
    )


def _check_document(
    *,
    bash: str,
    json_text: str,
    language: Language,
    layout: CollectionLayout,
) -> None:
    """Exercise one option combination in the native shell."""
    roundtrip_common.execute(
        label=(
            f"{_LABEL} {language.declaration_style.name}/"
            f"{language.string_format.name}/{language.integer_format.name}/"
            f"{layout.name}"
        ),
        source_filename="main.sh",
        program=_build_program(
            json_text=json_text, language=language, layout=layout
        ),
        steps=[
            roundtrip_common.Step(
                args=[bash, "main.sh"],
                failure_label="bash runtime error",
            ),
        ],
        excluded_keys=(),
        expected_json=json_text,
        extra_files={
            _JSON_HELPER_PATH.name: _JSON_HELPER_PATH.read_text(
                encoding="utf-8"
            )
        },
    )


@click.command()
def main() -> None:
    """Round-trip the shared corpus and compatible Bash option pairs."""
    bash = shutil.which(cmd="bash")
    if bash is None or bash == "":
        bash = "bash"
    _check_document(
        bash=bash,
        json_text=roundtrip_common.input_for_capabilities(
            capabilities=Bash.variant_metadata.round_trip_capabilities,
        ),
        language=Bash(),
        layout=CollectionLayout.COMPACT,
    )
    # The Bash backend admits only DECLARE and DECIMAL. Cross the two
    # quoting options with both layouts while those axes stay fixed.
    text = "quotes '\" and a literal dollar $ plus backslash \\ and café\n"
    source = json.dumps(
        obj={
            "text": text,
            "number": -9007199254740991,
            "array": [text, 0, True],
            "map": {"key with spaces": text, "number": 42},
        },
    )
    for quoting in Bash.StringFormats:
        for layout in (CollectionLayout.COMPACT, CollectionLayout.MULTILINE):
            _check_document(
                bash=bash,
                json_text=source,
                language=Bash(string_format=quoting),
                layout=layout,
            )


if __name__ == "__main__":
    main()
