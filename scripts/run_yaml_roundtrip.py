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

import click
import yaml

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Yaml
from scripts import roundtrip_common

_LABEL = "YAML"


def _build_document(json_text: str, *, variable_name: str | None) -> str:
    """Return a YAML document literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Yaml(),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=(
            None
            if variable_name is None
            else NewVariable(name=variable_name, modifiers=frozenset())
        ),
        wrap_in_file=variable_name is not None,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    if preamble != "":
        return f"{preamble}\n{result.code}\n"
    return f"{result.code}\n"


@click.command()
def main() -> None:
    """Round-trip the shared document through the YAML backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Yaml.variant_metadata.round_trip_capabilities,
    )
    for variable_name in (None, "null"):
        document = _build_document(
            json_text=json_text, variable_name=variable_name
        )
        parsed = roundtrip_common.json_object(
            value=yaml.safe_load(stream=document),
        )
        if variable_name is not None:
            parsed = roundtrip_common.json_object(value=parsed[variable_name])
        roundtrip_common.verify(
            label=_LABEL if variable_name is None else _LABEL + " named root",
            produced_json=json.dumps(obj=parsed),
            exclude_keys=(),
            expected_json=json_text,
        )
    _ = sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
