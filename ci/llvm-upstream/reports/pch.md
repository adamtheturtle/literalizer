Tested with the unmodified official LLVM 23.1.4 release (`7a941dfb2877a0b8cf30323fefa85ad019e0b0f5`), Ubuntu 24.04.5, Linux AArch64, GCC 13.3 standard-library headers.

A translation unit declaring an empty nested owning vector compiles in 0.104 seconds when headers are parsed directly, but exceeds ten seconds when `<vector>` is supplied through a PCH.

`reproducers/vector.hpp`:

```cpp
#include <vector>
```

`reproducers/pch.cpp`:

```cpp
#include <vector>
int main() { std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<std::vector<int>>>>>>>>>>>>>>>>>>>> value; (void)value; }
```

```sh
clang++ -std=c++20 -x c++-header reproducers/vector.hpp -o /tmp/vector.pch
timeout 10s clang++ -std=c++20 -fsyntax-only reproducers/pch.cpp
timeout 10s clang++ -std=c++20 -include-pch /tmp/vector.pch -fsyntax-only reproducers/pch.cpp
```

The first compile succeeds; the PCH compile reaches the limit (exit 124).
Reducing the nesting provides a smaller scaling control.
Raw commands and outputs are in [measurements.json](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/measurements.json).
The results are single sequential wall-clock samples, not statistical benchmarks.

Earlier profiling of our larger source showed repeated `TemplateArgumentHasher::AddTemplateArgument` / `AddDecl` frames while reading a serialized AST.
That is a candidate hotspot for this reduced case, rather than a confirmed diagnosis from a new profile.

Our temporary workaround parses the standard headers directly.
No LLVM implementation patch is proposed for this path yet.

Prepared with AI assistance.
