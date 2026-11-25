# Record composition discovery for #5494

The [tested Literalizer revision](https://github.com/adamtheturtle/literalizer/tree/b74c222df55e8071432ef11feef17a2ae6de2790) is the source pin. This branch holds the replay and output from the bounded investigation.

The 13 backend and document-pair combinations cover Python, Go, and Kotlin. The pairs include scalar records, records containing nested records, populated arrays, empty and populated sequences with a common element type, and maps with mixed scalar values. The replay admits compatible shared declarations. It executes 52 programs assembled with the public composition API in both declaration orders, with and without reference hints. It executes 26 more programs using only the chosen declaring document's preamble. All 78 passed. Native consumers check values and repeated references, including Go slice identity where the representation supports it.

Ten controls rejected the expected conditions. Those cover three wrong-value mutations, incompatible schemas, caller-owned name collisions, independently inferred Kotlin array types, and Python's standalone rejection of sibling records with different map shapes. The initial probe omitted the reference key and was excluded as an adapter error. The final replay supplies it explicitly.

Use an absolute path to this archive with the pinned repository checkout as the working directory. The observed tools were CPython 3.15.0, Go 1.27.4, and Kotlin 2.4.21. The replay applies a 40-second timeout to each compiler or runtime invocation. The observed run took 120.401 seconds within a 480-second overall budget.

```sh
uv sync --group=dev
PYTHONPATH="$PWD/src:$PWD" timeout 480 .venv/bin/python "$archive_dir/compose_records.py"
```

The existing Go, Rust, and C++ shared-record runners also passed on the source pin. The earlier [composition archive](https://github.com/adamtheturtle/literalizer/tree/e7f2199eb2d98b486b3f784ab91745bbaa71bbd3) retains the minimized defects and the earlier four-backend sweep.
