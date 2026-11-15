Golden cases
============

Start with the input directory under ``cases/``.
Its ``case.toml`` declares which public API, rendering contexts and option axes exercise that input.
The adjacent ``*@<version>.<extension>`` files are generated expectations that native CI jobs also consume.

Adding coverage
---------------

First look for an existing input with the same shape and behavior.
Extend its manifest when it can express the regression; create a new directory when the input itself is significant.
Use a name describing the behavior, and keep issue or backend provenance in the rationale.

A complete literal rendering needs one input file and a manifest like this::

    schema_version = 1
    suites = ["base", "combined"]

    [[variants]]
    axis = "integer_format"

``base`` renders the input using its ``base_context`` and each selected language's defaults.
``combined`` exercises declaration followed by assignment where supported.
Each ``variants`` entry adds an option expansion declared in ``axes.toml``.
Omit suites and axes that the input cannot exercise.
For example, ``cases/scalar_int`` exercises integer formats, while ``cases/binary`` exercises byte formats.

Input format is inferred from a sole ``input.json``, ``input.jsonc``, ``input.json5``, ``input.toml`` or ``input.yaml``.
Set ``input`` explicitly when needed, as ``cases/multiline_string`` does.
Use ``gates`` to select declared capabilities or syntax support for specialized cases.
An ordinary shared case needs no language selection.

``owner`` selects a specialized runner, such as ``literalize-call``, ``literalize-ref`` or ``constructor-binding``.
Its corresponding manifest table supplies the API arguments.
``roles`` let additional scenarios find a canonical input, such as the indentation example, without repeating its directory name in Python.
Copy a nearby case using the same API when adding specialized coverage.
The accepted fields and consistency checks are defined in ``case_manifests.py``.

Keep typed failures, incomplete fragments, metadata and concurrency contracts in the directories described by ``../README.rst``.
A complete generated program belongs here; an executable round-trip case should also compare the reconstructed value with the input.

Checking and regenerating
-------------------------

Run commands from the repository root.
Validate manifests and fixture ownership first::

    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/harness

To inspect the literal runner's test IDs, then regenerate its Python fixtures::

    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/test_literalize_golden.py --collect-only -q
    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/test_literalize_golden.py -k Python --regen-all

Literal test IDs name a scenario, language and optional batch.
Input names appear in subtest details, so ``-k scalar_int`` does not select a single literal input.
Call, reference and constructor runners include their case identities in the collected IDs.
Run the owning test module to regenerate all languages for a changed case; for the ordinary literal suites::

    UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/integration/test_literalize_golden.py --regen-all

Review the generated diff, then rerun the owning tests without ``--regen-all`` and run ``harness/test_orphan_golden_files.py``.
Rendering errors declared as skips can leave stale fixtures: verification reports them, while explicit regeneration removes those marked stale.
Keep the effective configuration matrix when renaming a case, including role references, axis suffixes and path-derived module names.

The Python golden checks verify rendered text and harness contracts.
The native jobs in ``.github/workflows/lint.yml`` separately compile, parse or execute the generated files.
Use both results when assessing an output change.

Finding the implementation
--------------------------

Follow the ordinary literal path in this order:

1. ``case_manifests.py`` validates ``case.toml`` and resolves its input.
2. ``case_discovery.py`` selects representable inputs; ``variant_cases.py`` pairs inputs with options expanded by ``variant_plans.py`` from ``axes.toml``.
3. ``golden_scenarios.py`` assembles ``GoldenRendering`` records from ``golden_renderings.py``; ``golden_batches.py`` bounds pytest work items.
4. ``test_literalize_golden.py`` renders each effective spec and ``golden_checks.py`` compares the result or handles declared skips.
5. ``harness/test_orphan_golden_files.py`` checks fixture ownership across all runners.

The specialized entry points are ``test_calls.py``, ``test_literalize_ref_golden.py``, ``test_literalize_ref_default.py`` and ``test_constructor_targets.py``.
Backend-specific fixture naming, native consumer scaffolds and sample options live under ``languages/``.
``language_specs.py`` applies those naming rules and creates versioned fixture paths.
