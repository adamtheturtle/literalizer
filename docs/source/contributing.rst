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

Non-default inputs can be explicit with ``input = "input.toml"``.  Supported
variant context fields are ``variable_form`` (``new``, ``existing``, or
``both``), ``collection_layout``, ``pre_indent_level``, and
``record_null_substitutions``.  The loader rejects unknown fields or axes,
missing inputs, duplicate logical cases, and duplicate golden targets.

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
