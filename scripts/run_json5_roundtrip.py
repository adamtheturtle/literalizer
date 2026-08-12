"""JSON5 JSON round-trip check (issue #1867).

Literalize the shared ``roundtrip_input.json`` document to a JSON5
value, parse the resulting JSON5 text with ``json5``, then re-serialize
the parsed value as JSON and hand it to :func:`roundtrip_common.verify`.

Like the TOML round-trip, there is no language runtime to invoke: the
analogous "back to JSON" step is a JSON5 parser re-emitting the parsed
value.  ``json5`` is already a core ``literalizer`` dependency, so the
JSON5 lint job's ``uv run`` (project mode) resolves it without extra
``--with`` layering.  Unlike most other backends, ``Json5`` does not
support a ``variable_form``: the literalized output is a bare JSON5
value, so the parsed result is fed directly to ``verify``.
"""

import json
import sys

import json5

from literalizer import InputFormat, literalize
from literalizer.languages import Json5
from scripts import roundtrip_common

_LABEL = "JSON5"


def _build_document(json_text: str) -> str:
    """Return a JSON5 document literalized from *json_text*."""
    result = literalize(
        source=json_text,
        input_format=InputFormat.JSON,
        language=Json5(),
        pre_indent_level=0,
        include_delimiters=True,
        wrap_in_file=False,
    )
    preamble = "\n".join((*result.preamble, *result.body_preamble))
    return f"{preamble}\n{result.code}\n" if preamble else f"{result.code}\n"


def main() -> None:
    """Round-trip the shared document through the JSON5 backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Json5.variant_metadata.round_trip_capabilities,
    )
    document = _build_document(json_text=json_text)
    parsed: dict[str, object] = json5.loads(
        s=document,
        allow_duplicate_keys=False,
    )
    produced_json = json.dumps(obj=parsed)
    roundtrip_common.verify(
        label=_LABEL,
        produced_json=produced_json,
        exclude_keys=(),
        expected_json=json_text,
    )
    sys.stdout.write(f"{_LABEL} round-trip OK\n")


if __name__ == "__main__":
    main()
