"""Acceptance side of V's null-in-collection contract.

The rejection side -- V's default (``ERROR``) strategy refusing
null-only containers, and Java's ``List.of()`` refusing null elements
-- is declared in the ``v_null_only_containers`` and
``java_list_null_elements`` rejection manifests.  The ``INTERFACE``
strategy accepting the same input has no golden-file surface (the
``null_list`` case does not run the heterogeneous-strategy axis), so
that acceptance keeps unit coverage here.
"""

import json

from literalizer import InputFormat, literalize
from literalizer.languages import V


def test_v_interface_strategy_admits_null_only_container() -> None:
    """The ``INTERFACE`` strategy wraps each null in ``IVal(...)``, so a
    null-only list is representable and is not rejected.
    """
    result = literalize(
        source=json.dumps(obj=[None, None]),
        input_format=InputFormat.JSON,
        language=V(
            heterogeneous_strategy=V.heterogeneous_strategies.INTERFACE,
        ),
        pre_indent_level=0,
        include_delimiters=True,
        variable_form=None,
    )
    assert result.code == (
        "[\n\tIVal(unsafe { nil }),\n\tIVal(unsafe { nil }),\n]"
    )
