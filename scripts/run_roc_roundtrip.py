"""Roc JSON round-trip check (issue #2676).

Literalize the shared ``roundtrip_input.json`` document to a Roc
``my_data : Val`` binding, splice it into a basic-cli ``app`` that walks
the tag-union with a hand-rolled ``val_to_json`` encoder and prints the
result via ``Stdout.line!``, run it under ``roc``, and hand the emitted
JSON to :func:`roundtrip_common.verify`.

This lives here, driven by the ``Roc roundtrip`` step of the
``lint-roc`` job in ``.github/workflows/lint.yml``, because that job is
where the Roc toolchain is installed (the pinned ``roc`` nightly).  It
shares the same input and comparison logic as the other per-language
round-trip helpers.

Roc has no standard-library JSON serializer that derives an ``Encoding``
implementation for an arbitrary ad-hoc tag union, so per the issue
brief's preference order this script falls back to hand-rolling a tiny
encoder that pattern-matches on the literalized ``Val`` constructors.

One top-level key is excluded from the comparison:

* ``float_large_exponent`` -- ``format_float_repr`` emits the literal
  with ``e+308``, and Roc's float lexer rejects the explicit ``+`` sign
  in the exponent ("Floating point literals can only contain the
  digits 0-9, or use scientific notation 10e4, or have a float
  suffix").  The key is trimmed from the input before literalization
  (so the generated Roc file does not contain it) and from both sides
  of the parsed comparison.
"""

import shutil

from literalizer.languages import Roc
from scripts import roundtrip_common

# basic-cli is the canonical Roc platform; pinned to the 0.20.0 release
# whose tarball hash is verified by ``roc`` itself when it fetches the
# platform.  ``roc run`` will download and cache the platform on first
# invocation in CI.  Bump in lockstep with the ``ROC_NIGHTLY_BUILD``
# pin in ``.github/workflows/lint.yml`` when upgrading the nightly.
_BASIC_CLI_URL = (
    "https://github.com/roc-lang/basic-cli/releases/download/0.20.0/"
    "X73hGh05nNTkDHU06FHC0YfFaQB1pimX7gncRcao5mU.tar.br"
)

_VAR_NAME = "my_data"
_LABEL = "Roc"
_EXCLUDED_KEYS = ("float_large_exponent",)

# Hand-rolled JSON encoder over the literalized ``Val`` tag union.
# ``escape_str`` walks UTF-8 bytes: bytes >= 0x80 are part of multi-byte
# code points and pass through untouched (JSON allows raw UTF-8); only
# the JSON-mandatory escapes for ``"``, ``\`` and the C0 whitespace
# controls are rewritten.  Any other C0 controls would need the
# ``\u00XX`` form -- the shared input does not contain them so the
# encoder does not bother.
_WALKER = """\
val_to_json : Val -> Str
val_to_json = |v|
    when v is
        RBool(b) -> if b then "true" else "false"
        RInt(n) -> Num.to_str(n)
        RFloat(f) -> Num.to_str(f)
        RStr(s) -> escape_str(s)
        RList(items) ->
            parts = List.map(items, |x| val_to_json(x))
            joined = Str.join_with(parts, ",")
            "[${joined}]"
        RDict(entries) ->
            parts = List.map(entries, |e| entry_to_json(e))
            joined = Str.join_with(parts, ",")
            "{${joined}}"

entry_to_json : (Str, Val) -> Str
entry_to_json = |entry|
    (k, v) = entry
    key_json = escape_str(k)
    val_json = val_to_json(v)
    "${key_json}:${val_json}"

escape_str : Str -> Str
escape_str = |s|
    bytes = Str.to_utf8(s)
    escaped = List.walk(bytes, [], |acc, b| List.concat(acc, escape_byte(b)))
    inner = Result.with_default(Str.from_utf8(escaped), "")
    "\\"${inner}\\""

escape_byte : U8 -> List U8
escape_byte = |b|
    when b is
        0x22 -> [0x5c, 0x22]
        0x5c -> [0x5c, 0x5c]
        0x08 -> [0x5c, 0x62]
        0x0c -> [0x5c, 0x66]
        0x0a -> [0x5c, 0x6e]
        0x0d -> [0x5c, 0x72]
        0x09 -> [0x5c, 0x74]
        _ -> [b]
"""


def _build_program(json_text: str) -> str:
    """Return a runnable Roc app literalized from *json_text*."""
    trimmed = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Roc(),
        json_text=trimmed,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    return (
        f'app [main!] {{ pf: platform "{_BASIC_CLI_URL}" }}\n'
        "\n"
        "import pf.Stdout\n"
        "import pf.Arg exposing [Arg]\n"
        "\n"
        f"{result.code}\n"
        "\n"
        f"{_WALKER}\n"
        "main! : List Arg => Result {} _\n"
        "main! = |_args|\n"
        f"    Stdout.line!(val_to_json({_VAR_NAME}))\n"
    )


def main() -> None:
    """Round-trip the shared document through the Roc backend."""
    program = _build_program(json_text=roundtrip_common.read_input())
    roc = shutil.which(cmd="roc") or "roc"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.roc",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[roc, "run", "--linker=legacy", "main.roc"],
                failure_label="roc run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
    )


if __name__ == "__main__":
    main()
