Contributing to |project|
=========================

Contributions to this repository must pass tests and linting.

CI is the canonical source of truth.

Install contribution dependencies
---------------------------------

Install Python dependencies in a virtual environment.

.. code-block:: console

   $ pip install --editable . --group dev

Install ``prek`` hooks:

.. code-block:: console

   $ prek install

Linting
-------

Run lint tools either by committing, or with:

.. code-block:: console

   $ prek run --all-files --hook-stage pre-commit --verbose
   $ prek run --all-files --hook-stage pre-push --verbose
   $ prek run --all-files --hook-stage manual --verbose

Running tests
-------------

.. code-block:: console

   $ uv run --group dev pytest

Golden verification preserves existing fixtures when rendering skips.
A stale skipped fixture fails verification with its path.
To remove it, run the corresponding golden test with ``--regen-all``.
Regeneration also rewrites supported golden files, so select only the affected test and review its diff.

Changelog entries
-----------------

Describe each user-facing change in a news fragment at :file:`newsfragments/<issue>.change.md`.
Write fragments in Markdown using the ``.change.md`` suffix.
Towncrier rejects invalid fragment names at release time.
The release workflow assembles the fragments into ``CHANGELOG.md`` and the GitHub release notes, then deletes them.
Do not re-add a fragment that a release has already consumed, for example when merging ``main`` into a long-running branch.

Golden case manifests
---------------------

Every directory under :file:`tests/integration/cases/` contains a versioned :file:`case.toml`.
The manifest is the source of truth for the input's suite, variant-axis and ``literalize_call`` coverage; language capability checks and expansion remain in the typed Python runner.

A YAML case that deliberately reuses an anchor declares its expected parser warning:

.. code-block:: toml

   [expected_reused_anchor_warning]
   anchor = "x"
   count = 1

The anchor must be non-empty and the count must be a positive integer.
Fixture discovery and public-API golden rendering both assert the declared warning type, anchor and count.
Omitting the table leaves warnings visible, and unrelated warnings remain visible when the table is present.
Other input formats cannot declare this YAML warning.

Ordinary format variants exercise every supported language version.
An axis that explicitly selects ``language_version`` stays pinned to that version; a format requiring newer syntax uses its effective version once.
To exercise only its default version, a typed axis can declare ``per_version = false``.
The orphan check uses those same effective specs for ordinary and call variants, so a compiling file still needs a rendering that compares its contents.

An ordinary case participates in the base and combined suites.
Its ``input.yaml`` is inferred because it is the directory's sole input:

.. code-block:: toml

   schema_version = 1
   suites = ["base", "combined"]

The default module-name suite checks each constructor's public default across its language versions:

.. code-block:: toml

   schema_version = 1
   suites = ["default-module-name"]
   gates = [{ kind = "capability_flag", flag = "supports_module_name" }]

Its input lives beside the manifest, while its golden files remain under :file:`tests/integration/default_module_names/`.
Those files retain the default module names; regular compiler fixtures use unique names derived from their paths.

A variant-only case declares its specialized owner and the axes that consume it.
A suffix distinguishes multiple logical uses of one input:

.. code-block:: toml

   schema_version = 1
   owner = "variant"

   [[variants]]
   axis = "nested_tuple_strategy"
   suffix = "_mixed"

Simple render context also belongs beside the input.
This base case replaces null record fields before inference:

.. code-block:: toml

   schema_version = 1
   suites = ["base", "combined"]

   [base_context.record_null_substitutions]
   replacement = -1

Some runners render one chosen input rather than the whole inventory: the non-default indent, the bare value at file scope, the pre-indent shapes.
The input declares the part it plays in a ``roles`` list, and the runner looks it up by role, so the directory name stays a single source of truth on disk:

.. code-block:: toml

   schema_version = 1
   suites = ["base", "combined"]
   roles = ["indent-input"]

A ``literalize_call`` case declares that owner and describes its call in a ``[call]`` table, so the whole case lives in one directory:

.. code-block:: toml

   schema_version = 1
   owner = "literalize-call"

   [call]
   target_function = "throttler.check"
   parameter_names = ["user_id", "ts"]
   per_element = true
   call_transform = "emit({call})"
   transform_stub_names = ["emit"]
   requires_call_returns_expression = true

``owner = "literalize-call"`` and a ``[call]`` table require each other.
``call_transform`` is a template, not code: it may substitute only ``{call}`` and ``{zipped}``, and any other placeholder fails at load time.
Enum- and type-valued fields are named by string and resolved by the loader: ``call_style`` (``keyword``, ``positional``, ``object``, or ``command``), ``zip_input_format``, and the ``variable_form`` pair (``new`` or ``existing``).
``variant_only = true`` keeps a case out of the default per-language call matrix, leaving it to the call-variant suite.

A ``$ref`` case declares one of the two ref owners and describes itself in a ``[ref]`` table:

.. code-block:: toml

   schema_version = 1
   owner = "literalize-ref"

   [ref]
   ref_case_override = "camel"

   [ref.value_sources]
   my_int = "42"

``owner = "literalize-ref"`` (the case renders with an explicit ``ref_case``) or ``owner = "literalize-ref-default"`` (the case renders without one) and a ``[ref]`` table require each other, so the table is spelled even when it is empty.
``ref_key`` defaults to ``"$ref"``.
``ref_case_override`` names an identifier case (``snake``, ``camel``, ``pascal``, ``upper_snake``, or ``kebab``) that replaces the language's default and skips any language whose ``supported_ref_cases`` excludes it.
Each ``[ref.value_sources]`` entry maps a ref name to a JSON source that seeds the bound value for that ref.

Keep regressions with the same input and API context together.
A shared ``[call]`` or ``[ref]`` table can own named ``[[call_examples]]`` or ``[[ref_examples]]`` that exercise specific source syntax or representation options:

.. code-block:: toml

   schema_version = 1
   owner = "literalize-ref"

   [ref]
   value_sources = { shared = '[1,"x"]' }

   [[ref_examples]]
   example = "tagged_enum"
   gates = [{ kind = "enum_member_present", option = "heterogeneous_strategy", member = "TAGGED_ENUM" }]
   heterogeneous_strategy = "TAGGED_ENUM"
   value_sources = { shared = '[1,"x"]' }

The primary table exercises the shared scenario across languages; each example selects the capabilities its additional contract needs.
Examples share the owning input and use the same renderer, version expansion, compiler checks and orphan checks as the primary table.
Each example declares its complete API configuration rather than inheriting options from the primary table.
Its unique ``example`` name uses lowercase letters, digits and underscores and is appended to its golden filenames and test identifiers.
Keep the original regression provenance with the example when consolidating cases.

A case renders under every language unless it narrows.
``gates`` names the property the narrowing follows from, in the same vocabulary the variant axes and the rejection manifests use, so a language that later gains that property is covered without editing the manifest:

.. code-block:: toml

   schema_version = 1
   suites = ["base"]
   gates = [{ kind = "capability_flag", flag = "default_allows_empty_dict_keys" }]

This gate belongs to an input containing an empty mapping key.
Use the input's actual requirements to select its languages, and keep source-syntax regressions as capability-gated examples of shared scenarios.
The ``[call]``, ``[ref]`` and named example tables use the same gate vocabulary.

Non-default inputs can be explicit with ``input = "input.toml"``.
Supported variant context fields are ``variable_form`` (``new``, ``existing``, or ``both``), ``collection_layout``, ``pre_indent_level``, and ``record_null_substitutions``.
The loader rejects unknown fields or axes, missing inputs, duplicate logical cases, and duplicate golden targets.

Rejection manifests
-------------------

Each scenario under :file:`tests/errors/rejections/` declares an API call in :file:`rejection.toml` and records its results in an :file:`expected.toml` golden file.
Scenarios run across every language by default; the input manifest has no language list.
The golden counts languages accepting and rejecting, groups exact messages by exception type, and records successful calls in an ``Accepted`` table.
For example, a scalar null scenario includes these entries:

.. code-block:: toml

   [Accepted]
   Python = ""

   [UnrepresentableInputError]
   Toml = "TOML cannot represent null values; remove the null or choose a language with a null literal"

A case is keyed by its language, then by the option member it ran under and the declared value it substituted, if the manifest varies either.
Option members use their names (``[CJSON]``), and declared values are quoted (``['9Entry']``).
A language may accept one source and reject another, so it can appear in both population counts.
Changes between acceptance and rejection, exception types, or messages fail golden comparison.

The manifest declares what provokes the rejection:

.. code-block:: toml

   schema_version = 1
   summary = "A JSON value type keys its objects with strings."
   exceptions = ["UnrepresentableInputError"]
   option = "json_type"
   gates = [{ kind = "spec_field_present", field = "json_type" }]

   [call]
   api = "literalize"
   sources = ["1: one"]
   input_format = "yaml"

Optional ``gates`` narrow the scenario by capability using the same vocabulary as the golden suite's variant axes.
A new language joining those gates is covered automatically.
``option`` runs each applicable language once per member of that option, and ``values`` runs a case per declared value, which any ``{value}`` in a constructor argument substitutes.
Languages lacking an enum member or declaration modifier needed to express the call do not contribute that combination.
This selection reads option declarations, without executing the call to decide whether it belongs.

Declaration modifiers normally resolve against the target's enum.
``modifier_source = "all"`` repeats the call using every enum that declares the requested modifier names, covering both local and foreign modifier ownership without naming an implementation in the manifest.
Those cases add a ``['modifiers=Owner']`` part to the golden identifier, so distinct enum sources cannot overwrite each other's results.

``api`` is ``constructor``, ``literalize``, or ``literalize_call``, and the loader rejects an argument the named API does not take.
Each type in ``exceptions`` must occur in at least one case, keeping a scenario from silently losing the rejection it covers.
Other public Literalizer errors are recorded with their exact types and messages too; unexpected exceptions escape the runner.
For parser diagnostics, an optional top-level ``position = [line, column]`` asserts the public error's one-based ``line`` and ``column`` attributes when the declared exception occurs.
The same rule applies to optional ``attributes`` assertions; ``language_name = "{language}"`` checks the current language name.
Python-version-specific message overrides remain in the golden, and regeneration preserves inactive versions.

Documentation
-------------

Documentation is built on GitHub Pages.

Run the following commands to build and view documentation locally:

.. code-block:: console

   $ uv run --group=dev sphinx-build -M html docs/source docs/build -W
   $ python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("docs/build/html/index.html"))'

Continuous integration
----------------------

Tests are run on GitHub Actions.
The configuration for this is in :file:`.github/workflows/`.

Code generation benchmarks
~~~~~~~~~~~~~~~~~~~~~~~~~~

The benchmarks in :file:`tests/benchmarks/test_bench_literalize.py` measure code generation with CodSpeed's CPU simulation instrument.
The six benchmark shards in :file:`.github/workflows/ci.yml` publish results to the same CodSpeed report.
They use Ubuntu 24.04, managed CPython 3.14.8 and a fixed ``PYTHONHASHSEED`` of ``0``.
Changing the benchmark runtime requires a new baseline for meaningful performance comparisons.
Compiler correctness is checked by the integration golden tests and language round-trip checks.
Individual compiler commands have deadlines to bound pathological workloads.

Performing a release
--------------------

See :doc:`release-process`.
