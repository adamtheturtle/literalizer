"""Names understood by the typed integration variant runner.

An axis name is registered in exactly one place: as a declared plan or a
special axis in ``axes.toml``, or as an escape-hatch builder in
:mod:`variant_escape_hatches`.  The sets here are derived from those
registrations, so a case manifest naming an axis no expansion knows
about still fails at load, against a set that cannot drift.
"""

from .variant_escape_hatches import ESCAPE_HATCH_VARIANT_AXES
from .variant_plans import declared_axis_names, special_axis_names

SPECIAL_VARIANT_AXES = special_axis_names()

KNOWN_VARIANT_AXES = (
    declared_axis_names() | ESCAPE_HATCH_VARIANT_AXES | SPECIAL_VARIANT_AXES
)
