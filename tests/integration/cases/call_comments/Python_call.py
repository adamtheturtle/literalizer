from __future__ import annotations
def process(*_args: object, **_kwargs: object) -> object: ...
# Test cases
process(value="hello")  # single word
process(value="hello world")  # two words
# trailing comment
