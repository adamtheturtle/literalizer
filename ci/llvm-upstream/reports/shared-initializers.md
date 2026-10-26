Tested with official LLVM 23.1.4 (`7a941dfb2877a0b8cf30323fefa85ad019e0b0f5`) on Ubuntu 24.04.5, Linux AArch64.

This valid C99 input should produce the single sizeof warning without repeatedly expanding the shared initializer graph.

```c
typedef struct V { const struct V *child; } V;
int main(void) {
  V value = (V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = (V[]){(V){.child = 0}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}};
  (void)value;
  return sizeof(sizeof(int));
}
```

Run from the [reproducer bundle](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/README.md):

```sh
timeout 10s clang-tidy reproducers/shared-initializers.c --checks=-*,bugprone-sizeof-expression --config={} -- -std=c99
```

The unmodified release exceeded the ten-second limit (exit 124).
The same input completed in 0.019 seconds with the [candidate implementation](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/patches/shared-initializers.patch).
These are single sequential wall-clock samples, not statistical benchmarks.
Raw commands and outputs are in [measurements.json](https://github.com/adamtheturtle/literalizer/blob/codex/llvm-toolchain-prerequisite-20261026/ci/llvm-upstream/measurements.json).

C compound literals and designated initializers expose shared expression nodes through syntactic and semantic forms.
Re-expanding the same children along every incoming path amplifies traversal.

Candidate fix: Preserve every parent edge while expanding each statement once; cache only missing descendant searches, respect direct-child search depth, and avoid duplicate visits in outer compound-literal matching and padding analysis.
The candidate intentionally removes duplicate callbacks for the same expression/context.
Parent-edge and positive binding-multiplicity controls are retained in the downstream builder.

The isolated patch applies to LLVM main `fac4500420cdeed42f35537a26eea1e4e17badf0` and contains a regression test.
The new test and the downstream semantic controls were run with the patched 23.1.4 tools; a complete build of current LLVM main has not been performed.

Prepared with AI assistance.
