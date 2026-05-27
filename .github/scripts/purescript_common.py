"""Shared helpers for the PureScript lint scripts."""

import textwrap
from pathlib import Path

PRELUDE_PURS = textwrap.dedent(
    text="""\
    module Prelude where
    foreign import data Unit :: Type
    foreign import unit :: Unit
    foreign import negate :: forall a. a -> a
    foreign import div :: forall a. a -> a -> a
    infixl 7 div as /
    """,
)

PRELUDE_JS = textwrap.dedent(
    text="""\
    export const unit = {};
    export const negate = x => -x;
    export const div = x => y => x / y;
    """,
)

# Minimal shims for ``PureScript(json_type=ARGONAUT_JSON)`` fixtures.
# Real ``argonaut-core`` / ``argonaut-parser`` / ``either`` packages
# would require a spago or psc-package setup; the lint job's existing
# hand-rolled ``PRELUDE_*`` shims already establish the
# foreign-import-against-tiny-JS-runtime pattern, so the json_type
# fixtures get the same treatment here.  The JS implementations defer
# to the runtime's ``JSON.parse``, so the round-tripping invariant
# pinned by the goldens still gets a real compile + run check.
EITHER_PURS = textwrap.dedent(
    text="""\
    module Data.Either where
    foreign import data Either :: Type -> Type -> Type
    foreign import fromRight :: forall a b. b -> Either a b -> b
    """,
)

EITHER_JS = textwrap.dedent(
    text="""\
    export const fromRight = d => e => e.tag === "Right" ? e.value : d;
    """,
)

ARGONAUT_CORE_PURS = textwrap.dedent(
    text="""\
    module Data.Argonaut.Core where
    foreign import data Json :: Type
    foreign import jsonNull :: Json
    """,
)

ARGONAUT_CORE_JS = textwrap.dedent(
    text="""\
    export const jsonNull = null;
    """,
)

ARGONAUT_PARSER_PURS = textwrap.dedent(
    text="""\
    module Data.Argonaut.Parser where
    import Data.Argonaut.Core (Json)
    import Data.Either (Either)
    foreign import jsonParser :: String -> Either String Json
    """,
)

ARGONAUT_PARSER_JS = textwrap.dedent(
    text="""\
    export const jsonParser = s => {
        try {
            return { tag: "Right", value: JSON.parse(s) };
        } catch (e) {
            return { tag: "Left", value: e.message };
        }
    };
    """,
)


def write_lint_environment(tmpdir: Path) -> list[Path]:
    """Write the Prelude + Argonaut/Either shim modules to *tmpdir*.

    Returns the list of ``.purs`` paths to pass to ``purs compile``
    alongside the fixture under check.  The matching ``.js`` files are
    written next to each module so PureScript's FFI resolution picks
    them up automatically.
    """
    modules: list[tuple[str, str, str]] = [
        ("Prelude.purs", PRELUDE_PURS, PRELUDE_JS),
        ("Either.purs", EITHER_PURS, EITHER_JS),
        ("ArgonautCore.purs", ARGONAUT_CORE_PURS, ARGONAUT_CORE_JS),
        ("ArgonautParser.purs", ARGONAUT_PARSER_PURS, ARGONAUT_PARSER_JS),
    ]
    purs_paths: list[Path] = []
    for purs_filename, purs_text, js_text in modules:
        purs_path = tmpdir / purs_filename
        purs_path.write_text(data=purs_text, encoding="utf-8")
        js_path = purs_path.with_suffix(suffix=".js")
        js_path.write_text(data=js_text, encoding="utf-8")
        purs_paths.append(purs_path)
    return purs_paths
