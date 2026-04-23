#!/usr/bin/env python3
"""Concatenate C++ fixtures into one TU for clang-tidy.

Wrap each fixture's body in its own namespace (file-scope decls such as
``struct clientType_`` collide between fixtures) and hoist ``#include``
lines to file scope (STL headers misbehave inside a namespace).
"""

import pathlib
import sys


def main() -> None:
    """Write the concatenated blob to ``sys.argv[2]``."""
    root = pathlib.Path(sys.argv[1])
    out = pathlib.Path(sys.argv[2])
    includes: set[str] = set()
    bodies: list[str] = []
    for idx, path in enumerate(sorted(root.rglob("*.cpp"))):
        body: list[str] = []
        for line in path.read_text().splitlines():
            if line.lstrip().startswith("#include"):
                includes.add(line.strip())
            else:
                body.append(line)
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
