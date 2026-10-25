# C++ compiler performance fixes

The C++ golden corpus includes thirty nested owning `std::vector` levels.
Clang 23.1.4 spends the fixture's entire time budget expanding unused SFINAE diagnostics and revisiting template arguments during argument-dependent lookup.
The WebKit virtual-destructor checker also expands unrelated standard-library types before checking whether their namespace can match its exemption.

`scripts/build_cpp_toolchain.py` builds `performance.patch` without changing overload viability, associated namespaces, native container types, or enabled clang-tidy checks.
The SFINAE diagnostic problem is tracked in [LLVM issue 38701](https://github.com/llvm/llvm-project/issues/38701).

Clang-tidy's exception analyzer also repeatedly follows the same constructor calls in C++20, as reported in [LLVM issue 224308](https://github.com/llvm/llvm-project/issues/224308).
Cache complete function analyses within one traversal, preserving exception types and rebasing diagnostic call stacks at each use.
Do not reuse results that depend on caught exceptions or a recursive back edge.
The analyzer's object layout is unchanged; only its implementation and private call signatures change.

The builder verifies the official LLVM 23.1.4 release archive, checks out its exact source commit, and rebuilds the five affected translation units.
It replaces those objects in copies of their original static libraries and links the upstream compiler and clang-tidy drivers.
The remaining libraries and checker modules come from that release.
The compiler's original formatter for a failing condition remains available when a rejected candidate is diagnosed.

Compile fixtures without a precompiled standard-library header.
Loading that header makes Clang's `TemplateArgumentHasher` recursively expand the same nested types while looking up specializations in the serialized AST.
Direct header parsing avoids this separate exponential path and retains the existing fixture deadlines.

Remove a patch after an upstream release contains its fix and the complete compiler-backed C++ corpus passes within the existing fixture budgets.

The patch derives from LLVM source licensed under Apache 2.0 with LLVM exceptions; see `LICENSE.TXT`.
The runtime artifact retains that license.
