"""Groovy JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a Groovy
``def myData = ...`` declaration, wrap it in a tiny script whose final
statement prints ``groovy.json.JsonOutput.toJson(myData)``, run it, and
hand the emitted JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Groovy roundtrip`` step of the
``lint-jvm-mini`` job in ``.github/workflows/lint.yml``, because that
job is where the pinned Apache Groovy distribution is installed; it is
deliberately not a pytest test under ``tests/``.  No separate
serializer is needed because ``groovy.json.JsonOutput`` (Groovy
stdlib) already serializes ``Map``/``List``/``BigInteger``/``Number``
/``String``/``Boolean`` directly.
"""

import shutil

import roundtrip_common

from literalizer.languages import Groovy

_VAR_NAME = "myData"
_LABEL = "Groovy"


def _build_script(json_text: str) -> str:
    """Return a runnable Groovy script literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Groovy(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    imports = "\n".join(result.preamble)
    body_preamble = "\n".join(result.body_preamble)
    return (
        "import groovy.json.JsonOutput\n"
        f"{imports}\n"
        f"{body_preamble}\n"
        f"{result.code}\n"
        f"print JsonOutput.toJson({_VAR_NAME})\n"
    )


def main() -> None:
    """Round-trip the shared document through the Groovy backend."""
    program = _build_script(json_text=roundtrip_common.read_input())
    groovy = shutil.which(cmd="groovy") or "groovy"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="Main.groovy",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[groovy, "Main.groovy"],
                failure_label="groovy error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
