Contributing to |project|
=========================

Contributions to this repository must pass tests and linting.

CI is the canonical source of truth.

Install contribution dependencies
---------------------------------

Install Python dependencies in a virtual environment.

.. code-block:: console

   $ pip install --editable '.[dev]'

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

   $ uv run --extra dev pytest

Golden case manifests
---------------------

Every directory under :file:`tests/integration/cases/` contains a versioned
:file:`case.toml`.  The manifest is the source of truth for the input's suite,
variant-axis and ``literalize_call`` coverage; language capability checks and
expansion remain in the typed Python runner.

An ordinary case participates in the base and combined suites.  Its
``input.yaml`` is inferred because it is the directory's sole input:

.. code-block:: toml

   schema_version = 1
   suites = ["base", "combined"]

A variant-only case declares its specialized owner and the axes that consume
it.  A suffix distinguishes multiple logical uses of one input:

.. code-block:: toml

   schema_version = 1
   owner = "variant"

   [[variants]]
   axis = "nested_tuple_strategy"
   suffix = "_mixed"

Simple render context also belongs beside the input.  This base case replaces
null record fields before inference:

.. code-block:: toml

   schema_version = 1
   suites = ["base", "combined"]

   [base_context.record_null_substitutions]
   replacement = -1

Some runners render one chosen input rather than the whole inventory: the
non-default indent, the bare value at file scope, the pre-indent shapes.  The
input declares the part it plays in a ``roles`` list, and the runner looks it
up by role, so the directory name stays a single source of truth on disk:

.. code-block:: toml

   schema_version = 1
   suites = ["base", "combined"]
   roles = ["indent-input"]

A ``literalize_call`` case declares that owner and describes its call in a
``[call]`` table, so the whole case lives in one directory:

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
``call_transform`` is a template, not code: it may substitute only ``{call}``
and ``{zipped}``, and any other placeholder fails at load time.  Enum- and
type-valued fields are named by string and resolved by the loader:
``call_style`` (``keyword``, ``positional``, ``object``, or ``command``),
``zip_input_format``, and the ``variable_form`` pair (``new`` or
``existing``).  ``variant_only = true`` keeps a case out of the default
per-language call matrix, leaving it to the call-variant suite.

A ``$ref`` case declares one of the two ref owners and describes itself in a
``[ref]`` table:

.. code-block:: toml

   schema_version = 1
   owner = "literalize-ref"

   [ref]
   ref_case_override = "camel"

   [ref.value_sources]
   my_int = "42"

``owner = "literalize-ref"`` (the case renders with an explicit ``ref_case``)
or ``owner = "literalize-ref-default"`` (the case renders without one) and a
``[ref]`` table require each other, so the table is spelled even when it is
empty.  ``ref_key`` defaults to ``"$ref"``.  ``ref_case_override`` names an
identifier case (``snake``, ``camel``, ``pascal``, ``upper_snake``, or
``kebab``) that replaces the language's default and skips any language whose
``supported_ref_cases`` excludes it.  Each ``[ref.value_sources]`` entry maps
a ref name to a JSON source that seeds the bound value for that ref.

Non-default inputs can be explicit with ``input = "input.toml"``.  Supported
variant context fields are ``variable_form`` (``new``, ``existing``, or
``both``), ``collection_layout``, ``pre_indent_level``, and
``record_null_substitutions``.  The loader rejects unknown fields or axes,
missing inputs, duplicate logical cases, and duplicate golden targets.

Rejection manifests
-------------------

A rejection that holds for a family of languages -- every language with a
``json_type`` refusing a non-string dict key, every language taking
``record_shape_names`` refusing a name that is not PascalCase -- is declared
once under :file:`tests/errors/rejections/`.  Each directory holds a
:file:`rejection.toml` and an :file:`expected.txt` golden file.  The golden
opens with the split of the languages the manifest selected, then records what
each raised, one line per case:

.. code-block:: text

   # languages rejecting: 21; languages accepting: 0

   C[CJSON] -> UnrepresentableInputError: C json_type can only represent dict keys as JSON object strings, not int

A case is keyed by its language, then by the option member it ran under and the
declared value it substituted, if the manifest varies either.  An option member
is named (``[CJSON]``) and a declared value is quoted (``['9Entry']``).

The manifest itself declares only what provokes the rejection:

.. code-block:: toml

   schema_version = 1
   summary = """
   A JSON value type keys its objects with strings.
   """
   exceptions = ["UnrepresentableInputError"]
   option = "json_type"
   gates = [{ kind = "spec_field_present", field = "json_type" }]

   [call]
   api = "literalize"
   source = "{1: one}"
   input_format = "yaml"

``gates`` selects the languages the rejection is claimed for, using the same
vocabulary as the golden suite's variant axes; a language that later joins
those gates is covered without editing the manifest.  A rejection about one
language's own rendering names it in ``languages`` instead.  ``option`` runs
each language once per member of that option, and ``values`` runs a case per
declared value, which any ``{value}`` in a constructor argument substitutes.

``api`` is ``constructor``, ``literalize``, or ``literalize_call``, and the
loader rejects an argument the named API does not take.  ``exceptions`` lists
the exception types any selected language may raise; the golden file records
which one each raised, together with its message.

A language a gate admits that represents the input rather than refusing it is
declared in an ``accepts`` entry with the reason it does:

.. code-block:: toml

   [[accepts]]
   languages = ["Rust", "Scala"]
   reason = """
   Renders tuples alongside the JSON value type rather than instead of it.
   """

An entry there is an assertion rather than a mute: the suite makes the same
call for those languages and fails if it stops going through, so a language
that starts rejecting cannot sit behind a stale reason.

Documentation
-------------

Documentation is built on GitHub Pages.

Run the following commands to build and view documentation locally:

.. code-block:: console

   $ uv run --extra=dev sphinx-build -M html docs/source docs/build -W
   $ python -c 'import os, webbrowser; webbrowser.open("file://" + os.path.abspath("docs/build/html/index.html"))'

Continuous integration
----------------------

Tests are run on GitHub Actions.
The configuration for this is in :file:`.github/workflows/`.

Performing a release
--------------------

See :doc:`release-process`.
