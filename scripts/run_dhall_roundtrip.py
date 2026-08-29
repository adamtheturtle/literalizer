"""Dhall JSON round-trip check (issue #1867).

Literalize a Dhall-compatible subset of the shared
``roundtrip_input.json`` document to a Dhall ``myData = {...}`` binding
under :attr:`Dhall.heterogeneous_strategy` ``= UNION_TYPE`` (so the
record's heterogeneous scalar values share a single auto-generated
``Value`` union type), wrap it in a Dhall program whose hand-rolled
``valueToJson`` walker converts each ``Value`` variant to JSON text and
concatenates the per-key entries into a JSON object, evaluate it under
``dhall text``, and hand the emitted JSON to
:func:`roundtrip_common.verify`.

This lives here, driven by the ``Dhall roundtrip`` step of the
``lint-fast`` job in ``.github/workflows/lint.yml``, because that job
is where the ``dhall`` binary (the only toolchain dependency) is
installed.  It shares the same input and comparison logic as the other
per-language round-trip helpers.

Dhall is strictly typed, so the shared input's heterogeneous root --
where some keys hold scalars and others hold containers (lists, dicts)
-- cannot be represented uniformly: with
:attr:`Dhall.heterogeneous_strategy` ``= UNION_TYPE`` the literalizer
wraps scalar values into a single ``Value`` union, but the strategy
has no ``wrap_non_scalar`` so a dict mixing scalar and container
values still raises ``MixedDictValuesError``.  The trimmed subset
below keeps every JSON-safe scalar-valued top-level key (twelve of
them: full Integer / Double / Bool / Text coverage), drops every
container-valued one, and omits the multiline string because the small
JSON walker does not escape control characters.  The root therefore
becomes a uniform-family record of ``Value``-wrapped scalars.  The
dropped keys still ride through
``exclude_keys`` so :func:`roundtrip_common.verify` ignores them on
both sides, matching the per-language exclusion pattern used by the
Lua, Elm, Go, etc. scripts for fields their backends cannot represent
losslessly.

The serializer is hand-rolled rather than a Dhall ``Prelude.JSON``
import for two reasons: (1) ``dhall`` imports require either network
access or a pre-populated cache, neither of which the ``lint-fast``
job already has, and (2) the trimmed input only exercises four scalar
``Value`` variants, so the walker stays a handful of lines.  The
``valueToJson`` ``merge`` returns ``Text`` (not ``Prelude.JSON.Type``)
and the per-key JSON fragments are concatenated by the program
itself; ``dhall text`` strips the surrounding double quotes off the
final ``Text`` so the emitted JSON reaches stdout verbatim.
"""

import json
import re
import shutil
from collections.abc import Mapping, Sequence
from types import MappingProxyType

from literalizer.languages import Dhall
from scripts import roundtrip_common

_VAR_NAME = "myData"
_LABEL = "Dhall"

# Top-level container-valued keys.  Dhall's ``UNION_TYPE`` strategy
# wraps scalars only (no ``wrap_non_scalar``), so a root dict that mixes
# scalar and container values raises ``MixedDictValuesError``.  The
# hand-rolled JSON walker also cannot escape control characters in Text,
# so the multiline scalar is omitted.  Trimming these keys keeps the root
# a uniform-family record of JSON-safe ``Value``-wrapped scalars.
_EXCLUDED_KEYS: tuple[str, ...] = (
    "empty_array",
    "int_array",
    "double_array",
    "bool_array",
    "mixed_array",
    "nested_array",
    "empty_object",
    "flat_object",
    "nested_object",
    "string_multiline",
)

# Tail that the ``Dhall`` ``NewVariable`` form appends to the literalize
# output (`let myData = {...} in myData`); the round-trip script replaces
# this with its own ``let``-chain plus a final concatenation expression,
# so the literalized binding flows into our JSON assembly rather than
# evaluating to the bare record.
_VARIABLE_TAIL = f"in {_VAR_NAME}"

# Hand-rolled ``Value`` -> JSON text walker.  Each ``merge`` branch
# returns ``Text`` so the variants unify on the same return type;
# ``Integer/show`` is sign-prefixed (``+42`` / ``-7``) per the Dhall
# standard, so the ``+`` is stripped with ``Text/replace`` before the
# result reaches JSON output.  String escaping covers the two
# JSON-significant ASCII characters the shared input actually carries
# (``"`` and ``\``); the unicode and non-control characters in
# ``string_unicode`` pass through unchanged because JSON allows them
# verbatim in string literals.
_TEXT_HELPERS = """\
let stripPlus : Text -> Text = \\(s : Text) -> Text/replace "+" "" s

let jsonEscape : Text -> Text =
      \\(s : Text) ->
        Text/replace "\\"" "\\\\\\"" (Text/replace "\\\\" "\\\\\\\\" s)

"""

# ``valueToJson`` mentions ``Value``, which the ``UNION_TYPE`` strategy
# declares only for a document whose scalars span more than one family,
# and Dhall's ``merge`` wants exactly the handlers the union declares --
# an extra one is an ``Unused handler`` error.  So the helper is emitted
# only when the union exists, with the handlers its variants name, and
# each entry is converted directly otherwise (issue #4545).
_VALUE_HANDLERS: Mapping[str, str] = MappingProxyType(
    mapping={
        "Int": "Int = \\(i : Integer) -> stripPlus (Integer/show i)",
        "Double": "Double = \\(d : Double) -> Double/show d",
        "Bool": 'Bool = \\(b : Bool) -> if b then "true" else "false"',
        "Str": 'Str = \\(s : Text) -> "\\"" ++ jsonEscape s ++ "\\""',
    }
)


def _value_to_json(*, variants: Sequence[str]) -> str:
    """Return ``valueToJson`` handling exactly *variants*."""
    handlers = "\n          , ".join(
        _VALUE_HANDLERS[variant] for variant in variants
    )
    return (
        "let valueToJson : Value -> Text =\n"
        "      \\(v : Value) ->\n"
        "        merge\n"
        f"          {{ {handlers}\n"
        "          }\n"
        "          v\n"
    )


def _union_variants(*, preamble: str) -> tuple[str, ...]:
    """Return the variant names the emitted ``Value`` union declares."""
    match = re.search(pattern=r"let Value = <([^>]*)>", string=preamble)
    if match is None:
        return ()
    return tuple(
        part.split(sep=":")[0].strip()
        for part in match.group(1).split(sep="|")
    )


def _scalar_to_json(*, expression: str, value: object) -> str:
    """Return the Dhall text conversion for one bare scalar.

    Parenthesized because the result is spliced into a ``++`` chain,
    where a bare ``if`` is a parse error.
    """
    match value:
        case bool():
            return f'(if {expression} then "true" else "false")'
        case int():
            return f"(stripPlus (Integer/show {expression}))"
        case float():
            return f"(Double/show {expression})"
        case _:
            return f'("\\"" ++ jsonEscape {expression} ++ "\\"")'


def _entry_line(
    key: str,
    *,
    is_first: bool,
    value: object,
    has_union: bool,
) -> str:
    r"""Return one ``"<sep>\"key\":" ++ <conversion>`` fragment.

    Trimmed-input keys are pure-ASCII identifiers, so the Dhall string
    literal for the key needs no escaping beyond the surrounding
    backslash-quoted delimiters that JSON requires around object keys.
    The separator (``""`` for the first entry, ``","`` for the rest) is
    inlined into the leading literal because Dhall's ``Text`` builtins
    have no ``concatSep`` -- only the Prelude exposes ``Text.concatSep``
    and the script intentionally avoids Prelude imports so the
    ``lint-fast`` job does not need network or a populated import cache.
    """
    sep = "" if is_first else ","
    expression = f"{_VAR_NAME}.{key}"
    converted = (
        f"valueToJson {expression}"
        if has_union
        else _scalar_to_json(expression=expression, value=value)
    )
    return f'"{sep}\\"{key}\\":" ++ {converted}'


def _build_program(json_text: str) -> str:
    """Return a runnable Dhall program literalized from *json_text*."""
    trimmed_json = roundtrip_common.trim_keys(
        json_text=json_text,
        excluded_keys=_EXCLUDED_KEYS,
    )
    parsed = json.loads(s=trimmed_json)
    # ``UNION_TYPE`` is looked up dynamically because
    # :attr:`Dhall.HeterogeneousStrategies` is declared on the language
    # metaclass and ``basedpyright`` cannot statically resolve the
    # enum's members.  Mirrors the same iteration pattern
    # ``tests/integration/variant_cases.py`` uses for the union-type
    # variants.
    default_spec = Dhall()
    union_type = next(
        strategy
        for strategy in default_spec.heterogeneous_strategies
        if strategy.name == "UNION_TYPE"
    )
    result = roundtrip_common.literalize_new_variable(
        language=Dhall(heterogeneous_strategy=union_type),
        json_text=trimmed_json,
        var_name=_VAR_NAME,
        pre_indent_level=0,
    )
    preamble_text = "\n".join(result.preamble)
    binding = result.code
    if not binding.endswith(_VARIABLE_TAIL):
        msg = (
            "Expected literalize output to end with "
            f"{_VARIABLE_TAIL!r}; got {binding!r}"
        )
        raise AssertionError(msg)
    binding_without_tail = binding[: -len(_VARIABLE_TAIL)]
    variants = _union_variants(preamble=preamble_text)
    has_union = bool(variants)
    entry_lines = "\n      ++ ".join(
        _entry_line(
            key=key,
            is_first=index == 0,
            value=value,
            has_union=has_union,
        )
        for index, (key, value) in enumerate(iterable=parsed.items())
    )
    helpers = _TEXT_HELPERS + (
        _value_to_json(variants=variants) if has_union else ""
    )
    return (
        f"{preamble_text}\n"
        f"{binding_without_tail}"
        f"{helpers}"
        "in\n"
        '      "{"\n'
        f"      ++ {entry_lines}\n"
        '      ++ "}"\n'
    )


def main() -> None:
    """Round-trip the trimmed shared document through the Dhall
    backend.
    """
    json_text = roundtrip_common.input_for_capabilities(
        capabilities=Dhall.variant_metadata.round_trip_capabilities,
    )
    program = _build_program(json_text=json_text)
    dhall = shutil.which(cmd="dhall") or "dhall"
    roundtrip_common.execute(
        label=_LABEL,
        source_filename="main.dhall",
        program=program,
        steps=[
            roundtrip_common.Step(
                args=[dhall, "text", "--file", "main.dhall"],
                failure_label="dhall text error",
            ),
        ],
        excluded_keys=_EXCLUDED_KEYS,
        expected_json=json_text,
        extra_files=None,
    )


if __name__ == "__main__":
    main()
