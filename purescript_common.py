"""Shared helpers for the PureScript lint scripts."""

import textwrap

PRELUDE_PURS = textwrap.dedent(
    text="""\
    module Prelude where
    foreign import negate :: forall a. a -> a
    foreign import div :: forall a. a -> a -> a
    infixl 7 div as /
    """,
)

PRELUDE_JS = textwrap.dedent(
    text="""\
    export const negate = x => -x;
    export const div = x => y => x / y;
    """,
)
