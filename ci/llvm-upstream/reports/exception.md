Tested with official LLVM 23.1.4 (`7a941dfb2877a0b8cf30323fefa85ad019e0b0f5`) on Ubuntu 24.04.5, Linux AArch64.

The checker should report that `test` may throw, including the diagnostic call chain, without re-analyzing the same callee twice at every level.

```cpp
template<int N> void repeated() {
  repeated<N - 1>();
  repeated<N - 1>();
}
template<> void repeated<0>() { throw 1; }
void test() noexcept { repeated<28>(); }
```

Run from the [reproducer bundle](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/README.md):

```sh
timeout 10s clang-tidy reproducers/exception.cpp --checks=-*,bugprone-exception-escape --config={} -- -std=c++20
```

The unmodified release exceeded the ten-second limit (exit 124).
The same input completed in 0.021 seconds with the [candidate implementation](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/patches/exception.patch).
These are single sequential wall-clock samples, not statistical benchmarks.
Raw commands and outputs are in [measurements.json](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/measurements.json).

Each specialization calls the same lower specialization twice.
The number of distinct functions is linear in the depth, but uncached recursive analysis repeats those functions.

Candidate fix: Cache completed analyses within one traversal.
Do not reuse results that depend on caught exceptions or recursive back edges; rebase diagnostic call stacks at each use.
The attached regression test checks caught/rethrown exception types, recursive paths, repeated calls and a fully caught negative control.

The isolated patch applies to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0` and contains a regression test.
The new test and the downstream semantic controls were run with the patched 23.1.4 tools; a complete build of current LLVM main has not been performed.

This is intended as a follow-up to https://github.com/llvm/llvm-project/issues/224308, rather than a new duplicate issue.

Prepared with AI assistance.
