"""Type aliases describing the values a golden harness parses.

These mirror ``literalizer._types.Value`` without importing from a
private module (see issue #1947), so a scalar type the library learns to
represent is added here once rather than in each harness.

The mirrored shape describes data on its way *out* of a parser, where
the containers are concrete and a harness narrows them with
``isinstance``; the parsed YAML in particular yields ruamel
comment-tracking subclasses of ``list`` and ``dict``.  A value on its
way *into* the public interface is annotated with the ``ValueInput``
that interface declares instead, which accepts any ``Sequence`` or
mapping.
"""

import datetime

type Scalar = (
    str
    | int
    | float
    | bool
    | datetime.date
    | datetime.datetime
    | datetime.time
    | bytes
    | None
)
type ParsedValue = (
    Scalar | list[ParsedValue] | dict[Scalar, ParsedValue] | set[Scalar]
)
