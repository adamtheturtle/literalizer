Tested with official LLVM 23.1.4 (`7a941dfb2877a0b8cf30323fefa85ad019e0b0f5`) on Ubuntu 24.04.5, Linux AArch64.

A valid overload call should select the ellipsis overload without constructing an unused diagnostic string.
The qualified `::accept` call intentionally disables ADL, isolating diagnostic construction.

```cpp
#include <type_traits>
template<class T, class U=T> struct Node {};
template<class T, std::enable_if_t<(sizeof(T) == 0), int> = 0> void accept(T) {}
void accept(...) {}
int main() { ::accept(Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<int>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>{}); }
```

Run from the [reproducer bundle](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/README.md):

```sh
timeout 10s clang++ -std=c++17 -fsyntax-only reproducers/sfinae.cpp
```

The unmodified release exceeded the ten-second limit (exit 124).
The same input completed in 0.028 seconds with the [candidate implementation](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/patches/sfinae.patch).
These are single sequential wall-clock samples, not statistical benchmarks.
Raw commands and outputs are in [measurements.json](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/measurements.json).

The false `sizeof(T) == 0` requirement is cheap to evaluate.
The expensive work is eagerly pretty-printing its substituted type for a diagnostic that is discarded when the fallback overload succeeds.

Candidate fix: Defer formatting the failed boolean condition until a rejected candidate is actually diagnosed.
Keep expression evaluation and overload viability unchanged.
The candidate patch includes a compiler-driven regression test.

The isolated patch applies to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0` and contains a regression test.
The new test and the downstream semantic controls were run with the patched 23.1.4 tools; a complete build of current LLVM main has not been performed.

The older https://github.com/llvm/llvm-project/issues/38701 is related compile-time-performance context, rather than a demonstrated duplicate of this reduced case.

Prepared with AI assistance.
