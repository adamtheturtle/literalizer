# LLVM upstream review bundle

Six reduced performance reports and five isolated candidate patches, prepared for human review.
Nothing in this bundle has been submitted to LLVM.
LLVM requires contributors to review AI-assisted text and code before requesting upstream review; see its [AI Tool Use Policy](https://llvm.org/docs/AIToolPolicy.html#policy).

| Topic | Draft destination | Report | Candidate patch |
| --- | --- | --- | --- |
| sfinae | New LLVM issue | [Draft](reports/sfinae.md) | [Patch and regression test](patches/sfinae.patch) |
| adl | New LLVM issue | [Draft](reports/adl.md) | [Patch and regression test](patches/adl.patch) |
| webkit | New LLVM issue | [Draft](reports/webkit.md) | [Patch and regression test](patches/webkit.patch) |
| exception | Comment on [#224308](https://github.com/llvm/llvm-project/issues/224308) | [Draft](reports/exception.md) | [Patch and regression test](patches/exception.patch) |
| shared-initializers | New LLVM issue | [Draft](reports/shared-initializers.md) | [Patch and regression test](patches/shared-initializers.patch) |
| pch | New LLVM issue | [Draft](reports/pch.md) | No implementation fix yet |

Each source is in [reproducers](reproducers).
Commands are shown in the reports.
[measurements.json](measurements.json) contains the exact commands, source hashes, exit statuses, toolchain manifest and sample wall times.
[submission-plan.json](submission-plan.json) records the intended titles, destinations and bodies.

The patches independently apply to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0`.
Their new compiler-driven tests pass with the patched LLVM 23.1.4 tools.
The builder also preserves registered checks, existing SFINAE diagnostics, stack-exhaustion controls, caught/rethrown exception diagnostics, parent edges, positive matcher bindings and the checked C diagnostics.
A complete build of current LLVM main has not been run.

The captured `/repo/upstream/llvm` paths name the measurement mount before this CI-only bundle was placed here.
The source hashes match the files in `reproducers`.

The SFINAE reproducer uses a qualified call to exclude ADL.
The WebKit source uses four small templates/records and no standard headers.
The exception report extends the existing issue rather than opening a duplicate.
The PCH report identifies a candidate profiling hotspot and does not claim an implementation fix.

These candidate patches derive from LLVM code under Apache 2.0 with LLVM exceptions; see [the retained license](../clang/LICENSE.TXT).
Prepared with AI assistance.
