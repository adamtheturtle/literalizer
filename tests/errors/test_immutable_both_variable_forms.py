"""Where a once-bound declaration modifier still belongs.

The rejections are declared in ``tests/errors/rejections`` and run by
``test_rejections.py``.  What is left here is the acceptance side --
the modifier that names a storage class rather than a binding. Single
declaration acceptance is covered by the ``immutable_sequence_declaration``
modifier golden fixtures.
"""

import enum
from textwrap import dedent

import pytest

from literalizer import (
    BothVariableForms,
    InputFormat,
    Language,
    literalize,
)
from literalizer.languages import Cpp, CSharp, Java


@pytest.mark.parametrize(
    argnames=("language", "modifier", "expected"),
    argvalues=[
        pytest.param(
            Cpp(),
            Cpp.modifiers.STATIC,
            dedent(
                text="""\
                #include <initializer_list>
                #include <vector>
                int Module() {
                static auto my_val = std::vector<int>{
                    1,
                    2,
                };
                (void)my_val;
                my_val = std::vector<int>{
                    1,
                    2,
                };
                    (void)my_val;
                    return 0;
                }"""
            ),
            id="cpp",
        ),
        pytest.param(
            Java(),
            Java.modifiers.STATIC,
            dedent(
                text="""\
                class Module {
                static int[] my_val = new int[]{
                    1,
                    2
                };
                my_val = new int[]{
                    1,
                    2
                };
                }"""
            ),
            id="java",
        ),
        pytest.param(
            CSharp(),
            CSharp.modifiers.STATIC,
            dedent(
                text="""\
                using System;
                static int[] my_val = (
                    1,
                    2
                );
                my_val = (
                    1,
                    2
                );"""
            ),
            id="csharp",
        ),
    ],
)
def test_rebindable_modifier_accepted(
    language: Language,
    modifier: enum.Enum,
    expected: str,
) -> None:
    """``static`` names a storage class, not a once-only binding."""
    result = literalize(
        source="[1, 2]",
        input_format=InputFormat.JSON,
        language=language,
        variable_form=BothVariableForms(
            name="my_val",
            modifiers=frozenset({modifier}),
        ),
        wrap_in_file=True,
    )
    assert result.code == expected
