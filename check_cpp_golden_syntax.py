"""Check syntax of C++ golden files using clang++."""

import shutil
import subprocess
import sys
import textwrap
from pathlib import Path


def main() -> None:
    """Check syntax of each given C++ golden file."""
    clangpp_path = shutil.which(cmd="clang++") or "clang++"
    for filename in sys.argv[1:]:
        content = Path(filename).read_text(encoding="utf-8").strip()
        # Wrap content in a struct that accepts any value or nested initializer
        # list, allowing mixed-type and nested brace-init syntax to compile as
        # valid C++.
        template = """\
            #include <initializer_list>
            #include <cstddef>
            struct _Any {
                template<class T> _Any(T&&) noexcept {}
                _Any(std::initializer_list<_Any>) noexcept {}
            };
            void _check() {
                [[maybe_unused]] _Any _v = CONTENT;
            }
            """
        wrapped = textwrap.dedent(text=template).replace("CONTENT", content)
        result = subprocess.run(
            args=[
                clangpp_path,
                "-fsyntax-only",
                "-std=c++17",
                "-x",
                "c++",
                "-",
            ],
            input=wrapped,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            msg = f"{filename}: C++ syntax error\n{result.stderr}"
            sys.stderr.write(msg)
            sys.exit(1)


if __name__ == "__main__":
    main()
