"""Focused tests for :class:`literalizer.LiteralizeResult`.

Golden fixtures always render with ``wrap_in_file=True``, which folds
both prefix kinds into the wrapped file and leaves
:attr:`~literalizer.LiteralizeResult.body_preamble` and
:attr:`~literalizer.LiteralizeResult.pre_declaration_comments` empty, so
they never exercise the composition this test covers.
"""

from literalizer import InputFormat, NewVariable, literalize
from literalizer.languages import Haskell


def test_code_prepends_body_preamble_and_comments() -> None:
    """``code`` orders body preamble, then comments, then declaration.

    ``bare_code`` drops the body preamble but keeps the comments.
    ``body_preamble`` elements are not one line each: the ``Num``
    instance is a single multi-line element.
    """
    num_instance = (
        "instance Num Val where\n"
        "    fromInteger = HInt\n"
        '    _ + _ = error "not implemented"\n'
        '    _ * _ = error "not implemented"\n'
        '    abs _ = error "not implemented"\n'
        '    signum _ = error "not implemented"\n'
        "    negate (HInt n) = HInt (negate n)"
    )
    result = literalize(
        source="# note\n42\n",
        input_format=InputFormat.YAML,
        language=Haskell(),
        variable_form=NewVariable(name="my_data", modifiers=frozenset()),
        wrap_in_file=False,
    )

    assert result.body_preamble == ("data Val = HInt Integer", num_instance)
    assert result.pre_declaration_comments == ("-- note",)
    assert result.declaration_code == "my_data :: Val\nmy_data = 42"
    assert result.code == (
        "data Val = HInt Integer\n"
        + num_instance
        + "\n-- note\nmy_data :: Val\nmy_data = 42"
    )
    assert result.bare_code == "-- note\nmy_data :: Val\nmy_data = 42"
