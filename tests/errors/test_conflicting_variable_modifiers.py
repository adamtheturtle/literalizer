"""Declaration modifiers that combine, beside the pairs that do not.

The conflicting pairs are declared in ``tests/errors/rejections`` and
run by ``test_rejections.py``.  What is left here is the acceptance
side, which no rejection manifest expresses.
"""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import CSharp, Java


def test_csharp_accepts_private_protected() -> None:
    """``private protected`` is one combined C# accessibility level."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=CSharp(),
        variable_form=NewVariable(
            name="value",
            modifiers=frozenset(
                {CSharp.modifiers.PRIVATE, CSharp.modifiers.PROTECTED},
            ),
        ),
    )

    assert result.code == "private protected int value = 1;"


def test_one_modifier_per_group_is_accepted() -> None:
    """Modifiers from different groups still combine."""
    result = literalize(
        source="1",
        input_format=InputFormat.JSON,
        language=Java(),
        variable_form=NewVariable(
            name="value",
            modifiers=frozenset(
                {
                    Java.modifiers.PUBLIC,
                    Java.modifiers.STATIC,
                    Java.modifiers.FINAL,
                },
            ),
        ),
    )

    assert result.code == "public static final int value = 1;"
