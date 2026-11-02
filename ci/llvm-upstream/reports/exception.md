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

Candidate fix: Cache completed analyses within one traversal and rebase diagnostic call stacks at each use.
The initial implementation is under review in [PR 235716](https://github.com/llvm/llvm-project/pull/235716).

The initial global recursion-generation counter conservatively invalidates every caller above a recursive helper.
Each analysis frame has a set of unresolved recursive calls.
Completing a recursive root resolves that dependency, allowing its callers to reuse the result.
Results with unfinished ancestor dependencies remain uncached.
A shared direct call graph records the traversed callees without duplicating transitive callee sets in every cache entry.
A cache entry is reusable only if no reachable callee is active in the new caller's stack.
Caught-exception contexts remain excluded from caching.

The additional [recursive reproducer](../reproducers/exception-recursive.cpp) puts a self-recursive helper below the repeated-call tree.
With the initial memoization patch it exceeded a ten-second limit; the follow-up completed in approximately 0.033 seconds and retained the expected warning.
The commands, source and binary hashes, toolchain manifests and single-sample times are in [recursive-exception-cache.json](../recursive-exception-cache.json).
These measurements use the same LLVM 23.1.4 Linux AArch64 release and are not statistical benchmarks.

Stock-versus-patched controls compare every exception type and diagnostic stack, behavior states and unknown exceptions in C++14, C++17 and C++20.
They exercise function and statement entry points with all combinations of the two optional analyzer assumptions.
The regression also checks that a cached component is traversed again when one of its callees is already active: otherwise an exception can be invented in a fully caught function.
The existing cached caller-location assertion is preserved.

The isolated patch applies to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0` and contains a regression test.
The new test and the downstream semantic controls were run with the patched 23.1.4 tools; a complete build of current LLVM main has not been performed.

This is intended as a follow-up to https://github.com/llvm/llvm-project/issues/224308, rather than a new duplicate issue.

Prepared with AI assistance.
