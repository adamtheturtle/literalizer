# `Skipper` is not thread-safe: `skip: next` skips the wrong example under parallel evaluation

## Summary

`sybil.evaluators.skip.Skipper` keeps mutable per-document state (`active`, `remove`, `last_action`) on a shared `SkipState` and relies on the *next* post-skip example reading that state and removing the evaluator before any subsequent example sees it. When two or more post-skip examples are evaluated concurrently (for example, via a `concurrent.futures.ThreadPoolExecutor`), the state is read and mutated racily, so:

- the directive sometimes skips an example *other than* the one immediately following the `skip: next`, and / or
- the directive sometimes *fails to skip* the immediately-following example at all.

Both directions are reproducible on `sybil==10.0.1`.

## Minimal reproduction

```python
"""Minimal repro: sybil's Skipper races under ThreadPoolExecutor."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from sybil import Sybil
from sybil.example import NotEvaluated
from sybil.parsers.rest import CodeBlockParser, SkipParser

RST = """\
Title
=====

.. code-block:: python

   x = 1

.. skip: next

.. code-block:: python

   bad_undefined_name

.. code-block:: python

   y = 2
"""


def run_once(*, parallel: bool) -> tuple[int, ...]:
    path = Path("/tmp/repro.rst")
    path.write_text(RST)
    ran: list[int] = []
    sybil = Sybil(
        parsers=[
            SkipParser(),
            CodeBlockParser("python", lambda e: ran.append(e.line)),
        ],
    )
    document = sybil.parse(path=path)
    examples = list(document.examples())
    if parallel:
        with ThreadPoolExecutor(max_workers=len(examples)) as pool:
            futs = [pool.submit(e.evaluate) for e in examples]
            for f in as_completed(futs):
                try:
                    f.result()
                except NotEvaluated:
                    pass
    else:
        for e in examples:
            try:
                e.evaluate()
            except NotEvaluated:
                pass
    return tuple(sorted(ran))


print("Sequential (correct, deterministic):")
print(" ", Counter(run_once(parallel=False) for _ in range(20)))

print("Parallel (buggy, varies run-to-run):")
print(" ", Counter(run_once(parallel=True) for _ in range(50)))
```

Output on this machine:

```
Sequential (correct, deterministic):
  Counter({(4, 14): 20})
Parallel (buggy, varies run-to-run):
  Counter({(4, 10): 27, (4, 14): 23})
```

The intended behavior is that the example at line 10 (`bad_undefined_name`) is skipped on every run, leaving `(4, 14)`. Sequential evaluation matches that. Parallel evaluation flips between skipping line 10 (correct) and skipping line 14 (incorrect: the block right after the skip directive runs unchecked, while the *following* block is dropped).
