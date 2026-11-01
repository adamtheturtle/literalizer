Test layout
===========

Complete public rendering examples belong in the manifest-owned compiling cases under ``integration/cases``.
The Python tests below retain contracts that a fixed compiling example cannot replace.

* ``errors`` checks typed failures, error locations, exception relationships, and the rejection manifests.
  Its manifest validation checks stay with the rejection runner and data.
* ``metadata`` checks language options, constructor boundaries, result metadata, round-trip capability declarations, and project configuration.
* ``fragments`` checks incomplete public output and references to externally owned declarations whose definitions cannot be supplied by the generator.
* ``internals`` checks formatter composition and scanner behavior that is unreachable as a complete public rendering.
* ``runtime`` checks generated round-trip properties, concurrent calls, and mutation of caller-owned state.
* ``stress`` generates large inputs and checks invariants at depth limits without checking in a large fixed output.
* ``integration`` contains the golden rendering drivers and the multiline golden execution oracle.
  Its supporting modules build the cases, while ``integration/harness`` checks discovery, manifests, ownership, version selection, and regeneration behavior.
* ``benchmarks`` measures rendering performance.

Shared Python helpers live directly under ``tests``, with declarative unit data in ``unit_cases`` and rejection data in ``errors/rejections``.

Run the ordinary suite with ``UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest --ignore=tests/benchmarks``.
A directory can also be selected directly, for example ``UV_PYTHON=3.14 uvx uv@0.13.0 run --group=dev pytest tests/stress``.
