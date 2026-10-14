C++ toolchain validation
========================

Run static analysis, compilation, and execution separately when investigating a C++ toolchain discrepancy.
A successful execution tests one path through a program; it does not establish that the static analysis diagnostic is harmless.
Record the checker, compiler, standard library, SDK, language standard, and configuration for each result.

Reproduce issue 5449
--------------------

The investigation for `issue 5449 <https://github.com/adamtheturtle/literalizer/issues/5449>`__ used commit ``91a58466dd`` on 2026-10-14 and the unchanged :file:`tests/integration/cases/call_cpp_multislot_carrier/Cpp_call@cpp14.cpp` fixture.
All analysis used the repository's unchanged :file:`.clang-tidy`, warnings as errors, and the PyPI ``clang-tidy==22.1.8`` package.
The fixture requires C++14 and no third-party headers.

On macOS, select the SDK explicitly and use Apple's compiler with its SDK headers and runtime:

.. code-block:: shell

   cpp_sdk=$(xcrun --show-sdk-path)
   cpp_fixture=tests/integration/cases/call_cpp_multislot_carrier/Cpp_call@cpp14.cpp
   sw_vers
   xcrun --show-sdk-version
   clang++ --version
   uvx --from clang-tidy==22.1.8 clang-tidy --version
   uvx --from clang-tidy==22.1.8 clang-tidy "$cpp_fixture" \
       --config-file=.clang-tidy --warnings-as-errors='*' -- \
       -std=c++14 -isysroot "$cpp_sdk"

The final command exits with status 1 for the recorded macOS setup.
Compile and run the same file independently:

.. code-block:: shell

   set -e
   cpp_sdk=$(xcrun --show-sdk-path)
   cpp_fixture=tests/integration/cases/call_cpp_multislot_carrier/Cpp_call@cpp14.cpp
   cpp_output=$(mktemp -d)
   clang++ -std=c++14 -Werror -isysroot "$cpp_sdk" \
       "$cpp_fixture" -o "$cpp_output/run"
   "$cpp_output/run"
   rm -r "$cpp_output"

On Linux, install Clang and both standard libraries before comparing them.
The recorded setup used Ubuntu 24.04 on arm64, ``clang-22``, ``libc++-22-dev``, and ``libc++abi-22-dev`` from `LLVM's package repository <https://apt.llvm.org/>`__, plus Ubuntu's ``libstdc++-13-dev``.
The LLVM packages were version ``1:22.1.8~++20260714014902+ca7933e47d3a-1~exp1~20260714135019.80``; the GNU headers were version ``13.3.0-6ubuntu2~24.04.1``.
Select each library explicitly with the same checker and configuration:

.. code-block:: shell

   cpp_fixture=tests/integration/cases/call_cpp_multislot_carrier/Cpp_call@cpp14.cpp
   uvx --from clang-tidy==22.1.8 clang-tidy "$cpp_fixture" \
       --config-file=.clang-tidy --warnings-as-errors='*' -- \
       -std=c++14 -stdlib=libstdc++
   uvx --from clang-tidy==22.1.8 clang-tidy "$cpp_fixture" \
       --config-file=.clang-tidy --warnings-as-errors='*' -- \
       -std=c++14 -stdlib=libc++

Compile and execute each selection separately with ``clang++-22 -std=c++14 -Werror -stdlib=libstdc++`` or ``clang++-22 -std=c++14 -Werror -stdlib=libc++``.
Inspect the actual header search path with the same flags and ``-E -v -x c++ /dev/null`` if multiple library versions are installed.

Recorded results
----------------

.. list-table:: Unchanged carrier fixture, C++14, clang-tidy 22.1.8
   :header-rows: 1

   * - Platform and library
     - Compiler for execution
     - Static analysis
     - Compile and run
   * - macOS 27.0, SDK 27.0 ``libc++``
     - Apple Clang 21.0.0
     - Fail
     - Pass
   * - macOS 27.0, Homebrew ``libc++`` 22.1.8
     - Homebrew Clang 22.1.8
     - Fail
     - Pass
   * - Ubuntu 24.04, ``libstdc++`` 13
     - Clang 22.1.8
     - Pass
     - Pass
   * - Ubuntu 24.04, ``libc++`` 22.1.8
     - Clang 22.1.8
     - Fail
     - Pass

The Homebrew comparison selected :file:`/opt/homebrew/opt/llvm@22/include/c++/v1` with ``-nostdinc++ -isystem`` and linked :file:`/opt/homebrew/opt/llvm@22/lib/c++` with ``-L`` and ``-Wl,-rpath``.
It retained the same macOS SDK.
Matching LLVM 22.1.8 components therefore does not clear the diagnostic.
Linux with ``libc++`` reproduces it too: the difference follows the standard library, rather than macOS alone.
This local Linux comparison does not constitute a new hosted CI result.

Diagnosis and limits
--------------------

`LLVM's check documentation <https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-22.1.8/clang-tools-extra/docs/clang-tidy/checks/bugprone/exception-escape.rst>`__ includes ``main`` among functions checked for escaping exceptions.
This is a checker policy; C++ does not implicitly declare ``main`` as ``noexcept``.
The allocator and string diagnostics follow throw expressions visible inside ``libc++`` headers, including ``bad_array_new_length`` and ``length_error``.
GNU's corresponding helpers are declarations in `bits/functexcept.h <https://raw.githubusercontent.com/gcc-mirror/gcc/releases/gcc-13.3.0/libstdc%2B%2B-v3/include/bits/functexcept.h>`__ with definitions outside the translation unit.

The pinned `ExceptionAnalyzer implementation <https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-22.1.8/clang-tools-extra/clang-tidy/utils/ExceptionAnalyzer.cpp>`__ traverses available function bodies and constructor initializers.
A function without a body or a typed exception specification contributes an unknown result, rather than a known thrown type.
The `check implementation <https://raw.githubusercontent.com/llvm/llvm-project/llvmorg-22.1.8/clang-tools-extra/clang-tidy/bugprone/ExceptionEscapeCheck.cpp>`__ reports known throws; an unknown result alone does not trigger a diagnostic.
It also ignores ``std::bad_alloc`` by name, which does not include ``std::bad_array_new_length``.
These implementation details explain why passing with ``libstdc++`` provides different evidence from passing with ``libc++``.

The following reduced control produces the same library-dependent diagnostic:

.. code-block:: cpp

   #include <memory>
   int main() {
       const auto value = std::make_shared<int>(1);
       return *value - 1;
   }

With the full configuration, this control passed with Linux ``libstdc++`` and failed with Apple's SDK ``libc++`` and Linux ``libc++`` 22.1.8.
Adding ``try { ... } catch (...) { return 1; }`` around its body passed in each of those setups.
A direct ``throw`` in ``main`` failed in each setup, while a call to a separately defined throwing function passed analysis when only its declaration was visible.
A visible function containing ``if (value < 0) { throw 1; }`` also produced an escape diagnostic when called with ``value = 1``: the analysis does not establish the allocator branch's reachability for the fixture's concrete values.

Preserve strict validation
--------------------------

Keep failures from the native standard-library setup visible alongside Linux results.
Do not disable ``bugprone-exception-escape``, ignore the reported exception types, disable exceptions, or substitute a library solely to obtain a passing result.
The evidence identifies the checker limitation; it does not establish that every escaping exception is harmless.

The existing C++ file wrapper catches exceptions for JSON output and returns status 1, but native output has no equivalent catch boundary.
Extending that boundary would require an explicit contract for complete-file output: successful construction and calls return status 0, and exceptions return a failure status.
Validate such a change with both successful execution and a deliberately throwing call, as well as strict checks with both libraries.
The investigation itself does not change generated values, wrappers, or lint policy.
