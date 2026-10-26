Tested with official LLVM 23.1.4 (`7a941dfb2877a0b8cf30323fefa85ad019e0b0f5`) on Ubuntu 24.04.5, Linux AArch64.

The source has no WTF classes and no reference-counting interface.
This checker should reject the namespace exemption cheaply.
Ordinary syntax checking of this source completes promptly.

```cpp
template<class T> struct Alloc {};
template<class T, class A> struct Storage {};
template<class T, class A=Alloc<T>> struct Node : Storage<T,A> {};
struct Derived : Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<Node<int>>>>>>>>>>>>>>>>>>>>>>>>>>>> {};
```

Run from the [reproducer bundle](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/README.md):

```sh
timeout 10s clang-tidy reproducers/webkit.cpp --checks=-*,clang-analyzer-webkit.RefCntblBaseVirtualDtor --config={} -- -std=c++20
```

The unmodified release exceeded the ten-second limit (exit 124).
The same input completed in 0.022 seconds with the [candidate implementation](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/patches/webkit.patch).
These are single sequential wall-clock samples, not statistical benchmarks.
Raw commands and outputs are in [measurements.json](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/measurements.json).

The exemption condition calls `T.getAsString()` before checking whether the declaring namespace is WTF.
Printing this instantiated base expands repeated allocator/type arguments.

Candidate fix: Check the namespace before calling `getAsString()`.
This reorders the same conjunction; it does not change which classes are exempt.
The candidate includes a compiler-analyzer regression test with no standard-library dependency.

The isolated patch applies to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0` and contains a regression test.
The new test and the downstream semantic controls were run with the patched 23.1.4 tools; a complete build of current LLVM main has not been performed.

Prepared with AI assistance.
