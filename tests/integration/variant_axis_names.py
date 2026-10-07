"""Names understood by the typed integration variant runner.

An axis name is registered in exactly one place: as a declared plan or a
special axis in ``axes.toml``.  The sets here are derived from those
registrations, so a case manifest naming an axis no expansion knows
about still fails at load, against a set that cannot drift.
"""

from .variant_plans import declared_axis_names, special_axis_names

SPECIAL_VARIANT_AXES = special_axis_names()

KNOWN_VARIANT_AXES = declared_axis_names() | SPECIAL_VARIANT_AXES
