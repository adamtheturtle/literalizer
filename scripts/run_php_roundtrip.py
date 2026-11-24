"""PHP JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a PHP
``$myData = ...`` assignment, wrap it in a tiny script that prints
``json_encode($myData)``, run it with PHP, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Php roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the PHP toolchain is installed.  It shares the same input and
comparison logic as the other per-language round-trip helpers.

Two fields are excluded from the comparison because PHP's JSON encoder
cannot represent them losslessly:

* ``biginteger`` -- the 26-digit literal overflows PHP's signed 64-bit
  integer and is widened to ``float``, so ``json_encode`` re-emits it
  as ``1.0e+26``.
* ``empty_object`` -- PHP has a single sequence/map array type, so an
  empty associative array is indistinguishable from an empty list; the
  literalizer raises
  :class:`literalizer.exceptions.UnrepresentableEmptyDictError` on this
  language and the field is trimmed from the input *before*
  literalization.
"""

import json
import shutil
from random import Random

import click
from pydantic import JsonValue

from literalizer import InputFormat, literalize_call
from literalizer.languages import Php
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "PHP"
_EXCLUDED_KEYS = ("biginteger", "empty_object")
_GENERATED_SEEDS = (7, 19, 83)
_SAMPLES_PER_SEED = 16


def _build_program(json_text: str) -> str:
    """Return a runnable PHP program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Php(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\necho json_encode(${_VAR_NAME});\n"


def _generated_value(*, generator: Random, depth: int) -> JsonValue:
    """Generate a bounded value PHP can represent without coercion."""
    kind_count = 6
    if depth == 0:
        kind_count = 4
    match generator.randrange(start=kind_count):
        case 0:
            return generator.randint(a=-32768, b=32767)
        case 1:
            return generator.choice(seq=(None, True, False))
        case 2:
            return "".join(
                generator.choices(
                    population="ab09 '\"\\$\n日本語",
                    k=generator.randrange(start=17),
                )
            )
        case 3:
            return (generator.randint(a=-32768, b=32767) * 2 + 1) / 8
        case 4:
            return [
                _generated_value(generator=generator, depth=depth - 1)
                for _ in range(generator.randrange(start=4))
            ]
        case _:
            # PHP arrays cannot distinguish an empty map or retain
            # purely numeric string keys.
            return {
                f"key_{index}": _generated_value(
                    generator=generator, depth=depth - 1
                )
                for index in range(generator.randint(a=1, b=3))
            }


def _check_document(
    *, label: str, php: str, json_text: str, excluded_keys: tuple[str, ...]
) -> None:
    """Render and execute one document in the shared round-trip runner."""
    trimmed = roundtrip_common.trim_keys(
        json_text=json_text, excluded_keys=excluded_keys
    )
    roundtrip_common.execute(
        label=label,
        source_filename="main.php",
        program=_build_program(json_text=trimmed),
        steps=[
            roundtrip_common.Step(
                args=[php, "main.php"],
                failure_label="php runtime error",
            ),
        ],
        excluded_keys=excluded_keys,
        expected_json=json_text,
        extra_files=None,
    )


def _check_generated_calls(*, php: str) -> None:
    """Round-trip generated values through ordered, two-argument calls."""
    for seed in _GENERATED_SEEDS:
        generator = Random(x=seed)  # noqa: S311 - reproducible fixture data
        rows: list[list[JsonValue]] = [
            [f"{seed}:{index}", _generated_value(generator=generator, depth=3)]
            for index in range(_SAMPLES_PER_SEED)
        ]
        result = literalize_call(
            source=json.dumps(obj=rows),
            input_format=InputFormat.JSON,
            language=Php(),
            target_function="collect",
            parameter_names=("tag", "payload"),
            per_element=True,
        )
        program = "\n".join(
            (
                *result.preamble,
                *result.body_preamble,
                "$rows = [];",
                "function collect(string $tag, mixed $payload): void {",
                '    $GLOBALS["rows"][] = [$tag, $payload];',
                "}",
                result.code,
                'echo json_encode(["rows" => $rows], JSON_THROW_ON_ERROR);',
            )
        )
        roundtrip_common.execute(
            label=f"{_LABEL} generated call rows (seed {seed})",
            source_filename="main.php",
            program=program,
            steps=[
                roundtrip_common.Step(
                    args=[php, "main.php"], failure_label="php runtime error"
                ),
            ],
            excluded_keys=(),
            expected_json=json.dumps(obj={"rows": rows}),
            extra_files=None,
        )


@click.command()
def main() -> None:
    """Round-trip the shared corpus and seeded nested documents."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Php.variant_metadata.round_trip_capabilities,
    )
    php = shutil.which(cmd="php")
    if php is None or php == "":
        php = "php"
    _check_document(
        label=_LABEL,
        php=php,
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    for seed in _GENERATED_SEEDS:
        generator = Random(x=seed)  # noqa: S311 - reproducible fixture data
        samples = [
            _generated_value(generator=generator, depth=3)
            for _ in range(_SAMPLES_PER_SEED)
        ]
        _check_document(
            label=f"{_LABEL} generated nested values (seed {seed})",
            php=php,
            json_text=json.dumps(obj={"samples": samples}),
            excluded_keys=(),
        )
    _check_generated_calls(php=php)


if __name__ == "__main__":
    main()
