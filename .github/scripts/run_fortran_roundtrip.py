"""Fortran JSON round-trip check (issue #2652).

Literalize the shared ``roundtrip_input.json`` document to a Fortran
``my_data = fmap([...])`` binding via the default ``Fortran()`` config,
splice it into a tiny ``program main`` that calls ``to_json(my_data)``
and writes the result to stdout, gfortran-compile that program against
the real ``fval_m.f90`` module sitting next to this script (the lint-
only stubs the literalizer emits as its ``static_preamble``/
``static_body_preamble`` are replaced wholesale with a real backing
module — see ``fval_m.f90``), run it, and hand the produced JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Fortran roundtrip`` step of the lint
job that already installs gfortran in ``.github/workflows/lint.yml``,
because that job is where the toolchain is available; ``uv run``
(project mode) is required so ``import literalizer`` resolves. It is
not a pytest test under ``tests/``.

The shared input's ``biginteger`` field is excluded from the comparison
because the Fortran backend's default integer kind is ``int64``, and
the 26-digit ``biginteger`` value raises
:class:`literalizer.exceptions.UnrepresentableIntegerError` long before
literalization can produce a Fortran source. Same exclusion shape as
the Rust / C++ / Go / Swift / TypeScript / Zig / D scripts.
"""

import shutil
from pathlib import Path

import roundtrip_common

from literalizer.languages import Fortran

_SCRIPT_DIR = Path(__file__).resolve().parent
_FVAL_M_SRC = _SCRIPT_DIR / "fval_m.f90"
_VAR_NAME = "my_data"
_LABEL = "Fortran"
_EXCLUDED_KEYS = ("biginteger",)


def _build_main(json_text: str) -> str:
    """Return a runnable ``program main`` literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    # ``pre_indent_level=1`` aligns the binding inside the four-space
    # body indent that the program template below uses.
    result = roundtrip_common.literalize_new_variable(
        language=Fortran(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=1,
    )
    # ``result.code`` already opens with ``type(fval_t) :: my_data``
    # followed by the assignment, in the order Fortran's specification-
    # before-executable rule demands; don't redeclare ``my_data`` here.
    return (
        "program main\n"
        "    use fval_m\n"
        "    implicit none\n"
        f"{result.code}\n"
        f"    write(*, '(a)', advance='no') to_json({_VAR_NAME})\n"
        "end program main\n"
    )


def main() -> None:
    """Round-trip the shared document through the Fortran backend."""
    program = _build_main(json_text=roundtrip_common.read_input())
    gfortran = shutil.which(cmd="gfortran") or "gfortran"
    fval_m_text = _FVAL_M_SRC.read_text(encoding="utf-8")
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.f90",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    gfortran,
                    "-std=f2008",
                    "-ffree-line-length-none",
                    _FVAL_M_SRC.name,
                    "main.f90",
                    "-o",
                    "main",
                ],
                failure_label="gfortran error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        extra_files={_FVAL_M_SRC.name: fval_m_text},
    )


if __name__ == "__main__":
    main()
