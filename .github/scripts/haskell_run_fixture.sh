#!/usr/bin/env bash
set -euo pipefail
f="$1"
mod=$(basename "$f" .hs)
builddir=$(mktemp -d)
trap 'rm -rf "$builddir"' EXIT
if grep -qE "^main " "$f"; then
    ghc -Wall -Werror -main-is "$mod" -outputdir "$builddir" \
        -o "$builddir/run" "$f"
else
    sed "s/MODULE_PLACEHOLDER/$mod/g" .github/scripts/haskell_main.hs \
        > "$builddir/Main.hs"
    ghc -Wall -Werror -outputdir "$builddir" \
        -o "$builddir/run" "$builddir/Main.hs" "$f"
fi
"$builddir/run"
