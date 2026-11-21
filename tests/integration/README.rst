Golden cases
============

Start with the input directory under ``cases/``.
Its ``case.toml`` declares which public API, rendering contexts and option axes exercise that input.
The adjacent ``*@<version>.<extension>`` files are generated expectations that native CI jobs also consume.

Adding coverage
---------------

First look for an existing input with the same structure and behavior.
Extend its manifest when it can express the regression; create a new directory when the input itself is significant.
Use a name describing the behavior, and keep issue or backend provenance in the rationale.

A complete literal rendering needs one input file and a manifest like this::

    schema_version = 1
    suites = ["base", "combined"]

    [[variants]]
    axis = "integer_format"

``base`` renders the input using its ``base_context`` and each selected language's defaults.
``combined`` exercises declaration followed by assignment where supported.
Each ``variants`` entry selects a named expansion defined in ``variant_axes.py``.
To add an axis, use the shared helpers in ``axis_builders.py`` for option members, pairings and version coverage.
Select languages by the relevant capability or option, and use the axis name in the case manifest.
Omit suites and axes that the input cannot exercise.
For example, ``cases/scalar_int`` exercises integer formats, while ``cases/binary`` exercises byte formats.

Input format is inferred from one ``input.json``, ``input.jsonc``, ``input.json5``, ``input.toml`` or ``input.yaml``.
Set ``input`` explicitly when needed, as ``cases/multiline_string`` does.
Use ``gates`` to select declared capabilities or syntax support for specialized cases.
An ordinary shared case runs across languages by default.

``owner`` selects a specialized runner, such as ``literalize-call``, ``literalize-ref`` or ``constructor-binding``.
Its corresponding manifest table supplies the API arguments.
``roles`` let additional scenarios find a canonical input, such as the indentation example, without repeating its directory name in Python.
Copy a nearby case using the same API when adding specialized coverage.
The accepted fields and consistency checks are defined in ``case_manifests.py``.

Keep typed failures, metadata and concurrency contracts in the directories described by ``../README.rst``.
A complete generated program belongs here; an executable round-trip case should also compare the reconstructed value with the input.
Native success fixtures should use complete expressions and public composition.
Do not snapshot incidental output from malformed caller-owned transforms.
Add focused unit coverage for a demonstrated robustness regression with a meaningful invariant, such as avoiding a crash or hang.
The comment-placement lexer is not a target-language syntax validator.

Checking and regenerating
-------------------------

Run commands from the repository root.
Validate manifests and fixture ownership first::

    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/harness

To inspect the literal runner's test IDs, then regenerate its Python fixtures::

    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/test_literalize_golden.py --collect-only -q
    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/test_literalize_golden.py -k Python --regen-all

Literal test IDs identify the scenario, language, and optional batch.
Input names appear in subtest details, so ``-k scalar_int`` does not select one literal input.
Call, reference and constructor runners include their case identities in the collected IDs.
Run the test for the case module to regenerate all languages for a changed case; for the ordinary literal suites::

    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/test_literalize_golden.py --regen-all

Review the generated diff, then rerun the test for the cases without ``--regen-all`` and run ``harness/test_orphan_golden_files.py``.
A declared success compares rendered text, a declared rejection asserts its exception, and a capability exclusion reports its reason.
A rejected or excluded rendering that still has a native fixture fails even with ``--regen-all``.
Review the expectation and fixture diff when support changes.
Literal and format-variant cases resolve their expected outcomes before rendering.
Shared capability checks live in ``literal_expectations.py``.
When a specific authored input and option combination exercises a backend limit, declare the exception and a stable message pattern in ``literal_rejections.toml``.
Select the effective constructor options or render arguments that trigger the limit.
The harness checks that every declared selector still has a corresponding rendering.
Call and reference cases still use legacy skip policies for some constraints.
Keep the effective configuration matrix when renaming a case, including role references, axis suffixes and path-derived module names.

The Python golden checks verify rendered text and harness contracts.
The native jobs in ``.github/workflows/lint.yml`` separately compile, parse or execute the generated files.
Use both results when assessing an output change.

Finding the implementation
--------------------------

Follow the ordinary literal path in this order:

1. ``case_manifests.py`` validates ``case.toml`` and resolves its input.
2. ``case_discovery.py`` selects representable inputs; ``variant_cases.py`` pairs inputs with options expanded by the builders in ``variant_axes.py``.
3. ``golden_scenarios.py`` assembles ``GoldenRendering`` records from ``golden_renderings.py``; ``golden_batches.py`` bounds pytest work items.
4. ``test_literalize_golden.py`` renders each effective spec and ``golden_checks.py`` compares the result or asserts the declared rejection.
5. ``harness/test_orphan_golden_files.py`` checks fixture ownership across all runners.

The specialized entry points are ``test_calls.py``, ``test_literalize_ref_golden.py``, ``test_literalize_ref_default.py`` and ``test_constructor_targets.py``.
Backend-specific fixture naming, native consumer scaffolds and sample options live under ``languages/``.
``language_specs.py`` applies those naming rules and creates versioned fixture paths.

Observable call receivers
-------------------------

Ordinary unary integer calls can declare ``integer_receiver_events`` in their call table.
For example, ``[["call", 1], ["result", 101], ["zipped", 42]]`` checks the actual argument, the returned result and its zipped companion in order.
Author these expected events independently of renderer metadata.
The native receiver returns its argument plus 100; separate consumers observe the result and companion, and a final public call checks that every expected event occurred.
Existing bindings start from literal declarations, with their initial and final values observed through the real consumer.

``call_receivers.toml`` shares implementations by native integer signature and calling convention.
Capability declarations select participants before the syntax table is consulted.
Both ordinary and option-variant calls retain their effective spec, and external references retain their original inference hints.
Public ``wrap_in_file`` cases continue to exercise the library's generated-stub contract.

Native Java checks
------------------

With a JDK installed, run the same warm compiler host as CI::

    uv run --only-group=cli python -m scripts.run_java_fixtures
    uv run --only-group=cli python -m scripts.run_java_fixtures --release 11

Both JDK 11 and 16 fixture populations are checked by default.
Set ``LITERALIZER_LINT_CLASSPATH`` to the Jackson jars for JSON-type cases.
Each batch compiles with the matching ``--release`` and ``-Werror``, then executes initializers and consumer entry points.
The warm JVM checks up to 512 fixtures per batch, with a 300-second deadline.
Empty selections fail before execution.

Native interpreter checks
-------------------------

Native value assertions belong in the same case manifests and compiling golden files as their inputs.
Use ``base_context.consumer_templates`` for the base rendering or ``variants.consumer_templates`` for an option variant.
Templates receive the generated ``code`` and the selected enum option names, such as ``bytes_format`` and ``datetime_format``.
These names let an assertion check the intended representation's type as well as its value.
Other languages and variants retain their existing coverage when no consumer is declared.

For a wrapped C# variable, ``variants.after_binding`` supplies native statement lines to ``literalize``.
The generated wrapper places these assertions in the variable's scope.

Expected values must be independent of the renderer.
The typed scalar, byte and datetime consumers use native type checks and standard-library inspection: binary64 bit patterns, independently constructed byte ranges, Gregorian dates, and exact datetime instants and offsets.
Python lists and tuples share ordered sequence semantics; record consumers check authored fields and their native types.
Byte encodings and epoch/ISO conversions follow the explicitly selected option.
Python native datetimes retain naive values; Ruby represents naive input in UTC.
Special floats compare by NaN/infinity classification, and finite floats retain their exact bits.
Existing JSON roundtrips and specialized native assertions retain their distinct contracts.

The ordinary native jobs execute these self-contained files without another runner or transport format.
``test_native_value_consumers.py`` verifies failures after corrupting generated declarations while leaving their assertions unchanged, using bounded native execution.
The Python corruption checks run with the regular pytest suite.

Successful execution of the original programs remains with the existing native jobs.
Fixtures without native assertions retain their existing snapshot, compiler and native checks.

After installing Bash 5.1+, Ruby or Node, run the same fixture checks as CI::

    uv run --only-group=cli python -m scripts.run_interpreted_fixtures bash
    uv run --only-group=cli python -m scripts.run_interpreted_fixtures ruby
    uv run --only-group=cli python -m scripts.run_interpreted_fixtures javascript

Syntax checks complete before execution for interpreters that support a separate syntax phase.
Each command has a 60-second deadline.
Missing interpreters and empty selections fail.

Native Dart checks
------------------

Feed the same null-separated fixture paths used by native CI::

    find tests/integration/cases -name '*.dart' -print0 | uv run --group=dev python -m scripts.run_dart_fixtures

The runner stages the files, analyzes them and forces their bindings during execution.
An empty selection fails before starting the toolchain.
