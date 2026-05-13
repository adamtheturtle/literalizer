"""Golden-file integration tests for literalizer.

Every module in this package is part of the golden-file suite: the
``test_*.py`` modules drive parameterized cases against the fixtures in
``cases/``, and the supporting modules (``call_cases``,
``case_discovery``, ``check_golden``, ``language_specs``,
``literalize_ref_cases``, ``variant_cases``) build and check those
cases. Non-golden tests live alongside this package under ``tests/``
(see ``tests/errors``, ``tests/formats``, ``tests/metadata``, and the
top-level modules).
"""
