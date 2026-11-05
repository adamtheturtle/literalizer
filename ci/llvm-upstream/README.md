# LLVM upstream review bundle

Local copies of six reduced performance reports and five isolated patches submitted upstream.
As of 2026-11-05, the WebKit fix and an alternative ADL fix are merged into LLVM main.
LLVM 23.1.5 still lacks both fixes; the remaining three PRs and the PCH issue remain open.
Retain the [patched toolchain](../clang/README.md) until released tools pass the complete C and C++ fixture checks and semantic controls within their existing deadlines.

| Topic | Upstream status | Report | Local patch |
| --- | --- | --- | --- |
| sfinae | [PR 235715](https://github.com/llvm/llvm-project/pull/235715) open | [Report](reports/sfinae.md) | [Patch and regression test](patches/sfinae.patch) |
| adl | [PR 238975](https://github.com/llvm/llvm-project/pull/238975) merged; supersedes [PR 235714](https://github.com/llvm/llvm-project/pull/235714) | [Report](reports/adl.md) | [Patch and regression test](patches/adl.patch) |
| webkit | [PR 235713](https://github.com/llvm/llvm-project/pull/235713) merged | [Report](reports/webkit.md) | [Patch and regression test](patches/webkit.patch) |
| exception | [PR 235716](https://github.com/llvm/llvm-project/pull/235716) open, including the recursive-component follow-up for [#224308](https://github.com/llvm/llvm-project/issues/224308) | [Report and follow-up](reports/exception.md) | [Patch and regression test](patches/exception.patch) |
| shared-initializers | [PR 235717](https://github.com/llvm/llvm-project/pull/235717) open | [Report](reports/shared-initializers.md) | [Patch and regression test](patches/shared-initializers.patch) |
| pch | [Issue 235707](https://github.com/llvm/llvm-project/issues/235707) open | [Report](reports/pch.md) | No implementation fix yet |

Each source is in [reproducers](reproducers).
Commands are shown in the reports.
[measurements.json](measurements.json) contains the exact commands, source hashes, exit statuses, toolchain manifest and sample wall times.
[submission-plan.json](submission-plan.json) retains the original submission titles, destinations and bodies.

The original patches independently applied to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0`.
Their new compiler-driven tests passed with the patched LLVM 23.1.4 tools.
The builder also preserves registered checks, existing SFINAE diagnostics, stack-exhaustion controls, caught/rethrown exception diagnostics, parent edges, positive matcher bindings and the checked C diagnostics.

The captured `/repo/upstream/llvm` paths name the measurement mount before this CI-only bundle was placed here.
The source hashes match the files in `reproducers`.

The SFINAE reproducer uses a qualified call to exclude ADL.
The WebKit source uses four small templates/records and no standard headers.
The exception report extends the existing issue rather than opening a duplicate.
The PCH report identifies a candidate profiling hotspot and does not claim an implementation fix.

These candidate patches derive from LLVM code under Apache 2.0 with LLVM exceptions; see [the retained license](../clang/LICENSE.TXT).
Prepared with AI assistance.
