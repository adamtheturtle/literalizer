# Clang compiler performance fixes

The C++ golden corpus includes thirty nested owning `std::vector` levels.
Clang 23.1.4 spends the fixture's entire time budget expanding unused SFINAE diagnostics and revisiting template arguments during argument-dependent lookup.
The WebKit virtual-destructor checker also expands unrelated standard-library types before checking whether their namespace can match its exemption.

`scripts/build_cpp_toolchain.py` builds `performance.patch` without changing overload viability, associated namespaces, native container types, or enabled clang-tidy checks.
The SFINAE diagnostic problem is tracked in [LLVM issue 38701](https://github.com/llvm/llvm-project/issues/38701).

Clang-tidy's exception analyzer also repeatedly follows the same constructor calls in C++20, as reported in [LLVM issue 224308](https://github.com/llvm/llvm-project/issues/224308).
Cache complete function analyses within one traversal, preserving exception types and rebasing diagnostic call stacks at each use.
Do not reuse results that depend on caught exceptions or a recursive back edge.
The analyzer's object layout is unchanged; only its implementation and private call signatures change.

C designated initializers share expression subtrees between their syntactic and semantic forms.
Thirty nested C containers cause the parent-map builder, descendant matchers, outer matcher traversal, and padding checker to revisit those same subtrees exponentially.
Record every incoming parent edge while expanding each statement's children once.
Cache only descendant searches with no matches, preserving successful binding multiplicity, and stop direct-child searches below their requested depth.
Match a shared C compound literal once in each traversal context instead of issuing identical callbacks for repeated paths to the same expression.
The padding checker likewise visits each distinct statement, retaining all record and array checks.

The builder links parent-graph and matcher controls against both stock and patched libraries and requires identical output.
These cover designated initializers, multiple template parents, lambdas, type locations, positive descendant binding multiplicity, missing descendants, and distinct direct-child matches.
Duplicate outer callbacks for the same C expression are intentionally removed; distinct matches and diagnostics remain checked.

The builder verifies the official LLVM 23.1.4 release archive, checks out its exact source commit, and rebuilds the eight affected translation units.
It replaces those objects in copies of their original static libraries and links the upstream compiler and clang-tidy drivers.
The remaining libraries and checker modules come from that release.
The compiler's original formatter for a failing condition remains available when a rejected candidate is diagnosed.

Compile fixtures without a precompiled standard-library header.
Loading that header makes Clang's `TemplateArgumentHasher` recursively expand the same nested types while looking up specializations in the serialized AST.
Direct header parsing avoids this separate exponential path and retains the existing fixture deadlines.

Remove a patch after an upstream release contains its fix and the complete compiler-backed C and C++ corpora passes within the existing fixture budgets.

The patch derives from LLVM source licensed under Apache 2.0 with LLVM exceptions; see `LICENSE.TXT`.
The runtime artifact retains that license.
