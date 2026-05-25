"""Clojure JSON round-trip check (issue #2642).

Literalize the shared ``roundtrip_input.json`` document to a Clojure
``(def my-data ...)`` form, wrap it in a tiny script that prints
``cheshire.core/generate-string`` of that value, run it under
``bb`` (Babashka), and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Clojure roundtrip`` step of the
``lint-jvm-mini`` job in ``.github/workflows/lint.yml``, because that is
the job where Babashka is installed (pinned by the
``Install clj-kondo and Babashka`` step).  It shares the same input and
comparison logic as the other per-language round-trip helpers.

``cheshire.core`` ships built in with Babashka and is the de-facto
Clojure JSON library, so no extra rock/dependency install is needed and
no hand-rolled serializer is involved (per the issue brief, which
prefers a built-in/library serializer).
"""

import shutil

import roundtrip_common

from literalizer.languages import Clojure

_VAR_NAME = "my-data"
_LABEL = "Clojure"


def _build_program(json_text: str) -> str:
    """Return a runnable Clojure program literalized from *json_text*."""
    result = roundtrip_common.literalize_new_variable(
        language=Clojure(),
        json_text=json_text,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return (
        "(require '[cheshire.core :as json])\n"
        f"{preamble}\n"
        f"{result.code}\n"
        f"(print (json/generate-string {_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Clojure backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    bb = shutil.which(cmd="bb") or "bb"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.clj",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[bb, "main.clj"],
                failure_label="bb runtime error",
            ),
        ],
        excluded_keys=(),
    )


if __name__ == "__main__":
    main()
