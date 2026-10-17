---
name: literalizer-golden-tests
description: Add or update Literalizer golden-file tests for non-error rendering behavior. Use when a change affects language output, a formatting option, or a cross-language capability.
---

# Literalizer Golden Tests

Use the shared fixtures under ``tests/integration/cases`` for output that should work across languages.
A base case runs for every language and version; use that whenever the input can be represented everywhere.

For a capability-specific case, discover participating languages through an explicit capability attribute declared on every language class.
Do not select languages with ``getattr`` or rely on inherited capability defaults.

Keep unit tests for error paths and behavior with no compiling golden-file surface.
Run the orphan-fixture test after adding or removing golden files.

Name shared cases and variant axes after their input shape, rendering behavior or option interaction.
Keep the original backend and issue provenance in the rationale or regression documentation.
Retain language qualifiers when they describe actual source syntax, a version constraint or another language-specific contract.
Before adding or expanding a case, check for an existing equivalent shared scenario and choose its canonical name.
When renaming, preserve the effective configuration matrix and update role/owner references, axis keys and path-derived wrapper names.
