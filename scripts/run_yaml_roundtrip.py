"""YAML JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a YAML
flow-style value, parse the resulting YAML with ``PyYAML``, then
re-serialize the parsed value as JSON and hand it to
:func:`roundtrip_common.verify`.

Like the TOML round-trip, there is no language runtime to invoke:
the analogous "back to JSON" step is a YAML parser re-emitting the
parsed value.  The :class:`literalizer.languages.Yaml` backend emits
flow mappings / sequences, which ``yaml.safe_load`` parses to native
Python ``dict``/``list``/``int``/``float``/``bool``/``str`` values.

This lives here, driven by the ``Yaml roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, alongside the
existing ``Lint Yaml`` syntax check.  It shares the same input and
comparison logic as the other per-language round-trip helpers.
"""

import json
import sys

import yaml

from literalizer import InputFormat, literalize
from literalizer.languages import Yaml
from scripts import roundtrip_common

_LABEL = "YAML"


def _build_document(json_text: str) -> str:
    """Return a YAML document literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Yaml(),
        pre_indent_level=0,
        include_delimiters=True,
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\n" if preamble else f"{result.code}\n"


def main() -> None:
    """Round-trip the shared document through the YAML backend."""
    document = _build_document(json_text=roundtrip_common.read_input())
    parsed: dict[str, object] = yaml.safe_load(  # type: ignore[no-untyped-call]
        stream=document,
    )
    produced_json = json.dumps(obj=parsed)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=produced_json,
        exclude_keys=(),
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
