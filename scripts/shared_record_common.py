"""Shared pieces for the cross-file record-declaration checks (#3748).

Under the ``RECORD`` strategy a record field whose dict has no record
shape of its own widens to a plain map, and by default that map's value
type follows the data: uniform scalars narrow to the bare scalar type,
mixed ones take the strategy's value carrier.  Two data files sharing
one record shape then declare the field two different ways, so the
second file's literals no longer compile against the first file's
declaration.

``record_map_value_typing=WIDE`` pins the carrier instead.  Every
``run_<lang>_shared_record.py`` helper literalizes both documents below
under that setting and compiles both sets of literals against one set of
declarations. C++ and Rust use the mixed document's declarations, so
the shared value carrier includes the boolean alternative. Go checks
both orders and compares the values returned by the native consumer.

The C++ and Rust runners also check complete files assembled with
``literalize_call_with_declarations`` for compatible records and
repeated references. Cross-file reuse requires compatible inferred
types and matching generated names. Callers provide the surrounding
scope and own the names of their helpers. See the function-call guide
for the composition contract.

The two documents share one record shape (``name`` plus ``attributes``)
and in each of them the inner ``attributes`` maps have differing key
sets, so neither is recordizable and both widen.  The dependent document
is the interesting half: all of its widened scalars are strings, which
is exactly the uniformity the default narrows on.
"""

DECLARING_DOCUMENT = """\
[
  {"name": "row_1", "attributes": {"colour": "red", "discounted": true}},
  {"name": "row_2", "attributes": {"colour": "blue", "size": "large"}}
]
"""

DEPENDENT_DOCUMENT = """\
[
  {"name": "row_3", "attributes": {"colour": "green", "size": "small"}},
  {"name": "row_4", "attributes": {"colour": "white"}}
]
"""

DECLARING_VAR_NAME_SNAKE = "declaring_data"
DEPENDENT_VAR_NAME_SNAKE = "dependent_data"
DECLARING_VAR_NAME_CAMEL = "declaringData"
DEPENDENT_VAR_NAME_CAMEL = "dependentData"

# The compiled program has no data to re-emit -- it is the compiler's
# acceptance of the dependent literals that is under test -- so each one
# prints this fixed document for ``roundtrip_common.verify`` to compare
# against, reusing that module's tmpdir, subprocess and diagnostic
# handling rather than repeating it here.
OK_DOCUMENT = '{"ok": true}'
