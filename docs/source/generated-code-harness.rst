Generated-code harness evaluation
=================================

Decision (issue #5532)
----------------------

Retain a small project runner locally; do not publish a new package or move this functionality into Doccmd yet.
The experiment demonstrates a reusable boundary, but does not establish demand from another maintained generator project.
An independent toy schema generator proves that the API does not depend on Literalizer; it is not evidence of adoption.

``scripts/generated_code.py`` accepts a fixture label, a mapping of relative file names to UTF-8 source/supporting files, and an ordered sequence of ``Step(args=..., failure_label=...)`` values.
``run_project`` writes a fresh temporary project, runs each argv without a shell, captures output, and returns the completed steps.
A failed command raises an assertion with the label, argv, status, streams and project files.
Temporary directories are removed on success and failure; unavailable commands report their label and argv.
The module uses only the Python standard library and imports neither Literalizer nor its tests.

Assertions compose independently
--------------------------------

* Snapshot only: pass generated source to the existing ``pytest-regressions`` ``file_regression.check`` fixture.
  No compiler invocation is required.
* Compile or type-check only: supply a compiler command and assert that it succeeds.
  Nothing requires executing the generated program.
* Execute: add a consumer or runtime step and inspect any returned step's stdout/stderr.
  Caller assertions define semantic equality.

``tests/integration/test_generated_code.py`` exercises all three with a tiny schema-to-dataclass generator and a separate consumer.
Its assertions distinguish integers from booleans and check the sign of negative zero; ordinary Python equality alone would miss those distinctions.
A second example copies only the runner into an isolated temporary project and invokes an independent generator with Python's site initialization disabled.
It checks that neither Literalizer nor its test package was imported.

Representative Literalizer callers
----------------------------------

``scripts/roundtrip_common.py`` delegates project execution to this runner.
The existing per-language adapters still choose executable paths, compiler versions, flags, supporting files and compile/run order.
The round-trip module retains capability selection, excluded keys, rendering, JSON parsing and its existing equality policy.
This experiment deliberately does not change that policy to a new cross-language definition of equality.

``scripts/check_typescript_consumers.py`` supplies generated declarations with consumer probes as separate module files in one project.
It still invokes one ``tsc`` per input batch with the existing strict, target and library flags.
Fixture names remain embedded in filenames so compiler diagnostics identify the failing case.
Different invocations get independent temporary projects; the runner does not combine batches or split them into one compiler process per file.

Deadline and process ownership remain explicit.
Multi-step round trips still wrap every command with ``bounded_command`` and GNU timeout, including its process-group termination and fixture-labelled diagnostics.
Single-step round trips and TypeScript batches retain their existing outer workflow timeout policy.
The runner itself does not install toolchains, discover versions, impose a timeout, or implement another process supervisor.
Callers outside these workflows must provide a bounded command or supervise the entire invocation themselves.
A POSIX validation probe exercised a wrapper command that started a descendant process and verified that the descendant could not write after timeout.

``tests/integration/golden_checks.py`` remains responsible for Literalizer's skip and stale-fixture policy.
``tests/integration/test_orphan_golden_files.py`` still verifies fixture ownership against effective version/axis scenarios.
Neither policy belongs in a generic project runner, and both continue to use the existing manifest vocabulary.

Existing projects
-----------------

`Trybuild <https://docs.rs/trybuild/latest/trybuild/>`_ offers Rust compile-fail diagnostic snapshots and compile/pass execution through Cargo.
Use it for Rust library UI tests; its Rust/Cargo contract does not directly replace Python-driven multi-language generated-project tests.

`LLVM lit/FileCheck <https://www.llvm.org/docs/TestingGuide.html>`_ supplies command-driven regression tests and output pattern checks, with substitutions and platform constraints.
It can express compile/run pipelines already.
Adopting its test-file and configuration model would be a larger migration than sharing this small Python runner, while semantic assertions and Literalizer's manifest expansion would still need glue.

`pytest-regressions <https://pytest-regressions.readthedocs.io/en/latest/overview.html>`_ already supplies snapshot comparison, diffs and explicit regeneration in pytest.
Keep using it rather than inventing another snapshot format, update flag or pytest plugin.
The prototype's ordinary Python assertions and assertion exceptions work directly with pytest without plugin registration.

`Doccmd <https://github.com/adamtheturtle/doccmd>`_ runs caller-selected tools over documentation code blocks, including grouped examples.
It remains the appropriate tool for documentation linting and formatting.
This runner instead starts from an in-memory generated project with supporting files, ordered compiler/runtime steps and returned outputs.
Adding schema/generator assertions and fixture ownership to Doccmd would broaden its documented purpose without demonstrated demand.

Publication threshold
---------------------

A separate project would be justified by maintained, independent generators needing the same project execution and diagnostics API across toolchains.
Before extraction, validate that demand, choose the supported process/deadline policy on Windows and POSIX, and measure compiler batching on those consumers.
Then extract the runner with its process contract and tests, keeping snapshots in pytest-regressions and toolchain installation with callers.
Do not publish Literalizer's JSON policy, capability model, manifests, version/axis vocabulary or source-text consumer-probe heuristics as generic APIs.
