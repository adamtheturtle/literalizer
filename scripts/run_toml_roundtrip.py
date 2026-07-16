"""TOML JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a TOML
``myData = { ... }`` assignment, parse the resulting TOML document with
``tomli``, then re-serialize the inner value as JSON and hand it to
:func:`roundtrip_common.verify`.

Unlike the executable-language round-trips, there is no language
runtime to invoke: the analogous "back to JSON" step is a TOML parser
re-emitting the parsed value.  ``tomli`` is used (rather than the
stdlib ``tomllib``) because the literalized output uses TOML 1.1
multiline inline tables, which ``tomli`` >= 2.4 understands but
stdlib ``tomllib`` does not.

This lives here, driven by the ``Toml roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, alongside the
existing ``Lint Toml`` syntax check that uses the same ``tomli``
dependency.  It shares the same input and comparison logic as the
other per-language round-trip helpers.
"""

import json
import sys

import tomli

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Toml
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "TOML"


def _build_document(json_text: str) -> str:
    """Return a TOML document literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Toml(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=NewVariable(name=_VAR_NAME, modifiers=frozenset()),
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\n" if preamble else f"{result.code}\n"


def main() -> None:
    """Round-trip the shared document through the TOML backend."""
    document = _build_document(json_text=roundtrip_common.read_input())
    parsed: dict[str, object] = tomli.loads(document)
    produced_json = json.dumps(obj=parsed[_VAR_NAME])
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=produced_json,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
