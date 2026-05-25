"""Julia JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Julia
``my_data = ...`` assignment, wrap it in a tiny script that prints
``JSON.json(my_data)``, run it with Julia, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Julia roundtrip`` step of the
``lint-julia`` job in ``.github/workflows/lint.yml``, because that job
is where the Julia toolchain is installed and a project with the
``JSON`` package is provisioned (the ``JULIA_PROJECT`` env var is set
there so ``using JSON`` resolves).  It shares the same input and
comparison logic as the other per-language round-trip helpers.

The shared input's ``biginteger`` field is excluded from the comparison:
its 26-digit value overflows Julia's ``Int64`` so the literal is parsed
as ``Int128`` / ``BigInt`` and ``JSON.json`` for big integers cannot be
relied on across versions to emit a JSON-number representation matching
the input.  Same shape as the Go, TypeScript, Zig, Rust, and Elm
exclusions.
"""

import shutil

import roundtrip_common

from literalizer.languages import Julia

_VAR_NAME = "my_data"
_LABEL = "Julia"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable Julia program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Julia(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "using JSON\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"print(JSON.json({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Julia backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    julia = shutil.which(cmd="julia") or "julia"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.jl",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[julia, "--startup-file=no", "main.jl"],
                failure_label="julia runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
