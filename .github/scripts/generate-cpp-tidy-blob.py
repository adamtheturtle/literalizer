#!/usr/bin/env python3
"""Concatenate C++ fixtures into one TU for clang-tidy.

The ``lint-cpp-tidy`` job would otherwise re-parse every standard
header and re-initialize ``clang-analyzer-*`` symbolic execution once
per fixture (~280 times). Feeding clang-tidy a single concatenated
translation unit amortizes both costs across all fixtures.

The workflow discovers fixtures with ``find ... -print0`` and pipes
them in via ``xargs -0``. This script only concatenates — it does not
walk the filesystem itself.

Usage:
    python generate-cpp-tidy-blob.py <output> <fixture>...
"""

import pathlib
import sys


def main() -> None:
    """Write the concatenated blob to ``sys.argv[1]``."""
    # First arg is the output path; the rest are fixture paths that the
    # workflow fed in via xargs. Sort so output is deterministic even
    # when filesystem enumeration order differs between runs/platforms.
    out = pathlib.Path(sys.argv[1])
    fixtures = sorted(pathlib.Path(p) for p in sys.argv[2:])

    # Collect all unique ``#include`` lines from every fixture. We
    # dedup because every fixture repeats the same small set of STL
    # headers — pulling each one in 280 times bloats parse cost for no
    # benefit.
    includes: set[str] = set()
    bodies: list[str] = []

    for idx, path in enumerate(fixtures):
        body: list[str] = []
        for line in path.read_text().splitlines():
            # Hoist ``#include``s out of each fixture and into file
            # scope. STL headers contain constructs like ``extern "C"``
            # and global-namespace declarations that misbehave or fail
            # to compile when nested inside a namespace, so we cannot
            # leave them inside the wrapping ``namespace fX { ... }``
            # block below.
            if line.lstrip().startswith("#include"):
                includes.add(line.strip())
            else:
                body.append(line)

        # Wrap each fixture's body in its own uniquely-named namespace.
        # Several fixtures define file-scope helpers with the same name
        # (e.g. ``auto process(auto...)``, ``struct clientType_``,
        # ``const appType_ app``) — without namespaces, concatenating
        # them produces ODR violations.
        #
        # The trailing ``// namespace fX`` comment is not cosmetic: the
        # ``llvm-namespace-comment`` and
        # ``google-readability-namespace-comments`` checks in our
        # ``.clang-tidy`` config require it and emit one error per
        # namespace otherwise.
        bodies.append(
            f"namespace f{idx} {{\n"
            + "\n".join(body)
            + f"\n}}  // namespace f{idx}",
        )

    out.write_text(
        data="\n".join(sorted(includes)) + "\n" + "\n".join(bodies) + "\n",
    )


if __name__ == "__main__":
    main()
