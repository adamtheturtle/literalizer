"""TypeScript JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a TypeScript
``const myData = ...;`` declaration, wrap it in a tiny script that
writes ``JSON.stringify(myData)`` to stdout, run it with ``tsx``, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-typescript-run`` job in
``.github/workflows/lint.yml``, because that job is where the Node and
``tsx`` toolchain are installed.  It follows the same template as
``run_ruby_roundtrip.py``: a single ``.py`` file, no separate serializer
source, because ``JSON.stringify`` is in the JavaScript standard
library.

The shared input's ``biginteger`` field is trimmed before
literalization: JavaScript's ``number`` is an IEEE-754 double whose
integer precision tops out at ``Number.MAX_SAFE_INTEGER`` (``2**53 -
1``), so the literalizer raises
:class:`literalizer.exceptions.UnrepresentableIntegerError` for the
26-digit value rather than emit a numeric literal that loses precision
on parse.
"""

import json
import math
import shutil
from collections.abc import Iterator
from pathlib import Path
from random import Random

import click
from pydantic import JsonValue

from literalizer import CollectionLayout, InputFormat, NewVariable, literalize
from literalizer.languages import TypeScript
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "TypeScript"
_EXCLUDED_KEYS = ("biginteger",)
_CONSUMER = Path(__file__).with_name(name="typescript_roundtrip_consumer.ts")
_SEEDS = (5493, 7319, 0)
_SAMPLES_PER_SEED = 16
_KEYS = ("", "0", "__proto__", "line\nbreak", "quoted'key")


def _build_program(json_text: str) -> str:
    """Return a runnable TypeScript program literalized from
    *json_text*.
    """
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=TypeScript(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        f"{preamble}\n"
        f"{result.code}\n"
        f"process.stdout.write(JSON.stringify({_VAR_NAME}));\n"
    )


def _generated_value(*, generator: Random, depth: int) -> JsonValue:
    """Generate bounded JSON values within TypeScript's exact number range."""
    kinds = 6 if depth > 0 else 4
    match generator.randrange(start=kinds):
        case 0:
            return generator.randint(a=-(2**53 - 1), b=2**53 - 1)
        case 1:
            return generator.choice(seq=(None, True, False))
        case 2:
            return "".join(
                generator.choices(
                    population="ab09 '🐈\"\\$\n\x00日本語",
                    k=generator.randrange(start=17),
                )
            )
        case 3:
            return generator.choice(
                seq=(-0.0, 0.0, generator.randint(a=-32768, b=32767) / 8),
            )
        case 4:
            return [
                _generated_value(generator=generator, depth=depth - 1)
                for _ in range(generator.randrange(start=4))
            ]
        case _:
            return {
                key: _generated_value(generator=generator, depth=depth - 1)
                for key in generator.sample(
                    population=_KEYS,
                    k=generator.randrange(start=4),
                )
            }


def _negative_zero_paths(
    *,
    value: JsonValue,
    path: tuple[str | int, ...],
) -> Iterator[str]:
    """Find the input positions where JSON serialization would lose a sign."""
    if isinstance(value, dict):
        for key, entry in value.items():
            yield from _negative_zero_paths(value=entry, path=(*path, key))
    elif isinstance(value, list):
        for index, entry in enumerate(iterable=value):
            yield from _negative_zero_paths(value=entry, path=(*path, index))
    elif (
        isinstance(value, float)
        and value == 0.0
        and math.copysign(1.0, value) < 0
    ):
        yield json.dumps(obj=path, ensure_ascii=False, separators=(",", ":"))


def _check_generated_documents(*, tsc: str, tsx: str) -> None:
    """Compile and execute fixed seeds under four TypeScript
    configurations.
    """
    samples: dict[str, JsonValue] = {}
    for seed in _SEEDS:
        generator = Random(x=seed)  # noqa: S311 - reproducible fixture data
        samples[str(object=seed)] = [
            {
                "nested": [
                    _generated_value(generator=generator, depth=3),
                    _generated_value(generator=generator, depth=3),
                ],
                "zeros": [-0.0, 0.0],
            }
            for _ in range(_SAMPLES_PER_SEED)
        ]
    samples["propertyNames"] = {"constructor": "own property"}
    source = json.dumps(obj=samples, allow_nan=False)
    expected = json.dumps(
        obj={
            "values": samples,
            "negativeZeroPaths": dict.fromkeys(
                _negative_zero_paths(value=samples, path=()),
                True,
            ),
        },
        allow_nan=False,
    )
    consumer = _CONSUMER.read_text(encoding="utf-8")
    profiles = (
        (TypeScript(), CollectionLayout.COMPACT),
        (
            TypeScript(
                string_format=TypeScript.string_formats.SINGLE,
                variable_type_hints=TypeScript.VariableTypeHints.ALWAYS,
            ),
            CollectionLayout.MULTILINE,
        ),
        (
            TypeScript(dict_format=TypeScript.DictFormats.MAP),
            CollectionLayout.COMPACT,
        ),
        (
            TypeScript(
                dict_format=TypeScript.DictFormats.MAP,
                string_format=TypeScript.string_formats.SINGLE,
                variable_type_hints=TypeScript.VariableTypeHints.SAFE,
            ),
            CollectionLayout.MULTILINE,
        ),
    )
    for language, layout in profiles:
        result = literalize(
            source=source,
            input_format=InputFormat.JSON,
            language=language,
            variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
            collection_layout=layout,
        )
        map_expected = json.dumps(
            obj=language.dict_format is TypeScript.DictFormats.MAP,
        )
        program = "\n".join(
            (
                f'import {{ printRoundtrip }} from "./{_CONSUMER.stem}";',
                *result.preamble,
                *result.body_preamble,
                result.code,
                f"printRoundtrip({_VAR_NAME}, {map_expected});",
            )
        )
        roundtrip_common.execute(
            label=(
                f"{_LABEL} seeds {_SEEDS} ({language.dict_format.name}/"
                f"{layout.name}/{language.variable_type_hints.name})"
            ),
            source_filename="main.ts",
            program=program,
            steps=[
                roundtrip_common.Step(
                    args=[
                        tsc,
                        "--noEmit",
                        "--strict",
                        "--target",
                        "es2022",
                        "main.ts",
                    ],
                    failure_label="tsc type check error",
                ),
                roundtrip_common.Step(
                    args=[tsx, "main.ts"],
                    failure_label="tsx runtime error",
                ),
            ],
            excluded_keys=(),
            expected_json=expected,
            extra_files={_CONSUMER.name: consumer},
        )


@click.command()
def main() -> None:
    """Round-trip the shared document through the TypeScript backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=TypeScript.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    tsx = shutil.which(cmd="tsx")
    if tsx is None or tsx == "":
        tsx = "tsx"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.ts",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[tsx, "main.ts"],
                failure_label="tsx runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files=None,
    )
    tsc = shutil.which(cmd="tsc")
    if tsc is None or tsc == "":
        tsc = "tsc"
    _check_generated_documents(tsc=tsc, tsx=tsx)


if __name__ == "__main__":
    main()
