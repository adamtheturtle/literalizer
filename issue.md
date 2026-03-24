### Describe the Bug

```python
"""Example of false positive."""

from collections import OrderedDict

OrderedDict([("a", 1), ("b", "c")])
```

This passes mypy but pyrefly 0.57.1 reports:

```
ERROR No matching overload found for function `dict.__init__` called with arguments: (list[tuple[str, int] | tuple[str, str]]) [no-matching-overload]
```

The `iterable: Iterable[tuple[_KT, _VT]]` overload should match with `_KT=str, _VT=int | str`.

The sandbox (which runs a newer unreleased version) does not reproduce the error. The fix appears to be [`b34ae71429ba`](https://github.com/facebook/pyrefly/commit/b34ae71429ba5078f0daf8d104a8060f5bf946c9) ("Collect lower bounds on Variable::Quantified and Variable::Unwrap"), which landed 2026-03-19 after the 0.57.1 release.

### Sandbox Link

https://pyrefly.org/sandbox/?code=eJxLK8rPVUjOz8lJTS7JzM8rVsjMLcgvKlHwL0pJLUpNcclMLuHiqlCwRRbQiNZQSlTSUTDU1FHQUEoCspSSlTRjNbkAHQ8Xpg
