Tested with official LLVM 23.1.4 (`7a941dfb2877a0b8cf30323fefa85ad019e0b0f5`) on Ubuntu 24.04.5, Linux AArch64.

Lookup should find `assoc::consume`; revisiting the same nested specialization through two identical template arguments should not multiply lookup cost.

```cpp
namespace assoc {
struct Leaf {};
template<class T, class U=T> struct Node {};
void consume(...);
}
void test(assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Node<assoc::Leaf>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> value) { consume(value); }
```

Run from the [reproducer bundle](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/README.md):

```sh
timeout 10s clang++ -std=c++17 -fsyntax-only reproducers/adl.cpp
```

The unmodified release exceeded the ten-second limit (exit 124).
The same input completed in 0.025 seconds with the [candidate implementation](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/patches/adl.patch).
These are single sequential wall-clock samples, not statistical benchmarks.
Raw commands and outputs are in [measurements.json](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/measurements.json).

Each `Node<T, T>` has two paths to the same argument specialization.
Repeating those paths at every nesting level produces redundant associated-namespace traversal.

Candidate fix: Remember which specializations have had their template arguments visited, separately from transitive base-class traversal.
The regression test also checks a specialization appearing through a base and as a direct argument.

The isolated patch applies to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0` and contains a regression test.
The new test and the downstream semantic controls were run with the patched 23.1.4 tools; a complete build of current LLVM main has not been performed.

Prepared with AI assistance.
