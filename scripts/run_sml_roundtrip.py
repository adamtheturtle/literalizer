r"""Standard ML JSON round-trip check (issue #2678).

Literalize the shared ``roundtrip_input.json`` document to a Standard
ML ``val myData : val_t = ...`` binding (with the generated tagged
``val_t`` datatype), append a small ``toJson`` walker that maps each
constructor to a JSON fragment and prints the result, compile with
``mlton``, run the binary, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by a step of the ``lint-sml`` job in
``.github/workflows/lint.yml``, because that job is where the MLton
toolchain is provisioned.  It shares the same input and comparison
logic as the other per-language round-trip helpers.

SML's standard basis has no JSON encoder.  MLton ships ``smlnj-lib``
which includes a ``JSONPrinter`` structure, but that printer emits
SML-flavored numbers (``~`` for negation) without translating to JSON's
``-`` and calls :func:`Real.fmt` with default precision (12 significant
digits), which loses the bits of ``1.7976931348623157``.  Rather than
post-process around those mismatches, this script walks the generated
``val_t`` constructors directly and emits JSON using a tiny
``toJson`` function.  The walker covers exactly the six variants the
shared input exercises (``SBool``, ``SInt``, ``SReal``, ``SStr``,
``SList``, ``SMap``); a future expansion of ``roundtrip_input.json``
adding a new scalar kind would fail compilation here until the match
is extended.

The shared input's ``biginteger`` field is excluded from the
comparison: its 26-digit value exceeds SML's
``BareIntegerWidthStrategies.BARE`` limit, so the literalizer raises
``UnrepresentableIntegerError`` before emitting any code.
``float_large_exponent`` is also excluded: ``format_float_repr``
round-trips Python's ``repr(1.7976931348623157e308)`` verbatim as
``1.7976931348623157e+308``, but the SML '97 numeric-literal grammar
requires an uppercase ``E`` and ``~`` (not ``+``) before a positive
exponent, so MLton rejects the literal.  Trimming the field
keeps this round-trip focused on what the SML backend can actually
emit today, separate from those orthogonal literalizer limitations.

The literalized input contains the ``unicode é 中`` string, which
embeds UTF-8 bytes in a source-level string literal.  MLton rejects
those bytes under its default annotation set, so the compile step
passes ``-default-ann 'allowExtendedTextConsts true'`` to opt in.  The
``toJson`` emitter walks the string as bytes (``Char.ord c >= 32`` is
passed through verbatim), so the UTF-8 sequence reconstitutes in the
emitted JSON without ``\\uXXXX`` escaping.
"""

import re
import shutil
from collections.abc import Mapping
from types import MappingProxyType

from literalizer.languages import Sml
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "SML"
_EXCLUDED_KEYS = ("biginteger", "float_large_exponent")

_TO_JSON = r"""
fun jsonString s =
  let
    fun escape c =
      case c of
        #"\"" => "\\\""
      | #"\\" => "\\\\"
      | #"\n" => "\\n"
      | #"\r" => "\\r"
      | #"\t" => "\\t"
      | _ =>
          if Char.ord c < 32
          then "\\u00" ^ StringCvt.padLeft #"0" 2
                 (Int.fmt StringCvt.HEX (Char.ord c))
          else String.str c
  in
    "\"" ^ String.concat (List.map escape (String.explode s)) ^ "\""
  end

fun stripTilde s =
  if String.isPrefix "~" s
  then "-" ^ String.extract (s, 1, NONE)
  else s

fun jsonInt i = stripTilde (LargeInt.toString i)

fun jsonReal r =
  String.implode
    (List.map (fn #"~" => #"-" | c => c)
       (String.explode (Real.fmt (StringCvt.GEN (SOME 17)) r)))

"""

_PRINT = "val () = print (toJson myData)\n"

# One ``toJson`` clause per constructor.  ``Sml`` declares only the
# constructors the document actually uses, so a clause for an absent one
# would not compile; the clauses are selected from the emitted
# ``datatype`` rather than written out in full (issue #4545).
_TO_JSON_CLAUSES: Mapping[str, str] = MappingProxyType(
    mapping={
        "SBool": '    SBool true => "true"\n  | SBool false => "false"',
        "SInt": "    SInt i => jsonInt i",
        "SReal": "    SReal r => jsonReal r",
        "SStr": "    SStr s => jsonString s",
        "SList": (
            "    SList xs => "
            '"[" ^ String.concatWith "," (List.map toJson xs) ^ "]"'
        ),
        "SMap": (
            "    SMap kvs =>\n"
            '      "{" ^ String.concatWith ","\n'
            "              (List.map (fn (k, v) => "
            'jsonString k ^ ":" ^ toJson v) kvs)\n'
            '        ^ "}"'
        ),
    }
)


def _to_json(*, declaration: str) -> str:
    """Return a ``toJson`` matching only the declared constructors."""
    clauses = [
        clause
        for name, clause in _TO_JSON_CLAUSES.items()
        if re.search(pattern=rf"\b{name}\b", string=declaration) is not None
    ]
    body = "\n  | ".join(clause.removeprefix("    ") for clause in clauses)
    return f"\nfun toJson v =\n  case v of\n    {body}\n"


def _build_program(json_text: str) -> str:
    """Return a runnable SML program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    result = roundtrip_common.literalize_new_variable(
        language=Sml(),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    # ``Sml.literalize`` already inlines ``result.body_preamble`` (the
    # ``datatype val_t`` declaration) at the top of ``result.code``, so
    # we only join ``preamble`` (currently empty) with ``code`` here.
    # Prepending ``body_preamble`` separately would duplicate the
    # ``val_t`` type and break compilation.
    preamble = "\n".join(result.preamble)
    to_json = _to_json(declaration=result.code)
    return f"{preamble}\n{result.code}\n{_TO_JSON}{to_json}\n{_PRINT}"


def main() -> None:
    """Round-trip the shared document through the SML backend."""
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Sml.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    mlton = shutil.which(cmd="mlton") or "mlton"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.sml",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[
                    mlton,
                    "-default-ann",
                    "allowExtendedTextConsts true",
                    "-output",
                    "main",
                    "main.sml",
                ],
                failure_label="mlton error",
            ),
            roundtrip_common.Step(
                args=["./main"],
                failure_label="run error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files=None,
    )


if __name__ == "__main__":
    main()
