Sequences containing references with no value hints no longer infer element types from the reference marker.
C++ retains those references' native element types, and Go uses its unknown-element representation.
Rust preserves non-consuming references whose value hints are missing, rather than assuming that their bindings implement `Copy`.
Mojo copies reference arguments with missing value hints so owned containers remain available for reuse, while preserving native null values.
