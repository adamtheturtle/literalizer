"""PowerShell JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a PowerShell
``$myData = ...`` assignment, wrap it in a tiny script that prints
``ConvertTo-Json $myData``, run it with ``pwsh``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``PowerShell roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job is
where the PowerShell toolchain is installed.  It shares the same input
and comparison logic as the other per-language round-trip helpers.

``ConvertTo-Json`` is the built-in serializer, used with ``-Compress``
for minimal output and ``-Depth 100`` so the nested document is not
truncated at the default depth of 2.

One field is excluded from the comparison because PowerShell's number
parsing cannot represent it losslessly:

* ``biginteger`` -- the 26-digit literal overflows PowerShell's signed
  64-bit ``[long]`` and is parsed as ``[double]``, so ``ConvertTo-Json``
  re-emits it as ``99999999999999999999999999.0``.  The field is trimmed
  from the input *before* literalization so the generated program does
  not carry a value the round-trip would reject.
"""

import shutil

from literalizer.languages import PowerShell
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "PowerShell"
_EXCLUDED_KEYS = ("biginteger",)


def _build_program(json_text: str) -> str:
    """Return a runnable PowerShell program literalized from
    *json_text*.
    """
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=PowerShell(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    emit = (
        "[Console]::Out.Write("
        f"(ConvertTo-Json -InputObject ${_VAR_NAME} -Depth 100 -Compress))"
    )
    return f"{preamble}\n{result.code}\n{emit}\n"


def main() -> None:
    """Round-trip the shared document through the PowerShell backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    pwsh = shutil.which(cmd="pwsh") or "pwsh"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.ps1",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    pwsh,
                    "-NoProfile",
                    "-NonInteractive",
                    "-File",
                    "main.ps1",
                ],
                failure_label="pwsh runtime error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
