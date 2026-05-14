# `isinstance()` against a `@runtime_checkable` Protocol is O(N) in member count when any member resolves to `None`

## Summary

`isinstance(obj, P)` where `P` is a `@runtime_checkable` `Protocol`
has a **fast path** that runs in constant time regardless of how many
members `P` declares — so long as every member on `obj` resolves to a
non-`None` value.

The moment one member's value on `obj` is `None`, every subsequent
`isinstance(obj, P)` call falls into a slow path whose cost scales
linearly with `len(P.__protocol_attrs__)`. With our 112-member
Protocol the per-call cost goes from ~0.1 µs to ~70 µs, a ~700×
slowdown of the isinstance check itself.

This is plain CPython behavior — beartype is not involved. beartype
does amplify the impact, because every `@beartype`-decorated
function whose parameter is typed as a `runtime_checkable` Protocol
calls `isinstance` on every invocation.

beartype 0.22.9, Python 3.14.4 (also reproduces with default
`BeartypeConf` and with `is_pep484_tower=False`).

## Minimal repro

See [`repro.py`](./repro.py): builds a `@runtime_checkable Protocol`
with N `bool` properties and an instance whose last property is set
to either `True` or `None`, then calls `isinstance(instance, P)` in
a tight loop.

Run with [hyperfine](https://github.com/sharkdp/hyperfine):

```sh
hyperfine --warmup 1 \
  'python repro.py true-5' \
  'python repro.py true-110' \
  'python repro.py none-5' \
  'python repro.py none-110'
```

Output (200,000 isinstance calls per benchmark):

```
Benchmark 1: python repro.py true-5
  Time (mean ± σ):      60.2 ms ±  21.7 ms

Benchmark 2: python repro.py true-110
  Time (mean ± σ):      58.6 ms ±  20.3 ms

Benchmark 3: python repro.py none-5
  Time (mean ± σ):     616.1 ms ±  58.9 ms

Benchmark 4: python repro.py none-110
  Time (mean ± σ):     11.869 s ±  0.571 s

Summary
  python repro.py true-110 ran
    1.03 ± 0.51 times faster than python repro.py true-5
   10.51 ± 3.78 times faster than python repro.py none-5
  202.56 ± 70.95 times faster than python repro.py none-110
```

Two clean signals:

- **Fast path is O(1) in member count**: `true-5` and `true-110`
  finish in the same ~60 ms.
- **Slow path is O(N) in member count, triggered by a `None` value**:
  `none-5` is 10× slower than `true-5`; `none-110` is 200× slower.

## How we hit this in the wild

This was discovered while working on a project (`literalizer`) whose
`Language` Protocol has 112 members.  A new `Optional[int]` member
was added to that Protocol with a default value of `None` on 62 of
the 63 implementing classes.  Every per-element formatter in the
codebase is decorated with `@beartype` and takes `language: Language`,
so a single `literalize()` call on a moderately nested document
performs ~30,000 `isinstance(_, Language)` checks.  At ~70 µs per
check that is ~2 s of new cost per call — on a benchmark that
previously ran in ~1.3 ms.

## Suspected cause

`runtime_checkable` Protocol membership checks delegate to a
`_proto_hook` that walks `__protocol_attrs__` and validates each.
The fast path appears to short-circuit once it has confirmed the
class has all the required attributes; we believe encountering a
`None` value during attribute traversal disables that short-circuit
and forces a per-attribute walk on every subsequent call.
